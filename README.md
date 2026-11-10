# Mirage Watch Cyber Lab

> **Author:** Ray. An offline teaching lab about prompt injection and social
> engineering, from a defensive point of view. Everything here is fictional.

An offline classroom lab about **prompt injection** and **social
engineering**, taught from a **defensive** point of view.

The default story is a fictional training unit called **Mirage Watch**,
at an invented place called **Saffron Port Training Centre**. Students
are recruits. Their job is to keep **Hadi**, a practice duty assistant,
safe. The unit and the place are invented. They are not a real force
or a real location.

The original classroom story is still here as `--theme school`. In that
pack, students keep **Buddy**, a friendly practice robot, safe. The
shields and the fake tools are the same in both themes.

Everything is fake and local. There is no API key, no network call, and
nothing to install with pip. Python 3.8 or newer is enough (tested on
3.8, 3.9 and 3.13).

## Start here

- **Students:** open [STUDENT_GUIDE.md](STUDENT_GUIDE.md). It is written in
  simple English, with a word list and tick boxes.
- **Teachers:** open [TEACHER_GUIDE.md](TEACHER_GUIDE.md). It has a short
  briefing script, timings for a 60-90 minute lesson, a debrief, talking
  points, and how to add a real model later. Quiz answers are in
  [TEACHER_QUIZ_ANSWERS.md](TEACHER_QUIZ_ANSWERS.md).

## Quick start

```bash
python lab.py --list
python lab.py --stage 1
python lab.py --all
python lab.py --stage 14
python lab.py --theme school --all --no-pause
python lab.py --quiz
python lab.py --challenge
```

On some systems the command is `python3` instead of `python`.

On Windows, you can also type `py` instead of `python`.

## All options

| Option | What it does |
| --- | --- |
| `--list` | Show the missions and stop. |
| `--stage N` | Run one mission, `N` = 1 to 14. |
| `--all` | Run every mission in order. It does **not** wait for Enter. Add `--pause` to wait. |
| `--theme unit` / `--theme school` | Story: Hadi (default) or Buddy. Other names: `mirage`, `watch`, `military`, `default` = unit; `buddy`, `classroom` = school. |
| `--no-pause` | Never wait for Enter. Wins over `--pause`. |
| `--pause` | Always wait for Enter, also with `--all` or when the output is not a terminal. |
| `--no-color` | Plain text. Wins over `--color`. Colour also turns off by itself in a file or with `NO_COLOR`. |
| `--color` | Force colour. |
| `--approve` | A person says YES to the "ask a person" shield (default: NO). It changes Mission 5 and Mission 13 with `human`. In Missions 7 and 14 part B the word filter stops the page first. |
| `--shields LIST` | Mission 13 only. `all`, `none` (or `off`), or a comma list: `label,filter,tools,address,human,output,ignore,pictures`. Without it, a normal terminal asks y/n; `--all` and `--no-pause` use all shields. |
| `--doc NAME` | The bad page for Missions 1-7 and 13: `clean`, `comment` (default), `footnote`, `memo`, or a file inside this folder. |
| `--quiz` | The end-of-lab quiz (10 questions; school theme: 8). |
| `--challenge` | Test your own hidden-word picture (`documents/my_trap.png`). |
| `--image PATH` | Another picture for `--challenge`. |
| `--name NAME` | Your name on the scoreboard (default: Recruit; school: Agent). |
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
