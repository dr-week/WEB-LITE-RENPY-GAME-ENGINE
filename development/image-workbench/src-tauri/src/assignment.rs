use crate::{project::checked_root, requests};
use serde_json::{json, Value};
use std::{fs, path::Path};

pub fn prepare(value: &str, name: &str, key: Option<String>, category: &str, role: &str) -> Result<String, String> {
    let root = checked_root(value)?;
    validate_category(category)?;
    if !matches!(role, "cg" | "background" | "reference") {
        return Err("Role must be cg, background, or reference.".into());
    }
    let images = root.join("game/images");
    let image = images.join(name);
    if Path::new(name).file_name().and_then(|value| value.to_str()) != Some(name)
        || !image.is_file() || !supported_image(&image) {
        return Err("Choose an image staged at the top level of game/images.".into());
    }
    let mut metadata = read_sidecar(&image)?;
    if !metadata.is_object() { return Err("Image sidecar must contain a JSON object.".into()); }
    if let Some(key) = key {
        if role == "reference" { return Err("Reference images cannot target story requests.".into()); }
        let request = requests::load(&root)?.into_iter().find(|item| item.story_key == key)
            .ok_or_else(|| format!("Request ID is not in the latest scan: {key}"))?;
        for (field, value) in [("story_key", json!(request.story_key)),
            ("story_file", json!(request.story_file)), ("story_label", json!(request.story_label)),
            ("dialogue_contains", json!(request.dialogue_contains)),
            ("reference_images", json!(request.reference_images)), ("starter_egg", json!(request.starter_egg))] {
            metadata[field] = value;
        }
    } else {
        for field in ["story_key", "story_file", "story_label", "dialogue_contains"] {
            metadata.as_object_mut().unwrap().remove(field);
        }
        metadata.as_object_mut().unwrap().remove("story_target");
    }
    metadata["category"] = json!(category);
    metadata["role"] = json!(role);
    metadata["placement_status"] = json!(if role == "reference" { "reference_only" } else { "staged" });
    let sidecar = image.with_extension("json");
    fs::write(&sidecar, serde_json::to_vec_pretty(&metadata).unwrap())
        .map_err(|error| format!("Cannot save image metadata: {error}"))?;
    Ok(format!("Saved metadata for {name}; preview it before import."))
}

fn read_sidecar(image: &Path) -> Result<Value, String> {
    let path = image.with_extension("json");
    if !path.is_file() { return Ok(json!({})); }
    let text = fs::read_to_string(path).map_err(|error| error.to_string())?;
    serde_json::from_str(&text).map_err(|error| format!("Invalid image sidecar: {error}"))
}

fn validate_category(category: &str) -> Result<(), String> {
    if !category.is_empty() && category.bytes().all(|byte| byte.is_ascii_lowercase() || byte.is_ascii_digit() || b"_-".contains(&byte)) {
        Ok(())
    } else { Err("Category must use lowercase letters, numbers, underscores, or hyphens.".into()) }
}

fn supported_image(path: &Path) -> bool {
    matches!(path.extension().and_then(|value| value.to_str()).map(str::to_ascii_lowercase).as_deref(),
        Some("png" | "jpg" | "jpeg" | "webp"))
}
