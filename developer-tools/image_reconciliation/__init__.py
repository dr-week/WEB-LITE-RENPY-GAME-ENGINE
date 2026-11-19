"""Scan, propose, and apply safe placements for unused game artwork."""


def __getattr__(name):
    if name == "apply_reconciliation":
        from .apply import apply_reconciliation
        return apply_reconciliation
    if name == "plan_reconciliation":
        from .scan import plan_reconciliation
        return plan_reconciliation
    if name == "write_story_proposals":
        from .log import write_story_proposals
        return write_story_proposals
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
