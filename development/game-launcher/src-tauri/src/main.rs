#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod launcher_core;
mod media;
use launcher_core::{
    detect_version, is_game_running, launch_renpy, load_settings, project_root, save_settings,
    LauncherState,
};
use media::hero_data_url;

#[tauri::command]
fn get_launcher_state() -> LauncherState {
    let root = project_root();
    let cfg = load_settings(&root);
    LauncherState {
        version: detect_version(&root),
        sdk: cfg.sdk,
        mode: cfg.mode,
        fullscreen: cfg.fullscreen,
        hero_data_url: hero_data_url(&root),
        game_running: is_game_running(&root),
    }
}

#[tauri::command]
fn save_launcher_settings(mode: String, fullscreen: bool, sdk: Option<String>) -> Result<(), String> {
    let root = project_root();
    let mut cfg = load_settings(&root);
    cfg.mode = mode;
    cfg.fullscreen = fullscreen;
    if let Some(s) = sdk { cfg.sdk = s; }
    save_settings(&root, &cfg)
}

#[tauri::command]
fn launch_lola_game(app: tauri::AppHandle) -> Result<(), String> {
    let root = project_root();
    let cfg = load_settings(&root);
    launch_renpy(&root, &cfg)?;
    app.exit(0);
    Ok(())
}

#[tauri::command]
fn exit_launcher(app: tauri::AppHandle) {
    app.exit(0);
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            get_launcher_state,
            save_launcher_settings,
            launch_lola_game,
            exit_launcher
        ])
        .run(tauri::generate_context!())
        .expect("error while running LOLA game launcher");
}
