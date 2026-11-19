"""Output formatter and stateful REPL loop for Modular Flow Engine."""

import json
import shlex
import click


def emit(payload: dict, as_json: bool):
    if as_json:
        return click.echo(json.dumps(payload, indent=2, ensure_ascii=False))
    for k, v in payload.items():
        if k not in ("flow_batch", "items", "open_requests"):
            click.echo(f"{k}: {v}")
    if "flow_batch" in payload:
        click.echo("\n" + payload["flow_batch"])


def run_repl(cli_group, ctx, as_json: bool):
    click.echo("LOLA Modular Flow REPL (type 'help' or 'exit').")
    while True:
        try:
            line = input("lola-flow> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if line in ("exit", "quit"):
            break
        if line == "help":
            click.echo("Commands: session | prompt menu | prompt story | flow open | flow ingest | pipeline <audit|catalog|preview|organize>")
        elif line:
            try:
                cli_group.main(args=shlex.split(line), standalone_mode=False, obj=ctx.obj)
            except Exception as exc:
                click.echo(json.dumps({"ok": False, "error": str(exc)}) if as_json else f"Error: {exc}")
