use std::{collections::BTreeMap, fs, path::Path};
use super::{models::{ImageCategory, ImageFile, ImageInventory}, scan::{image_paths, story_image_paths}};

pub fn image_inventory(game: &Path) -> Result<ImageInventory, String> {
    let used_paths = story_image_paths(game)?;
    let mut groups: BTreeMap<String, Vec<ImageFile>> = BTreeMap::new();
    for path in image_paths(&game.join("images"))? {
        let category = path.split('/').next().filter(|_| path.contains('/')).unwrap_or("Uncategorized").to_string();
        let used = used_paths.contains(&format!("images/{path}").to_ascii_lowercase());
        let name = path.rsplit('/').next().unwrap_or(&path).to_string();
        let metadata = read_metadata(&game.join("images").join(&path));
        let story_key = text_field(&metadata, "story_key");
        let target = story_target(&metadata);
        let status = text_field(&metadata, "placement_status")
            .unwrap_or_else(|| if used { "placed".into() } else if story_key.is_some() { "generated".into() } else { "untracked".into() });
        groups.entry(category).or_default().push(ImageFile {
            name, path, used_in_story: used,
            asset_id: text_field(&metadata, "asset_id"), story_key,
            role: text_field(&metadata, "role"), category_hint: text_field(&metadata, "category"),
            placement_status: status,
            story_target: target,
        });
    }
    let categories: Vec<ImageCategory> = groups.into_iter().map(category).collect();
    let total = categories.iter().map(|item| item.total).sum();
    let story_used = categories.iter().map(|item| item.story_used).sum();
    Ok(ImageInventory { total, story_used, unused: total - story_used, categories })
}

fn read_metadata(image: &Path) -> serde_json::Value {
    fs::read_to_string(image.with_extension("json"))
        .ok().and_then(|text| serde_json::from_str(&text).ok())
        .unwrap_or(serde_json::Value::Null)
}

fn text_field(data: &serde_json::Value, key: &str) -> Option<String> {
    data.get(key).and_then(serde_json::Value::as_str)
        .filter(|value| !value.is_empty()).map(str::to_string)
}

fn story_target(data: &serde_json::Value) -> Option<String> {
    let target = data.get("story_target").unwrap_or(data);
    let file = text_field(target, "file").or_else(|| text_field(target, "story_file"))?;
    let label = text_field(target, "label").or_else(|| text_field(target, "story_label"))?;
    Some(format!("{file} · {label}"))
}

fn category((name, mut files): (String, Vec<ImageFile>)) -> ImageCategory {
    files.sort_by(|a, b| a.name.to_lowercase().cmp(&b.name.to_lowercase()));
    let total = files.len();
    let story_used = files.iter().filter(|file| file.used_in_story).count();
    ImageCategory { name, total, story_used, unused: total - story_used, files }
}
