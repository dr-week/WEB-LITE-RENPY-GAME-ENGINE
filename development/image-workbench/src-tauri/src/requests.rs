use serde::{Deserialize, Serialize};
use std::{fs, path::Path};

#[derive(Clone, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct StoryRequest {
    pub story_key: String,
    pub category: String,
    pub role: String,
    pub story_file: String,
    pub story_label: String,
    pub dialogue_contains: String,
    #[serde(default)]
    pub reference_images: Vec<String>,
    #[serde(default)]
    pub starter_egg: String,
    #[serde(default)]
    pub prompt: String,
    #[serde(default)]
    pub image_path: String,
    #[serde(default)]
    pub status: String,
}

#[derive(Clone, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct StoryTarget {
    pub story_key: String,
    pub story_file: String,
    pub story_label: String,
    pub dialogue_contains: String,
    pub line: usize,
    #[serde(default)]
    pub current_scene: String,
}

#[derive(Deserialize)]
struct RequestCatalog {
    #[serde(default)]
    requests: Vec<StoryRequest>,
    #[serde(default)]
    story_targets: Vec<StoryTarget>,
}

fn read_catalog(root: &Path) -> Result<RequestCatalog, String> {
    let path = root.join("developer-tools/image_requests.json");
    if !path.is_file() {
        return Ok(RequestCatalog { requests: Vec::new(), story_targets: Vec::new() });
    }
    let text = fs::read_to_string(&path).map_err(|error| format!("Cannot read requests: {error}"))?;
    let catalog: RequestCatalog = serde_json::from_str(&text)
        .map_err(|error| format!("Invalid request catalog: {error}"))?;
    Ok(catalog)
}

pub fn load(root: &Path) -> Result<Vec<StoryRequest>, String> {
    Ok(read_catalog(root)?.requests)
}

pub fn load_targets(root: &Path) -> Result<Vec<StoryTarget>, String> {
    Ok(read_catalog(root)?.story_targets)
}

pub fn load_target(root: &Path, key: &str) -> Result<StoryRequest, String> {
    let catalog = read_catalog(root)?;
    if let Some(request) = catalog.requests.into_iter().find(|item| item.story_key == key) {
        return Ok(request);
    }
    let target = catalog.story_targets.into_iter().find(|item| item.story_key == key)
        .ok_or_else(|| "That story moment is out of date. Refresh the story list.".to_string())?;
    Ok(StoryRequest { story_key: target.story_key, category: "general_scenes".into(), role: "cg".into(),
        story_file: target.story_file, story_label: target.story_label,
        dialogue_contains: target.dialogue_contains, reference_images: Vec::new(), starter_egg: String::new(),
        prompt: String::new(), image_path: String::new(), status: "manual_target".into() })
}
