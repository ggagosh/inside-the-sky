# Decisions

Status: agreed · Owner: ggagosh · Updated: 2026-11-02

Newest at the top. Each entry says what we decided, why, and what we chose against. To change a decision, add a new entry that points to the old one; don't edit history.

### 2026-11-02 · Raw scans live in git, converted by a script
**Decision:** original scans and photos go in `art/raw/` as JPEGs at 300 dpi. `mise run art` (`tools/art.py`, OpenCV) converts them into game assets. This replaces "No Git LFS yet" below, which kept raw scans outside git.
**Why:** an A4 scan at 300 dpi is about 2–4 MB, and the whole MVP is roughly 100 MB, which plain git handles fine. Keeping originals next to the exports means anyone can redo a conversion, and the painter needs nothing but git.
**Instead of:** a shared drive outside git; Git LFS (unnecessary at this size); cleaning up each scan by hand in an image editor.

### 2026-11-02 · Simulation separate from UI
**Decision:** game rules, state and AI live in `game/core/` with no Nodes; the UI only reads state and sends commands.
**Why:** headless tests, AI-vs-AI balance simulations, and simple save/load.
**Instead of:** logic inside scene scripts, the Godot default.

### 2026-11-02 · Tiny built-in test runner
**Decision:** `game/tests/run.gd`, about 50 lines, no addon.
**Why:** enough for rule tests; nothing extra to install or update.
**Instead of:** GUT or gdUnit4. Switch when we need mocks, fixtures or reports.

### 2026-11-02 · No Git LFS yet
**Decision:** commit only exported art (PNG at game size). Raw scans stay outside git.
**Why:** exported assets are small; LFS adds setup for every contributor and has a storage quota.
**Instead of:** LFS from day one. Revisit when exported assets pass ~500 MB.

### 2026-11-02 · Art painted on paper
**Decision:** our painter works on paper only. We scan or photograph the work, then clean it up and import it. The brief is in [art/painter-brief.html](art/painter-brief.html).
**Why:** that's how the painter works best, and the textured, hand-made look fits the game.
**Instead of:** digital painting.

### 2026-11-02 · PC first, English text, Compatibility renderer
**Decision:** mouse and keyboard, 1920×1080 landscape. Game text in English. Godot's Compatibility renderer.
**Why:** strategy UIs are easiest to design for a big screen. The Compatibility renderer covers 2D fully, runs on old hardware and keeps a web export possible.
**Instead of:** mobile first; the Forward+ renderer.

### 2026-11-02 · Turn-based strategy with illustrated story events
**Decision:** the player leads the underground across a city map, one turn per day, with story told through illustrated event cards.
**Why:** it plays to the painter's strengths (still paintings, no animation), the scope is smaller, the tower network becomes the core mechanic, and the AI can be tested with simulations.
**Instead of:** a side-view story RPG following Max (the first plan).

### 2026-11-02 · Inspired by the novel, with our own names
**Decision:** our own names, places and designs, listed in [game/glossary.md](game/glossary.md).
**Why:** the novel is still under copyright, so this keeps the option to publish.
**Instead of:** a direct adaptation.

### 2026-11-01 · Godot 4.7 and GDScript, tools through mise
**Decision:** Godot 4.7.2, with GDScript. Every tool is pinned in `mise.toml`.
**Why:** scenes and scripts are plain text that agents can read and edit; headless CLI for tests; free, small and open source. mise gives everyone the same tool versions.
**Instead of:** Unity, a web engine (Phaser), Homebrew installs.
