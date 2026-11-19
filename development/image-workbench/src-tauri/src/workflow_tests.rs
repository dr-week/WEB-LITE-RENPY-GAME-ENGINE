use crate::{assignment, project, staging, story_assignment};
use std::{fs, path::PathBuf};

fn fixture() -> PathBuf {
    let nonce = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let root = std::env::temp_dir().join(format!("lola-workbench-{}-{nonce}", std::process::id()));
    for path in ["game/images", "developer-tools"] {
        fs::create_dir_all(root.join(path)).unwrap();
    }
    for path in [
        "generate_image_list.py",
        "integrate_story_images.py",
        "audit_images.py",
    ] {
        fs::write(root.join("developer-tools").join(path), "").unwrap();
    }
    root
}

#[test]
fn default_project_root_is_the_game_workspace() {
    assert!(project::status(project::default_root().to_str().unwrap()).is_ok());
}

#[test]
fn staging_copies_image_and_sidecar_without_overwriting() {
    let root = fixture();
    let input = root.join("incoming");
    fs::create_dir_all(&input).unwrap();
    fs::write(input.join("campus.png"), b"image").unwrap();
    fs::write(input.join("campus.json"), b"{\"category\":\"college\"}").unwrap();
    let staged = staging::stage(
        root.to_str().unwrap(),
        vec![input.join("campus.png").display().to_string()],
    )
    .unwrap();
    assert_eq!(staged.copied, ["campus.png"]);
    assert_eq!(
        fs::read(root.join("game/images/campus.json")).unwrap(),
        b"{\"category\":\"college\"}"
    );
    let repeated = staging::stage(
        root.to_str().unwrap(),
        vec![input.join("campus.png").display().to_string()],
    )
    .unwrap();
    assert_eq!(repeated.skipped.len(), 1);
    fs::remove_dir_all(root).unwrap();
}

#[test]
fn request_assignment_writes_sidecar_from_current_request_catalog() {
    let root = fixture();
    fs::write(root.join("game/images/new_scene.jpg"), b"image").unwrap();
    fs::write(root.join("developer-tools/image_requests.json"), r#"{"requests":[{
        "storyKey":"story_a102", "category":"college", "role":"cg",
        "storyFile":"40_story/day.rpy", "storyLabel":"campus",
        "dialogueContains":"Maya reaches campus.", "referenceImages":[],
        "starterEgg":"", "prompt":"", "imagePath":"", "status":"needs_generation"
    }]}"#).unwrap();
    assignment::prepare(root.to_str().unwrap(), "new_scene.jpg", Some("story_a102".into()), "college", "cg").unwrap();
    let sidecar: serde_json::Value = serde_json::from_slice(
        &fs::read(root.join("game/images/new_scene.json")).unwrap()).unwrap();
    assert_eq!(sidecar["story_key"], "story_a102");
    assert_eq!(sidecar["story_label"], "campus");
    assert_eq!(sidecar["placement_status"], "staged");
    fs::remove_dir_all(root).unwrap();
}

#[test]
fn user_can_assign_existing_picture_to_unique_story_dialogue() {
    let root = fixture();
    fs::create_dir_all(root.join("game/images/college")).unwrap();
    fs::write(root.join("game/images/college/old_art.jpg"), b"image").unwrap();
    fs::write(root.join("game/images/college/duplicate.jpg"), b"other image").unwrap();
    fs::write(root.join("developer-tools/image_requests.json"), r#"{"story_targets":[{
        "storyKey":"story_abcd", "storyFile":"40_story/day.rpy", "storyLabel":"campus",
        "dialogueContains":"Maya reaches campus.", "line":12, "currentScene":"bg_campus"
    }]}"#).unwrap();
    story_assignment::assign(root.to_str().unwrap(), "college/old_art.jpg", "story_abcd").unwrap();
    let sidecar: serde_json::Value = serde_json::from_slice(
        &fs::read(root.join("game/images/college/old_art.json")).unwrap()).unwrap();
    assert_eq!(sidecar["dialogue_contains"], "Maya reaches campus.");
    assert_eq!(sidecar["placement_status"], "target_selected");
    assert!(story_assignment::assign(root.to_str().unwrap(), "college/duplicate.jpg", "story_abcd").is_err());
    fs::remove_dir_all(root).unwrap();
}
