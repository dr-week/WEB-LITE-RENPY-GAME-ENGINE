use serde::Serialize;
use std::path::Path;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ImageFile {
    pub name: String,
    pub path: String,
    pub used_in_story: bool,
    pub asset_id: Option<String>,
    pub story_key: Option<String>,
    pub role: Option<String>,
    pub category_hint: Option<String>,
    pub placement_status: String,
    pub story_target: Option<String>,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ImageCategory {
    pub name: String,
    pub total: usize,
    pub story_used: usize,
    pub unused: usize,
    pub files: Vec<ImageFile>,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ImageInventory {
    pub total: usize,
    pub story_used: usize,
    pub unused: usize,
    pub categories: Vec<ImageCategory>,
}

pub fn importable_image(path: &Path) -> bool {
    matches!(extension(path).as_deref(), Some("png" | "jpg" | "jpeg" | "webp"))
}

pub fn supported_image(path: &Path) -> bool {
    matches!(extension(path).as_deref(), Some("png" | "jpg" | "jpeg" | "webp" | "gif" | "bmp" | "avif"))
}

fn extension(path: &Path) -> Option<String> {
    path.extension().and_then(|value| value.to_str()).map(str::to_ascii_lowercase)
}
