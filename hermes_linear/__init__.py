"""Linear Agent platform plugin."""


def register(ctx) -> None:
    """Register the Linear Agent platform adapter lazily.

    Lazy import keeps `python -m hermes_linear.oauth` from importing the
    gateway adapter before the OAuth CLI module executes.
    """
    from .adapter import register as _register

    return _register(ctx)


__all__ = ["register"]
