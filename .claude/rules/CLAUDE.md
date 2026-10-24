# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Calculadora de Faltas (version 1.0): a Spanish-language Python CLI that tracks school attendance absences per subject (a vocational-cycle student's own project). No dependencies (stdlib only, Windows: uses `msvcrt`), build, lint or test setup; there is a `.venv` (gitignored-style, don't read it). Run with `python main.py` from a real terminal (arrow keys don't work in some IDE consoles).

## Read first: NORMAS.MD

`NORMAS.MD` (in Spanish) is the authoritative spec: attendance rules (max 20% absences per subject, per school year, measured against each subject's own total hours), UI requirements, per-action behaviour (añadir / consultar / modificar) and a "Funciones por añadir" section (startup 15% warning, new-school-year reset). Consult it before implementing or changing any feature. Key UI rules: lists paginated 5 at a time navigated with arrow keys (previous options erased on redraw), subjects shown as `N. Name`, absences shown as id + subject + justified (S/N), and "press enter to continue" after every action.

## Ownership convention

The author writes all program logic themself; **only the database code (`../../acciones/db_check.py` and DB calls) is meant to be written by Claude**. Code comments in the source (e.g. in `../../lista_asignaturas/asignaturas.py`) are often TODO instructions from the author to Claude. Don't rewrite the author's non-DB code unprompted.

## Architecture

- `../../main.py` → calls `comprobar_db()` (`acciones/db_check.py`) then `menu()`.
- `../../sistema/menu.py` → main loop; dispatches options 1/2/3 to `añadir`, `consultar`, `modificar` (in `acciones/`), 4 exits.
- `../../acciones/db_check.py` → only connects to (`conectar()`) or creates (`comprobar_db()`) the SQLite DB `faltas.db` (table `faltas`: id, asignatura, fecha AAAA-MM-DD, justificada 0/1, horas). SQL queries live in each action's own file, not here.
- `../../acciones` → only the program's own functions: `añadir`, `consultar`, `modificar` (+ `db_check`). No standalone helper scripts: each action does everything itself (ask the date, choose the subject, draw tables) with private `_functions` inside its own file, even if that duplicates a little code. Actions must not import `menu` (menu loops on its own).
- `../../lista_asignaturas/asignaturas.py` → `ASIGNATURAS` dict name → total hours (33/66/99/132) and `asignaturas()` accessor. Counts are per subject.

## Code rules (from NORMAS.MD)

- One script per action the user or program can do; any action needing the DB calls it from its own file via `conectar()`.
- Use `"{}".format(x)`, never f-strings.
- Every list shown (subjects, absences) is an ASCII table MySQL-CLI style (`+`, `-` and `|` borders), paginated 5 at a time with arrow keys, clearing the screen on each redraw.
- Validate all user input (numbers, dates, S/N) and re-ask instead of crashing.
- If NORMAS.MD changes, copy the new rules into this file; if a rule change contradicts how the program currently works, rework the program.
- Git commits must pass `-m` with a general summary of all changes made.

## Pending / known issues

- NORMAS.MD "Funciones por añadir" (startup 15% warning, new school year) are not implemented.
