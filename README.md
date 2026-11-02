# Inside the Sky

A turn-based strategy game for PC. You lead a secret underground in a grey city where radio towers broadcast loyalty twice a day.

Built with Godot 4.7 and GDScript. The project is **AI-native**: humans decide what the game is, AI agents draft and build, and the docs in this repo are the spec both work from.

> Inspired by the Strugatsky brothers' novel *The Inhabited Island*. All names, places and designs are our own.

## Quick start

1. Ask ggagosh to add you to the GitHub repo, then `gh repo clone ggagosh/inside-the-sky`.
2. Install [mise](https://mise.jdx.dev/getting-started.html).
3. In the repo folder, run `mise install`. It installs the pinned Godot, uv and gdtoolkit versions.
4. Check that `mise run check` passes. On Linux, if `godot` isn't found, see the note in `.github/workflows/ci.yml`; it's a known mise issue with one-line fix.
5. Then:

| Command | What it does |
|---|---|
| `mise run edit` | Open the project in the Godot editor |
| `mise run play` | Run the game |
| `mise run check` | Lint and tests, the same as CI |
| `mise run fmt` | Format all GDScript |

## Repo layout

```
CLAUDE.md          instructions for AI agents (AGENTS.md points here)
mise.toml          pinned tools and project commands
docs/
  README.md        how docs are organized and written
  decisions.md     log of decisions and why
  dev/             workflow, code conventions
  game/            game design docs: vision, world, systems, content, chapters
  art/             art pipeline and the painter's brief
  templates/       templates for every kind of design doc
game/              the Godot project
  core/            simulation: rules, state, AI (no nodes)
  ui/              scenes and screens
  data/            content and tuning numbers
  assets/          art, audio, fonts
  tests/           headless tests
```

## Where to read next

- [docs/README.md](docs/README.md): how we write docs
- [docs/dev/workflow.md](docs/dev/workflow.md): how humans and agents work together
- [docs/dev/conventions.md](docs/dev/conventions.md): code structure, style, tests
- [docs/game/README.md](docs/game/README.md): how the game is documented, layer by layer
- [docs/art/README.md](docs/art/README.md): from paper paintings to game assets

## Tools

| Tool | Why |
|---|---|
| [mise](https://mise.jdx.dev) | Installs every tool below at the version pinned in `mise.toml`, and runs project commands |
| Godot 4.7.2 | Game engine |
| gdtoolkit (`gdformat`, `gdlint`) | GDScript formatter and linter, installed through uv |
| git + [gh](https://cli.github.com) | Version control and GitHub from the terminal |
| Claude Code (or another coding agent) | Drafts docs, writes code and tests. Reads `CLAUDE.md`. |
| A scanner or phone, GIMP or Krita | Art arrives as paintings on paper; see [docs/art](docs/art/README.md) |
