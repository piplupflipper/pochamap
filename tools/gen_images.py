# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""layout/keymap.yaml から images/*.svg を生成する。

使い方（リポジトリのルートで実行）:
    uv run tools/gen_images.py
"""

from __future__ import annotations

import hashlib
import re
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "layout" / "keymap.yaml"
# 画像を埋め込んでいる Markdown。画像リンクの ?v= を更新する対象
DOCS = [ROOT / "README.md", ROOT / "docs" / "思想.md"]

U = 56  # 1u のピクセル数
GAP = 4  # キーとキーの隙間
PAD = 24  # 画像の外周の余白
HEADER = 0  # 画像の上端からキーまでの、外周の余白に足す高さ
LEGEND = 40  # 凡例の高さ

KIND_LABELS = {
    "remap": "置き換え",
    "combo": "Ctrl・Shift と押したときだけ変わる",
    "modifier": "修飾キー",
    "output": "押している間の出力",
    "ahk": "AHK の操作",
}

STYLE = """
.bg { fill: #ffffff; }
.key { fill: #f6f8fa; stroke: #c9d1d9; stroke-width: 1; }
.orig { fill: #8c959f; font-size: 11px; }
.orig-plain { fill: #57606a; font-size: 13px; }
.to { fill: #1f2328; font-size: 17px; font-weight: 700; }
.sub { fill: #1f2328; font-size: 9.5px; }
.legend-text { fill: #1f2328; font-size: 12px; }
.k-remap { fill: #ddf4ff; stroke: #54aeff; }
.k-combo { fill: #fbefff; stroke: #c297ff; }
.k-modifier { fill: #fff1c2; stroke: #d4a72c; }
.k-output { fill: #dafbe1; stroke: #4ac26b; }
.k-ahk { fill: #ffebe9; stroke: #ff8182; }
@media (prefers-color-scheme: dark) {
  .bg { fill: #0d1117; }
  .key { fill: #161b22; stroke: #3d444d; }
  .orig { fill: #9198a1; }
  .orig-plain { fill: #9198a1; }
  .to, .sub, .legend-text { fill: #e6edf3; }
  .k-remap { fill: #0c2d6b; stroke: #388bfd; }
  .k-combo { fill: #3c1e70; stroke: #a371f7; }
  .k-modifier { fill: #4b3800; stroke: #bb8009; }
  .k-output { fill: #033a16; stroke: #2ea043; }
  .k-ahk { fill: #67060c; stroke: #f85149; }
}
text { font-family: "BIZ UDPGothic", "Noto Sans CJK JP", "Hiragino Sans", "Yu Gothic UI", "Meiryo", sans-serif; }
"""


def layout_keys(keyboard: dict) -> list[dict]:
    """行ごとの定義を、x と y を確定したキーの一覧にする。"""
    keys = []
    for row in keyboard["rows"]:
        cursor = 0.0
        for k in row["keys"]:
            x = k.get("x", cursor)
            w = k.get("w", 1.0)
            keys.append({**k, "x": x, "y": row["y"], "w": w})
            cursor = x + w
    return keys


def key_shape(k: dict, cls: str) -> str:
    x0 = PAD + k["x"] * U + GAP / 2
    y0 = PAD + HEADER + k["y"] * U + GAP / 2
    w = k["w"] * U - GAP
    if k.get("shape") == "enter":
        # 上段が w、下段が w2 の逆 L 字（右端を揃える）
        w2 = k["w2"] * U - GAP
        x1 = x0 + w
        xl = x1 - w2
        y1 = y0 + U - GAP
        y2 = y0 + 2 * U - GAP
        d = f"M{x0},{y0} H{x1} V{y2} H{xl} V{y1} H{x0} Z"
        return f'<path class="key {cls}" d="{d}" stroke-linejoin="round"/>'
    h = U - GAP
    return f'<rect class="key {cls}" x="{x0}" y="{y0}" width="{w}" height="{h}" rx="6"/>'


def text_width(text: str, size: float) -> float:
    """文字幅の概算。全角は size、半角は size の 0.6 倍とみなす。"""
    return sum(size if ord(c) > 0x2E7F else size * 0.6 for c in text)


def fit(text: str, size: float, max_w: float) -> str:
    """概算の幅が max_w を超えるなら、textLength で横に縮めて収める。"""
    if text_width(text, size) <= max_w:
        return ""
    return f' textLength="{max_w:.1f}" lengthAdjust="spacingAndGlyphs"'


def key_texts(k: dict, m: dict | None) -> str:
    x0 = PAD + k["x"] * U + GAP / 2
    y0 = PAD + HEADER + k["y"] * U + GAP / 2
    # 文字は上段（Enter なら上段の矩形）の中に置く
    cx = x0 + (k["w"] * U - GAP) / 2
    label = escape(k["label"])
    if m is None:
        return f'<text class="orig-plain" x="{cx}" y="{y0 + (U - GAP) / 2 + 5}" text-anchor="middle">{label}</text>'
    out = [f'<text class="orig" x="{x0 + 5}" y="{y0 + 13}">{label}</text>']
    to = escape(str(m["to"]))
    sub = m.get("sub")
    to_y = y0 + (U - GAP) / 2 + (4 if sub else 9)
    max_w = k["w"] * U - GAP - 6
    size = "" if len(str(m["to"])) <= 4 else ' style="font-size:13px"'
    adj = fit(str(m["to"]), 17 if not size else 13, max_w)
    out.append(f'<text class="to" x="{cx}" y="{to_y}" text-anchor="middle"{size}{adj}>{to}</text>')
    if sub:
        adj = fit(sub, 9.5, max_w)
        out.append(
            f'<text class="sub" x="{cx}" y="{y0 + U - GAP - 6}" text-anchor="middle"{adj}>{escape(sub)}</text>'
        )
    return "".join(out)


def legend(kinds: list[str], y: float) -> str:
    parts = []
    x = PAD
    for kind in kinds:
        parts.append(f'<rect class="key k-{kind}" x="{x}" y="{y}" width="16" height="16" rx="3"/>')
        text = KIND_LABELS[kind]
        parts.append(f'<text class="legend-text" x="{x + 22}" y="{y + 13}">{escape(text)}</text>')
        x += 22 + text_width(text, 12) + 24
    return "".join(parts)


def render(keyboard: dict, keys: list[dict], layer: dict) -> str:
    width_u = max(k["x"] + k["w"] for k in keys)
    height_u = max(k["y"] + 1 for k in keys)
    width = PAD * 2 + width_u * U
    height = PAD * 2 + HEADER + height_u * U + LEGEND
    mapping = layer["keys"]
    unknown = set(mapping) - {k["id"] for k in keys}
    if unknown:
        raise SystemExit(f"{layer['id']}: 配列に無いキー id があります: {sorted(unknown)}")

    body = []
    for k in keys:
        m = mapping.get(k["id"])
        cls = f"k-{m['kind']}" if m else ""
        body.append(key_shape(k, cls))
        body.append(key_texts(k, m))

    kinds = [kind for kind in KIND_LABELS if any(v["kind"] == kind for v in mapping.values())]
    title = escape(layer["title"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="{title}">'
        f"<style>{STYLE}</style>"
        f'<rect class="bg" width="100%" height="100%" rx="12"/>'
        + "".join(body)
        + legend(kinds, PAD + HEADER + height_u * U + 16)
        + "</svg>\n"
    )


def main() -> None:
    data = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    keyboard = data["keyboard"]
    keys = layout_keys(keyboard)
    for layer in data["layers"]:
        out = ROOT / layer["file"]
        out.parent.mkdir(parents=True, exist_ok=True)
        svg = render(keyboard, keys, layer)
        out.write_text(svg, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")
        bust_readme_cache(layer["file"], svg)


def bust_readme_cache(path: str, svg: str) -> None:
    """画像を埋め込んでいる Markdown の画像リンクに、内容のハッシュを ?v= で付ける。

    GitHub の README は画像のキャッシュが残り、更新しても古い画像を表示することがあるため、
    画像が変わるたびに URL を変えてキャッシュを避ける。
    """
    digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()[:8]
    pattern = re.compile(re.escape(path) + r"(\?v=[0-9a-f]+)?\)")
    for doc in DOCS:
        text = doc.read_text(encoding="utf-8")
        new = pattern.sub(f"{path}?v={digest})", text)
        if new != text:
            doc.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
