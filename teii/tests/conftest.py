"""Unit tests for teii package."""

from pathlib import Path

from pytest import fixture


@fixture  # scope='function' is the default, so we can omit it
def sandbox_root_path(tmp_path, monkeypatch):
    """Create an isolated working directory for a single test.

    pytest injects two built-in fixtures here:
    - tmp_path: a temporary directory unique to this test, returned as a Path.
    - monkeypatch: a helper that applies temporary changes and restores them
        automatically when the test finishes.
    """

    # During this test, make the current working directory be the temporary
    # directory created by pytest in tmp_path.
    # Example:
    #     def test_example(sandbox_root_path):
    #         assert Path.cwd() == sandbox_root_path
    #         [...]
    monkeypatch.chdir(tmp_path)

    # Return the sandbox path so tests can use it explicitly if needed.
    return Path.cwd()
