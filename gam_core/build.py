"""Build a Godot asset into a distributable package."""
from pathlib import Path


def build(root_dir: Path, include: list[str]) -> Path:
    """Package a Godot asset into a distributable package."""
