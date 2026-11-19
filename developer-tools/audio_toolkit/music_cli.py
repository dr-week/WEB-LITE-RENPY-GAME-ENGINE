"""CLI-Anything Click CLI & REPL for LOLA's Modular Music & Colab DJ System."""

import json
import shlex
import shutil
import zipfile
from pathlib import Path
import click

from checks.audio_health import check_audio_health
from .dj_planner import MIX_PLAN, MUSIC_DB, build_mix_plan
from .import_music import CREDITS_OUT, LOFI_DIR, import_music_folder, merge_colab_analysis, write_music_credits

ROOT = Path(__file__).resolve().parents[2]
STEMS_DIR = ROOT / "game" / "audio" / "music" / "stems"
DEFAULT_PACK_ZIP = Path.home() / "Downloads" / "lola_colab_tracks.zip"


def _emit(payload: dict, as_json: bool):
    if as_json:
        return click.echo(json.dumps(payload, indent=2, ensure_ascii=False))
    for k, v in payload.items():
        click.echo(f"{k}: {v}")


def _music_status() -> dict:
    health = check_audio_health(ROOT / "game")
    tracks = list(LOFI_DIR.iterdir()) if LOFI_DIR.is_dir() else []
    mp3s = sum(1 for p in tracks if p.suffix.lower() == ".mp3")
    oggs = sum(1 for p in tracks if p.suffix.lower() == ".ogg")
    stems = sum(1 for d in STEMS_DIR.iterdir() if d.is_dir()) if STEMS_DIR.is_dir() else 0
    return {
        "ok": health["ok"], "audio_mb": health["audio_mb"], "over_budget": health["over_budget"],
        "mp3_tracks": mp3s, "ogg_tracks": oggs, "stem_packs": stems,
        "missing": len(health["missing"]), "oversized_sfx": len(health["oversized_sfx"]),
    }


def _pack_for_colab(out_zip: Path) -> dict:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in LOFI_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".mp3", ".ogg", ".wav"})
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_STORED) as zf:
        for p in files:
            zf.write(p, arcname=p.name)
    return {"ok": True, "zip": str(out_zip), "tracks_packed": len(files)}


def _unpack_from_colab(export_zip: Path, replace_mp3: bool = True) -> dict:
    if not export_zip.is_file():
        return {"ok": False, "error": f"Missing zip: {export_zip}"}
    tmp_dir = export_zip.parent / "_colab_unpack_tmp"
    shutil.rmtree(tmp_dir, ignore_errors=True)
    with zipfile.ZipFile(export_zip, "r") as zf:
        zf.extractall(tmp_dir)
    analysis_files = list(tmp_dir.rglob("music_analysis.json"))
    merged = merge_colab_analysis(analysis_files[0]) if analysis_files else 0
    ogg_count, replaced_mp3 = 0, 0
    imported_oggs = set()
    for ogg in tmp_dir.rglob("*.ogg"):
        if "stems" in ogg.parts:
            dest = STEMS_DIR / ogg.parent.name / ogg.name
        else:
            dest = LOFI_DIR / ogg.name
            imported_oggs.add(ogg.stem)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ogg, dest)
        ogg_count += 1
    if replace_mp3 and imported_oggs and MUSIC_DB.is_file():
        db_tracks = json.loads(MUSIC_DB.read_text(encoding="utf-8-sig"))
        for track in db_tracks:
            if track["id"] in imported_oggs:
                old_mp3 = LOFI_DIR / f"{track['id']}.mp3"
                if old_mp3.is_file():
                    old_mp3.unlink()
                    replaced_mp3 += 1
                track["audio_file"] = f"game/audio/music/lofi/{track['id']}.ogg"
        MUSIC_DB.write_text(json.dumps(db_tracks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.rmtree(tmp_dir, ignore_errors=True)
    MIX_PLAN.write_text(json.dumps(build_mix_plan(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_music_credits()
    return {"ok": True, "analysis_merged": merged, "ogg_imported": ogg_count, "replaced_mp3": replaced_mp3}


def _repl(ctx, as_json: bool):
    click.echo("LOLA Modular Music REPL (type 'help' or 'exit').")
    while True:
        try:
            line = input("lola-music> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if line in ("exit", "quit"):
            break
        if line == "help":
            click.echo("Commands: status | plan | import --source <dir> --apply | colab pack | colab unpack <zip>")
        elif line:
            try:
                cli.main(args=shlex.split(line), standalone_mode=False, obj=ctx.obj)
            except Exception as exc:
                click.echo(json.dumps({"ok": False, "error": str(exc)}) if as_json else f"Error: {exc}")


@click.group(invoke_without_command=True)
@click.option("--json", "as_json", is_flag=True, help="Emit deterministic JSON output.")
@click.pass_context
def cli(ctx, as_json):
    """Agent-native CLI-Anything harness for LOLA's Modular Music & Colab workflow."""
    ctx.ensure_object(dict)["json"] = as_json
    if ctx.invoked_subcommand is None:
        _repl(ctx, as_json)


@cli.command("status")
@click.pass_context
def status_cmd(ctx):
    _emit(_music_status(), ctx.obj["json"])


@cli.command("plan")
@click.pass_context
def plan_cmd(ctx):
    plan = build_mix_plan()
    MIX_PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _emit({"ok": True, "tracks_planned": len(plan.get("tracks", {})), "mix_plan": str(MIX_PLAN)}, ctx.obj["json"])


@cli.command("import")
@click.option("--source", required=True, type=click.Path(path_type=Path))
@click.option("--recent-minutes", default=None, type=float)
@click.option("--apply", is_flag=True)
@click.pass_context
def import_cmd(ctx, source, recent_minutes, apply):
    _emit(import_music_folder(source, apply=apply, recent_minutes=recent_minutes), ctx.obj["json"])


@cli.group()
def colab():
    """Package tracks for Google Colab and unpack Colab .ogg/stem exports."""


@colab.command("pack")
@click.option("--out", default=DEFAULT_PACK_ZIP, type=click.Path(path_type=Path))
@click.pass_context
def colab_pack(ctx, out):
    _emit(_pack_for_colab(out), ctx.obj["json"])


@colab.command("unpack")
@click.argument("export_zip", type=click.Path(path_type=Path))
@click.pass_context
def colab_unpack(ctx, export_zip):
    _emit(_unpack_from_colab(export_zip), ctx.obj["json"])
