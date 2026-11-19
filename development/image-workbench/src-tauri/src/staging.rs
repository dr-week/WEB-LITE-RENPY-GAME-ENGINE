use crate::{assets::supported_image, project::checked_root};
use serde::Serialize;
use std::{fs, path::PathBuf};

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct StageResult {
    pub copied: Vec<String>,
    pub skipped: Vec<String>,
}

pub fn stage(value: &str, files: Vec<String>) -> Result<StageResult, String> {
    let root = checked_root(value)?;
    let images = root.join("game/images");
    let mut copied = Vec::new();
    let mut skipped = Vec::new();
    for source in files {
        stage_one(&source, &images, &mut copied, &mut skipped);
    }
    Ok(StageResult { copied, skipped })
}

fn stage_one(source: &str, images: &PathBuf, copied: &mut Vec<String>, skipped: &mut Vec<String>) {
    let source = match fs::canonicalize(source) {
        Ok(path) => path,
        Err(error) => {
            skipped.push(format!("{source}: {error}"));
            return;
        }
    };
    if !source.is_file() || !supported_image(&source) {
        skipped.push(format!("{}: not a supported image", source.display()));
        return;
    }
    let Some(name) = source.file_name() else {
        skipped.push(format!("{}: invalid filename", source.display()));
        return;
    };
    let destination = images.join(name);
    let sidecar = source.with_extension("json");
    let sidecar_destination = destination.with_extension("json");
    if destination.exists() || (sidecar.exists() && sidecar_destination.exists()) {
        skipped.push(format!(
            "{}: destination already exists",
            name.to_string_lossy()
        ));
        return;
    }
    if let Err(error) = fs::copy(&source, &destination) {
        skipped.push(format!("{}: {error}", source.display()));
        return;
    }
    if sidecar.exists() {
        if let Err(error) = fs::copy(&sidecar, &sidecar_destination) {
            let _ = fs::remove_file(&destination);
            skipped.push(format!(
                "{}: sidecar copy failed: {error}",
                source.display()
            ));
            return;
        }
    }
    copied.push(name.to_string_lossy().into_owned());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn image_filter_is_case_insensitive_and_rejects_non_images() {
        assert!(supported_image(&PathBuf::from("new-art.PNG")));
        assert!(supported_image(&PathBuf::from("new-art.jpeg")));
        assert!(!supported_image(&PathBuf::from("metadata.json")));
        assert!(!supported_image(&PathBuf::from("notes.txt")));
    }
}
