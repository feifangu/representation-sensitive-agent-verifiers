from pathlib import Path

import pytest

from rsav.dataset import load_task_catalog


def test_load_task_catalog(tmp_path: Path):
    task = tmp_path / "task-a"
    task.mkdir()
    (task / "task.yaml").write_text("instruction: |\n  Do the exact task.\n")
    assert load_task_catalog(tmp_path) == {"task-a": "Do the exact task."}
