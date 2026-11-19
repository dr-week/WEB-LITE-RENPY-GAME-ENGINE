"""Persistent SQLite schema for LOLA image inventory, quality, feedback, and prompts."""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS image_assets (
    path TEXT PRIMARY KEY,
    bytes INTEGER NOT NULL,
    sha256 TEXT DEFAULT '',
    category TEXT DEFAULT '',
    width INTEGER DEFAULT 0,
    height INTEGER DEFAULT 0,
    quality_score INTEGER DEFAULT 100,
    quality_flags TEXT DEFAULT '[]',
    status TEXT DEFAULT 'active',
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS image_references (
    source TEXT,
    line INTEGER,
    target_path TEXT,
    found INTEGER,
    PRIMARY KEY(source, line, target_path)
);

CREATE TABLE IF NOT EXISTS image_aliases (
    alias TEXT PRIMARY KEY,
    source TEXT,
    line INTEGER
);

CREATE TABLE IF NOT EXISTS alias_references (
    source TEXT,
    line INTEGER,
    alias TEXT,
    defined INTEGER,
    PRIMARY KEY(source, line, alias)
);

CREATE TABLE IF NOT EXISTS image_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_path TEXT NOT NULL,
    rating TEXT NOT NULL CHECK(rating IN ('up', 'down')),
    reason TEXT DEFAULT '',
    scene_label TEXT DEFAULT '',
    prompt_hint TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    UNIQUE(asset_path, created_at)
);

CREATE TABLE IF NOT EXISTS prompt_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT DEFAULT '',
    asset_id TEXT DEFAULT '',
    category TEXT DEFAULT '',
    prompt_text TEXT NOT NULL,
    status TEXT DEFAULT 'generated',
    parent_asset_path TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS story_nodes (
    node_id TEXT PRIMARY KEY,
    node_type TEXT NOT NULL,
    label TEXT NOT NULL,
    file_path TEXT NOT NULL,
    title TEXT DEFAULT '',
    category TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS story_choices (
    choice_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    choice_text TEXT NOT NULL,
    stat_effects TEXT DEFAULT '[]',
    next_label TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS story_image_links (
    node_id TEXT NOT NULL,
    asset_path TEXT NOT NULL,
    alias TEXT DEFAULT '',
    link_type TEXT DEFAULT 'scene',
    PRIMARY KEY(node_id, asset_path)
);

CREATE TABLE IF NOT EXISTS story_endings (
    ending_id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    file_path TEXT NOT NULL,
    title TEXT DEFAULT ''
);

DROP VIEW IF EXISTS missing_images;
CREATE VIEW missing_images AS
    SELECT source, line, target_path FROM image_references WHERE found = 0;

DROP VIEW IF EXISTS missing_aliases;
CREATE VIEW missing_aliases AS
    SELECT r.source, r.line, r.alias FROM alias_references r
    LEFT JOIN image_aliases a ON a.alias = r.alias
    WHERE a.alias IS NULL;

DROP VIEW IF EXISTS flagged_assets;
CREATE VIEW flagged_assets AS
    SELECT a.path, a.category, a.quality_score, a.quality_flags, a.status,
           COALESCE(f.reason, '') AS last_reason, COALESCE(f.scene_label, '') AS scene_label
    FROM image_assets a
    LEFT JOIN image_feedback f ON f.id = (
        SELECT id FROM image_feedback
        WHERE asset_path = a.path AND rating = 'down'
        ORDER BY created_at DESC LIMIT 1
    )
    WHERE a.path LIKE 'images/%'
      AND a.path NOT LIKE 'images/ui/%'
      AND (a.status = 'needs_regen' OR a.quality_score < 70);

DROP VIEW IF EXISTS v_story_image_health;
CREATE VIEW v_story_image_health AS
    SELECT l.node_id, n.node_type, n.file_path, l.alias, l.asset_path,
           COALESCE(a.quality_score, 0) AS quality_score,
           COALESCE(a.status, 'missing') AS asset_status
    FROM story_image_links l
    JOIN story_nodes n ON n.node_id = l.node_id
    LEFT JOIN image_assets a ON a.path = l.asset_path;

DROP VIEW IF EXISTS v_unlinked_good_images;
CREATE VIEW v_unlinked_good_images AS
    SELECT a.path, a.category, a.width, a.height, a.quality_score, a.status
    FROM image_assets a
    LEFT JOIN story_image_links l ON l.asset_path = a.path
    WHERE l.asset_path IS NULL
      AND a.path LIKE 'images/%'
      AND a.category NOT IN ('character_reference', 'menu_assets', 'ui', '')
      AND a.quality_score >= 85
      AND a.status != 'needs_regen'
    ORDER BY a.quality_score DESC, a.path ASC;
"""
