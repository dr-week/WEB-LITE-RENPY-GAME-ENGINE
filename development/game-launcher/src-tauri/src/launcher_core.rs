use serde::{Deserialize, Serialize};
use std::{fs, path::{Path, PathBuf}, process::{Command, Stdio}};
#[cfg(windows)]
use std::os::windows::process::CommandExt;

#[derive(Serialize, Deserialize, Clone)]
pub struct Settings {
    pub sdk: String,
    pub mode: String,
    pub fullscreen: bool,
}

#[derive(Serialize)]
pub struct LauncherState {
    pub version: String,
    pub sdk: String,
    pub mode: String,
    pub fullscreen: bool,
    pub hero_data_url: Option<String>,
    pub game_running: bool,
}

const SDK_CANDIDATES: &[&str] = &[
    "C:/RenPy/renpy-8.6.0/renpy-8.6.0-sdk",
    "C:/RenPy/renpy-8.6.0-sdk",
    "C:/renpy-8.6.0-sdk",
];

pub fn project_root() -> PathBuf {
    let mut dir = std::env::current_exe().ok().and_then(|p| p.parent().map(Path::to_path_buf))
        .unwrap_or_else(|| std::env::current_dir().unwrap_or_default());
    for _ in 0..8 {
        if dir.join("game/script.rpy").is_file() { return dir; }
        if !dir.pop() { break; }
    }
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).ancestors().nth(3).unwrap_or(Path::new(".")).to_path_buf()
}

fn config_path(root: &Path) -> PathBuf { root.join("launcher/tools/launcher_settings.json") }
fn pid_path(root: &Path) -> PathBuf { root.join("launcher/tools/.lola_game.pid") }

pub fn load_settings(root: &Path) -> Settings {
    let mut cfg = fs::read_to_string(config_path(root)).ok()
        .and_then(|s| serde_json::from_str::<Settings>(&s).ok())
        .unwrap_or(Settings { sdk: String::new(), mode: "Auto (Recommended)".into(), fullscreen: false });
    if cfg.sdk.is_empty() || !Path::new(&cfg.sdk).join("renpy.py").is_file() {
        cfg.sdk = SDK_CANDIDATES.iter().find(|s| Path::new(s).join("renpy.py").is_file()).unwrap_or(&"").to_string();
    }
    cfg
}

pub fn save_settings(root: &Path, cfg: &Settings) -> Result<(), String> {
    if let Some(p) = config_path(root).parent() { let _ = fs::create_dir_all(p); }
    let body = serde_json::to_string_pretty(cfg).map_err(|e| e.to_string())?;
    fs::write(config_path(root), format!("{body}\n")).map_err(|e| e.to_string())
}

pub fn detect_version(root: &Path) -> String {
    let txt = fs::read_to_string(root.join("game/script.rpy")).unwrap_or_default();
    txt.lines().find(|l| l.contains("config.version")).and_then(|l| l.split('"').nth(1))
        .unwrap_or("0.1.0").to_string()
}

pub fn is_game_running(root: &Path) -> bool {
    let Ok(pid) = fs::read_to_string(pid_path(root)) else { return false };
    let pid = pid.trim();
    if pid.is_empty() { return false; }
    #[cfg(windows)]
    {
        let mut cmd = Command::new("tasklist");
        cmd.args(["/FI", &format!("PID eq {pid}"), "/NH"]).creation_flags(0x08000000);
        if let Ok(out) = cmd.output() {
            return String::from_utf8_lossy(&out.stdout).contains(pid);
        }
    }
    false
}

pub fn launch_renpy(root: &Path, cfg: &Settings) -> Result<(), String> {
    if is_game_running(root) { return Err("LOLA is already running.".into()); }
    if cfg.sdk.is_empty() { return Err("Ren'Py SDK not found.".into()); }
    let sdk = Path::new(&cfg.sdk);
    let pyw = sdk.join("lib/py3-windows-x86_64/pythonw.exe");
    let mut cmd = if pyw.is_file() { Command::new(&pyw) } else { Command::new(sdk.join("renpy.exe")) };
    if pyw.is_file() { cmd.arg(sdk.join("renpy.py")); }
    cmd.arg(root).arg("run").current_dir(sdk).stdin(Stdio::null());
    if cfg.mode == "ANGLE / DirectX" { cmd.env("RENPY_RENDERER", "angle2"); }
    if cfg.mode == "Software (No GPU)" { cmd.env("RENPY_RENDERER", "sw"); }
    if cfg.fullscreen { cmd.env("RENPY_FULLSCREEN", "1"); }
    if let Ok(log) = fs::File::create(root.join("launcher/last_launch.log")) {
        if let Ok(err) = log.try_clone() { cmd.stdout(Stdio::from(log)).stderr(Stdio::from(err)); }
    }
    #[cfg(windows)]
    cmd.creation_flags(0x08000000);
    let child = cmd.spawn().map_err(|e| format!("Failed to start LOLA: {e}"))?;
    let _ = fs::write(pid_path(root), child.id().to_string());
    Ok(())
}
