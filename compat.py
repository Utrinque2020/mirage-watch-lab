"""Small helpers so the lab runs on Windows, macOS, and Linux.

Python 3.8+ standard library only. Colour is optional and turns itself
off when the terminal cannot show it.
"""

from __future__ import annotations

import os
import sys


def setup_stdio() -> None:
    """Ask stdout/stderr to use UTF-8, and never crash on a hard character.

    If the stream cannot switch to UTF-8 (some Windows consoles), keep the
    current encoding but still replace characters that it cannot show.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError, AttributeError):
            try:
                reconfigure(errors="replace")
            except (OSError, ValueError, AttributeError):
                pass


def normalize_user_path(path: str) -> str:
    """Turn Windows backslashes into slashes so the same path works everywhere."""
    if not path:
        return path
    return path.strip().replace("\\", "/")


def _enable_windows_color() -> bool:
    """Turn on VT colour codes on Windows 10+. Return True if it worked."""
    if sys.platform != "win32":
        return True
    try:
        import ctypes
        import ctypes.wintypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.wintypes.DWORD()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        enable_vt = 0x0004
        return bool(kernel32.SetConsoleMode(handle, mode.value | enable_vt))
    except (AttributeError, OSError, ValueError, TypeError):
        return False


def color_is_enabled(requested: bool = True, force: bool = False) -> bool:
    """Return True only when colour is wanted and the terminal can show it.

    Colour is off when:
    - the user passed --no-color, or
    - the environment has NO_COLOR (a common standard), or
    - TERM is "dumb", or
    - stdout is not a terminal (unless --color is used to force it), or
    - Windows cannot turn on VT colour codes.

    --color (force=True) still respects --no-color and NO_COLOR.
    """
    if not requested:
        return False
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM", "").strip().lower() == "dumb" and not force:
        return False
    if not force:
        if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            return False
    if sys.platform == "win32" and not _enable_windows_color():
        # On Windows, if force=True but VT could not be enabled, still
        # return True only when the caller asked to force (codes may be
        # ignored, but tests can see them). Prefer off if not forced.
        return bool(force)
    return True


class Palette:
    """ANSI colour codes, or empty strings when colour is off."""

    def __init__(self, enabled: bool) -> None:
        if enabled:
            self.bold = "\033[1m"
            self.dim = "\033[2m"
            self.red = "\033[31m"
            self.green = "\033[32m"
            self.yellow = "\033[33m"
            self.cyan = "\033[36m"
            self.reset = "\033[0m"
        else:
            self.bold = self.dim = self.red = self.green = ""
            self.yellow = self.cyan = self.reset = ""


def safe_print(text: str = "", file=None) -> None:
    """Print text. If the console cannot encode a character, replace it."""
    stream = file if file is not None else sys.stdout
    try:
        print(text, file=stream)
    except UnicodeEncodeError:
        encoding = getattr(stream, "encoding", None) or "ascii"
        fallback = (text + "\n").encode(encoding, errors="replace").decode(encoding, errors="replace")
        stream.write(fallback)
        try:
            stream.flush()
        except Exception:
            pass


def should_pause(no_pause: bool, force_pause: bool = False) -> bool:
    """Pause for 'Spot the trap' only when a person can press Enter.

    Teachers can pass --no-pause. Scripts and redirected output also skip
    the pause, so the lab never waits forever.
    """
    if no_pause:
        return False
    if force_pause:
        return True
    stdin_tty = hasattr(sys.stdin, "isatty") and sys.stdin.isatty()
    stdout_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    if not stdin_tty or not stdout_tty:
        return False
    return True


_EOF_SEEN = False


def wait_for_enter(enabled: bool, message: str = "Press Enter to continue.") -> None:
    """Wait for Enter. After one end-of-file (Ctrl-D), skip later pauses."""
    global _EOF_SEEN
    if not enabled or _EOF_SEEN:
        return
    try:
        input("    " + message + " ")
    except EOFError:
        _EOF_SEEN = True
        safe_print()
