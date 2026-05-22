# System Utilities

The module `plotcdf.library.systems` provides small OS-detection helpers used by plotting code.

## Why this module exists

Plotting behavior can differ by platform.
For example, plot windows are maximized only on Windows in `plotcdf.discrete.plot`.

## Public functions

### `get_os_name()`

Returns `os.name`.
Typical values:

- `"nt"` on Windows
- `"posix"` on Linux/macOS

### `get_all_platform()`

Returns `platform.uname()` with full platform metadata.

### `get_system()`

Returns the OS name from `platform.system()`.
Typical values include `"Linux"`, `"Windows"`, and `"Darwin"`.

### `is_windows()`

Returns `True` when `os.name == "nt"`, otherwise `False`.

## Usage example

```python
from plotcdf.library import systems

if systems.is_windows():
    print("Windows-specific plotting behavior enabled")
```
