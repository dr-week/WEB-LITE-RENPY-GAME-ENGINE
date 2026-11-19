use crate::project::checked_root;
use serde::Serialize;
use std::{
    path::{Path, PathBuf},
    process::Command,
};

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct OperationResult {
    pub success: bool,
    pub stdout: String,
    pub stderr: String,
}

pub fn script_for(root: &Path, action: &str) -> Result<(PathBuf, Vec<&'static str>), String> {
    let (file, args): (&str, Vec<&str>) = match action {
        "generate" => ("generate_image_list.py", vec![]),
        "preview" => ("integrate_story_images.py", vec![]),
        "apply" => ("integrate_story_images.py", vec!["--apply"]),
        "audit" => ("audit_images.py", vec![]),
        "reconcile" => ("reconcile_story_images.py", vec![]),
        "reconcile_apply" => ("reconcile_story_images.py", vec!["--apply"]),
        "catalog" => ("build_image_story_catalog.py", vec![]),
        "organize" => ("organize_images.py", vec!["--apply"]),
        "verify_project" => ("checks/run_all_checks.py", vec![]),
        "story_validate" => ("story_maker.py", vec!["validate", "--json"]),
        "voice_status" => ("voice_maker.py", vec!["status"]),
        "voice_scan" => ("voice_maker.py", vec!["scan"]),
        "voice_synth" => ("voice_maker.py", vec!["synth", "--limit", "10"]),
        "voice_mumbles" => ("generate_maya_voice.py", vec![]),
        _ => return Err(format!("Unsupported workbench action: {action}")),
    };
    Ok((root.join("developer-tools").join(file), args))
}

pub fn run(root_value: &str, python: &str, action: &str) -> Result<OperationResult, String> {
    let root = checked_root(root_value)?;
    if python.trim().is_empty() {
        return Err("Enter a Python executable, such as python or its full path.".to_string());
    }
    let (script, args) = script_for(&root, action)?;
    let mut process = Command::new(python.trim());
    process.arg(script).args(args).current_dir(&root);
    let result = process
        .output()
        .map_err(|error| format!("Could not run Python: {error}"))?;
    Ok(OperationResult {
        success: result.status.success(),
        stdout: String::from_utf8_lossy(&result.stdout).into_owned(),
        stderr: String::from_utf8_lossy(&result.stderr).into_owned(),
    })
}

pub fn create_day(root_value: &str, python: &str, day_num: u32, theme: &str, seed: Option<u32>) -> Result<OperationResult, String> {
    let root = checked_root(root_value)?;
    let script = root.join("developer-tools/story_maker.py");
    let out_path = root.join(format!("game/40_story/chapters/day_{day_num:02}.rpy"));
    let mut cmd = Command::new(python.trim());
    cmd.arg(script).args(["create-day", "--day-num", &day_num.to_string(), "--theme", theme, "--out", &out_path.to_string_lossy()]);
    if let Some(s) = seed { cmd.args(["--seed", &s.to_string()]); }
    let res = cmd.current_dir(&root).output().map_err(|e| format!("Could not run Python: {e}"))?;
    Ok(OperationResult {
        success: res.status.success(),
        stdout: String::from_utf8_lossy(&res.stdout).into_owned(),
        stderr: String::from_utf8_lossy(&res.stderr).into_owned(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn only_known_project_scripts_can_run() {
        let root = Path::new("project");
        assert!(script_for(root, "preview")
            .unwrap()
            .0
            .ends_with("integrate_story_images.py"));
        assert_eq!(script_for(root, "apply").unwrap().1, vec!["--apply"]);
        assert!(script_for(root, "audit")
            .unwrap()
            .0
            .ends_with("audit_images.py"));
        assert!(script_for(root, "catalog")
            .unwrap()
            .0
            .ends_with("build_image_story_catalog.py"));
        assert!(script_for(root, "catalog").unwrap().1.is_empty());
        assert!(script_for(root, "organize")
            .unwrap()
            .0
            .ends_with("organize_images.py"));
        assert_eq!(script_for(root, "organize").unwrap().1, vec!["--apply"]);
        assert_eq!(script_for(root, "voice_scan").unwrap().1, vec!["scan"]);
        assert!(script_for(root, "arbitrary-command").is_err());
    }
}
