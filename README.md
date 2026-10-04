# resume-enhancer

A skill that rebuilds a resume to a one-page house style. It shows every change, with the rule
behind it, before making it, and renders the result to PDF with LaTeX. It never adds a number,
date, link or claim the person didn't give.

| Skill | What it does |
|---|---|
| `resume-enhancer` | Asks a few setup questions, audits the resume against 28 rules, shows a change table to approve, then renders a one-page PDF. |

## How it works

1. You share a resume: PDF, DOCX or pasted text. Your files go in
   `~/Documents/resume-enhancer/<your-name>/`.
2. It asks five setup questions at once: section order, page length, sections in or out,
   target role, and dense or roomy look. The house style is the default for each.
3. It writes `facts.md`, everything your resume states. Nothing else goes on the page.
4. It audits every line against [the rules](skills/resume-enhancer/rules.md) and writes
   `changes.md`: each change, before and after, and the rule behind it. Anything only you can
   answer, like a missing number, becomes a question.
5. You reply with the rows to reject, or "all good".
6. It renders `resume.pdf` and checks that no bullet wraps and the page has no gaps.

## Install

### Claude Code

```
/plugin marketplace add S3yon/resume-enhancer
/plugin install resume-enhancer@resume-enhancer
```

The skills then show as `resume-enhancer:resume-enhancer`.

Checked against https://code.claude.com/docs/en/plugin-marketplaces, 2026-10-02.

### GitHub Copilot CLI

Reads the same plugin manifests as Claude Code.

```
copilot plugin marketplace add S3yon/resume-enhancer
copilot plugin install resume-enhancer@resume-enhancer
```

Or in one step: `copilot plugin install S3yon/resume-enhancer`.

Checked against https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference, 2026-10-02.

### Qwen Code

Reads the same marketplace file as Claude Code.

```
qwen extensions install S3yon/resume-enhancer:resume-enhancer
```

Checked against https://github.com/QwenLM/qwen-code/blob/main/docs/users/extension/introduction.md, 2026-10-02.

### Gemini CLI

Reads `gemini-extension.json` and loads `skills/`.

```
gemini extensions install https://github.com/S3yon/resume-enhancer
```

Checked against https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md, 2026-10-02.

### Codex

Reads the root `plugin.json` and finds `skills/` on its own.

```
codex plugin marketplace add S3yon/resume-enhancer
codex plugin add resume-enhancer@resume-enhancer
```

Checked against https://developers.openai.com/plugins/build/plugins, 2026-10-02.

### Cursor

Reads the root `plugin.json` and `.cursor-plugin/marketplace.json`. Open Customize, then
From GitHub Repository, and enter `S3yon/resume-enhancer`.

Checked against https://cursor.com/docs/plugins, 2026-10-02.

### Copy a folder

Copy one folder from `skills/` into the tool's skills folder:

| Tool | For your user | For one project |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex, Cursor, Gemini CLI, Copilot CLI | `~/.agents/skills/` | `.agents/skills/` |
| Qwen Code | `~/.qwen/skills/` | `.qwen/skills/` |

The manifests use the same formats as skill-kit. No install test was run in each tool.


## LaTeX

Rendering needs `pdflatex` and `pdftotext`. Without LaTeX the skill hands you `resume.tex`
with steps to compile it online. Install lines for macOS, Ubuntu/Debian and Windows, and the
online steps, are in [latex.md](skills/resume-enhancer/latex.md).

## Tests

```
python3 -m unittest discover tests -v
python3 scripts/validate.py
```

Tests that render skip when LaTeX isn't installed, so CI runs without it.

## License

MIT. The template is adapted from Jake's Resume (MIT); see [NOTICE](NOTICE).
