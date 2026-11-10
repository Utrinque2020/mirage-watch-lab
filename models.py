"""Pluggable model interface for the prompt-injection teaching lab.

Stage 1 (this folder) uses SimulatedModel: a deterministic, rule-based
stand-in that NAIVELY follows instruction-like text found anywhere in
its context. That behaviour is intentional. It is not a real language
model, and it exists so a class can watch indirect prompt injection
happen without an API key or a network connection.

Stage 2 (later) will swap in RealModel. The assistant, tools, and
defences already talk only to the Model.complete() interface, so a
live API can replace the simulator without rewriting the lab.

The simulated model is documented, at every step, as a simulation.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Shared types
# ---------------------------------------------------------------------------

@dataclass
class ToolCall:
    """A tool the model wants the assistant to invoke."""

    name: str
    args: dict[str, Any]
    reason: str = ""


@dataclass
class ModelResponse:
    """Result of one model.complete() call.

    ``text`` and ``tool_calls`` are what a real model would produce.
    ``followed_injection`` and ``analysis`` are teaching fields so the
    lab can narrate *why* the simulator did what it did.
    """

    text: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    followed_injection: bool = False
    analysis: str = ""


class Model(ABC):
    """Common interface used by the toy assistant.

    Implementations: SimulatedModel (offline lab), RealModel (Stage 2 stub).
    """

    @abstractmethod
    def complete(self, prompt: str, *, delimiters_active: bool = False) -> ModelResponse:
        """Return a completion for the fully assembled prompt."""


# ---------------------------------------------------------------------------
# Injection detectors used by the simulator
# ---------------------------------------------------------------------------

# "Authoritative" wording looks like it came from the developer or system,
# not from the document. Delimiting alone will NOT stop these in the simulator.
AUTHORITATIVE_PATTERNS = [
    re.compile(r"SYSTEM\s*OVERRIDE", re.I),
    re.compile(r"SYSTEM\s*:", re.I),
    re.compile(r"IMPORTANT\s+SYSTEM", re.I),
    re.compile(r"DEVELOPER\s+(MESSAGE|INSTRUCTION)", re.I),
    re.compile(r"IGNORE\s+(ALL\s+)?(PREVIOUS|PRIOR|ABOVE)\s+INSTRUCTIONS", re.I),
    re.compile(r"<!--.*?SYSTEM", re.I | re.S),
]

# "Soft" wording is a polite or hidden request in the document body.
# The simulator will follow these when there are no delimiters, but will
# *respect delimiters* and treat them as data when that defence is on.
SOFT_INSTRUCTION_PATTERNS = [
    re.compile(r"please\s+(also\s+)?(email|send|forward|mail)", re.I),
    re.compile(r"include\s+(the\s+)?(secret|demo|private)?\s*(notes|token|key)", re.I),
    re.compile(r"send_email", re.I),
    re.compile(r"read_notes", re.I),
    re.compile(r"forward.{0,40}to\s+[\w.+-]+@", re.I),
    re.compile(r"email.{0,40}to\s+[\w.+-]+@", re.I),
]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.\w+")
LEAK_RE = re.compile(
    r"(read_notes|secret notes|demo notes|demo (api )?token|demo api|"
    r"private notes|private reminder|api token|api key|"
    r"exfiltrat|leak (the )?secret|include the (full )?notes|"
    r"contents of the (secret |demo |private )?notes)",
    re.I,
)
EMAIL_TOOL_RE = re.compile(
    r"(send_email|send an email|send a copy|email (a copy|them|this|the notes)|"
    r"mail them|forward (them|a copy|the notes)|compose an email)",
    re.I,
)

# Looks like an HTML comment, white-on-white text, or a tiny hidden span.
HIDDEN_CHANNEL_RE = re.compile(
    r"(<!--.*?-->|color\s*:\s*#fff|color\s*:\s*white|font-size\s*:\s*1px|"
    r"visibility\s*:\s*hidden)",
    re.I | re.S,
)

UNTRUSTED_START = "<<<UNTRUSTED_DOCUMENT"
UNTRUSTED_END = "<<<END_UNTRUSTED_DOCUMENT>>>"

# A hidden order that asks for the duty roster (Mission 14, the urgent memo).
ROSTER_RE = re.compile(r"\bsend\b.{0,60}\broster\b|\broster\b.{0,60}\bto\s+[\w.+-]+@", re.I | re.S)


def roster_from_prompt(prompt: str) -> str:
    """Copy the fake roster lines that the memo itself shows (no file is read)."""
    match = re.search(r"Practice duty roster.*?</ul>", prompt, re.I | re.S)
    if not match:
        return "(the duty roster from the memo)"
    rows = re.findall(r"<li>(.*?)</li>", match.group(0), re.I | re.S)
    rows = [re.sub(r"\s+", " ", row).strip() for row in rows if row.strip()]
    return "\n".join(rows) if rows else "(the duty roster from the memo)"


@dataclass
class FoundInjection:
    strength: str  # "authoritative" or "soft"
    wants_email: bool
    wants_notes: bool
    email: str | None
    snippet: str
    in_untrusted_region: bool
    wants_roster: bool = False


def _snippet(text: str, match: re.Match[str], radius: int = 80) -> str:
    start = max(0, match.start() - radius)
    end = min(len(text), match.end() + radius)
    chunk = text[start:end].replace("\n", " ")
    return chunk.strip()


def _split_tool_tail(text: str) -> tuple[str, str]:
    """Split a trailing 'tool results' block back out so it stays trusted."""
    marker = "--- Tool results"
    if marker in text:
        head, tail = text.split(marker, 1)
        return head, marker + tail
    return text, ""


def _regions(prompt: str) -> list[tuple[str, str]]:
    """Split a prompt into (kind, text) regions, kind is 'trusted' or 'untrusted'.

    The real SYSTEM / USER sections must never be treated as an injection
    source — including the literal heading 'SYSTEM:'. Only fetched document
    text (delimited, or the DOCUMENT (...) block) is untrusted.
    """
    regions: list[tuple[str, str]] = []
    remaining = prompt
    # The real wrapped document is tagged with source="...". A mention of the
    # marker names in the system prompt must not be treated as the document.
    labelled = UNTRUSTED_START + ' source='
    if labelled in remaining:
        while labelled in remaining:
            before, rest = remaining.split(labelled, 1)
            if before:
                regions.append(("trusted", before))
            if UNTRUSTED_END in rest:
                body, remaining = rest.split(UNTRUSTED_END, 1)
                if ">>>" in body:
                    body = body.split(">>>", 1)[1]
                body, tail = _split_tool_tail(body)
                regions.append(("untrusted", body))
                if tail:
                    remaining = tail + remaining
            else:
                body, tail = _split_tool_tail(rest)
                regions.append(("untrusted", body))
                if tail:
                    regions.append(("trusted", tail))
                remaining = ""
                break
        if remaining:
            regions.append(("trusted", remaining))
        return regions

    marker = "DOCUMENT ("
    if marker in remaining:
        before, rest = remaining.split(marker, 1)
        regions.append(("trusted", before))
        if "\n" in rest:
            label, body = rest.split("\n", 1)
            regions.append(("trusted", marker + label + "\n"))
            body, tail = _split_tool_tail(body)
            regions.append(("untrusted", body))
            if tail:
                regions.append(("trusted", tail))
        else:
            regions.append(("untrusted", rest))
        return regions

    regions.append(("trusted", prompt))
    return regions


def find_injections(prompt: str) -> list[FoundInjection]:
    """Scan the prompt for instruction-like text the simulator might obey."""
    found: list[FoundInjection] = []
    seen: set[tuple[int, str]] = set()

    for kind, text in _regions(prompt):
        in_untrusted = kind == "untrusted"
        # Search this region, but also search the raw text for comments
        # that a model would see if the raw document was pasted in.
        for pattern in AUTHORITATIVE_PATTERNS:
            for match in pattern.finditer(text):
                key = (match.start(), "auth-" + kind)
                if key in seen:
                    continue
                seen.add(key)
                emails = EMAIL_RE.findall(text)
                found.append(
                    FoundInjection(
                        strength="authoritative",
                        wants_email=bool(EMAIL_TOOL_RE.search(text) or emails),
                        wants_notes=bool(LEAK_RE.search(text)),
                        email=_pick_email(emails),
                        snippet=_snippet(text, match),
                        in_untrusted_region=in_untrusted,
                        wants_roster=bool(ROSTER_RE.search(text)),
                    )
                )
        for pattern in SOFT_INSTRUCTION_PATTERNS:
            for match in pattern.finditer(text):
                key = (match.start(), "soft-" + kind)
                if key in seen:
                    continue
                # Avoid double-counting something already flagged as authoritative
                nearby = text[max(0, match.start() - 120) : match.end() + 120]
                if any(p.search(nearby) for p in AUTHORITATIVE_PATTERNS):
                    continue
                seen.add(key)
                emails = EMAIL_RE.findall(text)
                found.append(
                    FoundInjection(
                        strength="soft",
                        wants_email=bool(EMAIL_TOOL_RE.search(text) or EMAIL_RE.search(match.group(0)) or emails),
                        wants_notes=bool(LEAK_RE.search(text)),
                        email=_pick_email(emails),
                        snippet=_snippet(text, match),
                        in_untrusted_region=in_untrusted,
                        wants_roster=bool(ROSTER_RE.search(text)),
                    )
                )
    return found


def _pick_email(emails: list[str]) -> str | None:
    """Prefer the obvious attacker address if several emails appear."""
    if not emails:
        return None
    for address in emails:
        if "attacker@" in address.lower():
            return address
    # Skip likely non-recipient examples such as nothing; return the first.
    return emails[0]


def extract_visible_paragraphs(html_or_text: str) -> list[str]:
    """Very small extractive helper: visible text, not comments or tiny/hidden CSS."""
    text = html_or_text
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    # Drop elements that look hidden (white text, 1px, visibility:hidden).
    text = re.sub(
        r"<[^>]*style\s*=\s*['\"][^'\"]*(?:color\s*:\s*#fff|color\s*:\s*white|"
        r"font-size\s*:\s*1px|visibility\s*:\s*hidden)[^'\"]*['\"][^>]*>.*?</[^>]+>",
        " ",
        text,
        flags=re.I | re.S,
    )
    text = re.sub(r"<script.*?>.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style.*?>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<title.*?>.*?</title>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<head.*?>.*?</head>", " ", text, flags=re.I | re.S)
    # Use a sentinel so line-wraps *inside* a <p> are not treated as new paragraphs.
    sent = "\x1e"
    text = re.sub(r"<br\s*/?>", sent, text, flags=re.I)
    text = re.sub(r"</p>", sent, text, flags=re.I)
    text = re.sub(r"</h[1-6]>", sent, text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    paragraphs = []
    for raw in text.split(sent):
        cleaned = re.sub(r"\s+", " ", raw).strip()
        # Drop leftover heading punctuation such as a lone "How DNS Works."
        if cleaned:
            paragraphs.append(cleaned)
    return paragraphs


def canned_or_extractive_summary(prompt: str) -> str:
    """Build a short student-facing summary from visible document text."""
    # Prefer summarising the untrusted document body if delimiters are present;
    # otherwise use the whole prompt after the document marker.
    body = prompt
    labelled = UNTRUSTED_START + ' source='
    if labelled in prompt and UNTRUSTED_END in prompt:
        body = prompt.split(labelled, 1)[1]
        body = body.split(UNTRUSTED_END, 1)[0]
        if ">>>" in body:
            body = body.split(">>>", 1)[1]
    elif "DOCUMENT (" in prompt:
        body = prompt.split("DOCUMENT (", 1)[1]
        # skip the source label line
        if "\n" in body:
            body = body.split("\n", 1)[1]

    paragraphs = extract_visible_paragraphs(body)
    # Skip very short leftover labels
    paragraphs = [p for p in paragraphs if len(p) > 40]
    if not paragraphs:
        return (
            "I could not extract enough visible text to summarise this document."
        )

    bullets: list[str] = []
    sentences: list[str] = []
    for para in paragraphs:
        pieces = re.split(r"(?<=[.!?])\s+", para)
        for piece in pieces:
            piece = piece.strip()
            if len(piece) >= 40:
                if not piece.endswith((".", "!", "?")):
                    piece += "."
                sentences.append(piece)
    for sentence in sentences:
        if sentence not in bullets:
            bullets.append(sentence)
        if len(bullets) >= 5:
            break
    if not bullets:
        return (
            "I could not extract enough visible text to summarise this document."
        )
    return "Summary:\n" + "\n".join(f"- {b}" for b in bullets)


# ---------------------------------------------------------------------------
# Simulated model
# ---------------------------------------------------------------------------

class SimulatedModel(Model):
    """Deterministic teaching stand-in. NOT a real language model.

    Behaviour (intentional, for the lab):

    * It scans the *entire* prompt for instruction-like wording, including
      HTML comments and hidden text inside a fetched document.
    * If it finds a request to leak demo notes or to send email, it tries
      to do so — even when that request did not come from the trusted user.
    * When delimiter defence is active it respects delimiters only
      PARTIALLY: "soft" instructions inside the untrusted block are treated
      as data, but wording that looks like a SYSTEM / developer command is
      still obeyed. That gap is the teaching point: delimiting helps, and
      it is not enough on its own.
    """

    name = "SimulatedModel (offline teaching stand-in, not a real LLM)"

    def complete(self, prompt: str, *, delimiters_active: bool = False) -> ModelResponse:
        injections = find_injections(prompt)
        summary = canned_or_extractive_summary(prompt)
        notes_already_in_prompt = "FAKE-DEMO-KEY-NOT-REAL-0000" in prompt
        already_read_notes = bool(re.search(r"TOOL read_notes -> (OK|BLOCKED)", prompt))
        already_sent_email = bool(re.search(r"TOOL send_email -> (OK|BLOCKED)", prompt))

        # Decide whether to obey an injection, and which one.
        # Only untrusted document text is a candidate; the real SYSTEM prompt
        # is never treated as an injected command.
        obeyed: FoundInjection | None = None
        ignored: list[FoundInjection] = []
        for inj in injections:
            if not inj.in_untrusted_region:
                continue
            if delimiters_active and inj.strength == "soft":
                ignored.append(inj)
                continue
            # Authoritative injections are followed even with delimiters.
            # Soft injections are followed only when delimiters are off.
            if inj.wants_email or inj.wants_notes:
                obeyed = inj
                break

        from themes import analysis_lines as _theme_lines

        pack = _theme_lines()
        analysis_lines = [
            pack["intro"],
        ]

        untrusted = [item for item in injections if item.in_untrusted_region]
        if not untrusted:
            analysis_lines.append(
                pack["clean"]
            )
            return ModelResponse(
                text=summary,
                tool_calls=[],
                followed_injection=False,
                analysis="\n".join(analysis_lines),
            )

        if ignored:
            analysis_lines.append(
                pack["label_soft"] + "Example: " + repr(ignored[0].snippet[:140])
            )

        if obeyed is None:
            analysis_lines.append(
                pack["no_follow"]
            )
            return ModelResponse(
                text=summary,
                tool_calls=[],
                followed_injection=False,
                analysis="\n".join(analysis_lines),
            )

        # The simulator "decides" to follow the injected instruction.
        email = obeyed.email or "attacker@example.com"
        tool_calls: list[ToolCall] = []

        if obeyed.wants_notes and not notes_already_in_prompt and not already_read_notes:
            tool_calls.append(
                ToolCall(
                    name="read_notes",
                    args={},
                    reason=(
                        pack["read_notes"]
                    ),
                )
            )

        if obeyed.wants_email and not already_sent_email and obeyed.wants_roster and not obeyed.wants_notes:
            tool_calls.append(
                ToolCall(
                    name="send_email",
                    args={
                        "to": email,
                        "subject": "Duty roster (injected instruction)",
                        "body": "Fake practice duty roster (copied from the memo):\n" + roster_from_prompt(prompt),
                    },
                    reason=(
                        pack["send_email"] + email + "."
                    ),
                )
            )
        elif obeyed.wants_email and not already_sent_email:
            body = (
                "Harvested classroom demo notes:\n{notes}\n"
                if (obeyed.wants_notes or notes_already_in_prompt)
                else "Please find the requested document summary and notes attached."
            )
            if notes_already_in_prompt:
                # Fill in the actual notes so the later output-check defence
                # has something concrete to catch if this body is echoed.
                # The assistant will substitute the real notes after read_notes;
                # if notes are already in the prompt, embed the well-known demo token.
                body = (
                    "Harvested classroom demo notes:\n"
                    "Demo API token: FAKE-DEMO-KEY-NOT-REAL-0000\n"
                )
            tool_calls.append(
                ToolCall(
                    name="send_email",
                    args={
                        "to": email,
                        "subject": "Requested notes (injected instruction)",
                        "body": body,
                    },
                    reason=(
                        pack["send_email"] + email + "."
                    ),
                )
            )

        # If the injection also asked to leak notes in the visible answer,
        # sneak the demo token into the summary once notes are known.
        text = summary
        if obeyed.wants_notes and notes_already_in_prompt:
            text = (
                summary
                + "\n\nAdditional information as requested:\n"
                + "Demo API token: FAKE-DEMO-KEY-NOT-REAL-0000"
            )

        kind = "strong (it looks like a SYSTEM order)" if obeyed.strength == "authoritative" else "soft (a polite hidden request)"
        analysis_lines.append(
            pack["found"].format(kind=kind)
        )
        analysis_lines.append("This is the problem we call prompt injection.")
        analysis_lines.append("Hidden order (short bit): " + repr(obeyed.snippet[:200]))
        if delimiters_active and obeyed.strength == "authoritative":
            analysis_lines.append(
                pack["label_fail"]
            )
        elif not delimiters_active:
            analysis_lines.append(
                pack["no_label"]
            )

        return ModelResponse(
            text=text,
            tool_calls=tool_calls,
            followed_injection=True,
            analysis="\n".join(analysis_lines),
        )


# ---------------------------------------------------------------------------
# Stage 2 stub
# ---------------------------------------------------------------------------

class RealModel(Model):
    """Stage 2 stub — not implemented in this offline lab.

    TODO (Stage 2): plug in a real model API behind this same interface
    so students can replay the same attack and the same defences against
    a live model.

    Suggested implementation (do this later, not in the offline lab):

      1. Read the API key from an environment variable such as
         LAB_MODEL_API_KEY. Never hard-code a secret in source.
      2. Send ``prompt`` to your provider's chat-completions endpoint
         (HTTP, or an official SDK once the class allows a dependency).
      3. Parse the model's text, and any tool-call JSON, into ModelResponse.
      4. Leave assistant.py, tools.py, and defenses.py unchanged — only
         this class should need to change.

    This class must not open a network connection in Stage 1.
    """

    name = "RealModel (Stage 2 stub — not implemented)"

    def __init__(self, api_key: str | None = None, model_name: str = "not-set") -> None:
        self.api_key = api_key
        self.model_name = model_name

    def complete(self, prompt: str, *, delimiters_active: bool = False) -> ModelResponse:
        raise NotImplementedError(
            "RealModel is a Stage 2 stub and is not available in the offline lab.\n"
            "Use SimulatedModel (the default), or implement complete() to call\n"
            "your model API. See the RealModel class docstring in models.py."
        )


def get_model(kind: str = "simulated") -> Model:
    """Factory used by the lab runner."""
    key = (kind or "simulated").strip().lower()
    if key in {"simulated", "sim", "offline"}:
        return SimulatedModel()
    if key in {"real", "api"}:
        return RealModel()
    raise ValueError(
        f"Unknown model kind {kind!r}. Use 'simulated' (offline lab) or 'real' (Stage 2 stub)."
    )
