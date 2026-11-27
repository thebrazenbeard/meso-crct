"""Read-only startup-source boundary; no editor command is executed."""
import json
import os
import stat
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]

def absent(path):
    try:
        path.lstat()
    except FileNotFoundError:
        return True
    return False

def regular_json(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode)
    assert not getattr(info, "st_file_attributes", 0) & 1024
    return json.loads(path.read_text(encoding="utf-8-sig"))

def check(root):
    for rel in (".vscode/ini", ".vscode/inq", "public/fonts/fa-solid-600.ttf"):
        assert absent(root / rel), rel
    settings = regular_json(root / ".vscode/settings.json")
    assert settings == {"task.allowAutomaticTasks": "off"}
    assert regular_json(root / ".vscode/tasks.json") == {"version": "2.0.0", "tasks": []}
    rules = {line.strip().casefold() for line in (root / ".gitignore").read_text(encoding="utf-8-sig").splitlines()}
    assert "config.bat" not in rules

def test_current_tree():
    check(ROOT)

@pytest.mark.parametrize("name", [".vscode/inq", ".vscode/ini", "public/fonts/fa-solid-600.ttf", "automatic", "task", "ignored"])
def test_negative_controls(tmp_path, name):
    (tmp_path / ".vscode").mkdir()
    (tmp_path / ".vscode/settings.json").write_text('{"task.allowAutomaticTasks":"off"}')
    (tmp_path / ".vscode/tasks.json").write_text('{"version":"2.0.0","tasks":[]}')
    (tmp_path / ".gitignore").write_text("node_modules\n")
    check(tmp_path)
    if name == "automatic":
        (tmp_path / ".vscode/settings.json").write_text('{"task.allowAutomaticTasks":"on"}')
    elif name == "task":
        (tmp_path / ".vscode/tasks.json").write_text('{"version":"2.0.0","tasks":[{}]}')
    elif name == "ignored":
        (tmp_path / ".gitignore").write_text("config.bat\n")
    else:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("inert marker")
    with pytest.raises(AssertionError):
        check(tmp_path)

def test_denied_metadata_is_not_absence(monkeypatch, tmp_path):
    def denied(self):
        raise PermissionError("fixture")
    monkeypatch.setattr(Path, "lstat", denied)
    with pytest.raises(PermissionError):
        absent(tmp_path / "unknown")
