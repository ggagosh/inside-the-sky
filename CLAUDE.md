# Inside the Sky: instructions for AI agents

Turn-based strategy game for PC, Godot 4.7, GDScript, English text. The player leads an underground in a city ruled through mind-control towers. Inspired by the Strugatskys' *The Inhabited Island*, with our own names.

## Commands

- `mise run check`: lint and tests. Run it before saying any code change is done.
- `mise run test`: headless tests only. `mise run fmt`: format GDScript.
- `mise run play` / `mise run edit`: run the game / open the editor (they open a window; the user runs these).

## Read before working

- `docs/README.md`: how docs work and the status rules
- `docs/dev/workflow.md`: the build loop and git rules
- `docs/dev/conventions.md`: code layout, style, tests
- The design docs for the feature you're touching, under `docs/game/`

## Rules

- **Docs are the spec.** Build only from docs with `Status: agreed`. If the doc is `draft`, missing, or unclear, ask before writing code.
- **Docs and code change together.** If the implementation had to differ from the doc, update the doc in the same change.
- **Chat is not documentation.** When a conversation settles a design question, write it into the right doc (use `docs/templates/`), and log real decisions in `docs/decisions.md`.
- **Core never touches UI.** Game rules, state and AI live in `game/core/` as plain classes with no Nodes, so they run headless.
- **Every rule gets a test.** System docs number their rules (R1, R2...); name tests after them (`test_r2_...`). A bug fix starts with a failing test.
- **Tuning numbers live in `game/data/`**, not scattered as constants in code.
- **Names:** never use the novel's original names in game text, code or assets (Maxim, Gai, Saraksh, Unknown Fathers, etc.). Use `docs/game/glossary.md`.
- **Art:** paintings arrive in `art/raw/<kind>/`; `mise run art` turns them into `game/assets/art/`. Never edit the exported PNGs by hand; fix the conversion (`art/art.toml` or `tools/art.py`) and re-run it. To check a crop, look at the image in `art/.preview/`.
- **Don't touch** `game/.godot/` (generated). Change `docs/art/painter-brief.html` only when asked; it's the painter's working brief and is also published as a shared page.
- **Two humans work here** (see `docs/dev/workflow.md`). Work on a branch, never on `main`, and don't rewrite or force-push someone else's branch.
- Commit, push or open PRs only when the user asks.
