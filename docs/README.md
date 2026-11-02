# How we write docs

Status: agreed · Owner: ggagosh · Updated: 2026-11-02

Docs here are read by teammates **and** by AI agents. Write so that someone with no context, human or agent, can act on the doc alone.

## Map

```
docs/
  README.md        this file
  decisions.md     why things are the way they are
  dev/
    workflow.md    how humans and agents work together, git
    conventions.md code layout, GDScript style, tests
  game/            game design, in layers (see game/README.md)
  art/             art pipeline, painter's brief
  templates/       starting point for every design doc
```

## Status line

Every doc starts with one line under its title:

```
Status: draft · Owner: <name> · Updated: YYYY-MM-DD
```

| Status | Meaning | Can we build from it? |
|---|---|---|
| `draft` | Being discussed | No. Ask first. |
| `agreed` | A human approved it | Yes |
| `implemented` | It's in the game; the doc describes what exists | Yes, it's the reference |
| `dropped` | Kept for history | No. Link to what replaced it. |

Only a human moves a doc to `agreed`.

## Rules

1. **Docs are the spec.** Code follows docs. When they disagree, fix one of them in the same change.
2. **One topic per file.** When a file grows past about two screens, split it.
3. **Use the templates** in [templates/](templates/). The same headings everywhere means people and agents know where to look.
4. **Be concrete.** Use numbers, examples and sample lines. If something is unknown, write `TBD` and add it to *Open questions*. Avoid vague words like "some", "balanced", "interesting".
5. **Number the rules** in system docs (R1, R2...). Tests reference those numbers, so each rule's test is easy to find.
6. **Link, don't copy.** Each fact lives in one place: names in [game/glossary.md](game/glossary.md), tuning numbers in `game/data/` once the data exists, decisions in [decisions.md](decisions.md).
7. **Diagrams in Mermaid**, inside the Markdown. GitHub renders them, and agents can read and edit them.
8. **Plain English.** Short sentences, present tense, written for a newcomer.
9. **Chat is not documentation.** When a conversation settles something, write it into a doc before anyone builds it.
10. **Log decisions.** Anything someone will later ask "why?" about goes into [decisions.md](decisions.md): what was decided, why, and what we chose against.
