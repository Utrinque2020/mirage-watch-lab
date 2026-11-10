# Exercise MIRAGE WATCH — AI intel cell lab

> **Author:** Utrinque2020. An offline teaching lab about **indirect prompt injection**
> and **social engineering**, from a defensive point of view.
> **EXERCISE ONLY.** Everything here is fictional.

For cyber intelligence students. English is kept simple
(about IELTS band 4).

The default story is the **SARAB Joint Cyber Fusion Cell**, an invented
intelligence cell on Watch Floor 2 of the invented **Saffron Port Exercise
Area**. Students are **duty analysts**. Their AI analyst assistant is
**SAQR** (Arabic for "falcon"). SAQR triages OSINT reports, adds partner
IMINT cards to the watch board, and summarises memos. The **red cell** hides
orders inside that content. The students turn on shields to keep SAQR safe.
The cell, the place and all people are invented. They are not a real force,
a real location or a real operation.

The fun parts: a **watch clock** (exercise time), an **INCOMING** traffic
line, a live **THREAT BOARD**, **SPOT REPORT** boxes, a **red-team exercise**
(Mission 13), an **AAR** (after-action review) box, callsigns, and ranks from
**Analyst Trainee** to **Watch Officer**.

Each mission is mapped to **MITRE ATLAS** (for example AML.T0051.001
Indirect prompt injection) and the **OWASP Top 10 for LLM Applications 2026**
(for example LLM01:2026 Prompt Injection, LLM03:2026 Excessive Agency). The
table is in TEACHER_GUIDE.md.

The classroom story is still here as `--theme school`. In that pack,
students keep **Buddy**, a friendly practice robot, safe. The shields and
the fake tools are the same in both themes.

Everything is fake and local. There is no API key, no network call, and
nothing to install with pip. Python 3.8 or newer is enough (tested on
3.8, 3.9 and 3.13).

The first version of this lab (the "recruit" story with Hadi) is kept on the
`v1-recruit` branch on GitHub.

## Start here

- **Students:** open [STUDENT_GUIDE.md](STUDENT_GUIDE.md). It is written in
  simple English, with a word list and tick boxes.
- **Teachers:** open [TEACHER_GUIDE.md](TEACHER_GUIDE.md). It has a short
  watch-floor briefing, timings for a 60-90 minute lesson, an AAR debrief,
  the ATLAS/OWASP table, and how to add a real model later.
- **Slides and PDFs:** the class deck (`Mirage_Watch_Lab_v2.pptx` and
  `.pdf`) and the teacher PDFs (`Mirage_Watch_Teacher_Framework.pdf`,
  `Mirage_Watch_Command_List.pdf`) are classroom files. They are not in
  this git repository, because the upload tool we use can only send text,
  not binary files such as .pptx or .pdf. Keep them with the lab zip, or
  add them by hand in the GitHub website under `slides/` and `docs/` if
  you want them next to the code.

## Quick start

```bash
python lab.py --list
python lab.py --stage 1 --name ORYX-3
python lab.py --all
python lab.py --stage 14
python lab.py --theme school --all --no-pause
python lab.py --challenge
```

On some systems the command is `python3` instead of `python`.

On Windows, you can type `py` or `py -3` if `python` does not work. If
`python` opens the Microsoft Store, Python is not installed yet. Install
Python, or run `python.exe` from a Python folder you already have. The
lab was tested on Windows 11 with Python 3.9 and 3.10, and on Linux with
3.8, 3.9 and 3.13.

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
| `--approve` | A person says YES to the "ask a person" shield (release authority; default: NO). It changes Mission 5 and Mission 13 with `human`. In Missions 7 and 14 part B the word filter stops the page first. |
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

The full, tested command list is in [COMMANDS.md](COMMANDS.md).

## Pictures

The almost-white pictures (`documents/briefing_card.png`, `documents/cat.png`) and their
"reveal" copies are made by the lab itself, with the Python standard library only.
The GitHub copy of this lab has **no .png files**, because the lab makes them.
If a picture is missing (for example, in a fresh copy from GitHub), the lab paints it
again the first time you run a picture mission. You can also make them yourself:

```bash
python generate_hidden_image.py --out documents/briefing_card.png --reveal documents/briefing_reveal.png
python generate_hidden_image.py --reveal
```

## Logs

`logs/scoreboard.txt` keeps points. `logs/tool_calls.log` keeps the fake emails.
`logs/attacker_requests.log` keeps the fake web visits. Nothing leaves the computer.

## Sample files (unit theme)

`documents/01_osint_report_clean.html`, `02_osint_report_poisoned.html`, `03_osint_report_hidden_text.html` (OSINT reports) and `04_flash_memo.html` (the FLASH memo). The school theme uses `01_clean_article.html` to `04_urgent_memo.html`. All are EXERCISE ONLY.
