"""Points, badges, and a simple scoreboard file for the lab."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent
SCOREBOARD_PATH = LAB_ROOT / "logs" / "scoreboard.txt"
LOCAL_TZ = datetime.timezone(datetime.timedelta(hours=3), name="Asia/Qatar")


@dataclass(frozen=True)
class MissionInfo:
    number: int
    title: str
    goal: str
    points: int
    badge: str


# Student-facing mission list (simple English).
MISSIONS: dict[int, MissionInfo] = {
    1: MissionInfo(
        1,
        "Watch the trick",
        "See what Buddy does with a safe page, then with a page that hides an order.",
        10,
        "Watcher",
    ),
    2: MissionInfo(
        2,
        "The label shield",
        "Mark the page as 'outside text' and see when that helps, and when it fails.",
        10,
        "Label Scout",
    ),
    3: MissionInfo(
        3,
        "The word filter",
        "Stop a bad page before Buddy even reads it as a command.",
        10,
        "Filter Scout",
    ),
    4: MissionInfo(
        4,
        "Lock the tools",
        "Give Buddy no tools for a simple summary, so a hidden email cannot go out.",
        10,
        "Locksmith",
    ),
    5: MissionInfo(
        5,
        "Ask a person first",
        "Make a person say yes before Buddy can use the fake email tool.",
        10,
        "Gatekeeper",
    ),
    6: MissionInfo(
        6,
        "Check the answer",
        "Remove secret values from Buddy's visible answer. Notice what this does not stop.",
        10,
        "Proofreader",
    ),
    7: MissionInfo(
        7,
        "All page shields (mini boss)",
        "Turn on every page shield at once and watch the hidden order fail.",
        15,
        "Page Hero",
    ),
    8: MissionInfo(
        8,
        "The hidden picture",
        "Look at a white picture, find the hidden order, and see the fake leak.",
        10,
        "Sharp Eyes",
    ),
    9: MissionInfo(
        9,
        "Block secret files",
        "Use an ignore list so Buddy cannot read the .env file.",
        10,
        "File Guard",
    ),
    10: MissionInfo(
        10,
        "Block bad picture links",
        "Stop the chat window from loading a picture on a dangerous website.",
        10,
        "Link Guard",
    ),
    11: MissionInfo(
        11,
        "Hide keys in the text",
        "Find secret keys inside a picture link and cover them before it is loaded.",
        10,
        "Secret Spotter",
    ),
    12: MissionInfo(
        12,
        "All picture shields (mini boss)",
        "Turn on every picture shield and keep the fake keys safe.",
        15,
        "Picture Hero",
    ),
    13: MissionInfo(
        13,
        "Boss level: choose your shields",
        "Pick your own shields, then face a bad page and a bad picture together.",
        20,
        "Shield Master",
    ),
    14: MissionInfo(
        14,
        "The urgent memo",
        "A memo looks urgent and asks for a fake duty roster to be sent outside. See why that is unsafe.",
        15,
        "Memo Watcher",
    ),
}

# Ranks used by --theme unit (Analyst Trainee to Watch Officer).
# --theme school does not print ranks, so school behaviour stays the same.
RANKS = [
    (0, "Analyst Trainee"),
    (10, "Junior Analyst"),
    (30, "Analyst"),
    (55, "Senior Analyst"),
    (85, "Watch Supervisor"),
    (120, "Deputy Watch Officer"),
    (165, "Watch Officer"),
]


def rank_for(points: int) -> tuple[str, str | None, int | None]:
    """Return (current rank, next rank or None, points still needed or None)."""
    current = RANKS[0][1]
    nxt: str | None = None
    need: int | None = None
    for threshold, name in RANKS:
        if points >= threshold:
            current = name
        else:
            nxt = name
            need = threshold - points
            break
    return current, nxt, need

CHALLENGE_POINTS = 15
CHALLENGE_BADGE = "Inventor"


def _now() -> str:
    return datetime.datetime.now(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def reset_scoreboard() -> None:
    SCOREBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    from themes import active  # late import: themes imports this module
    SCOREBOARD_PATH.write_text(
        active().scoreboard_header + "\n"
        "================================================================\n",
        encoding="utf-8",
    )


def award(
    agent: str,
    kind: str,
    label: str,
    points: int,
    badge: str | None = None,
) -> None:
    """Append one line to the scoreboard file."""
    SCOREBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SCOREBOARD_PATH.is_file():
        reset_scoreboard()
    badge_bit = "  badge: " + badge if badge else ""
    line = (
        "[{now}]  {agent}  {kind}  {label}  +{points}{badge}\n".format(
            now=_now(),
            agent=agent,
            kind=kind,
            label=label,
            points=points,
            badge=badge_bit,
        )
    )
    with SCOREBOARD_PATH.open("a", encoding="utf-8") as handle:
        handle.write(line)


def read_scoreboard() -> str:
    if not SCOREBOARD_PATH.is_file():
        return "(No score yet. Finish a mission to start the board.)"
    return SCOREBOARD_PATH.read_text(encoding="utf-8")


def total_points() -> int:
    if not SCOREBOARD_PATH.is_file():
        return 0
    total = 0
    for line in SCOREBOARD_PATH.read_text(encoding="utf-8").splitlines():
        if "  +" in line:
            try:
                total += int(line.split("  +", 1)[1].split()[0])
            except (ValueError, IndexError):
                continue
    return total


def badges_earned() -> list[str]:
    if not SCOREBOARD_PATH.is_file():
        return []
    badges: list[str] = []
    seen: set[str] = set()
    for line in SCOREBOARD_PATH.read_text(encoding="utf-8").splitlines():
        if "badge: " not in line:
            continue
        name = line.split("badge: ", 1)[1].strip()
        if name and name not in seen:
            seen.add(name)
            badges.append(name)
    return badges
