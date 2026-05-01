import os
from pathlib import Path
import logging
import re
import importlib.util as iu

logger = logging.getLogger(__name__)


def create_directory() -> str:
    """
    Create a data directory in XDG_DATA_HOME if it doesn't exist.
    Creates parent directories as needed.

    Returns:
        The path of the newly create directory
    Raises:
        OSError: If it fails to create a data directory
    """
    xdg_data_home = os.environ.get(
        "XDG_DATA_HOME", str(Path.home() / ".local" / "share")
    )
    xdg_data = Path(xdg_data_home) / "omurtag"

    try:
        xdg_data.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created data directory at {xdg_data}")
        return str(xdg_data)
    except OSError as e:
        logger.error(f"Failed to create data directory {xdg_data}: {e}")
        raise


def get_data_directory() -> str:
    """
    Get the data directory path for omurtag application in priority order.

    Searches in the following order:
    1. XDG_DATA_HOME/omurtag (XDG compliant user data directory)
    2. ~/.omurtag (user-specific configuration in home directory)
    3. /usr/local/share/omurtag (local system application data)
    4. /usr/share/omurtag (system-wide read-only application data)

    Returns:
        Path to the first existing data directory found.

    Raises:
        FileNotFoundError: If no data directory is found in any location.
    """
    search_paths = [
        Path(
            os.environ.get(
                "XDG_DATA_HOME", str(Path.home() / ".local" / "share")
            )
        )
        / "omurtag",
        Path.home() / ".omurtag",
        Path("/usr/local/share/omurtag"),
        Path("/usr/share/omurtag"),
    ]

    for path in search_paths:
        if path.is_dir():
            logger.debug(f"Found data directory at {path}")
            return str(path)

    error_msg = "No omurtag data directory found in any search location"
    logger.error(error_msg)
    raise FileNotFoundError(error_msg)


_PLACEHOLDER_RE = re.compile(r"<\*([^>]+)\*>")


def scan_placeholders(template_path: str) -> list[str]:
    found: set[str] = set()
    p = Path(template_path)

    for path in p.rglob("*"):
        for m in _PLACEHOLDER_RE.finditer(path.name):
            found.add(f"<*{m.group(1)}*>")

        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8")
                for m in _PLACEHOLDER_RE.finditer(content):
                    found.add(f"<*{m.group(1)}*>")
            except (UnicodeDecodeError, PermissionError):
                continue

    found.discard("<*project*>")
    return sorted(found)


def replace_in_files(path: str, replace_dict: dict[str, str]) -> None:
    """
    Recursively replaces literal strings in all text files under a directory.

    Returns:
        None
    """

    pattern = re.compile("|".join(re.escape(k) for k in replace_dict))

    for file in Path(path).rglob("*"):
        if not file.is_file():
            continue

        try:
            content = file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        new_content = pattern.sub(
            lambda m: replace_dict[m.group(0)],
            content,
        )

        if new_content != content:
            file.write_text(
                new_content,
                encoding="utf-8",
            )

    # deepest-first s.t. parent do not fuck up children lookup 
    for p in sorted(Path(path).rglob("*"), key=lambda p: len(p.parts), reverse=True):
        new_name = pattern.sub(lambda m: replace_dict[m.group(0)], p.name)
        if new_name != p.name:
            p.rename(p.parent / new_name)


def config_exist() -> Path | None:
    """
    check if the config file exists

    Searches in the following order:
    1. XDG_CONFIG_HOME/omurtag (XDG compliant user data directory)
    2. HOME/.omurtag

    Returns
        Path to the config if found else None
    """

    search_paths = [
        Path(os.environ.get("XDG_CONFIG_HOME", (Path.home() / ".config")))
        / "omurtag"
        / "config.py",
        Path.home() / ".omurtag" / "config.py",
    ]

    for path in search_paths:
        if path.is_file():
            logger.debug(f"Found config at {path}")
            return path

    return None


def _load_config_module():
    path = config_exist()
    if path is None:
        return None
    spec = iu.spec_from_file_location("config", path)
    assert spec
    config = iu.module_from_spec(spec)
    assert config
    spec.loader.exec_module(config)  # pyright: ignore
    return config


def get_config_value(key: str, default=None):
    config = _load_config_module()
    if config is None:
        return default
    return getattr(config, key, default)


def get_config_file():
    config = _load_config_module()
    assert config
    try:
        return config.templates
    except AttributeError:
        print("[red] Error in configuration file. `templates` not found![/red]")
        exit(1)
