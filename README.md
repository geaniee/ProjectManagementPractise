# Study & Revision Playbook

Interactive React + TypeScript + CSS study dashboard, based on the supplied PDF materials. Source PDFs are included under `public/sources`.

## Run locally

Install Node.js 18+ then run:

```bash
npm install
npm run dev
```

Open the localhost address displayed by Vite (usually http://localhost:5173).

Production build: `npm run build` then `npm run preview`.

**Use `npm install` for the first installation**. `npm ci` requires an existing `package-lock.json`.

## What is implemented

- Separate CEG1013 and BAC3002 source groups
- Week/topic selection and exact topic-level question counts, with insufficient-bank warnings
- Difficulty and question-format filters
- One-at-a-time quizzes, single/multiple/true-false answer submission, immediate feedback, explanations, hints and PDF page links
- Per-topic and per-week progress, quiz history and reset, persisted in localStorage
- Source-linked, expandable extracted notes and practice-topic shortcuts
- Light/dark theme and responsive layout

## Source fidelity and limitations

- `src/content.json` contains **short extracted source previews** (not complete lecture notes). Consult the linked original PDFs for full context.
- `src/questions.json` contains **automatically composed source-extract recognition questions**, not a human-vetted university examination bank. They are clearly marked as generated practice. Distractors are extracts from other sections of the same uploaded PDF; these questions test recognition more than deep application. No original tutorial question is represented as an original exam item.
- Question counts are not silently changed. When filters or wrong-answer mode reduce the available bank, the builder shows the shortfall and disables quiz start.
- No tutorial solutions were present in the provided source directory. Week 3 Agentic Payments is assigned to BAC3002 separately.
- To expand content, add records in `src/content.json` and `src/questions.json`, and add PDFs to `public/sources`. The source IDs and topic IDs must match.
- The `make_questions.py` script can regenerate recognition questions from source preview data. It does not create sophisticated scenario questions or verify whether an extracted passage contains a complete definition.
