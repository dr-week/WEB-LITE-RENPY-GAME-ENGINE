use std::{fs, path::{Path, PathBuf}};

pub fn hero_data_url(root: &Path) -> Option<String> {
    let mut pics: Vec<PathBuf> = fs::read_dir(root.join("game/images/menu_assets")).ok()?
        .filter_map(|e| e.ok().map(|x| x.path()))
        .filter(|p| p.extension().is_some_and(|e| e == "jpg"))
        .collect();
    pics.sort();
    if pics.is_empty() { return None; }
    let idx = (std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).ok()?.subsec_nanos() as usize) % pics.len();
    let bytes = fs::read(&pics[idx]).ok()?;
    Some(format!("data:image/jpeg;base64,{}", encode_b64(&bytes)))
}

fn encode_b64(data: &[u8]) -> String {
    const T: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut out = String::with_capacity((data.len() + 2) / 3 * 4);
    for chunk in data.chunks(3) {
        let b = [chunk[0], *chunk.get(1).unwrap_or(&0), *chunk.get(2).unwrap_or(&0)];
        let n = ((b[0] as u32) << 16) | ((b[1] as u32) << 8) | (b[2] as u32);
        out.push(T[((n >> 18) & 63) as usize] as char);
        out.push(T[((n >> 12) & 63) as usize] as char);
        out.push(if chunk.len() > 1 { T[((n >> 6) & 63) as usize] as char } else { '=' });
        out.push(if chunk.len() > 2 { T[(n & 63) as usize] as char } else { '=' });
    }
    out
}
