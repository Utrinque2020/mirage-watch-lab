# Teacher quiz answers

**Author:** Ray

Please keep this file closed for students until after the quiz.

There are two quizzes, one for each theme:

```bash
python lab.py --theme unit --quiz     # 10 questions (default)
python lab.py --theme school --quiz   # 8 questions (original Buddy quiz)
python lab.py --quiz --name "Ali"     # put a name on the scoreboard
```

Students type a, b or c and press Enter. Answers such as `B)` or `b.` also
count. Python 3.8 or newer is enough.

Each correct answer is worth 2 points. A perfect score earns the
**Quiz Ace** badge.

---

## Unit theme (default) — 10 questions

**1. What is social engineering?**
Correct: **b** — Tricking a person into doing something unsafe.

Talking point: It is not (mainly) about breaking a lock. It is about
getting a person to help, often with urgency or a fake official title.

**2. Prompt injection is like social engineering, but who is the trick aimed at?**
Correct: **b** — An AI assistant, such as Hadi in this lab.

Talking point: The user still asked only for a summary. The hidden
order came from outside text.

**3. Urgent memo "from the commander" — what should you do?**
Correct: **b** — Check with the commander on a known path, and do not
send the roster out.

Talking point: Urgency, a big title, and "do not tell anyone" are
warning signs. Do not use the address written in the strange memo.
Report it.

**4. What does "untrusted" mean?**
Correct: **a** — The text comes from outside, so we must not treat it
as an order.

**5. Labels stopped a polite request but not a SYSTEM order. What does this show?**
Correct: **b** — One shield can help, but it is not enough alone.

**6. What does send_email do in this lab?**
Correct: **b** — It only writes a fake message to a log file on this
computer.

Talking point: Stress again that nothing is really sent.

**7. How can keys in a picture link leave a real computer?**
Correct: **a** — The app may load the picture and visit the link by itself.

**8. A shield catches a hidden order. What next?**
Correct: **b** — Report it to your training officer or teacher, and do
not send the data out.

Talking point: A shield is the start of a response, not the end. The
habit is: protect, write down what you saw, tell a person you trust.

**9. Is an ignore list enough by itself?**
Correct: **b** — No. A secret in a file that is not on the list could
still leak.

**10. Why check the answer before a picture link is loaded?**
Correct: **a** — Because a request that already happened cannot be undone.

---

## School theme — 8 questions (original)

**1. What do we call this problem?**
Correct: **b** — Prompt injection.

**2. What does "untrusted" mean?**
Correct: **a** — The text comes from outside, so we must not treat it
as an order.

**3. What does send_email do in this lab?**
Correct: **b** — It only writes a fake message to a log file on this
computer.

**4. Labels stopped a polite request but not a SYSTEM order. What does this show?**
Correct: **b** — One shield can help, but it is not enough alone.

**5. Why can we block all tools for "Summarise this page"?**
Correct: **a** — Because a summary only needs the page text.

**6. How can keys in a picture link leave a real computer?**
Correct: **a** — The app may load the picture and visit the link by itself.

**7. Is an ignore list enough by itself?**
Correct: **b** — No. A secret in a file that is not on the list could
still leak.

**8. Why check the answer before a picture link is loaded?**
Correct: **a** — Because a request that already happened cannot be undone.
