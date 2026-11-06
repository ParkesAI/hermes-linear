"""Regenerate the declared tool list from explicit schema definitions."""

import ast
from pathlib import Path

import yaml

root = Path(__file__).resolve().parents[1]
tree = ast.parse((root / "hermes_linear/tools.py").read_text())
names = sorted(
    node.args[0].value
    for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == "_schema"
    and node.args
    and isinstance(node.args[0], ast.Constant)
    and isinstance(node.args[0].value, str)
    and node.args[0].value.startswith("linear_agent_")
)
assert len(names) == len(set(names)) == 58
path = root / "plugin.yaml"
manifest = yaml.safe_load(path.read_text())
manifest["provides_tools"] = names
manifest["author"] = "ParkesAI contributors (derived from Ritchie / Nous Research)"
manifest["license"] = "MIT"
manifest["homepage"] = "https://github.com/ParkesAI/hermes-linear"
path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True))
print("Regenerated manifest declarations for", len(names), "tools")
