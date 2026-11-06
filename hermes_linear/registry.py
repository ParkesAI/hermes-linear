"""Plugin-local registry for the active Linear Agent adapter.

A standalone plugin is loaded under one package identity per installation
mode, so it can keep runtime state locally instead of mutating Hermes' global
tool registry.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from hermes_constants import get_hermes_home

if TYPE_CHECKING:
    from .adapter import LinearAgentAdapter

_active_adapters: dict[str, LinearAgentAdapter] = {}


def set_active_adapter(adapter: LinearAgentAdapter | None) -> None:
    """Register or clear the currently connected Linear Agent adapter."""
    key = str(get_hermes_home().resolve())
    if adapter is None:
        _active_adapters.pop(key, None)
    else:
        _active_adapters[key] = adapter


def get_active_adapter() -> LinearAgentAdapter:
    """Return the currently connected Linear Agent adapter."""
    adapter = _active_adapters.get(str(get_hermes_home().resolve()))
    if adapter is None:
        raise RuntimeError(
            "linear_agent platform is not currently connected. "
            "Make sure the Linear Agent plugin is enabled and the gateway is running."
        )
    return adapter
