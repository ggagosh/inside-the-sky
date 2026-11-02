# Art pipeline

Status: agreed · Owner: ggagosh · Updated: 2026-11-02

Our painter works on paper and is also a developer on the team, so he runs this whole pipeline himself, with an agent's help if he wants it. This is how a painting becomes a game asset.

- **Painter's brief:** [painter-brief.html](painter-brief.html), also published as a shareable page at https://claude.ai/artifact/VLtcE2MYLmRaciGfVX5Qmi. The file in this repo is the source; republish the page after editing it.

## From paper to game

1. **Paint.** The painter follows the frame sizes in the brief and paints 1 cm past the frame.
2. **Digitize.** Scan at 600 dpi, or photograph as the brief describes. Originals arrive as files, not chat photos.
3. **Keep the originals** in the shared art folder (location TBD), never in git. They're large and we may need them again.
4. **Clean up:** crop to the frame, straighten, fix white balance and levels. For icons, remove the paper so the background is transparent. Any editor works (GIMP, Krita, Photopea), or a script.
5. **Export** a PNG in sRGB to `game/assets/art/<kind>/`, at the size and name below.
6. **Check in the game:** `mise run import`, then look at it with `mise run play`.
7. **Open a pull request** with the exported files (branch `art/<what>`, like `art/portrait-max`), so the other person can review it in the game before merging.

## Sizes and names

| Kind | Folder | Export size (px) | Example name |
|---|---|---|---|
| City map | `map/` | 3840 × 2160 | `map_capital.png` |
| Story scene | `scenes/` | 2560 × 1440 | `scene_01_pulse.png` |
| Portrait | `portraits/` | 1200 × 1600 | `portrait_max.png` |
| Icon | `icons/` | 256 × 256, transparent | `icon_money.png` |

- Names are lowercase English `snake_case`, with no spaces.
- When an asset is redone, keep the same file name so the game picks up the new version.
- At 600 dpi, every frame in the brief scans well above these sizes, so exports are always scaled down, never up.
