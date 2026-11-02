# /// script
# requires-python = ">=3.12"
# dependencies = ["opencv-python-headless>=5,<6", "numpy>=2,<3"]
# ///
"""Turn scans and photos of paintings in art/raw/ into game assets in game/assets/art/.

    mise run art                  convert everything in art/raw/
    mise run art -- <file> ...    convert only these files
    mise run art -- --self-test   check the pipeline on generated images

For every file it also writes art/.preview/<same path>.jpg with the detected outline drawn in,
so a person or an agent can check the crop. See docs/art/README.md.
"""

import sys
import tempfile
import tomllib
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "art" / "raw"
OUT = ROOT / "game" / "assets" / "art"
PREVIEW = ROOT / "art" / ".preview"
OVERRIDES = ROOT / "art" / "art.toml"
IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

# Folder in art/raw/ -> (file prefix, export size px, pencil frame cm, bleed cm). Same as docs/art/README.md.
KINDS = {
    "map": ("map", (3840, 2160), (40.0, 22.5), 1.0),
    "scenes": ("scene", (2560, 1440), (25.0, 14.0), 1.0),
    "portraits": ("portrait", (1200, 1600), (15.0, 20.0), 1.0),
    "icons": ("icon", (256, 256), None, 0.0),
}


def white_balance(img):
    """Scale each channel so the paper (median color of the image border) becomes white."""
    b = max(4, min(img.shape[:2]) // 40)
    border = np.concatenate([img[:b], img[-b:], img[:, :b].swapaxes(0, 1), img[:, -b:].swapaxes(0, 1)], axis=1)
    paper = np.median(border.reshape(-1, 3), axis=0)
    return np.clip(img.astype(np.float32) * (255.0 / np.maximum(paper, 1)), 0, 255).astype(np.uint8)


def paint_mask(img):
    """255 where the white-balanced image is noticeably not paper."""
    return np.where(255 - img.min(axis=2) > 40, 255, 0).astype(np.uint8)


def order(pts):
    """Sort 4 points as top-left, top-right, bottom-right, bottom-left."""
    s, d = pts.sum(axis=1), np.diff(pts, axis=1).ravel()
    return np.float32([pts[s.argmin()], pts[d.argmin()], pts[s.argmax()], pts[d.argmax()]])


def find_quad(img):
    """Corners of the largest painted area, in source pixels."""
    scale = min(1.0, 1500 / max(img.shape[:2]))
    small = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    kernel = np.ones((15, 15), np.uint8)
    mask = cv2.morphologyEx(paint_mask(small), cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("no painted area found")
    hull = cv2.convexHull(max(contours, key=cv2.contourArea))
    quad = cv2.approxPolyDP(hull, 0.02 * cv2.arcLength(hull, True), True)
    if len(quad) != 4:  # ragged edges: fall back to the tightest rotated rectangle
        quad = cv2.boxPoints(cv2.minAreaRect(hull))
    return order(np.float32(quad).reshape(4, 2) / scale)


def flatten(img, quad, size, frame, bleed):
    """Straighten the painted area, cut off the bleed past the pencil frame, resize to `size`."""
    w = int(max(np.linalg.norm(quad[1] - quad[0]), np.linalg.norm(quad[2] - quad[3])))
    h = int(max(np.linalg.norm(quad[3] - quad[0]), np.linalg.norm(quad[2] - quad[1])))
    if (w > h) != (size[0] > size[1]):
        raise ValueError("the painting looks rotated by 90°; save the file upright and run again")
    target = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    flat = cv2.warpPerspective(img, cv2.getPerspectiveTransform(quad, target), (w, h), flags=cv2.INTER_CUBIC)
    bx = int(w * bleed / (frame[0] + 2 * bleed))
    by = int(h * bleed / (frame[1] + 2 * bleed))
    flat = flat[by : h - by, bx : w - bx]
    if flat.shape[1] < size[0] or flat.shape[0] < size[1]:
        print(f"      warning: only {flat.shape[1]}x{flat.shape[0]} px of painting; scan at 300 dpi or more")
    return cv2.resize(flat, size, interpolation=cv2.INTER_AREA)


def split_icons(img, count):
    """Find `count` ink drawings on a sheet. Returns their boxes (x, y, w, h) in reading order."""
    gap = max(img.shape[:2]) // 30  # strokes closer than ~1 cm on an A4 sheet belong to one icon
    merged = cv2.dilate(paint_mask(img), np.ones((gap, gap), np.uint8))
    n, _, stats, _ = cv2.connectedComponentsWithStats(merged)
    min_area = img.shape[0] * img.shape[1] * 0.001
    boxes = [tuple(int(v) for v in stats[i, :4]) for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > min_area]
    if len(boxes) != count:
        raise ValueError(f"found {len(boxes)} drawings but art/art.toml lists {count} names")
    boxes.sort(key=lambda b: b[1] + b[3] / 2)
    rows, tolerance = [], float(np.median([b[3] for b in boxes])) / 2
    for box in boxes:
        center = box[1] + box[3] / 2
        if rows and abs(center - rows[-1][0]) < tolerance:
            rows[-1][1].append(box)
        else:
            rows.append((center, [box]))
    return [box for _, row in rows for box in sorted(row)]


def icon_rgba(img, box, size):
    """Square crop around one drawing; the paper becomes transparent."""
    x, y, w, h = box
    side = int(max(w, h) * 1.15)
    pad = side
    padded = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    cx, cy = x + w // 2 + pad, y + h // 2 + pad
    crop = padded[cy - side // 2 : cy - side // 2 + side, cx - side // 2 : cx - side // 2 + side]
    crop = cv2.resize(crop, size, interpolation=cv2.INTER_AREA).astype(np.float32)
    alpha = np.clip((255 - crop.min(axis=2) - 25) / (180 - 25), 0, 1)
    # Un-mix the white paper from semi-transparent edges, so icons don't get a light halo on dark UI.
    color = np.where(alpha[..., None] > 0, (crop - (1 - alpha[..., None]) * 255) / np.maximum(alpha[..., None], 1e-3), 0)
    return np.dstack([np.clip(color, 0, 255), alpha * 255]).astype(np.uint8)


def save_preview(img, rel, quad=None, boxes=()):
    scale = min(1.0, 1200 / max(img.shape[:2]))
    small = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    if quad is not None:
        cv2.polylines(small, [np.int32(quad * scale)], True, (0, 0, 255), 3)
    for x, y, w, h in boxes:
        cv2.rectangle(small, (int(x * scale), int(y * scale)), (int((x + w) * scale), int((y + h) * scale)), (0, 0, 255), 3)
    path = (PREVIEW / rel).with_suffix(".jpg")
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), small)


def convert(path, overrides):
    """Convert one raw file. Returns the written asset paths."""
    rel = path.relative_to(RAW)
    kind = rel.parts[0] if len(rel.parts) == 2 else None
    if kind not in KINDS:
        raise ValueError(f"put it in art/raw/<{'|'.join(KINDS)}>/")
    prefix, size, frame, bleed = KINDS[kind]
    options = overrides.get(rel.as_posix(), {})
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("not an image OpenCV can read")
    img = white_balance(img)
    (OUT / kind).mkdir(parents=True, exist_ok=True)
    if kind == "icons":
        names = options.get("names")
        if not names:
            raise ValueError(f'list the icons left-to-right, top-to-bottom in art/art.toml under ["{rel.as_posix()}"] names = [...]')
        boxes = split_icons(img, len(names))
        save_preview(img, rel, boxes=boxes)
        written = []
        for name, box in zip(names, boxes):
            out = OUT / kind / f"{prefix}_{name}.png"
            cv2.imwrite(str(out), icon_rgba(img, box, size))
            written.append(out)
        return written
    quad = order(np.float32(options["corners"])) if "corners" in options else find_quad(img)
    save_preview(img, rel, quad=quad)
    out = OUT / kind / f"{prefix}_{path.stem}.png"
    cv2.imwrite(str(out), flatten(img, quad, size, frame, bleed))
    return [out]


def self_test():
    """Generated 'photos' with known answers: a skewed, tinted painting and an icon sheet."""
    paper = (205, 215, 225)  # BGR: bluish, like a photo under daylight
    photo = np.full((2600, 2000, 3), paper, np.uint8)
    corners = np.int32([[300, 250], [1650, 300], [1700, 2350], [250, 2300]])
    cv2.fillPoly(photo, [corners], (90, 100, 110))
    balanced = white_balance(photo)
    assert balanced[5, 5].tolist() == [255, 255, 255], "paper should become white"
    quad = find_quad(balanced)
    assert np.abs(quad - corners).max() < 15, f"corners off: {quad.tolist()}"
    portrait = flatten(balanced, quad, (1200, 1600), (15.0, 20.0), 1.0)
    assert portrait.shape == (1600, 1200, 3)
    assert portrait[[0, -1]].max() < 200 and portrait[:, [0, -1]].max() < 200, "no paper may remain at the edges"

    sheet = np.full((3508, 2480, 3), (235, 238, 240), np.uint8)
    cv2.circle(sheet, (450, 500), 60, (20, 20, 20), -1)  # icon "a": two blobs close together
    cv2.circle(sheet, (580, 500), 60, (20, 20, 20), -1)
    cv2.rectangle(sheet, (1400, 350), (1700, 650), (20, 20, 20), -1)  # icon "b"
    cv2.fillPoly(sheet, [np.int32([[900, 1400], [1100, 1700], [700, 1700]])], (20, 20, 20))  # icon "c"
    sheet = white_balance(sheet)
    boxes = split_icons(sheet, 3)
    assert [b[0] < 1000 and b[1] < 1000 for b in boxes] == [True, False, False], f"wrong order: {boxes}"
    icon = icon_rgba(sheet, boxes[1], (256, 256))
    assert icon.shape == (256, 256, 4) and icon[0, 0, 3] == 0 and icon[128, 128, 3] > 200, "paper clear, ink solid"

    with tempfile.TemporaryDirectory() as tmp:  # file round trip, so imwrite/imread paths are exercised too
        cv2.imwrite(f"{tmp}/icon.png", icon)
        assert cv2.imread(f"{tmp}/icon.png", cv2.IMREAD_UNCHANGED).shape == (256, 256, 4)
    print("art self-test passed")
    return 0


def main(args):
    if args == ["--self-test"]:
        return self_test()
    overrides = tomllib.loads(OVERRIDES.read_text()) if OVERRIDES.exists() else {}
    files = [Path(a).resolve() for a in args] or sorted(p for p in RAW.rglob("*") if p.suffix.lower() in IMAGE_TYPES)
    if not files:
        print("nothing in art/raw/ yet")
    failed = 0
    for path in files:
        rel = path.relative_to(ROOT)
        try:
            outs = convert(path, overrides)
            print(f"ok    {rel} -> {', '.join(str(o.relative_to(ROOT)) for o in outs)}")
        except Exception as err:  # report every bad file, keep converting the rest
            failed += 1
            print(f"FAIL  {rel}: {err}")
    if files:
        print("\nCheck the crops in art/.preview/, then run `mise run import`.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
