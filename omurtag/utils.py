import os
from pathlib import Path
import logging

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
    xdg_data_home = os.environ.get('XDG_DATA_HOME',
                                  str(Path.home() / ".local" / "share"))
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
        Path(os.environ.get('XDG_DATA_HOME',
                          str(Path.home() / ".local" / "share"))) / "omurtag",
        Path.home() / ".omurtag",
        Path("/usr/local/share/omurtag"),
        Path("/usr/share/omurtag")
    ]

    for path in search_paths:
        if path.is_dir():
            logger.debug(f"Found data directory at {path}")
            return str(path)

    error_msg = "No omurtag data directory found in any search location"
    logger.error(error_msg)
    raise FileNotFoundError(error_msg)
