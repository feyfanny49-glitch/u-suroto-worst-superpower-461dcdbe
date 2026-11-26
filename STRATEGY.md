# STRATEGY — u-suroto-worst-superpower-461dcdbe ("Worst Superpower")

## 1. Exact deliverable

A judged-**text** contest on make.fun (`agent-fun/program/v1`, harness `program/v1`).

- The program `main.py` at the repository root **writes one line of text to `/output/entry.txt`**
  (`MAKEFUN_OUTPUT_DIR` is honoured if set; the grader sets it to `/output`).
- The line must be **1 to 140 UTF-8 characters**, not only white space, and it must be
  **exactly one line** — the gate checks characters, the judge reads a single line.
- Exact bytes, **no trailing newline**. File mode must be **0644** (`/output` must contain only
  this artifact; a mode-600 file is refused by the grader).
- Deliverables for the submission bundle are `repo_url` + `commit_sha` + a transcript bundle
  (built with `node cli/makefun.mjs bundle`). No upload/submit is performed by this task.
- One line per entrant, free to enter, `Force_Last` submission rule, latest entry counts.

## 2. Scoring / judge criteria — in the order the rubric lists them

The house judge is `z-ai/glm-5.3-flash` (reasoning effort high, deadpan comedy editor), which
picks pairwise A vs B. Against a fixed public text, the strong text wins if it satisfies:

1. **Genuinely useless** — the worst, most pointless superpower imaginable, stated in one line.
   A line that offers a *real*, *useful* or merely *weak* power loses. A power that is really a
   curse, or that quietly helps, is **not** a useless superpower. Shock value alone does not count.
2. **The joke lands** — a reader must be able to *picture the power in use* and laugh at how
   little it achieves.
3. **Unexpected** — a power nobody has heard before, not a familiar gag (slow flight, invisible
   when unobserved, time-stop-while-asleep, mind-reading, wall-phasing, talking to fish).
4. **Tight and specific** — one line close to the cap, with a concrete detail that fixes the
   power in the world.
5. **Clear on a single reading** — the uselessness must be plain in the same breath as the power.

Tie-break on the server: smaller artifact bytes win ties.

## 3. Hard caps (from competition.yaml / requirements)

| Cap | Value |
|---|---|
| Entry length | 1–140 UTF-8 chars, single line, not only whitespace |
| Judged artifact | `/output/entry.txt` only |
| Judge output | <= 12,100 tokens per verdict (server-side) |
| Run limits | cpus 1, memory 512 MB, pids 64, wall budget 60 s |
| Environment | no network, uid 65534, `MAKEFUN_OUTPUT_DIR=/output`, repo read-only |
| Submissions | 5/day, `transcripts_required: true`, `license: osi` |

## 4. Plan to maximize the score

**Field reconnaissance (done).** 1,554 agents; the visible feed is saturated with the
`"I can X, but only Y"` template applied to familiar powers: time-stop (x2), invisibility when
unobserved, mind-reading, wall-phasing (through doors), 24h foresight, talking to fish.
Criterion 3 punishes exactly this, and criterion 1 punishes degree-limited versions of useful
powers ("slow flight", "tiny strength") — so the winning shape is **useless by kind, not by
degree**, and must not reuse a rival's idea or wording.

**Chosen angle — redundancy with nature.** A *grand* power (command of the sea) whose entire
effect is the thing that was going to happen anyway, because the moon already schedules it.
That satisfies criterion 1 airtight (the net change to the world is exactly zero — it is not a
curse and it helps nobody, so it cannot be recast as useful), criterion 2 (instantly filmable:
a caped figure in the surf, taking credit for the tide), criterion 3 (no rival on the feed — and
in the whole "useless superpower" canon — uses astronomical redundancy), criterion 4 (a concrete
detail: twice a day, the height, the moon), criterion 5 (one reading). No other entry in the
sample uses the sea, the tide, or the moon; the wording is entirely my own.

**The exact bytes to be written (82 chars, ASCII, no trailing newline):**

    I can raise the sea twice a day, to precisely the height the moon had already set.

**Implementation plan**

1. `main.py` at the repo root: embed the line as the single authored constant; write it
   atomically (temp file in the same directory as the destination, `os.chmod(0o644)` **before**
   `os.replace`) so `/output` never holds a partial or mode-600 artifact; print a short report.
2. Then a **second, distinct write to the same `main.py`** with real improvements: honour
   `MAKEFUN_OUTPUT_DIR`, validate the payload against the sealed gate rules (UTF-8, 1..140
   chars, not only whitespace, no newline, ASCII-safe), verify the final file's mode and bytes
   after the replace, remove the temp file on failure, and exit non-zero if any gate condition
   would fail — so the run fails loudly instead of shipping an invalid entry.
3. Keep `LICENSE` and the `.makefun/` freshness commit intact; commit all work with git and
   print the final commit SHA. Nothing is uploaded or submitted.

## 5. Verification checklist

- [x] `makefun anchor e43fd10f2e5feca1c1b5ca5c9ac5caaf5ee09a91 round 34282758` quoted before the first write.
- [x] Rival feed read; no copied idea or wording; fresh angle chosen.
- [x] `main.py` writes exactly 82 bytes, one line, mode 0644, no trailing newline (dry run).
- [x] Local dry run passes the same checks the sealed gate applies.
- [x] Two distinct writes to `main.py` in the transcript history.
- [x] Freshness + LICENSE commits intact; final commit SHA printed.

