use crate::{assets::{files_below, importable_image}, project::checked_root, requests};
use serde_json::{json, Value};
use std::{fs, path::Path};

pub fn assign(value: &str, relative: &str, story_key: &str) -> Result<String, String> {
    let root = checked_root(value)?;
    let images = root.join("game/images").canonicalize().map_err(|error| error.to_string())?;
    let path = safe_image_path(&images, relative)?;
    if path.parent().is_some_and(|folder| folder.ends_with("character_reference")) {
        return Err("Reference pictures are not story scenes.".into());
    }
    let request = requests::load_target(&root, story_key)?;
    if request.role == "reference" { return Err("Reference pictures cannot be placed in story scenes.".into()); }
    reject_duplicate_target(&images, &path, story_key)?;
    save_assignment(&path, &request)?;
    Ok(format!("{} is ready for {}.", path.file_name().unwrap_or_default().to_string_lossy(), request.story_label))
}

fn safe_image_path(images: &Path, relative: &str) -> Result<std::path::PathBuf, String> {
    let given = Path::new(relative);
    if given.is_absolute() || given.components().any(|part| part == std::path::Component::ParentDir) {
        return Err("Choose a picture from the game image folders.".into());
    }
    let path = images.join(given).canonicalize().map_err(|error| error.to_string())?;
    if !path.starts_with(images) || !importable_image(&path) {
        return Err("That file is not a supported game picture.".into());
    }
    Ok(path)
}

fn reject_duplicate_target(images: &Path, selected: &Path, key: &str) -> Result<(), String> {
    for file in files_below(images)?.into_iter().filter(|item| item.extension().is_some_and(|ext| ext == "json")) {
        if file.with_extension("").canonicalize().ok().as_deref() == Some(selected) { continue; }
        let text = fs::read_to_string(&file).unwrap_or_default();
        let data: Value = serde_json::from_str(&text).unwrap_or(Value::Null);
        if data["story_key"] == key && data["role"] != "reference" {
            return Err("Another picture is already assigned to that story moment.".into());
        }
    }
    Ok(())
}

fn save_assignment(path: &Path, request: &requests::StoryRequest) -> Result<(), String> {
    let sidecar = path.with_extension("json");
    let mut data: Value = if sidecar.is_file() {
        serde_json::from_slice(&fs::read(&sidecar).map_err(|error| error.to_string())?)
            .map_err(|error| format!("Picture details are invalid: {error}"))?
    } else { json!({}) };
    let object = data.as_object_mut().ok_or("Picture details must be a JSON object.")?;
    for (field, value) in [("story_key", json!(&request.story_key)), ("story_file", json!(&request.story_file)),
        ("story_label", json!(&request.story_label)), ("dialogue_contains", json!(&request.dialogue_contains))] {
        object.insert(field.into(), value);
    }
    object.insert("role".into(), json!("cg"));
    object.insert("placement_status".into(), json!("target_selected"));
    fs::write(sidecar, serde_json::to_vec_pretty(&data).map_err(|error| error.to_string())?)
        .map_err(|error| format!("Could not save picture choice: {error}"))
}
