mod assets;
mod assignment;
mod commands;
mod pipeline;
mod project;
mod requests;
mod staging;
mod story_assignment;

#[cfg(test)]
mod workflow_tests;

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            commands::default_project_root,
            commands::project_status,
            commands::stage_images,
            commands::prepare_image_metadata,
            commands::assign_asset_to_story,
            commands::run_project_script,
            commands::create_story_day,
            commands::open_project_document
        ])
        .run(tauri::generate_context!())
        .expect("failed to start LOLA Image Workbench");
}
