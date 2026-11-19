use std::path::Path;
use super::{models::{importable_image, supported_image}, walk::files_below};

pub fn image_counts(images: &Path) -> Result<(usize, usize), String> {
    let mut pending = 0;
    let mut total = 0;
    for path in files_below(images)? {
        if !supported_image(&path) { continue; }
        total += 1;
        if path.parent() == Some(images) && importable_image(&path) { pending += 1; }
    }
    Ok((pending, total))
}
