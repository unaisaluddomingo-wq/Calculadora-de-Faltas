# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Calculadora de Faltas: a Spanish-language Python CLI that tracks school attendance absences per subject (a vocational-cycle student's own project). No dependencies, build, lint or test setup; there is a `.venv` (gitignored-style, don't read it). Run with `python main.py`.

## Read first: NORMAS.MD

`NORMAS.MD` (in Spanish) is the authoritative spec: attendance rules (max 20% absences per subject, per school year, measured against each subject's own total hours), UI requirements, per-action behaviour (añadir / consultar / modificar) and a "Funciones por añadir" section (startup 15% warning, new-school-year reset). Consult it before implementing or changing any feature. Key UI rules: lists paginated 5 at a time navigated with arrow keys (previous options erased on redraw), subjects shown as `N. Name`, absences shown as id + subject + justified (S/N), and "press enter to continue" after every action.

## Ownership convention

The author writes all program logic themself; **only the database code (`acciones/db_check.py` and DB calls) is meant to be written by Claude**. Code comments in the source (e.g. in `asignaturas.py`) are often TODO instructions from the author to Claude. Don't rewrite the author's non-DB code unprompted.

## Architecture

- `main.py` → calls `comprobar_db()` (`acciones/db_check.py`) then `menu()`.
- `menu.py` → main loop; dispatches options 1/2/3 to `añadir`, `consultar`, `modificar` (in `acciones/`), 4 exits.
- `acciones/db_check.py` → only connects to (`conectar()`) or creates (`comprobar_db()`) the SQLite DB `faltas.db` (table `faltas`: id, asignatura, fecha AAAA-MM-DD, justificada 0/1, horas). SQL queries live in each action's own file, not here.
- `acciones/` → one script per action (`añadir`, `consultar`, `modificar`, plus helpers `elegir_asignatura`, `pedir_fecha`). Actions must not import `menu` (menu loops on its own).
- `asignaturas.py` → `ASIGNATURAS` dict name → total hours (33/66/99/132) and `asignaturas()` accessor. Counts are per subject.

## Code rules (from NORMAS.MD)

- One script per action the user or program can do; any action needing the DB calls it from its own file via `conectar()`.
- Use `"{}".format(x)`, never f-strings.
- If NORMAS.MD changes, copy the new rules into this file; if a rule change contradicts how the program currently works, rework the program.
- Git commits must pass `-m` with a general summary of all changes made.

## Pending / known issues

- Arrow-key pagination (5 at a time, erasing the previous page) required by NORMAS.MD is not implemented; lists are shown in full.
- `menu.py`'s inner `while "1" or ...` is always true, so the "Opcion incorrecta" message is never reached.
- NORMAS.MD "Funciones por añadir" (startup 15% warning, new school year) are not implemented.
