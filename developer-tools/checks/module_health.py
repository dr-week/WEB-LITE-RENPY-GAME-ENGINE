"""Verify active .py and .rpy modules stay compact and modular."""

from pathlib import Path


def check_module_sizes(project_root: Path, warn_limit: int = 150) -> dict:
    """Flag active source files exceeding warn_limit lines."""
    oversized = []
    targets = [
        *sorted((project_root / "developer-tools").rglob("*.py")),
        *sorted((project_root / "game").rglob("*.rpy")),
    ]
    for path in targets:
        if any(part in {"__pycache__", "tests", "cache"} for part in path.parts):
            continue
        count = len(path.read_text(encoding="utf-8-sig", errors="ignore").splitlines())
        if count > warn_limit:
            oversized.append((path.relative_to(project_root).as_posix(), count))
    return {"ok": True, "checked": len(targets), "oversized": oversized}
