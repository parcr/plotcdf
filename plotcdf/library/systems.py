"""System utility helpers used by plotting routines.

This module centralizes lightweight platform checks so plotting code can adapt
behavior for specific operating systems when needed.
"""

import os
import platform
from typing import Any


def get_os_name() -> str:
    """Return the normalized OS-dependent module name (for example ``'nt'``)."""
    return os.name


def get_all_platform() -> Any:
    """Return full platform information from ``platform.uname()``."""
    return platform.uname()


def get_system() -> str:
    """Return the system/OS name (for example ``'Linux'`` or ``'Windows'``)."""
    return platform.system()


def is_windows() -> bool:
    """Return ``True`` when running on Windows, ``False`` otherwise."""
    if get_os_name() == 'nt':
        return True
    return False

#  print(get_system())
