use super::image_inventory;
use std::fs;

#[test]
fn inventory_counts_unique_story_assets_and_categories() {
    let root = std::env::temp_dir().join(format!("lola-image-inventory-{}", std::process::id()));
    let game = root.join("game");
    fs::create_dir_all(game.join("images/college")).unwrap();
    fs::create_dir_all(game.join("images/home")).unwrap();
    fs::create_dir_all(game.join("images/transport")).unwrap();
    fs::create_dir_all(game.join("10_characters")).unwrap();
    fs::create_dir_all(game.join("40_story/prologue")).unwrap();
    fs::write(game.join("images/college/class.jpg"), b"image").unwrap();
    fs::write(game.join("images/college/class.json"),
        r#"{"asset_id":"asset_a102","story_key":"story_01a102","role":"cg","placement_status":"placed","story_target":{"file":"40_story/prologue/day.rpy","label":"arrive_college"}}"#).unwrap();
    fs::write(game.join("images/home/room.png"), b"image").unwrap();
    fs::write(game.join("images/transport/bus.jpg"), b"image").unwrap();
    fs::create_dir_all(game.join("data")).unwrap();
    fs::write(game.join("data/image_story_catalog.json"),
        r#"{"events":[{"images":["transport/bus.jpg"]}]}"#).unwrap();
    fs::write(game.join("10_characters/art.rpy"), "image cg_class = fit_scene_art(\"images/college/class.jpg\")\n").unwrap();
    fs::write(game.join("40_story/prologue/day.rpy"), "label day:\n    scene cg_class\n    \"Class begins.\"\n").unwrap();

    let inventory = image_inventory(&game).unwrap();
    assert_eq!((inventory.total, inventory.story_used, inventory.unused), (3, 2, 1));
    assert_eq!(inventory.categories.len(), 3);
    assert_eq!(inventory.categories.iter().find(|item| item.name == "college").unwrap().story_used, 1);
    let class = inventory.categories.iter().find(|item| item.name == "college").unwrap()
        .files.iter().find(|file| file.name == "class.jpg").unwrap();
    assert_eq!(class.asset_id.as_deref(), Some("asset_a102"));
    assert_eq!(class.story_key.as_deref(), Some("story_01a102"));
    assert_eq!(class.placement_status, "placed");
    assert_eq!(class.story_target.as_deref(), Some("40_story/prologue/day.rpy · arrive_college"));
    assert_eq!(inventory.categories.iter().find(|item| item.name == "transport").unwrap().story_used, 1);
    fs::remove_dir_all(root).unwrap();
}
