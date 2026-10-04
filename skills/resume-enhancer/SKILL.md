---
name: resume-enhancer
description: Rebuild a resume to a one-page house style, show every change with the rule behind it before making it, and render it to PDF with LaTeX. Use when someone says "improve my resume", "fix this resume", "make my resume one page", "tailor my resume to this posting", or shares a resume to clean up.
---

# Resume enhancer

Rebuilds a resume to the house style in [rules.md](rules.md) and renders it in the house
template. Every change is shown first with the rule behind it, and nothing is made up.
Script paths are relative to this skill's folder.

## 1. Intake

- Ask for the resume if none was given: PDF, DOCX or pasted text.

- Make the person's folder: `~/Documents/resume-enhancer/<first-last>/`, or
  `~/resume-enhancer/<first-last>/` when there is no Documents folder. Say the path. Never put
  their files inside a git repository.

- Save the file there as `original.<ext>` and extract the text to `original.txt`: for a PDF,
  `pdftotext -layout original.pdf original.txt`; for a DOCX on macOS,
  `textutil -convert txt original.docx`. If that doesn't work, ask them to paste the text.

- For a PDF, also run `python3 scripts/pdf_links.py original.pdf`. pdftotext drops link
  targets; this lists each link with its text. Keep them in `facts.md`.

- Bold, italics and layout don't carry over from the original. Rule 19 decides what is bold.

- Empty text (a scanned PDF): ask for the DOCX or pasted text. Don't guess at a scan.

## 2. Custom questions, one batch
Ask all five in one message, multiple choice where the tool supports it. The house style is
each default:
1. Section order. Default: Technical Skills, Experience, Projects, Involvements, Education.
2. Page length. Default 1; 2 for a long career.
3. Sections in or out. Default: no summary or objective. Offer Certifications, Awards or
   Publications when they have them. Drop any section they have nothing for.
4. Target role: a pasted posting, a role name, or none (default). It reorders skill lines and projects
   (rule 24).
5. Look: dense (default) or roomy (wider margins, more space between lines).

Write the answers at the top of `facts.md` under `## Preferences`. A preference beats the rule
it touches, and its rows in the change table say "your choice, overrides rule N".

## 3. Facts file
Write `facts.md` from the resume: contact items, every job, project, involvement, school, date
and number, as stated. It is their source of truth (rule 25). Nothing goes on the page that
isn't in it. Answers they give later go in here first.

## 4. Audit
Check every line against rules.md and the preferences, then write `changes.md`:

| # | Section | Type | Before | After | Rule |
|---|---|---|---|---|---|

- **Layout:** a section moved, added or dropped; a heading reformatted; dates normalized; a URL
  shown as text; bold and italics set by rule 19. A change that repeats across many lines (all
  the dates) can be one row.

- **Rewrite:** a bullet or skill line reworded: strong verb first, right tense, technology and
  numbers in bold, about 120 characters at most. The verb never claims more than the original:
  "Helped with X" becomes a verb for their part, or a Gap asking which part was theirs.

- **Cut:** a line dropped, with the reason: a section rule, or the page limit (weakest first).

- **Gap:** something only the person can answer: no result or scale, a vague date, a claim
  that looks inflated or unclear, projects with no link or date (one question for all of
  them). The After column holds the question.

- **fit:** a change made in step 7 to stop a wrapped bullet or fill a short line.

Never invent a number, team size, result, date, link or contact item. A guess is a Gap row, not
an edit.

## 5. Gap questions, one batch
Ask every Gap row's question in one message. Each answer goes into `facts.md`, then into the
bullet, and the row is updated. Anything unanswered stays as the person wrote it, with
nothing added.

## 6. Approval
Show `changes.md` and ask for the row numbers to reject, or "all good". Rejected rows keep the
original text. Nothing is rendered before this reply.

## 7. Build
1. Write `body.tex` with the approved changes, using the macros below.
2. `python3 scripts/fill_template.py body.tex resume.tex --look <dense|roomy>`
3. `bash scripts/render.sh resume.tex resume.pdf <1|2>`, then act on what it prints:

| render.sh prints | Do this |
|---|---|
| `OK` | Go on. |
| `FAIL: rendered N pages` | Run `fill_check.py` on the `-overflow.pdf` it names to see what spilled. Propose Cut rows for about that much, weakest lines first, get a yes, rebuild. Never shrink fonts, margins or macros to fit. |
| `missing LaTeX package: X.sty` | Give the install line for their system from [latex.md](latex.md) and stop. |
| `no LaTeX found` (exit 3) | Hand over `resume.tex` and `changes.md` with the online steps and the install line from [latex.md](latex.md). Say the page count is unchecked: if it compiles past the limit, they can come back for cuts. Stop. Install nothing yourself. |

4. `python3 scripts/fill_check.py resume.pdf`. Shorten every line flagged `<- wrapped bullet`.
   A bullet under 90% has room: add a true detail from `facts.md` if one fits, otherwise leave
   it. Never pad. Log each fix as a row of type `fit`.
5. `pdftotext -layout resume.pdf -` must read cleanly: sections in order, each heading on one
   line with its dates (rule 23).

## 8. Hand over
Read the PDF first: no wrapped bullet, the bottom margin close to the top one, no heading
running into its date. Then give them `resume.pdf` and the final `changes.md`.

## Body macros
```latex
\begin{center}
  \textbf{\Huge \scshape First Last} \\ \vspace{1pt}
  \small City $|$ 555-0100 $|$ \href{mailto:me@example.com}{\uline{me@example.com}} $|$
  \href{https://linkedin.com/in/me}{\uline{linkedin.com/in/me}}
\end{center}

\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Languages}{: Python, Java, SQL} \\
     \textbf{Tools}{: Git, Docker, Linux}
    }}
 \end{itemize}

\section{Experience}
  \resumeSubHeadingListStart
    \resumeJobHeading{\textbf{Title} $|$ \small\emph{Company, City}}{May 2025 -- Present}
      \resumeItemListStart
        \resumeItem{Built a \textbf{Python} service used by \textbf{\emph{500+}} staff}
      \resumeItemListEnd
  \resumeSubHeadingListEnd
```
Projects and involvements use `\resumeProjectHeading{...}{date}` with the same item block.
Education uses `\resumeSubheading{School}{City}{Program, Credential $|$ GPA}{dates}`.
Escape `& % $ # _` as `\& \% \$ \# \_`.

## Done when
The person has `resume.pdf` within their page limit with no wrapped bullet (or `resume.tex` plus
compile steps when they have no LaTeX), and an approved `changes.md` in which every row names
its rule and every fact on the page is in `facts.md`.
