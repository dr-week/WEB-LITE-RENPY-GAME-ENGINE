"""CLI-Anything Click CLI & stateful REPL for LOLA's Modular Flow Engine."""

from pathlib import Path
import click
from modules.modular_flow_engine.adapters.flow_browser_adapter import copy_to_clipboard, open_flow_session
from modules.modular_flow_engine.adapters.workbench_adapter import run_pipeline_action
from modules.modular_flow_engine.cli.repl import emit, run_repl
from modules.modular_flow_engine.core.batch_builder import build_prompt_batch, list_open_story_requests
from modules.modular_flow_engine.core.session_state import load_session, save_session
from modules.modular_flow_engine.ingest.download_matcher import ingest_flow_downloads


@click.group(invoke_without_command=True)
@click.option("--json", "as_json", is_flag=True, help="Emit deterministic JSON output.")
@click.pass_context
def cli(ctx, as_json):
    """Agent-native CLI-Anything harness for LOLA's Modular Flow Engine."""
    ctx.ensure_object(dict)["json"] = as_json
    if ctx.invoked_subcommand is None:
        run_repl(cli, ctx, as_json)


@cli.command("session")
@click.option("--downloads", default=None, type=click.Path(path_type=Path), help="Set default downloads folder.")
@click.pass_context
def session_cmd(ctx, downloads):
    state = save_session({"downloads_dir": str(downloads)}) if downloads else load_session()
    emit({"ok": True, **state}, ctx.obj["json"])


@cli.group()
def prompt():
    """Generate Flow-ready menu and story image prompts."""


@prompt.command("menu")
@click.option("--count", default=5, show_default=True)
@click.option("--seed", default=None, type=int)
@click.option("--story", is_flag=True)
@click.option("--theme", default="")
@click.option("--copy", is_flag=True, help="Copy Flow batch to clipboard.")
@click.pass_context
def prompt_menu(ctx, count, seed, story, theme, copy):
    res = build_prompt_batch(count, seed, story, theme)
    save_session({"last_count": count, "last_asset_ids": [i["asset_id"] for i in res["items"]]})
    res["copied_to_clipboard"] = copy_to_clipboard(res["flow_batch"]) if copy else False
    emit(res, ctx.obj["json"])


@prompt.command("story")
@click.option("--refresh", is_flag=True)
@click.pass_context
def prompt_story(ctx, refresh):
    emit(list_open_story_requests(refresh), ctx.obj["json"])


@cli.group()
def flow():
    """Operate Google Flow batches and ingest downloaded images."""


@flow.command("open")
@click.option("--count", default=5, show_default=True)
@click.option("--theme", default="")
@click.pass_context
def flow_open(ctx, count, theme):
    res = build_prompt_batch(count=count, story=bool(theme), theme=theme)
    save_session({"last_count": count, "last_asset_ids": [i["asset_id"] for i in res["items"]]})
    emit(open_flow_session(res["flow_batch"], res["count"]), ctx.obj["json"])


@flow.command("ingest")
@click.option("--latest", default=None, type=int)
@click.option("--file", "file_path", default=None, type=click.Path(path_type=Path))
@click.option("--asset-id", default=None)
@click.option("--downloads", default=None, type=click.Path(path_type=Path))
@click.option("--no-rebuild", is_flag=True)
@click.pass_context
def flow_ingest(ctx, latest, file_path, asset_id, downloads, no_rebuild):
    dl = downloads or Path(load_session()["downloads_dir"])
    emit(ingest_flow_downloads(latest, file_path, asset_id, dl, not no_rebuild), ctx.obj["json"])


@cli.command("pipeline")
@click.argument("action", type=click.Choice(["audit", "catalog", "preview", "organize"]))
@click.pass_context
def pipeline(ctx, action):
    emit(run_pipeline_action(action), ctx.obj["json"])
