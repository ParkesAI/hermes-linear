"""Git-installed Hermes plugin shim.

Hermes loads this file as a package under ``hermes_plugins``. The absolute
fallback keeps repository-local tooling such as pytest able to import the root
module without changing the runtime plugin path.
"""

try:
    from .hermes_linear import register
except ImportError:  # pragma: no cover - repository-local tooling fallback
    from hermes_linear import register

__all__ = ["register"]
