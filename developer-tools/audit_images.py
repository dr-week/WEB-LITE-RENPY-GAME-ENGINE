"""CLI entry point for auditing game image references, aliases, and visual quality."""

from image_audit import (
    DATABASE,
    collect_sources,
    create_database,
    query_low_quality,
    query_missing,
    sync_feedback_file,
)


def main():
    assets, references, aliases, alias_refs = collect_sources()
    create_database(assets, references, aliases, alias_refs)
    sync_stats = sync_feedback_file()
    missing_images, missing_aliases = query_missing()
    low_quality = [row for row in query_low_quality(75) if not row[0].startswith("images/ui/")]
    print(f"Indexed {len(assets)} image files, {len(references)} file references, and {len(alias_refs)} scene aliases.")
    print(f"Database: {DATABASE}")
    if sync_stats["imported"]:
        print(f"Synced {sync_stats['imported']} new feedback entries ({sync_stats['flagged']} flagged, {sync_stats['approved']} approved).")
    for source, line, target in missing_images:
        print(f"MISSING FILE {source}:{line} -> {target}")
    for source, line, alias in missing_aliases:
        print(f"MISSING ALIAS {source}:{line} -> {alias}")
    for path, w, h, score, flags in low_quality[:10]:
        print(f"LOW QUALITY ({score}/100) {path} [{w}x{h}] -> {flags}")
    if not missing_images and not missing_aliases and not low_quality:
        print("All image references, aliases, and visual quality checks passed.")


if __name__ == "__main__":
    main()
