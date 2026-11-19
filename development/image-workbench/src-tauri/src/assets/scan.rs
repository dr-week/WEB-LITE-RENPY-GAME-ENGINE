use std::{collections::{HashMap, HashSet}, fs, path::Path};
use super::{models::supported_image, walk::files_below};

pub fn image_paths(root: &Path) -> Result<Vec<String>, String> {
    files_below(root)?.into_iter().filter(|path| supported_image(path)).map(|path| {
        path.strip_prefix(root).map(|relative| relative.to_string_lossy().replace('\\', "/"))
            .map_err(|error| format!("Cannot classify image path: {error}"))
    }).collect()
}

pub fn story_image_paths(game: &Path) -> Result<HashSet<String>, String> {
    let mut aliases = HashMap::new();
    let mut story_uses = Vec::new();
    for path in files_below(game)?.into_iter().filter(|path| path.extension().and_then(|v| v.to_str()) == Some("rpy")) {
        let contents = fs::read_to_string(&path).map_err(|error| format!("Cannot read {}: {error}", path.display()))?;
        for line in contents.lines() {
            let trimmed = line.trim();
            if let Some(definition) = trimmed.strip_prefix("image ") { capture_alias(definition, &mut aliases); }
            if path.starts_with(game.join("40_story")) { capture_story_use(trimmed, &mut story_uses); }
        }
    }
    let mut paths: HashSet<String> = story_uses.into_iter()
        .filter_map(|alias| aliases.get(&alias).cloned()).collect();
    add_loop_images(game, &mut paths)?;
    Ok(paths)
}

fn add_loop_images(game: &Path, paths: &mut HashSet<String>) -> Result<(), String> {
    let catalog = game.join("data/image_story_catalog.json");
    if !catalog.is_file() { return Ok(()); }
    let text = fs::read_to_string(&catalog).map_err(|error| error.to_string())?;
    let data: serde_json::Value = serde_json::from_str(&text)
        .map_err(|error| format!("Invalid image story catalog: {error}"))?;
    if let Some(events) = data.get("events").and_then(serde_json::Value::as_array) {
        for event in events {
            if let Some(images) = event.get("images").and_then(serde_json::Value::as_array) {
                for image in images.iter().filter_map(serde_json::Value::as_str) {
                    paths.insert(format!("images/{image}").to_ascii_lowercase());
                }
            }
        }
    }
    Ok(())
}

fn capture_alias(definition: &str, aliases: &mut HashMap<String, String>) {
    let Some((alias, body)) = definition.split_once('=') else { return; };
    let Some(start) = body.find("images/") else { return; };
    let value = &body[start..];
    let end = value.find(['"', '\'']).unwrap_or(value.len());
    aliases.insert(alias.trim().to_ascii_lowercase(), value[..end].replace('\\', "/").to_ascii_lowercase());
}

fn capture_story_use(line: &str, uses: &mut Vec<String>) {
    let mut words = line.split_whitespace();
    let Some(statement) = words.next() else { return; };
    if !matches!(statement, "scene" | "show") { return; }
    if let Some(alias) = words.next() {
        uses.push(alias.trim_matches(|c: char| !c.is_ascii_alphanumeric() && c != '_').to_ascii_lowercase());
    }
}
