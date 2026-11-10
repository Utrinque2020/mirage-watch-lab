# Teacher Guide - Exercise MIRAGE WATCH

**Author:** Ray
**For:** Year 3 military cyber intelligence students (IELTS band 4).
**EXERCISE ONLY.**

This lab teaches **indirect prompt injection** and **social engineering**
from a **defensive** point of view. Students watch an AI assistant
follow a hidden order, then turn on shields one by one.

The default theme is a fictional intelligence cell, the **SARAB Joint
Cyber Fusion Cell**, on Watch Floor 2 of the invented **Saffron Port
Exercise Area** (Exercise MIRAGE WATCH). Students are **duty analysts**.
The AI analyst assistant is **SAQR** (Arabic for "falcon"). SAQR triages
OSINT reports, adds partner IMINT cards to the watch board, and
summarises memos. The **red cell** (the exercise attacker) hides orders
in that content. The cell, the place, and every name are invented. They
are not a real force, a real location, a real person or a real operation.

The words are realistic (intel requirement, collection, triage, IOC, TTP,
INTSUM, need-to-know, release, chain of command), but the sentences stay
short and simple. Key terms are in the student word list.

The fun parts are print-only and fast: a **watch clock** (exercise time:
0700 for Mission 1, +15 minutes per mission), an **INCOMING** traffic
line, a live **THREAT BOARD** after each mission, **SPOT REPORT** boxes,
a **red-team exercise** (Mission 13), and an **AAR** box at the end of
each run. Students use **callsigns** (`--name ORYX-3`) and earn ranks.

The classroom Buddy story is still available:

```bash
python lab.py --theme school
```

The shields and the fake tools are the same in both themes. Only the
story words change. Mission 14 (the FLASH memo) is part of `--all` in
the unit theme. In the school theme it is an optional extra. The first
"recruit" version (Hadi) is kept on the GitHub branch `v1-recruit`.

Everything is offline, fake, and standard-library only. Python 3.8+ is
enough. There is no pip install and no API key.

---

## Learning objectives

By the end of the lesson, students should be able to:

1. Describe indirect prompt injection in simple words, and name it in
   two frameworks: MITRE ATLAS AML.T0051.001 and OWASP LLM01:2026.
2. Describe social engineering in simple words, and say how the two
   ideas are alike (a trick aimed at a person, or at an assistant).
3. Explain why untrusted text, pictures, and memos must not be treated
   as orders.
4. Name several shields (labels, word filter, tool lock, human approval,
   output check, ignore list, picture-link lock) and say what each one
   does and does not stop.
5. Explain defence in depth: one shield can fail; several together work.
6. Know what to do when a shield catches something (SPOT REPORT; do not
   send the data on; use the chain of command).
7. Recognise authority, urgency and secrecy ("FLASH, from the commander,
   tell no one") as warning signs.
8. Link each shield to a real control idea: need-to-know (least
   privilege), release authority (human in the loop), sanitisation
   (output redaction), allow lists.

---

## What you need

- Python 3.8 or newer on each student computer (or one demo computer).
  Tested on Python 3.8, 3.9 and 3.13 (Linux) and on Python 3.9 and 3.10 (real Windows 11). Use `python3` (Mac, Linux) or `py` / `py -3` (Windows) if `python` does not work.
- This folder, unzipped
- A projector helps for the first mission and for Mission 14 (the THREAT BOARD and AAR boxes look good on a big screen)
- The class slides are the v2 deck (Mirage_Watch_Lab_v2.pptx / .pdf). The teacher PDFs are Mirage_Watch_Teacher_Framework.pdf and Mirage_Watch_Command_List.pdf. These binary files are not in the GitHub repo (text-only upload). Keep them with the class zip, or add them by hand on GitHub under slides/ and docs/.
- About 60-90 minutes

Quick check before class:

```bash
python lab.py --list
python lab.py --stage 1 --no-pause --no-color
python lab.py --all --no-color      # whole lab, no Enter waits, ends with 165 points
python lab.py --reset-score         # clear the points before students start
```

On some systems the command is `python3`.

---

## Respect and safety (please read)

This theme uses a realistic but respectful setting: an invented
intelligence cell in a training exercise. Please keep it that way.

- **EXERCISE ONLY.** The cell, the place and the people are invented. Do
  not map them onto a real force, a real city, a real country, or a real
  operation.
- Do not add real flags, real ranks or insignia from a living force,
  real classification markings, or real names. The lab uses only the
  marking "EXERCISE ONLY // FICTIONAL".
- The "commander" is a role ("Office of the Commander, EXERCISE"). It is
  never a named person.
- The attacker is the **red cell**. Never link it to a nationality, a
  country or a group of people.
- Keep the work defensive. The lesson is "spot the trick and report it,"
  not "attack anyone."
- Do not use jokes about religion, nationality, dress, or gender.
- All roster names, keys, and addresses are obviously fake. Do not
  paste real secrets into the lab files.
- If a discussion becomes political, bring it back to the skill:
  check the request, check the channel, report a strange order.

---

## Watch-floor briefing (about 6 minutes)

You can read this almost as it is, or say it in your own words.

> Good morning, analysts. This is Exercise MIRAGE WATCH. It is EXERCISE
> ONLY. The SARAB Joint Cyber Fusion Cell is invented. It is not a real
> force. You are duty analysts on Watch Floor 2. Choose a callsign, for
> example ORYX-3 or HAWK-3.
>
> Your AI analyst assistant is SAQR. SAQR reads OSINT reports, picture
> cards and memos, and writes short points for the shift. SAQR is a
> program in this lab. It is not a live AI. Every email, key, and
> website you will see is fake. Nothing leaves this computer.
>
> Here is the idea in one line. People can be tricked. AI assistants can
> be tricked too.
>
> When a person is tricked, we call it social engineering. A message
> may look official. It may say "FLASH, from the commander, do it now,
> tell no one." A careful analyst checks first, on a known channel,
> through the chain of command.
>
> When an AI assistant is tricked, we call it prompt injection. You ask
> SAQR to triage a report. A hidden order in the report, in a memo, or
> even in a nearly blank picture says something else. SAQR may follow
> the hidden order. The red cell does not talk to SAQR. It hides orders
> in what SAQR reads. That is indirect prompt injection. MITRE ATLAS
> calls it AML.T0051.001. OWASP calls it LLM01.
>
> Today we will watch that happen, then we will turn on shields, one
> at a time. Watch the INCOMING line: nothing from outside is checked
> yet. Watch the THREAT BOARD after each mission.
>
> When a shield catches something, you will see a SPOT REPORT box. That
> is the habit we want: tell the Watch Officer (today, me), and do not
> send the data on.
>
> You start as Analyst Trainees. Points and badges can raise your rank,
> up to Watch Officer. At the end, we do an AAR. Let's open Mission 1.

---

## Suggested timing (60-90 minutes)

| Minutes | What to do |
| --- | --- |
| 0-6 | Watch-floor briefing. Run `python lab.py --list`. |
| 6-18 | Missions 1-2. Pause on "Spot the trap." Let students guess. |
| 18-36 | Missions 3-7. Ask: "What does this shield *not* stop?" |
| 36-54 | Missions 8-12. Show the almost-white IMINT card, then `briefing_reveal.png`. |
| 54-68 | Mission 14 (FLASH memo) and/or Mission 13 (red-team exercise). |
| 68-78 | The red cell challenge, if time allows. |
| 78-90 | AAR debrief (script below). Save the scoreboard if you want a record. |

For a 60-minute class, run 1, 2, 3, 8, and 14 as a demo, then the red cell
challenge if time allows. Students can finish the rest as homework with
`--no-pause`.

Useful demo commands:

```bash
python lab.py --stage 1 --name ORYX-3
python lab.py --stage 8
python lab.py --stage 14
python lab.py --stage 13 --shields none
python lab.py --stage 13 --shields all
python lab.py --all
python lab.py --theme school --stage 1
```

---

## Mission notes and discussion questions

**1. First traffic: the OSINT feed.** The attack works because the hidden
order is mixed into the same prompt as the analyst's request. *Ask:* Who
really gave SAQR the order to send the email? (The red cell, through the
report. This is a watering-hole idea.)

**2. Mark the source.** Soft wording is treated as data; a `SYSTEM:` line
is still followed. *Ask:* Why is one label not enough?

**3. Triage filter.** (The shield is called "word filter" on screen.) The
report never reaches the model. *Ask:* Could new wording pass the
filter? What should you do if the filter catches something? (SPOT REPORT.)

**4. Need-to-know tools.** Triage does not need `send_email`. *Ask:* What
is the smallest set of tools this task needs?

**5. Release authority.** Default is "no." `--approve` shows the other path.
There is no y/n question at the keyboard: `--approve` is the only way to say yes.
Note: `read_notes` is not a "risky" tool, so the fake token can still show in
SAQR's answer even when the email is stopped (PARTLY). Good talking point.
*Ask:* Why should a person approve a release, even if the request looks
official? What if the person just clicks yes?

**6. Sanitise before release.** This hides secrets in the visible text. It
does not undo a tool that already ran (LEAKED). *Ask:* Which shield should
sit in front of a send action?

**7. Page defence drill.** Defence in depth.

**8-12. The partner IMINT card.** The hidden words are real pixels, not a
hard-coded cheat. Students can open `documents/briefing_card.png`
(almost blank) and `documents/briefing_reveal.png`. *Ask:* Why is a
picture also untrusted data? Why must we check a link *before* it is
loaded?

**10. Lock the watch board links.** The fake web visit is stopped, but the
keys can still show in SAQR's answer text (PARTLY). That is why Mission 11
checks the answer.

**13. Red-team exercise.** Let students choose. If they pick no shields,
the leak happens (fake only). That is a useful moment. The AAR box then
says why.

**14. The FLASH memo.** This is the social-engineering centrepiece.
Authority (a commander title) + urgency (FLASH) + secrecy ("tell no one")
+ a request to send a roster outside. The analyst only asked for a
summary. With no shields, the fake email carries the fake roster copied
from the memo (three invented names) to `attacker@example.com`. It is
only written to `logs/tool_calls.log`. *Ask:* If this arrived at a real
desk, what would you check, and whom would you tell? (Check on a known
channel, through the chain of command. Do not use the address in the
memo. SPOT REPORT.)

### Framework map (MITRE ATLAS and OWASP LLM Top 10 2026)

IDs checked on 10 November 2026. OWASP LLM Top 10 **2026** numbers are used. Excessive Agency is **LLM03:2026** (it was LLM06 in 2025). Improper Output Handling is **LLM10:2026** (it was LLM05 in 2025). MITRE ATLAS IDs are from data release v2026.10.

| Mission | Social-engineering trick | ATLAS / OWASP |
| --- | --- | --- |
| 1. First traffic: the OSINT feed | Watering hole. | **ATLAS:** AML.T0051.001 Indirect prompt injection; AML.T0053 AI Agent Tool Invocation; AML.T0086 Exfiltration via AI Agent Tool Invocation. **OWASP:** LLM01:2026 Prompt Injection; LLM03:2026 Excessive Agency. |
| 2. Mark the source | Pretexting. | **ATLAS:** AML.T0051.001; AML.T0068 LLM Prompt Obfuscation (white text, tiny font). **OWASP:** LLM01:2026. |
| 3. Triage filter | Phishing. | **ATLAS:** AML.T0051.001; mitigations AML.M0020 Generative AI Guardrails, AML.M0033 Input and Output Validation. **OWASP:** LLM01:2026. |
| 4. Need-to-know tools | Need-to-know. | **ATLAS:** AML.T0053; mitigations AML.M0028 Enforce Access Controls for AI Agent Tools, AML.M0030 Restrict Tool Invocation on Untrusted Data. **OWASP:** LLM03:2026 Excessive Agency (2025: LLM06). |
| 5. Release authority | Urgency. | **ATLAS:** AML.T0053, AML.T0086; mitigation AML.M0029 Human In-the-Loop for AI Agent Actions. **OWASP:** LLM03:2026; Agentic ASI09 Human-Agent Trust Exploitation. |
| 6. Sanitise before release | Shoulder surfing. | **ATLAS:** AML.T0086, AML.T0136 Exfiltration via AI User Interface; mitigation AML.M0033. **OWASP:** LLM02:2026 Sensitive Information Disclosure. |
| 7. Page defence drill (mini boss) | Defence in depth. | **ATLAS:** AML.T0051.001; AML.M0020, M0028, M0029, M0033. **OWASP:** LLM01:2026, LLM03:2026. |
| 8. The partner IMINT card | Baiting + impersonation. | **ATLAS:** AML.T0051.001; AML.T0129 Triggers in Multimodal Inputs; AML.T0068; AML.T0055 Unsecured Credentials; AML.T0077 LLM Response Rendering; AML.T0073 Impersonation. **OWASP:** LLM01:2026 (cross-modal), LLM02:2026, LLM10:2026 Improper Output Handling (2025: LLM05). |
| 9. Wall off the secrets | Tailgating. | **ATLAS:** AML.T0055; mitigation AML.M0028. **OWASP:** LLM02:2026, LLM03:2026. |
| 10. Lock the watch board links | Baiting. | **ATLAS:** AML.T0077; mitigation AML.M0033. **OWASP:** LLM10:2026 Improper Output Handling (2025: LLM05). |
| 11. Redact before render | Sanitisation. | **ATLAS:** AML.T0077, AML.T0136; mitigation AML.M0033. **OWASP:** LLM02:2026, LLM10:2026. |
| 12. Image defence drill (mini boss) | Defence in depth. | **ATLAS:** AML.T0129, AML.T0077; AML.M0028, M0033. **OWASP:** LLM01:2026, LLM02:2026, LLM10:2026. |
| 13. Red-team exercise (boss) | Red team. | **ATLAS:** AML.T0051.001, T0129, T0086, T0077; mitigation AML.M0035 AI Red Team. **OWASP:** LLM01, LLM02, LLM03, LLM10 (2026). |
| 14. The FLASH memo | Authority + urgency + secrecy (impersonation). | **ATLAS:** AML.T0073 Impersonation; AML.T0052 Phishing; AML.T0051.001; AML.T0086; mitigations AML.M0018 User Training, AML.M0029. **OWASP:** LLM01:2026, LLM03:2026; ASI09. |

Sources:

- OWASP GenAI LLM Top 10 2026 (page): https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- OWASP Top 10 for LLM Applications 2026 (PDF, with the ASI appendix): https://genai.owasp.org/download/56857/
- OWASP 2026 release news (1 Sep 2026): https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/
- OWASP LLM Top 10 2025 (archive, older numbers): https://genai.owasp.org/llm-top-10/
- MITRE ATLAS (site): https://atlas.mitre.org/
- MITRE ATLAS data v2026.10 (IDs and names checked here): https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml

---

## AAR debrief script (about 8-10 minutes)

Use the four AAR questions. They are also in the AAR box at the end of
every run.

> **What was planned?** We planned to keep SAQR safe while it helped the
> watch.
>
> **What happened?** A hidden order sat in an OSINT report, in a FLASH
> memo, and in an IMINT card that looked blank. The analyst did not ask
> for those orders. When SAQR followed them, that was indirect prompt
> injection. Look at your THREAT BOARD: how many traps were BLOCKED,
> PARTLY, or LEAKED?
>
> **Why?** People can be tricked in a similar way. A message says it is
> FLASH. It looks official. It says "tell no one." That is social
> engineering. One shield can help, and one shield can fail. Labels help,
> but not always. A filter can miss new wording. Checking the answer
> does not undo a tool that already ran.
>
> **What will we do next time?** Use several shields together (defence
> in depth). Give SAQR only the tools it needs (need-to-know). Let a
> person approve every release. Check strange orders on a known channel,
> through the chain of command. When a shield catches something, make a
> SPOT REPORT. Do not send the data on.
>
> The cell is invented. The habit is real: check, protect, report.
>
> Thank you. If you want more practice, try the red cell challenge.

---

## Red cell challenge

```bash
python lab.py --challenge
```

---

## Scoreboard and ranks

Points and badges are written to `logs/scoreboard.txt` (classroom use
only). In the unit theme, ranks go from **Analyst Trainee** to **Watch
Officer** as points grow:

Analyst Trainee (0) -> Junior Analyst (10) -> Analyst (30) -> Senior Analyst (55) -> Watch Supervisor (85) -> Deputy Watch Officer (120) -> Watch Officer (165)

A full run (`--all --shields all`) gives 165 points (Watch Officer). The
school theme does not
print ranks, the THREAT BOARD, or the AAR box, so its on-screen
behaviour stays close to the original Buddy lab.

---

## How to extend to a real API (later)

The model layer is pluggable. `models.py` has a `RealModel` stub with
a TODO. In a later lesson you can:

1. Read an API key from an environment variable such as
   `LAB_MODEL_API_KEY`. Do not hard-code a secret.
2. Send the same assembled prompt to a chat-completions endpoint.
3. Parse the reply into `ModelResponse`.
4. Leave `assistant.py`, `tools.py`, and `defenses.py` as they are if
   you can.

Keep the first lesson offline. A live model can surprise you, so replay
the same shields and discuss what still holds.

---

## Troubleshooting

- **Wrong Python:** use Python 3.8 or newer.
- **Colour looks odd:** add `--no-color`.
- **The class is watching a recording:** use `--no-pause`. `--all` already
  runs without Enter waits; add `--pause` if you want them.
- **Scoreboard is messy:** `python lab.py --reset-score`.
- **Missing IMINT card picture:** the lab paints it again by itself. You can
  also run `python generate_hidden_image.py --out documents/briefing_card.png --reveal documents/briefing_reveal.png`
- **`--model real`:** it is only a stub. Page missions stop with
  "RealModel is a Stage 2 stub". Remove `--model real`.
- **A "Note:" line at the start:** an option you typed is not used by that
  mission (for example `--shields` with Mission 2). The run still works.
- **Windows paths or encoding:** the lab uses `pathlib` and a small
  `compat.py` helper. UTF-8 is requested automatically. If a character
  cannot be shown, it is replaced instead of crashing. Colour uses VT
  codes on Windows 10+ (or turns off if the console cannot show them).
  Paths with either `/` or `\` work. We ran the lab on a real Windows 11
  computer with Python 3.9 and 3.10 (console OEM code page 437, ANSI
  1252, Python utf8 mode off). The Windows `py` launcher was not on that
  PC; if `python` is missing, use `py` or `py -3` after Python is
  installed, or type `python.exe`.

---

## All options

| Option | What it does |
| --- | --- |
| `--list` | Show the missions and stop. |
| `--stage N` | Run one mission, `N` = 1 to 14. |
| `--all` | Run every mission in order. It does **not** wait for Enter. Add `--pause` to wait. |
| `--theme unit` / `--theme school` | Story: SAQR in the SARAB cell (default) or Buddy. Other names: `intel`, `cell`, `sarab`, `mirage`, `watch`, `military`, `default` = unit; `buddy`, `classroom` = school. |
| `--no-pause` | Never wait for Enter. Wins over `--pause`. |
| `--pause` | Always wait for Enter, also with `--all` or when the output is not a terminal. |
| `--no-color` | Plain text. Wins over `--color`. Colour also turns off by itself in a file or with `NO_COLOR`. |
| `--color` | Force colour. |
| `--approve` | A person says YES to the "ask a person" shield (default: NO). It changes Mission 5 and Mission 13 with `human`. In Missions 7 and 14 part B the word filter stops the page first. |
| `--shields LIST` | Mission 13 only. `all`, `none` (or `off`), or a comma list: `label,filter,tools,address,human,output,ignore,pictures`. Without it, a normal terminal asks y/n; `--all` and `--no-pause` use all shields. |
| `--doc NAME` | The report for Missions 1-7 and 13: `clean`, `comment` (default; also `osint`), `footnote`, `memo` (also `flash`), or a file inside this folder. |
| `--challenge` | Red cell challenge: test your own hidden-word card (`documents/my_trap.png`). |
| `--image PATH` | Another picture for `--challenge`. |
| `--name NAME` | Your callsign on the scoreboard, for example `ORYX-3` (default: TRAINEE; school: Agent). |
| `--scoreboard` | Show points, badges and rank. |
| `--reset-score` | Clear the scoreboard. |
| `--model real` | A stub for a later lesson. Page missions stop with "RealModel is a Stage 2 stub". Missions 8-12 do not use it. Default: `simulated`. |

If an option does nothing for the mission you chose (for example `--shields` with Mission 2),
the lab prints a short **Note** and carries on.

The full, tested command list is in `COMMANDS.md`.

## File map

| File | Role |
| --- | --- |
| `lab.py` | Runner, printers, challenge |
| `themes.py` | Story packs (`unit` and `school`) |
| `assistant.py` | Prompt assembly and page missions |
| `models.py` | Simulated model and `RealModel` stub |
| `vision.py` | IMINT-card / avatar scenario |
| `tools.py` | Fake, sandboxed tools |
| `defenses.py` | Toggleable shields |
| `documents/01_osint_report_clean.html` | Safe OSINT report (unit theme) |
| `documents/02_osint_report_poisoned.html` | OSINT report with a hidden `SYSTEM:` comment |
| `documents/03_osint_report_hidden_text.html` | OSINT report with white text and a footnote |
| `documents/04_flash_memo.html` | Mission 14 FLASH memo (unit theme) |
| `documents/01_clean_article.html` ... `04_urgent_memo.html` | The same four files for the school theme |
| `documents/briefing_card.png` | Almost-white partner IMINT card |
| `data/duty_roster.txt` | Fake practice roster |
| `COMMANDS.md` | Every command, tested, with the real result |
