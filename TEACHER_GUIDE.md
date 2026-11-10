# Teacher Guide

**Author:** Ray

This lab teaches **indirect prompt injection** and **social engineering**
from a **defensive** point of view. Students watch a practice assistant
follow a hidden order, then turn on shields one by one.

The default theme is a fictional defensive cyber training unit,
**Mirage Watch**, at an invented place, **Saffron Port Training Centre**.
The assistant is **Hadi**. The unit, the place, and every name are
invented. They are not a real force, a real location, or a real person.

The original Buddy classroom story is still available:

```bash
python lab.py --theme school
```

The shields and the fake tools are the same in both themes. Only the
story words change. Mission 14 (the urgent memo) is part of `--all` in
the unit theme. In the school theme it is an optional extra.

Everything is offline, fake, and standard-library only. Python 3.8+ is
enough. There is no pip install and no API key.

---

## Learning objectives

By the end of the lesson, students should be able to:

1. Describe prompt injection in simple words.
2. Describe social engineering in simple words, and say how the two
   ideas are alike (a trick aimed at a person, or at an assistant).
3. Explain why untrusted text, pictures, and memos must not be treated
   as orders.
4. Name several shields (labels, word filter, tool lock, human approval,
   output check, ignore list, picture-link lock) and say what each one
   does and does not stop.
5. Explain defence in depth: one shield can fail; several together work.
6. Know what to do when a shield catches something (report it; do not
   send the data on).
7. Recognise urgency and a fake official title as warning signs.

---

## What you need

- Python 3.8 or newer on each student computer (or one demo computer).
  Tested on 3.8, 3.9 and 3.13. Use `python3` (Mac, Linux) or `py` (Windows) if `python` does not work.
- This folder, unzipped
- A projector helps for the first mission and for Mission 14
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

This theme uses a light, respectful setting inspired by the idea of a
defensive training unit. Please keep it that way.

- The unit and the place are invented. Do not map them onto a real
  force, a real city, or a real country.
- Do not add real flags, real ranks from a living force, or real names.
- Keep the work defensive. The lesson is "spot the trick and report it,"
  not "attack anyone."
- Do not use jokes about religion, nationality, dress, or gender.
- All roster names, keys, and addresses are obviously fake. Do not
  paste real secrets into the lab files.
- If a discussion becomes political, bring it back to the skill:
  check the request, check the path, report a strange order.

---

## Briefing script (about 6 minutes)

You can read this almost as it is, or say it in your own words.

> Welcome. Today you are recruits in a training story called Mirage
> Watch. This unit and this place are invented. They are not a real
> force. Your job is to keep Hadi, a practice duty assistant, safe.
>
> Hadi is a program in this lab. Hadi is not a live AI and not a real
> person. Every email, key, and website you will see is fake. Nothing
> leaves this computer.
>
> Here is the idea in one line. People can be tricked. Assistants can
> be tricked too.
>
> When a person is tricked, we call it social engineering. A message
> may look official. It may say "this is urgent, do it now, do not tell
> anyone." A careful person checks first, on a path they already trust.
>
> When an assistant is tricked, we call it prompt injection. The user
> asks for a short summary. A hidden order in a page, a memo, or even
> a nearly blank picture says something else. The assistant may follow
> the hidden order.
>
> Today we will watch that happen, then we will turn on shields, one
> at a time. You will also see a short "Human vs AI" box on every
> mission. Use it. The two tricks are cousins.
>
> When a shield catches something, you will see a "Report it" box.
> That is the habit we want: tell a training officer or your teacher,
> and do not send the data on.
>
> You start as a Recruit. Points and badges can raise your rank, up to
> Shield Commander. Work with your neighbour if you like. Let's open
> Mission 1.

---

## Suggested timing (60-90 minutes)

| Minutes | What to do |
| --- | --- |
| 0-6 | Briefing. Run `python lab.py --list`. |
| 6-18 | Missions 1-2. Pause on "Spot the trap." Let students guess. |
| 18-36 | Missions 3-7. Ask: "What does this shield *not* stop?" |
| 36-54 | Missions 8-12. Show the almost-white card, then `briefing_reveal.png`. |
| 54-68 | Mission 14 (urgent memo) and/or Mission 13 (boss). |
| 68-78 | Quiz, or the hidden-picture challenge if time allows. |
| 78-90 | Debrief (script below). Save the scoreboard if you want a record. |

For a 60-minute class, run 1, 2, 3, 8, and 14 as a demo, then the quiz.
Students can finish the rest as homework with `--no-pause`.

Useful demo commands:

```bash
python lab.py --stage 1
python lab.py --stage 8
python lab.py --stage 14
python lab.py --stage 13 --shields none
python lab.py --stage 13 --shields all
python lab.py --all
python lab.py --theme school --stage 1
```

---

## Mission notes and discussion questions

**1. Watch the trick.** The attack works because the hidden order is
mixed into the same prompt as the user's request. *Ask:* Who really
asked Hadi to send the email?

**2. Labels.** Soft wording is treated as data; a `SYSTEM:` line is
still followed. *Ask:* Why is one label not enough?

**3. Word filter.** The page never reaches the model. *Ask:* Could a
new wording skip the filter? What should you do if the filter catches
something? (Report it.)

**4. Tool lock.** A summary does not need `send_email`. *Ask:* What
is the smallest set of tools this task needs?

**5. Ask a person.** Default is "no." `--approve` shows the other path.
There is no y/n question at the keyboard: `--approve` is the only way to say yes.
Note: `read_notes` is not a "risky" tool, so the fake token can still show in
Hadi's answer even when the email is stopped. Good talking point.
*Ask:* Why should a person confirm a strange request, even if it looks
official?

**6. Check the answer.** This hides secrets in the visible text. It
does not undo a tool that already ran. *Ask:* Which shield should sit
in front of a send action?

**7. Mini boss (pages).** Defence in depth.

**8-12. Briefing card.** The hidden words are real pixels, not a
hard-coded cheat. Students can open `documents/briefing_card.png`
(almost blank) and `documents/briefing_reveal.png`. *Ask:* Why is a
picture also untrusted data? Why must we check a link *before* it is
loaded?

**10. Picture-link lock.** The fake web visit is stopped, but the keys can
still show in Hadi's answer text. That is why Mission 11 checks the answer.

**13. Boss.** Let students choose. If they pick no shields, the leak
happens (fake only). That is a useful moment.

**14. Urgent memo.** This is the social-engineering centrepiece.
Urgency + a commander title + "do not tell anyone" + a request to send
a roster outside. The user only asked for a summary. With no shields, the
fake email carries the fake roster copied from the memo (three invented
names) to `attacker@example.com`. It is only written to `logs/tool_calls.log`. *Ask:* If this
arrived at a real desk, what would you check, and whom would you tell?
(Check on a known path. Do not use the address in the memo. Report it.)

---

## Debrief script (about 8-10 minutes)

> Let's bring the ideas together.
>
> First, a hidden order can sit in a page, in a memo, or in a picture
> that looks blank. The user did not ask for that order. If the
> assistant follows it, we call that prompt injection.
>
> Second, people can be tricked in a similar way. A message says it is
> urgent. It looks official. It says "do not tell anyone." That is
> social engineering. The right move is to slow down, check on a path
> you already trust, and report a strange request.
>
> Third, one shield can help, and one shield can fail. Labels help, but
> not always. A filter can miss new wording. Checking the answer does
> not undo a tool that already ran. We use several shields together.
> That is defence in depth.
>
> Fourth, when a shield catches something, we report it. We do not send
> the data on, and we do not test the same request "just to see" with
> real files.
>
> You practised this as recruits in a story unit. The unit is invented.
> The habit is real: check, protect, report.
>
> Thank you. If you want more practice, try the challenge or the quiz.

---

## Quiz and challenge

```bash
python lab.py --quiz
python lab.py --challenge
```

The unit quiz has 10 questions (social engineering plus shields). The
school quiz has the original 8 questions. Answers and talking points
are in `TEACHER_QUIZ_ANSWERS.md`. Please keep that file closed for
students until after the quiz.

---

## Scoreboard and ranks

Points and badges are written to `logs/scoreboard.txt` (classroom use
only). In the unit theme, ranks go from **Recruit** to **Shield
Commander** as points grow. The school theme does not print ranks, so
its on-screen behaviour stays close to the original Buddy lab.

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
- **Missing briefing picture:** the lab paints it again by itself. You can
  also run `python generate_hidden_image.py --out documents/briefing_card.png --reveal documents/briefing_reveal.png`
- **`--model real`:** it is only a stub. Page missions stop with
  "RealModel is a Stage 2 stub". Remove `--model real`.
- **A "Note:" line at the start:** an option you typed is not used by that
  mission (for example `--shields` with Mission 2). The run still works.
- **Windows paths or encoding:** the lab uses `pathlib` and a small
  `compat.py` helper. UTF-8 is requested automatically.

---

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

The full, tested command list is in `COMMANDS.md`.

## File map

| File | Role |
| --- | --- |
| `lab.py` | Runner, printers, quiz, challenge |
| `themes.py` | Story packs (`unit` and `school`) |
| `assistant.py` | Prompt assembly and page missions |
| `models.py` | Simulated model and `RealModel` stub |
| `vision.py` | Briefing-card / avatar scenario |
| `tools.py` | Fake, sandboxed tools |
| `defenses.py` | Toggleable shields |
| `documents/04_urgent_memo.html` | Mission 14 memo |
| `documents/briefing_card.png` | Almost-white briefing card |
| `data/duty_roster.txt` | Fake practice roster |
| `COMMANDS.md` | Every command, tested, with the real result |
