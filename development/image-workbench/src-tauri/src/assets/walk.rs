use std::{fs, path::{Path, PathBuf}};

pub fn files_below(root: &Path) -> Result<Vec<PathBuf>, String> {
    let mut files = Vec::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(folder) = stack.pop() {
        for entry in fs::read_dir(&folder)
            .map_err(|error| format!("Cannot scan {}: {error}", folder.display()))?
        {
            let entry = entry.map_err(|error| format!("Cannot read entry: {error}"))?;
            let kind = entry.file_type().map_err(|error| format!("Cannot inspect entry: {error}"))?;
            if kind.is_dir() { stack.push(entry.path()); }
            else if kind.is_file() { files.push(entry.path()); }
        }
    }
    Ok(files)
}
