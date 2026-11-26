#!/usr/bin/env python3
"""Rebuild the fifteen 32×32 character sprites. Standard library only; weapons stay separate.

Usage: python3 tools/build-sprites.py [--preview /tmp/doomsday-sprites.png]
The optional contact sheet shows dark/light backgrounds and a 36px size check.
"""

import argparse
from html import escape
import json
from pathlib import Path
import struct
import zlib

SIZE = 32
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "mods/doomsday-agents/sprites/doomsday"
INK = "#11151f"


class Sprite:
    def __init__(self, title, palette):
        self.title = title
        self.palette = {"K": INK, **palette}
        self.pixels = [[None] * SIZE for _ in range(SIZE)]

    def rect(self, x, y, w, h, color):
        assert color in self.palette, (self.title, color)
        assert 0 <= x < x + w <= SIZE and 0 <= y < y + h <= SIZE
        for row in self.pixels[y:y + h]:
            row[x:x + w] = [self.palette[color]] * w

    def stamp(self, x, y, rows):
        for dy, row in enumerate(rows):
            for dx, color in enumerate(row):
                if color != ".":
                    self.rect(x + dx, y + dy, 1, 1, color)

    def mirror(self, x, y, rows):
        """Stamp each left half and reflect it about the shared x=16 axis."""
        for dy, row in enumerate(rows):
            assert x + len(row) == 16, (self.title, dy, len(row))
            self.stamp(x, y + dy, [row + row[::-1]])

    def svg(self):
        # Merge adjacent pixels, keeping integer coordinates and no smoothing.
        lines = [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" '
            'width="36" height="36" shape-rendering="crispEdges">',
            f"  <title>{escape(self.title)} — pixel art</title>",
        ]
        for y, row in enumerate(self.pixels):
            x = 0
            while x < SIZE:
                color = row[x]
                end = x + 1
                while end < SIZE and row[end] == color:
                    end += 1
                if color:
                    lines.append(f'  <rect x="{x}" y="{y}" width="{end - x}" '
                                 f'height="1" fill="{color}"/>')
                x = end
        return "\n".join([*lines, "</svg>", ""])


# Original cast: one shared chibi body, then each hero's own costume, head and emblem.
BASE = {"F": "#e4a878", "s": "#b87555", "W": "#f4f1e6"}


def box(p, x, y, w, h, fill):
    p.rect(x, y, w, h, "K")
    p.rect(x + 1, y + 1, w - 2, h - 2, fill)


def body(title, palette, cape=False, head=True):
    p = Sprite(title, {**BASE, **palette})
    if cape:
        box(p, 6, 14, 20, 17, "C")
        p.rect(7, 15, 2, 15, "c")
        p.rect(23, 15, 2, 15, "c")
    box(p, 6, 16, 5, 10, "A")
    box(p, 21, 16, 5, 10, "A")
    p.rect(7, 17, 1, 7, "a")
    p.rect(7, 24, 3, 1, "F")
    p.rect(22, 24, 3, 1, "F")
    box(p, 10, 24, 6, 7, "L")
    box(p, 16, 24, 6, 7, "L")
    p.rect(11, 28, 4, 2, "B")
    p.rect(17, 28, 4, 2, "B")
    box(p, 9, 15, 14, 11, "A")
    p.rect(10, 16, 2, 8, "a")
    p.rect(10, 23, 12, 1, "T")
    if head:
        box(p, 10, 3, 12, 12, "F")
        p.rect(11, 4, 1, 9, "s")
        p.rect(13, 9, 2, 2, "K")
        p.rect(18, 9, 2, 2, "K")
        p.rect(13, 9, 1, 1, "W")
        p.rect(18, 9, 1, 1, "W")
        p.rect(15, 12, 3, 1, "s")
    return p


def hair(p, rows, x=10, y=2):
    p.stamp(x, y, rows)


def meridian():
    # Teal field captain with a gold sunrise emblem and swept dark hair.
    p = body("Captain Meridian", {"A": "#2f8f8a", "a": "#1f6a66", "T": "#d9b24a", "L": "#24524f",
                                  "B": "#d9dccf", "H": "#3b2a22", "h": "#5e4232", "G": "#f2c95b"})
    hair(p, ["..KKKKKKKK..", ".KHHHhhHHHK.", "KHHhHHHHHHHK", "KHHHHHHHHhHK", "KH........HK"])
    p.stamp(13, 17, ["..GG..", ".GGGG.", "GGGGGG", "TTTTTT"])
    p.rect(9, 15, 14, 1, "T")
    return p


def umbra():
    # Obsidian tyrant: horned gold crown, violet glare, long violet cape.
    p = body("King Umbra", {"A": "#2a2433", "a": "#1a1622", "T": "#c9a24a", "L": "#1f1a28",
                            "B": "#3a3247", "C": "#4b2a6b", "c": "#2f1a45", "E": "#c48bff",
                            "G": "#e0bd5c", "M": "#3a3247"}, cape=True)
    p.rect(11, 4, 10, 10, "M")
    p.rect(12, 9, 3, 1, "E")
    p.rect(17, 9, 3, 1, "E")
    p.rect(13, 12, 6, 1, "a")
    p.stamp(8, 0, ["K..........K..", "GK.K.KK.K.KG..", "KGKGKGGKGKGK..", ".KGGGGGGGGK...", "..KKKKKKKK...."], )
    p.rect(20, 1, 3, 1, "K")
    p.rect(21, 0, 1, 1, "G")
    p.rect(15, 17, 2, 6, "E")
    p.rect(13, 19, 6, 1, "E")
    return p


def vesper():
    # Signal officer: navy jacket, orange headset, long braid.
    p = body("Vesper", {"F": "#a86b4c", "s": "#7a4a35", "A": "#34507a", "a": "#24395a", "T": "#e8893a",
                        "L": "#2a2f3c", "B": "#1d2230", "H": "#1c1a1f", "h": "#3a3440", "O": "#f29a43"})
    hair(p, ["..KKKKKKKK..", ".KHHHHHHHHK.", "KHHhHHHHhHHK", "KHH......HHK", "KH........HK"])
    p.stamp(22, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", "KhK", "KHK", ".K."])
    p.stamp(8, 7, ["KOK", "KOK", "KOK"])
    p.rect(11, 12, 3, 1, "O")
    p.rect(12, 17, 3, 2, "O")
    return p


def rook():
    # Rogue pilot: leather jacket, red scarf, goggles pushed up into ginger hair.
    p = body("Rook Calder", {"A": "#7a4a2e", "a": "#59341f", "T": "#2c2a28", "L": "#3d4654", "B": "#2b2520",
                             "H": "#c0632f", "h": "#8e4421", "R": "#c4433a", "g": "#6fd0d8", "W": "#f1ece0"})
    hair(p, ["..K.KKKK.K..", ".KHKHHhHKHK.", "KHHHhHHHHHHK", "KHHHHHHhHHHK", "KH........HK"])
    p.stamp(10, 4, ["KKKKKKKKKKKK", "KgKKKKKKKKgK"])
    p.rect(13, 16, 6, 6, "W")
    p.rect(11, 15, 10, 2, "R")
    p.rect(19, 17, 2, 4, "R")
    return p


def basalt():
    # Stone giant: wide basalt plates split by molten seams, no hair, no costume.
    p = Sprite("Basalt", {**BASE, "A": "#6b6f76", "a": "#4a4e55", "l": "#8a8f96", "O": "#ff9a3c", "Y": "#ffd27a"})
    box(p, 3, 10, 26, 16, "A")
    box(p, 9, 24, 6, 7, "a")
    box(p, 17, 24, 6, 7, "a")
    box(p, 10, 3, 12, 10, "A")
    p.rect(4, 11, 6, 3, "l")
    p.rect(22, 11, 6, 3, "l")
    p.rect(12, 4, 8, 2, "l")
    p.rect(13, 8, 2, 1, "Y")
    p.rect(18, 8, 2, 1, "Y")
    p.rect(14, 11, 4, 1, "O")
    for x, y, w in [(10, 15, 4), (13, 16, 1), (13, 17, 5), (17, 18, 1), (17, 19, 4), (5, 19, 3), (24, 16, 3), (11, 27, 2), (19, 28, 2)]:
        p.rect(x, y, w, 1, "O")
    p.rect(3, 22, 5, 4, "a")
    p.rect(24, 22, 5, 4, "a")
    return p


def husk():
    # Faceless drone soldier: olive plates and one red sensor slit.
    p = body("Husk drone", {"A": "#5d6a5a", "a": "#434d41", "T": "#2d332c", "L": "#4a5448", "B": "#2d332c",
                            "M": "#77846f", "m": "#5d6a5a", "R": "#e0504a"}, head=False)
    box(p, 10, 3, 12, 12, "M")
    p.rect(11, 4, 1, 10, "m")
    p.rect(12, 9, 8, 1, "R")
    p.rect(12, 8, 8, 1, "K")
    p.rect(12, 10, 8, 1, "K")
    p.rect(14, 12, 4, 1, "m")
    for y in (17, 19, 21):
        p.rect(12, y, 8, 1, "a")
    return p


def cog():
    # Hovering brass orb with one cyan lens and a stubby antenna.
    p = Sprite("Cog", {**BASE, "A": "#d9a441", "a": "#a8782a", "l": "#f2cf7a", "C": "#58d6e6", "c": "#2a8fa0", "g": "#9be9f2"})
    p.stamp(8, 6, ["....KKKKKKKK....", "..KKAAAAAAAAKK..", ".KAlllAAAAAAAaK.", ".KAllAAAAAAAAaK.",
                   "KAlAAAKKKKAAAAaK", "KAAAAKCCCCKAAAaK", "KAAAAKCggCKAAAaK", "KAAAAKCgcCKAAAaK",
                   "KAAAAKCCCCKAAAaK", "KAAAAAKKKKAAAAaK", "KaAAAAAAAAAAAaaK", ".KaaAAAAAAAAaaK.",
                   ".KaaaaaaaaaaaaK.", "..KKaaaaaaaaKK..", "....KKKKKKKK...."])
    p.rect(15, 2, 2, 4, "K")
    p.rect(15, 1, 2, 2, "C")
    p.rect(12, 24, 8, 1, "c")
    p.rect(13, 26, 6, 1, "g")
    p.rect(14, 28, 4, 1, "c")
    return p


def aldric():
    # Veteran knight: silver plate, blue tabard, grey beard.
    p = body("Sir Aldric", {"A": "#a9b4bf", "a": "#7c8894", "T": "#c9a24a", "L": "#6d7883", "B": "#4a525b",
                            "H": "#c9c9c2", "h": "#9a9a92", "U": "#3b5fa8", "u": "#2a4680"})
    hair(p, ["..KKKKKKKK..", ".KHHHhHHHHK.", "KHHhHHHHhHHK", "KH........HK"])
    p.stamp(11, 11, ["HH......HH", "HHHHsHHHHH", ".HHhHHhHH.", "..HHHHHH.."])
    p.rect(12, 16, 8, 8, "U")
    p.rect(12, 16, 1, 8, "u")
    p.rect(15, 18, 2, 4, "T")
    p.rect(14, 19, 4, 1, "T")
    return p


def pip():
    # Pocket-sized fae duelist: dragonfly wings, leaf tunic, pink hair.
    p = Sprite("Pip", {**BASE, "A": "#5aa04a", "a": "#3d7a33", "L": "#2f5a28", "B": "#6b4a2c", "H": "#f08cb8",
                       "h": "#c9618f", "w": "#cdeefc", "v": "#8fcde8"})
    p.stamp(2, 11, ["KKK.......", "KwwKK.....", "KwvwwKK...", ".KwwvwwK..", "..KKwwwK..", "....KKK..."])
    p.stamp(20, 11, [".......KKK", ".....KKwwK", "...KKwwvwK", "..KwwvwwK.", "..KwwwKK..", "...KKK...."])
    box(p, 11, 8, 10, 10, "F")
    p.rect(12, 9, 1, 8, "s")
    p.stamp(10, 6, ["..KKKKKK..", ".KHHHHhHK.", "KHHhHHHHHK", "KHH....HHK"])
    p.rect(13, 12, 2, 2, "K")
    p.rect(17, 12, 2, 2, "K")
    p.rect(13, 12, 1, 1, "W")
    p.rect(17, 12, 1, 1, "W")
    p.rect(15, 15, 2, 1, "s")
    box(p, 11, 17, 10, 8, "A")
    p.rect(12, 18, 2, 6, "a")
    box(p, 12, 24, 4, 6, "L")
    box(p, 16, 24, 4, 6, "L")
    p.rect(13, 28, 2, 1, "B")
    p.rect(17, 28, 2, 1, "B")
    return p


def kestrel():
    # Winged scout: amber beaked hood, teal goggles, folded glider wings.
    p = body("Kestrel", {"A": "#a86b32", "a": "#7d4c20", "T": "#3c2a1a", "L": "#5b4630", "B": "#2e241a",
                         "M": "#c98a45", "m": "#a86b32", "g": "#5fd1c2", "w": "#d9c79a", "v": "#b29d6c"}, head=False)
    p.stamp(1, 12, ["KK...", "KwK..", "KwvK.", "KwwvK", "KwwwK", ".KwwK", ".KwvK", "..KwK", "..KK."])
    p.stamp(27, 12, ["...KK", "..KwK", ".KvwK", "KvwwK", "KwwwK", "KwwK.", "KvwK.", "KwK..", ".KK.."])
    box(p, 10, 2, 12, 13, "M")
    p.rect(11, 3, 1, 11, "m")
    p.rect(12, 8, 3, 2, "g")
    p.rect(17, 8, 3, 2, "g")
    p.rect(12, 7, 8, 1, "K")
    p.rect(12, 10, 8, 1, "K")
    p.stamp(14, 11, ["KmmK", ".KK."])
    return p


def juno():
    # Porcelain tactician android with a cyan visor band and circuit trim.
    p = body("Juno", {"A": "#e8e4f2", "a": "#bdb6d1", "T": "#58c7e0", "L": "#cfc9e0", "B": "#8e86a8",
                      "M": "#f4f1fb", "m": "#cfc9e0", "C": "#58c7e0"}, head=False)
    box(p, 10, 3, 12, 12, "M")
    p.rect(11, 4, 1, 10, "m")
    p.rect(11, 8, 10, 2, "C")
    p.rect(11, 7, 10, 1, "K")
    p.rect(11, 10, 10, 1, "K")
    p.rect(15, 4, 2, 3, "m")
    p.rect(14, 17, 4, 1, "C")
    p.rect(15, 18, 1, 4, "C")
    p.rect(16, 21, 3, 1, "C")
    return p


def vale():
    # Field medic: white coat over teal scrubs, curly hair, round glasses.
    p = body("Dr. Vale", {"F": "#8a5a40", "s": "#643f2c", "A": "#f1f1ea", "a": "#c9c9bf", "T": "#2f9c8f",
                          "L": "#2f9c8f", "B": "#2a3438", "H": "#231a17", "h": "#3d2e28", "S": "#2f9c8f"})
    hair(p, [".KKK.KK.KKK.", "KHHHKHHKHHHK", "KHhHHHhHHhHK", "KHHHHHHHHHHK", "KH........HK", "KH........HK"], y=1)
    p.stamp(12, 8, ["KKKK.KKKK", "K..KKK..K", "KKKK.KKKK"])
    p.rect(13, 16, 6, 7, "S")
    p.rect(15, 18, 2, 3, "W")
    p.rect(14, 19, 4, 1, "W")
    return p


def nyx():
    # Shadow duelist: indigo suit, silver hair, half mask with white marks.
    p = body("Nyx", {"A": "#2b2f5c", "a": "#1d2042", "T": "#d9dbe6", "L": "#23264a", "B": "#151731",
                     "H": "#d9dbe6", "h": "#a9acc0", "M": "#1d2042"})
    hair(p, ["..KKKKKKKK..", ".KHHHHHHhHK.", "KHHhHHHHHHHK", "KHH.....HHHK", "KHH......HHK"])
    p.stamp(21, 7, ["KHK", "KHK", "KhK", "KHK", "KHK", "KhK", "KK."])
    p.rect(11, 11, 10, 3, "M")
    p.rect(12, 12, 1, 1, "T")
    p.rect(19, 12, 1, 1, "T")
    p.rect(12, 18, 1, 4, "T")
    p.rect(19, 18, 1, 4, "T")
    return p


def hexa():
    # Sigil witch: magenta robe, high collar, black bob with a violet streak.
    p = body("Hexa", {"F": "#c98f6c", "s": "#9a6448", "A": "#8a3a8f", "a": "#62276a", "T": "#f2c95b",
                      "L": "#4a1f50", "B": "#2c1330", "H": "#17131c", "h": "#9b5cff", "G": "#f5d36a"})
    hair(p, ["..KKKKKKKK..", ".KHHHHhHHHK.", "KHHHHHhHHHHK", "KHH....hHHHK", "KHH......HHK", "KHH......HHK", "KHH......HHK"])
    p.stamp(8, 13, ["KK..............KK", "KAK............KAK", ".KAK..........KAK."])
    p.stamp(13, 17, [".KGGK.", "KG..GK", "KG..GK", ".KGGK."])
    return p


def morrow():
    # Hollow sorcerer: ragged hood, bone mask with three eyes, void ring.
    p = body("Morrow", {"A": "#1e2a2e", "a": "#121a1d", "T": "#56e0c8", "L": "#162024", "B": "#0d1417",
                        "C": "#1e2a2e", "c": "#121a1d", "M": "#e6dfcf", "m": "#b8ae98", "E": "#56e0c8"},
                cape=True, head=False)
    box(p, 8, 1, 16, 15, "C")
    p.rect(9, 2, 2, 13, "c")
    box(p, 11, 5, 10, 10, "M")
    p.rect(12, 6, 1, 8, "m")
    p.rect(13, 9, 2, 1, "E")
    p.rect(17, 9, 2, 1, "E")
    p.rect(15, 7, 2, 1, "E")
    p.rect(14, 12, 4, 1, "m")
    p.stamp(12, 17, ["..KKKKKK..", ".K......K.", "K..EEEE..K"])
    p.rect(9, 29, 3, 1, "c")
    p.rect(20, 29, 3, 1, "c")
    return p


def write_preview(sprites, path):
    # Dependency-free PNG: rows are large nearest-neighbour art, then actual-size checks.
    backgrounds = [json.loads((ROOT / "themes" / f"{side}.json").read_text())["background"]
                   for side in ["eclipse", "vanguard"]]
    width, height, cell = len(sprites) * 144, 424, 144
    rgb = lambda color: bytes.fromhex(color.lstrip("#"))
    rows = []
    for y in range(height):
        bg = backgrounds[y // (height // 2)]
        row = bytearray(rgb(bg) * width)
        local_y = y % (height // 2)
        for index, sprite in enumerate(sprites):
            for scale, top in [(4, 8), (1.125, 160)]:
                size = round(SIZE * scale)
                if not top <= local_y < top + size:
                    continue
                sy = int((local_y - top) / scale)
                left = index * cell + (cell - size) // 2
                for dx in range(size):
                    color = sprite.pixels[sy][int(dx / scale)]
                    if color:
                        row[(left + dx) * 3:(left + dx + 1) * 3] = rgb(color)
        rows.append(b"\0" + row)
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 2, 0, 0, 0))
    Path(path).write_bytes(png + chunk(b"IDAT", zlib.compress(b"".join(rows))) + chunk(b"IEND", b""))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()
    drawings = {
        "umbra": umbra, "meridian": meridian, "vesper": vesper, "rook": rook,
        "basalt": basalt, "husk": husk, "cog": cog,
        "aldric": aldric, "pip": pip, "kestrel": kestrel,
        "juno": juno, "vale": vale, "nyx": nyx,
        "hexa": hexa, "morrow": morrow,
    }
    DEST.mkdir(parents=True, exist_ok=True)
    characters = {name: draw() for name, draw in drawings.items()}
    for name, sprite in characters.items():
        (DEST / f"{name}.svg").write_text(sprite.svg(), encoding="utf-8")
    print(f"Built {len(characters)} character sprites in {DEST}")
    if args.preview:
        write_preview(list(characters.values()), args.preview)
        print(f"Preview: {args.preview}")


if __name__ == "__main__":
    main()
