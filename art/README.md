# Drop paintings here

Put each scan or photo in the folder for its kind, named in English, lowercase:

| Folder | Example | Becomes |
|---|---|---|
| `raw/portraits/` | `max.jpg` | `game/assets/art/portraits/portrait_max.png` |
| `raw/scenes/` | `01_pulse.jpg` | `game/assets/art/scenes/scene_01_pulse.png` |
| `raw/map/` | `capital.jpg` | `game/assets/art/map/map_capital.png` |
| `raw/icons/` | `sheet-1.jpg` | one `icon_<name>.png` per drawing; list the names in `art.toml` |

Then run `mise run art`. The full pipeline is in [docs/art/README.md](../docs/art/README.md).
