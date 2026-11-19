use crate::{pipeline, project, staging};

#[tauri::command]
pub fn default_project_root() -> String {
    project::default_root().display().to_string()
}

#[tauri::command]
pub fn project_status(project_root: String) -> Result<project::ProjectStatus, String> {
    project::status(&project_root)
}

#[tauri::command]
pub fn stage_images(
    project_root: String,
    files: Vec<String>,
) -> Result<staging::StageResult, String> {
    staging::stage(&project_root, files)
}

#[tauri::command]
pub fn prepare_image_metadata(
    project_root: String,
    image_name: String,
    story_key: Option<String>,
    category: String,
    role: String,
) -> Result<String, String> {
    crate::assignment::prepare(&project_root, &image_name, story_key, &category, &role)
}

#[tauri::command]
pub fn assign_asset_to_story(project_root: String, image_path: String, story_key: String) -> Result<String, String> {
    crate::story_assignment::assign(&project_root, &image_path, &story_key)
}

#[tauri::command]
pub fn run_project_script(
    project_root: String,
    python_exe: String,
    action: String,
) -> Result<pipeline::OperationResult, String> {
    pipeline::run(&project_root, &python_exe, &action)
}

#[tauri::command]
pub fn open_project_document(project_root: String, document: String) -> Result<(), String> {
    project::open_document(&project_root, &document)
}

#[tauri::command]
pub fn create_story_day(
    project_root: String,
    python_exe: String,
    day_num: u32,
    theme: String,
    seed: Option<u32>,
) -> Result<pipeline::OperationResult, String> {
    pipeline::create_day(&project_root, &python_exe, day_num, &theme, seed)
}
