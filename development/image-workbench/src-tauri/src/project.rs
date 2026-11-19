use crate::assets::{image_counts, image_inventory, ImageCategory};
use serde::Serialize;
use std::{
    fs,
    path::{Path, PathBuf},
    process::Command,
};

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ProjectStatus {
    pub root: String,
    pub root_images: usize,
    pub total_images: usize,
    pub story_images: usize,
    pub unused_images: usize,
    pub categories: Vec<ImageCategory>,
    pub report_text: String,
    pub requests: Vec<crate::requests::StoryRequest>,
    pub story_targets: Vec<crate::requests::StoryTarget>,
}

pub fn default_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .unwrap_or(Path::new("."))
        .to_path_buf()
}

pub fn checked_root(value: &str) -> Result<PathBuf, String> {
    let root =
        fs::canonicalize(value).map_err(|error| format!("Cannot open project folder: {error}"))?;
    for relative in [
        "game/images",
        "developer-tools/generate_image_list.py",
        "developer-tools/integrate_story_images.py",
        "developer-tools/audit_images.py",
    ] {
        if !root.join(relative).exists() {
            return Err(format!("Not a LOLA project folder; missing {relative}."));
        }
    }
    Ok(root)
}

pub fn status(value: &str) -> Result<ProjectStatus, String> {
    let root = checked_root(value)?;
    let (root_images, total_images) = image_counts(&root.join("game/images"))?;
    let inventory = image_inventory(&root.join("game"))?;
    let report = root.join("developer-tools/image_generation_list.md");
    let report_text = if report.exists() {
        fs::read_to_string(report).map_err(|error| format!("Cannot read image list: {error}"))?
    } else {
        "Select Refresh image list to generate the report.".to_string()
    };
    Ok(ProjectStatus {
        root: root.display().to_string(),
        root_images,
        total_images,
        story_images: inventory.story_used,
        unused_images: inventory.unused,
        categories: inventory.categories,
        report_text,
        requests: crate::requests::load(&root)?,
        story_targets: crate::requests::load_targets(&root)?,
    })
}

pub fn open_document(value: &str, document: &str) -> Result<(), String> {
    let root = checked_root(value)?;
    let path = match document {
        "report" => root.join("developer-tools/image_generation_list.md"),
        "guide" => root.join("developer-tools/IMAGE_IMPORT.md"),
        "template" => root.join("developer-tools/image_metadata.template.json"),
        "story-proposals" => root.join("developer-tools/story_image_proposals.json"),
        "story-bible" => root.join("documentation/design/STORY_BIBLE.md"),
        "roadmap" => root.join("documentation/roadmap/PHASE_ROADMAP.md"),
        _ => return Err(format!("Unknown project document: {document}")),
    };
    if !path.is_file() {
        return Err(format!("File not found: {}", path.display()));
    }
    Command::new("explorer.exe")
        .arg(path)
        .spawn()
        .map(|_| ())
        .map_err(|error| format!("Cannot open project document: {error}"))
}
