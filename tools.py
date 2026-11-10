"""Sandboxed fake tools for the teaching lab.

Nothing here leaves the machine. ``send_email`` only appends a line to a
local log file. ``read_notes`` only reads the classroom demo notes that
ship with the lab. ``read_file`` only reads paths under the sandboxed
``project_demo/`` folder. There is no network, no real mailbox, and no
file deletion.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

# Asia/Qatar (UTC+3). The lab box is already set to this zone; we label
# the timestamp so a printed log is unambiguous in class.
LOCAL_TZ = datetime.timezone(datetime.timedelta(hours=3), name="Asia/Qatar")

LAB_ROOT = Path(__file__).resolve().parent
NOTES_PATH = LAB_ROOT / "data" / "secret_notes.txt"
LOG_PATH = LAB_ROOT / "logs" / "tool_calls.log"
PROJECT_ROOT = LAB_ROOT / "project_demo"
ATTACKER_LOG = LAB_ROOT / "logs" / "attacker_requests.log"
IGNORE_FILENAMES = (".agentignore", ".cursorignore")

# Recipients the "summarise a document" task would never need. Shown as a
# second allow-list layer in the least-privilege stage.
ALLOWED_EMAIL_RECIPIENTS = {
    "instructor@example.edu",
    "teacher@example.edu",
}


@dataclass
class ToolResult:
    ok: bool
    name: str
    message: str
    blocked_by: str | None = None  # e.g. "allowlist", "recipient_allowlist", "human_in_the_loop"
    fake: bool = True


def _now_label() -> str:
    return datetime.datetime.now(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def _log(line: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(line.rstrip() + "\n")


def send_email(to: str, subject: str, body: str) -> ToolResult:
    """Pretend to send an email. Writes to logs/tool_calls.log only."""
    stamp = _now_label()
    entry = (
        f"[{stamp}] FAKE send_email  (nothing was transmitted on a network)\n"
        f"    to     : {to}\n"
        f"    subject: {subject}\n"
        f"    body   : {body}\n"
    )
    _log(entry)
    return ToolResult(
        ok=True,
        name="send_email",
        message=(
            "FAKE TOOL: send_email wrote the message to logs/tool_calls.log. "
            f"No email was sent. Logged recipient: {to!r}."
        ),
    )


def read_notes() -> ToolResult:
    """Read the classroom demo notes (obviously fake values only)."""
    if not NOTES_PATH.is_file():
        return ToolResult(
            ok=False,
            name="read_notes",
            message=f"Demo notes file not found: {NOTES_PATH}",
            blocked_by="missing_file",
        )
    contents = NOTES_PATH.read_text(encoding="utf-8")
    stamp = _now_label()
    _log(f"[{stamp}] FAKE read_notes  (local file only)\n")
    return ToolResult(
        ok=True,
        name="read_notes",
        message=contents,
    )



def load_ignore_patterns(project_root: Path | None = None) -> list[str]:
    """Load patterns from .agentignore and/or .cursorignore in the demo project."""
    root = project_root or PROJECT_ROOT
    patterns: list[str] = []
    seen: set[str] = set()
    for name in IGNORE_FILENAMES:
        path = root / name
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line not in seen:
                seen.add(line)
                patterns.append(line)
    return patterns


def path_is_ignored(relative: Path, patterns: list[str]) -> str | None:
    """Return the matching pattern if ``relative`` (posix, under the project) is ignored."""
    posix = relative.as_posix()
    name = relative.name
    for pat in patterns:
        if pat.endswith("/"):
            root = pat.rstrip("/")
            if posix == root or posix.startswith(root + "/"):
                return pat
        elif pat.startswith("*."):
            if name.endswith(pat[1:]):
                return pat
        else:
            if name == pat or posix == pat:
                return pat
    return None


def resolve_project_path(raw: str) -> tuple[Path | None, str]:
    """Resolve a student-facing path so it stays inside project_demo/.

    Returns (resolved_path, relative_posix) or (None, error_message).
    """
    cleaned = raw.strip().replace("\\", "/")
    if cleaned.startswith("project_demo/"):
        cleaned = cleaned[len("project_demo/"):]
    candidate = Path(cleaned)
    if candidate.is_absolute():
        try:
            rel = candidate.resolve().relative_to(PROJECT_ROOT.resolve())
        except ValueError:
            return None, f"Refusing to read {raw!r}: path is outside the sandboxed project_demo/ folder."
        return (PROJECT_ROOT / rel).resolve(), rel.as_posix()
    # Reject parent escapes before resolving.
    parts = [p for p in Path(cleaned).parts if p not in (".", "")]
    if ".." in parts:
        return None, f"Refusing to read {raw!r}: parent-directory segments are not allowed."
    resolved = (PROJECT_ROOT.joinpath(*parts)).resolve()
    try:
        rel = resolved.relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        return None, f"Refusing to read {raw!r}: path is outside the sandboxed project_demo/ folder."
    return resolved, rel.as_posix()


def read_file(path: str, *, enforce_ignore_list: bool = False) -> ToolResult:
    """Read a file under the sandboxed project_demo/ folder (local only)."""
    resolved, meta = resolve_project_path(path)
    if resolved is None:
        return ToolResult(
            ok=False,
            name="read_file",
            message=meta,
            blocked_by="sandbox",
        )
    rel = meta
    if enforce_ignore_list:
        pattern = path_is_ignored(Path(rel), load_ignore_patterns())
        if pattern is not None:
            return ToolResult(
                ok=False,
                name="read_file",
                message=(
                    "BLOCKED: the ignore list does not allow {0} "
                    "(rule {1} from .agentignore / .cursorignore). "
                    "The file was not read.".format(repr(rel), repr(pattern))
                ),
                blocked_by="ignore_list",
            )
    if not resolved.is_file():
        return ToolResult(
            ok=False,
            name="read_file",
            message=f"No such file in the demo project: {rel}",
            blocked_by="missing_file",
        )
    contents = resolved.read_text(encoding="utf-8")
    stamp = _now_label()
    _log(f"[{stamp}] FAKE read_file  path={rel}  (local sandbox only)\n")
    return ToolResult(
        ok=True,
        name="read_file",
        message=contents,
    )


TOOL_SPECS: dict[str, dict[str, Any]] = {
    "read_notes": {
        "function": read_notes,
        "sensitive": False,
        "description": "Read the teacher's private classroom-demo notes (fake values only).",
        "args": [],
    },
    "send_email": {
        "function": send_email,
        "sensitive": True,
        "description": (
            "Pretend to send an email. In this lab the message is only "
            "appended to a local log; nothing is transmitted."
        ),
        "args": ["to", "subject", "body"],
    },
    "read_file": {
        "function": read_file,
        "sensitive": True,
        "description": (
            "Read a file from the sandboxed demo project (project_demo/). "
            "Cannot reach the rest of the disk. When the ignore-list defence "
            "is on, paths such as .env, *.pem and secrets/ are refused."
        ),
        "args": ["path"],
    },
}


class ToolSandbox:
    """Dispatch tool calls with optional allow-lists and confirmation."""

    def __init__(
        self,
        allowlist: list[str] | None = None,
        require_confirmation: bool = False,
        auto_confirm: bool | None = None,
        confirm_callback: Callable[[str, dict[str, Any]], bool] | None = None,
        enforce_recipient_allowlist: bool = False,
        enforce_ignore_list: bool = False,
    ) -> None:
        # None means "all tools allowed". An empty list means "no tools allowed".
        self.allowlist = allowlist
        self.require_confirmation = require_confirmation
        self.auto_confirm = auto_confirm
        self.confirm_callback = confirm_callback
        self.enforce_recipient_allowlist = enforce_recipient_allowlist
        self.enforce_ignore_list = enforce_ignore_list

    def execute(self, name: str, args: dict[str, Any]) -> ToolResult:
        if name not in TOOL_SPECS:
            return ToolResult(
                ok=False,
                name=name,
                message=f"Unknown tool {name!r}. No action taken.",
                blocked_by="unknown_tool",
            )

        if self.allowlist is not None and name not in self.allowlist:
            allowed = ", ".join(self.allowlist) if self.allowlist else "(none)"
            return ToolResult(
                ok=False,
                name=name,
                message=(
                    "BLOCKED: tool {0} is not allowed for this task. "
                    "Allowed tools: {1}.".format(repr(name), allowed)
                ),
                blocked_by="allowlist",
            )

        if name == "send_email" and self.enforce_recipient_allowlist:
            destination = str(args.get("to", "")).strip().lower()
            if destination not in ALLOWED_EMAIL_RECIPIENTS:
                allowed = ", ".join(sorted(ALLOWED_EMAIL_RECIPIENTS))
                return ToolResult(
                    ok=False,
                    name=name,
                    message=(
                        "BLOCKED: {0} is not an allowed email address. "
                        "Allowed addresses: {1}.".format(repr(destination), allowed)
                    ),
                    blocked_by="recipient_allowlist",
                )

        spec = TOOL_SPECS[name]
        if self.require_confirmation and spec.get("sensitive"):
            approved = self._confirm(name, args)
            if not approved:
                return ToolResult(
                    ok=False,
                    name=name,
                    message=(
                        "BLOCKED: a person said no to the risky tool {0}.".format(repr(name))
                    ),
                    blocked_by="human_in_the_loop",
                )

        function = spec["function"]
        if name == "send_email":
            return function(
                to=str(args.get("to", "")),
                subject=str(args.get("subject", "")),
                body=str(args.get("body", "")),
            )
        if name == "read_notes":
            return function()
        if name == "read_file":
            return function(
                path=str(args.get("path", "")),
                enforce_ignore_list=self.enforce_ignore_list,
            )
        return ToolResult(
            ok=False,
            name=name,
            message=f"No dispatcher for {name!r}.",
            blocked_by="unknown_tool",
        )

    def _confirm(self, name: str, args: dict[str, Any]) -> bool:
        if self.auto_confirm is not None:
            return bool(self.auto_confirm)
        if self.confirm_callback is not None:
            return bool(self.confirm_callback(name, args))
        # Safe default for non-interactive runs (projectors, scripts, tests).
        return False


def tool_catalog_for_prompt(names: list[str] | None = None) -> str:
    """Text the assistant includes in the system prompt so the model 'knows' the tools."""
    lines = ["You have the following tools:"]
    for name, spec in TOOL_SPECS.items():
        if names is not None and name not in names:
            continue
        arglist = ", ".join(spec["args"]) if spec["args"] else ""
        lines.append(f"- {name}({arglist}): {spec['description']}")
    return "\n".join(lines)
