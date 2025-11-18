# tests/90_integration/test_deterministic_build_content.py
"""Integration tests for deterministic build output content.

These tests verify that builds with disabled timestamps produce
identical, reproducible output suitable for verification purposes.
They check the actual content of generated build files.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.utils.constants import PROJ_ROOT


def test_disable_build_timestamp_produces_identical_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two builds with disable_build_timestamp=True should produce identical output."""
    # --- setup ---
    # Create a minimal test package structure
    pkg_dir = tmp_path / "src" / "testpkg"
    pkg_dir.mkdir(parents=True)
    (pkg_dir / "__init__.py").write_text('"""Test package."""\n')
    (pkg_dir / "module.py").write_text('"""Test module."""\n\nvalue = 42\n')

    # Create serger config with disable_build_timestamp
    config = tmp_path / ".serger.jsonc"
    config_data = {
        "builds": [
            {
                "package": "testpkg",
                "include": ["src/testpkg/**/*.py"],
                "out": "dist/testpkg.py",
                "disable_build_timestamp": True,
            }
        ]
    }
    config.write_text(json.dumps(config_data, indent=2))

    serger_script = PROJ_ROOT / "dev" / "serger.py"
    monkeypatch.chdir(tmp_path)

    # --- execute: first build ---
    result1 = subprocess.run(  # noqa: S603
        [sys.executable, str(serger_script), "--config", str(config)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result1.returncode == 0, (
        f"First build failed: {result1.stdout}\n{result1.stderr}"
    )
    output_file1 = tmp_path / "dist" / "testpkg.py"
    assert output_file1.exists(), "First build output file not created"
    content1 = output_file1.read_text()

    # Delete the output file to force a fresh build
    output_file1.unlink()

    # --- execute: second build ---
    result2 = subprocess.run(  # noqa: S603
        [sys.executable, str(serger_script), "--config", str(config)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result2.returncode == 0, (
        f"Second build failed: {result2.stdout}\n{result2.stderr}"
    )
    output_file2 = tmp_path / "dist" / "testpkg.py"
    assert output_file2.exists(), "Second build output file not created"
    content2 = output_file2.read_text()

    # --- verify: outputs are identical ---
    assert content1 == content2, (
        "Two builds with disable_build_timestamp=True should produce identical output"
    )


def test_disable_build_timestamp_cli_produces_identical_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two builds using CLI --disable-build-timestamp produce identical output."""
    # --- setup ---
    # Create a minimal test package structure
    pkg_dir = tmp_path / "src" / "testpkg"
    pkg_dir.mkdir(parents=True)
    (pkg_dir / "__init__.py").write_text('"""Test package."""\n')
    (pkg_dir / "module.py").write_text('"""Test module."""\n\nvalue = 42\n')

    # Create config WITHOUT disable_build_timestamp (will use CLI flag instead)
    config = tmp_path / ".serger.jsonc"
    config_data = {
        "builds": [
            {
                "package": "testpkg",
                "include": ["src/testpkg/**/*.py"],
                "out": "dist/testpkg.py",
                # No disable_build_timestamp in config - will use CLI flag
            }
        ]
    }
    config.write_text(json.dumps(config_data, indent=2))

    serger_script = PROJ_ROOT / "dev" / "serger.py"
    monkeypatch.chdir(tmp_path)

    # --- execute: first build with CLI flag ---
    result1 = subprocess.run(  # noqa: S603
        [
            sys.executable,
            str(serger_script),
            "--config",
            str(config),
            "--disable-build-timestamp",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result1.returncode == 0, (
        f"First build failed: {result1.stdout}\n{result1.stderr}"
    )
    output_file1 = tmp_path / "dist" / "testpkg.py"
    assert output_file1.exists(), "First build output file not created"
    content1 = output_file1.read_text()

    # Delete the output file to force a fresh build
    output_file1.unlink()

    # --- execute: second build with CLI flag ---
    result2 = subprocess.run(  # noqa: S603
        [
            sys.executable,
            str(serger_script),
            "--config",
            str(config),
            "--disable-build-timestamp",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result2.returncode == 0, (
        f"Second build failed: {result2.stdout}\n{result2.stderr}"
    )
    output_file2 = tmp_path / "dist" / "testpkg.py"
    assert output_file2.exists(), "Second build output file not created"
    content2 = output_file2.read_text()

    # --- verify: outputs are identical ---
    assert content1 == content2, (
        "Two builds with --disable-build-timestamp CLI flag should produce "
        "identical output"
    )
