#!/usr/bin/env python3
"""Bomb Run's local Avengers pixel-art decks, props, bitmap lettering and walking atlases.

Uses only the standard library. Character palettes come from the existing
32px Avengers cast; each atlas has idle / left stride / right stride, in four directions.
Run: python3 tools/build-bomb-run-art.py [--preview /tmp/bomb-run-decks.png]
"""
import argparse
from html import escape
from pathlib import Path
import json
import re
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "mods/doomsday-tabs/arcade"
CAST = ROOT / "mods/doomsday-agents/sprites/doomsday"
INK = "#11151f"


class Canvas:
    def __init__(self, width, height, title):
        self.width, self.height, self.title = width, height, title
        self.pixels = [[None] * width for _ in range(height)]

    def rect(self, x, y, width, height, color):
        for yy in range(max(0, y), min(self.height, y + height)):
            for xx in range(max(0, x), min(self.width, x + width)):
                self.pixels[yy][xx] = color

    def svg(self):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}" shape-rendering="crispEdges">',
               f"<title>{escape(self.title)}</title>"]
        for y, row in enumerate(self.pixels):
            x = 0
            while x < self.width:
                color, end = row[x], x + 1
                while end < self.width and row[end] == color:
                    end += 1
                if color:
                    out.append(f'<rect x="{x}" y="{y}" width="{end - x}" height="1" fill="{color}"/>')
                x = end
        return "\n".join([*out, "</svg>", ""])

    def save(self, name):
        path = ART / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.svg())

    def png(self, path):
        raw = b"".join(b"\x00" + bytes(int((color or "#09131f")[index:index + 2], 16)
                        for color in line for index in (1, 3, 5)) for line in self.pixels)
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 2, 0, 0, 0))
                              + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


# Small native bitmap alphabet: no downloaded font, emoji or platform glyphs.
FONT = {
    "A": "010/101/111/101/101", "B": "110/101/110/101/110", "C": "011/100/100/100/011",
    "D": "110/101/101/101/110", "E": "111/100/110/100/111", "F": "111/100/110/100/100",
    "G": "011/100/101/101/011", "H": "101/101/111/101/101", "I": "111/010/010/010/111",
    "J": "001/001/001/101/010", "K": "101/101/110/101/101", "L": "100/100/100/100/111",
    "M": "10001/11011/10101/10001/10001", "N": "1001/1101/1011/1001/1001",
    "O": "010/101/101/101/010", "P": "110/101/110/100/100", "Q": "010/101/101/111/011",
    "R": "110/101/110/101/101", "S": "011/100/010/001/110", "T": "111/010/010/010/010",
    "U": "101/101/101/101/111", "V": "101/101/101/101/010", "W": "10001/10001/10101/10101/01010",
    "X": "101/101/010/101/101", "Y": "101/101/010/010/010", "Z": "111/001/010/100/111",
    " ": "00/00/00/00/00", "-": "000/000/111/000/000",
}


def lettering(text, name, color):
    width = sum(len(FONT[c].split('/')[0]) + 1 for c in text) - 1
    p = Canvas(width, 5, text)
    x = 0
    for char in text:
        glyph = FONT[char].split('/')
        for y, line in enumerate(glyph):
            for dx, dot in enumerate(line):
                if dot == "1":
                    p.rect(x + dx, y, 1, 1, color)
        x += len(glyph[0]) + 1
    p.save(f"{name}.svg")


def deck(spec):
    p = Canvas(208, 224, f"{spec['name']} — Avengers pixel-art zone")
    p.rect(0, 0, 208, 224, "#080e16")
    # Upper header bulkhead + recessed skyline frame.
    p.rect(0, 0, 208, 30, "#1c2a37")
    p.rect(0, 0, 208, 2, "#607380")
    # Walkable deck: subtle floor tiles with rivets.
    p.rect(0, 30, 208, 178, "#192732")
    for y in range(32, 208, 16):
        for x in range(0, 208, 16):
            p.rect(x, y, 16, 16, "#1d2c37" if (x + y) % 32 else "#202f39")
            p.rect(x + 1, y + 15, 14, 1, "#14232d")
            if (x * 3 + y) % 48 == 0:
                p.rect(x + 3, y + 3, 1, 1, "#3a4b56")
                p.rect(x + 12, y + 12, 1, 1, "#101d27")
    # Continuous outer walls follow the level's collision border.
    for x, y, w, h in [(0, 30, 208, 18), (0, 192, 208, 16), (0, 48, 16, 144), (192, 48, 16, 144)]:
        p.rect(x, y, w, h, "#0c1824")
        p.rect(x + 2, y + 2, max(1, w - 4), max(1, h - 4), "#344554")
    p.rect(16, 45, 176, 2, "#72919b")
    p.rect(16, 191, 176, 2, "#72919b")
    p.rect(13, 48, 2, 144, "#58717c")
    p.rect(193, 48, 2, 144, "#58717c")
    # Control banks and status lights embedded in the walls.
    for x in range(23, 190, 24):
        p.rect(x, 34, 17, 7, "#111f2b")
        p.rect(x + 2, 35, 7, 3, "#365c6d")
        p.rect(x + 3, 35, 3, 1, "#8ab2b8")
        p.rect(x + 11, 36, 2, 2, "#bf7258")
        p.rect(x + 14, 36, 1, 2, "#dbc080")
        p.rect(x, 197, 15, 3, "#172a37")
        p.rect(x + 2, 198, 6, 1, "#86a8b2")
    for y in range(54, 185, 24):
        for x in (4, 198):
            p.rect(x, y, 6, 16, "#172330")
            for dy in (2, 5, 8, 11):
                p.rect(x + 1, y + dy, 4, 1, "#516572")
            p.rect(x + 2, y + 18, 2, 2, "#d8a85f")
    # Recessed lower bay hatch and hazard chevrons.
    p.rect(0, 208, 208, 16, "#14212c")
    p.rect(60, 211, 88, 11, "#263b49")
    p.rect(63, 214, 82, 6, "#0b1722")
    p.rect(100, 214, 8, 6, "#4e6770")
    for x in list(range(20, 54, 6)) + list(range(156, 190, 6)):
        p.rect(x, 211, 3, 2, "#9b7952")
        p.rect(x + 1, 213, 3, 2, "#9b7952")

    # Iconic Avengers location skylines & architectural floor markings!
    zone = spec["id"]
    accent = spec["accent"]
    if zone == "reactor":
        # Stark Arc Core: glowing cyan Arc Reactor turbines & Stark energy conduits!
        p.rect(10, 4, 188, 22, "#0a1724")
        for cx in (34, 78, 130, 174):
            p.rect(cx - 10, 6, 20, 18, "#29465c")
            p.rect(cx - 8, 8, 16, 14, "#0d2236")
            p.rect(cx - 6, 9, 12, 12, "#35a4cc")
            p.rect(cx - 4, 11, 8, 8, "#0d2236")
            p.rect(cx - 2, 13, 4, 4, "#9ef4ff")
        # Central Arc Reactor ring in skyline + floor energy conduit cross.
        p.rect(96, 5, 16, 20, "#355a75")
        p.rect(98, 7, 12, 16, "#5ce6ff")
        p.rect(100, 9, 8, 12, "#0d2236")
        p.rect(102, 11, 4, 8, "#d9fbff")
        p.rect(103, 48, 2, 144, "#234a63")
        p.rect(16, 119, 176, 2, "#234a63")
    elif zone == "hangar":
        # Helicarrier Deck: open sky with spinning Helicarrier turbine bays & carrier runway lines!
        p.rect(10, 4, 188, 22, "#122238")
        p.rect(14, 6, 180, 18, "#1d3554")
        # Cloud wisps in open sky + twin rotor turbines on flanks.
        for x in (58, 92, 128):
            p.rect(x, 12, 18, 4, "#4b698a")
            p.rect(x + 4, 10, 10, 2, "#6c8bad")
        for tx in (18, 164):
            p.rect(tx, 6, 26, 18, "#3a4d5c")
            p.rect(tx + 3, 8, 20, 14, "#101b24")
            p.rect(tx + 5, 14, 16, 2, "#8aa0b0")
            p.rect(tx + 12, 9, 2, 12, "#8aa0b0")
            p.rect(tx + 11, 13, 4, 4, accent)
        # Aircraft carrier launch stripes & chevrons.
        for y in range(56, 187, 24):
            for x in (20, 184):
                p.rect(x, y, 4, 8, "#947c44")
                p.rect(x + 2, y + 6, 4, 2, "#947c44")
        for y in range(52, 188, 12):
            p.rect(103, y, 2, 6, "#8c7d52")
        p.rect(94, 48, 1, 144, "#3d4e59")
        p.rect(113, 48, 1, 144, "#3d4e59")
    elif zone == "cryo":
        # Hydra Siberia Lab: Winter Soldier stasis pods & heavy frost seams!
        p.rect(10, 4, 188, 22, "#112836")
        for x in range(14, 192, 22):
            p.rect(x, 6, 18, 17, "#365f73")
            p.rect(x + 2, 8, 14, 13, "#1c4359")
            p.rect(x + 3, 9, 3, 9, "#91d4e6")
            p.rect(x + 8, 11, 4, 7, "#2c5f78")
            p.rect(x + 11, 17, 3, 3, "#c4eef5")
        for y in range(48, 192, 8):
            p.rect(15, y, 2 + y % 3, 3, "#83b8cc")
            p.rect(191, y, 2, 4, "#83b8cc")
    elif zone == "cargo":
        # Wakanda Vibranium Vault: golden-trimmed vibranium ore alcoves & royal violet glow!
        p.rect(10, 4, 188, 22, "#191326")
        for x in range(15, 195, 30):
            p.rect(x, 6, 25, 17, "#614987")
            p.rect(x + 2, 8, 21, 13, "#211833")
            p.rect(x + 4, 9, 17, 2, "#e0b858")
            p.rect(x + 7, 12, 11, 7, "#8d52db")
            p.rect(x + 9, 13, 7, 4, "#d2a8ff")
        # Subtle golden Wakandan floor trim.
        for x in (24, 80, 136):
            for y in (54, 118, 174):
                p.rect(x, y, 40, 1, "#6b558a")
                p.rect(x, y, 1, 9, "#6b558a")
    elif zone == "engine":
        # Sanctum Sanctorum: iconic circular Window of the Worlds seal + mystic warm windows!
        p.rect(10, 4, 188, 22, "#241715")
        # Side arched mystic windows.
        for x in (22, 54, 134, 166):
            p.rect(x, 6, 20, 18, "#6e4635")
            p.rect(x + 2, 8, 16, 14, "#1e1624")
            p.rect(x + 9, 8, 2, 14, "#a66c49")
            p.rect(x + 2, 14, 16, 2, "#a66c49")
            p.rect(x + 5, 10, 3, 3, "#f5be67")
        # Center iconic circular Sanctum Sanctorum Window of the Worlds!
        p.rect(92, 4, 24, 22, "#8a5a3c")
        p.rect(94, 6, 20, 18, "#1b1424")
        p.rect(96, 7, 16, 16, "#e89d46")
        p.rect(98, 9, 12, 12, "#2a1b2e")
        p.rect(103, 7, 2, 16, "#f7cb6a")
        p.rect(96, 14, 16, 2, "#f7cb6a")
        p.rect(101, 12, 6, 6, "#ffe69e")
        # Warm mystic floor carpet lines.
        for y in (82, 146):
            p.rect(20, y, 168, 2, "#633830")
    elif zone == "bridge":
        # Avengers Tower: panoramic Manhattan night skyline + glowing Avengers 'A' beacon!
        p.rect(9, 4, 190, 22, "#4b628c")
        p.rect(12, 6, 184, 18, "#0c1429")
        # Manhattan skyscrapers silhouette in window.
        for bx, bw, bh in [(18, 14, 10), (36, 12, 14), (52, 16, 8), (138, 14, 12), (156, 18, 15), (178, 12, 9)]:
            p.rect(bx, 24 - bh, bw, bh, "#1e2f52")
            p.rect(bx + 2, 26 - bh, 2, 2, "#7ab8ff")
            p.rect(bx + 6, 26 - bh, 2, 2, "#f2d283")
        # Glowing Avengers 'A' crest centered in the glass!
        for rx, ry, rw, rh in [(101, 8, 6, 2), (99, 10, 2, 11), (107, 10, 2, 11), (99, 15, 11, 2)]:
            p.rect(rx, ry, rw, rh, "#7ab8ff")
        for x in (48, 84, 124, 160):
            p.rect(x, 6, 1, 18, "#4b628c")
        for x in (27, 180):
            p.rect(x, 48, 1, 143, "#3b4e75")
        p.rect(36, 185, 136, 2, "#3b4e75")
    elif zone == "detention":
        # The Raft: underwater ocean viewports with bubbles & maximum-security bars!
        p.rect(10, 4, 188, 22, "#102124")
        for x in range(14, 194, 23):
            p.rect(x, 5, 18, 19, "#486965")
            p.rect(x + 2, 7, 14, 14, "#0b2a33")
            p.rect(x + 4, 9, 2, 2, "#78d4b5")
            p.rect(x + 11, 14, 2, 2, "#52a898")
            for xx in range(x + 5, x + 15, 4):
                p.rect(xx, 7, 1, 14, "#7ea39a")
            p.rect(x + 6, 22, 5, 1, "#d95b54")
        for y in range(54, 190, 24):
            p.rect(8, y, 2, 8, "#78d4b5")
            p.rect(198, y, 2, 8, "#78d4b5")
    elif zone == "foundry":
        # Castle Doom Foundry: Latverian gothic iron arches & emerald arcane Doombot furnaces!
        p.rect(10, 4, 188, 22, "#15211a")
        for x in range(16, 194, 32):
            p.rect(x, 6, 24, 18, "#3e5446")
            p.rect(x + 2, 7, 20, 2, "#6a8775")
            p.rect(x + 6, 10, 12, 13, "#0d1a12")
            p.rect(x + 9, 12, 6, 9, "#289e4f")
            p.rect(x + 10, 14, 4, 5, "#8cffad")
        for y in (65, 113, 161):
            p.rect(18, y, 172, 5, "#111c16")
            for x in range(20, 190, 6):
                p.rect(x, y + 1, 2, 3, "#2d593c")
    replacements = {
        "#1d2c37": spec["floor"], "#202f39": spec["floor"],
        "#344554": spec["wall"], "#72919b": accent,
    }
    p.pixels = [[replacements.get(color, color) for color in line] for line in p.pixels]
    p.save(f"deck-{zone}.svg")


def zone_props():
    for kind in ("barricade", "cryo-pod", "cargo-rack", "turbine", "terminal", "cell-door", "press"):
        p = Canvas(16, 16, kind.replace("-", " "))
        p.rect(1, 13, 14, 3, "#0a1320")
        if kind == "barricade":
            # Helicarrier flight deck blast shield.
            p.rect(1, 3, 14, 10, "#273541")
            p.rect(2, 4, 12, 2, "#b8c7d4")
            p.rect(2, 7, 12, 4, "#e0b34a")
            for x in (2, 7, 12):
                p.rect(x, 7, 2, 2, "#233440")
                p.rect(x + 1, 9, 2, 2, "#233440")
        elif kind == "cryo-pod":
            # Hydra Siberia cryo stasis pod.
            p.rect(3, 0, 10, 14, "#355063")
            p.rect(4, 1, 8, 2, "#b5d2db")
            p.rect(4, 4, 8, 7, "#3e8aa8")
            p.rect(5, 4, 2, 7, "#9ce2ed")
            p.rect(8, 5, 2, 4, "#d4f7f0")
            p.rect(5, 12, 6, 2, "#7d9aa8")
        elif kind == "cargo-rack":
            # Wakanda Vibranium containment crate with glowing violet core.
            p.rect(1, 2, 14, 12, "#281f38")
            for x in (2, 12):
                p.rect(x, 1, 2, 13, "#e0b858")
            p.rect(4, 3, 8, 9, "#4d3573")
            p.rect(5, 4, 6, 7, "#9f63f0")
            p.rect(6, 5, 4, 3, "#e3c7ff")
            p.rect(4, 9, 8, 1, "#281f38")
        elif kind == "turbine":
            # Sanctum Sanctorum mystic relic pedestal with golden Eldritch orb.
            p.rect(3, 10, 10, 4, "#5c392a")
            p.rect(4, 7, 8, 4, "#7a4c38")
            p.rect(5, 8, 6, 1, "#d9a24c")
            p.rect(4, 1, 8, 6, "#d97828")
            p.rect(5, 2, 6, 4, "#f7c454")
            p.rect(7, 3, 2, 2, "#fff5d1")
        elif kind == "terminal":
            # Avengers Tower JARVIS holographic console.
            p.rect(1, 1, 14, 9, "#46628c")
            p.rect(2, 2, 12, 6, "#162d52")
            p.rect(3, 3, 5, 1, "#85c7ff")
            p.rect(3, 5, 9, 1, "#5ca3f5")
            p.rect(10, 3, 2, 2, "#d4f0ff")
            p.rect(3, 10, 10, 4, "#314261")
            for x in range(4, 12, 2):
                p.rect(x, 11, 1, 1, "#85c7ff")
        elif kind == "cell-door":
            # The Raft maximum-security containment cell door.
            p.rect(1, 0, 14, 14, "#4b6966")
            p.rect(3, 2, 10, 11, "#102429")
            for x in (4, 7, 10):
                p.rect(x, 2, 1, 11, "#90b8b0")
            p.rect(1, 6, 2, 2, "#e05a52")
        else:
            # Castle Doom Doombot assembly forge with emerald arcane core.
            p.rect(1, 0, 14, 3, "#7a8791")
            for x in (2, 11):
                p.rect(x, 3, 3, 10, "#46574c")
                p.rect(x, 4, 1, 6, "#8fa396")
            p.rect(6, 3, 4, 5, "#289e4f")
            p.rect(7, 4, 2, 3, "#9effba")
            p.rect(5, 8, 6, 2, "#2b3830")
            p.rect(2, 13, 12, 2, "#46574c")
        p.save(f"{kind}.svg")


def pickups():
    glyphs = {
        "range": ("#f2bd66", [(7, 3, 2, 10), (3, 7, 10, 2), (5, 4, 6, 1), (5, 11, 6, 1)]),
        "nova": ("#ef9678", [(6, 3, 4, 10), (3, 6, 10, 4), (4, 4, 2, 2), (10, 10, 2, 2), (4, 10, 2, 2), (10, 4, 2, 2)]),
        "echo": ("#c2b0ef", [(3, 4, 6, 2), (3, 4, 2, 6), (3, 8, 6, 2), (7, 6, 6, 2), (11, 6, 2, 6), (7, 10, 6, 2)]),
        "rack": ("#9ccc8e", [(3, 4, 10, 2), (3, 7, 10, 2), (3, 10, 10, 2), (4, 3, 2, 10)]),
        "line": ("#78ced1", [(3, 6, 2, 4), (6, 6, 2, 4), (9, 6, 2, 4), (11, 4, 2, 8)]),
        "speed": ("#8fbaf2", [(3, 3, 2, 3), (5, 5, 2, 3), (3, 8, 2, 4), (8, 3, 2, 3), (10, 5, 2, 3), (8, 8, 2, 4)]),
    }
    for name, (color, marks) in glyphs.items():
        p = Canvas(16, 16, f"{name} power-up")
        p.rect(2, 0, 12, 16, "#0b1420")
        p.rect(0, 2, 16, 12, "#0b1420")
        p.rect(2, 1, 12, 14, color)
        p.rect(1, 2, 14, 12, color)
        p.rect(3, 3, 10, 10, "#1c2a38")
        for x, y, w, h in marks:
            p.rect(x, y, w, h, color)
        p.rect(7, 7, 2, 2, "#f4efd6")
        p.save(f"buff-{name}.svg")


def props():
    # Stark Arc Pylon: armored Stark reactor column with glowing cyan Arc core.
    p = Canvas(16, 16, "Stark Arc pylon")
    p.rect(1, 13, 14, 3, "#080e17")
    p.rect(2, 1, 12, 13, "#0b1420")
    p.rect(3, 0, 10, 1, "#0b1420")
    p.rect(3, 1, 10, 2, "#65849c")
    p.rect(2, 3, 12, 9, "#2c465c")
    p.rect(3, 3, 1, 8, "#88a8bf")
    p.rect(12, 3, 1, 9, "#182938")
    p.rect(5, 4, 6, 6, "#102030")
    p.rect(6, 5, 4, 4, "#4ad9ff")
    p.rect(7, 6, 2, 2, "#e0fbff")
    p.rect(4, 12, 8, 2, "#24384a")
    p.rect(6, 12, 1, 1, "#d95b54")
    p.rect(9, 12, 1, 1, "#5ce6ff")
    p.save("console.svg")
    # Destructible Gamma/Arc energy cell: rounded containment canister.
    for phase in (0, 1):
        p = Canvas(16, 18, "Unstable energy cell")
        p.rect(2, 15, 12, 3, "#0b1420")
        p.rect(5, 1, 6, 15, "#0b1420")
        p.rect(3, 3, 10, 11, "#0b1420")
        p.rect(4, 3, 8, 11, "#2a695c")
        p.rect(5, 3, 6, 10, "#3ca37c")
        p.rect(6, 4, 2, 8, "#7cf2b4")
        p.rect(8, 6, 2, 5, "#c4ffd6" if phase else "#8ef0be")
        for y in (2, 13):
            p.rect(4, y, 8, 2, "#7c8e94")
            p.rect(5, y, 3, 1, "#c7d4d9")
        p.rect(5, 15, 6, 1, "#3b535d")
        p.rect(4, 7, 1, 4, "#a8f7c8")
        p.rect(10, 3, 1, 3, "#1f4f45")
        p.save(f"coolant-{phase}.svg")
    # Stark Arc Charge: red-gold armored casing with pulsing cyan/gold/white Arc core!
    for phase in (0, 1, 2):
        p = Canvas(16, 16, "Armed Stark Arc charge")
        p.rect(3, 13, 11, 2, "#0b1420")
        for x, y, w, h in [(5, 2, 6, 12), (3, 4, 10, 8), (2, 6, 12, 4)]:
            p.rect(x, y, w, h, "#101820")
        p.rect(5, 3, 6, 10, "#b82830")
        p.rect(4, 5, 8, 6, "#c92c34")
        p.rect(3, 6, 10, 4, "#8f1b22")
        p.rect(5, 4, 6, 1, "#f0c246")
        p.rect(5, 11, 6, 1, "#c99628")
        # Glowing central Arc Reactor core!
        core = ["#4ad9ff", "#ffd254", "#ffffff"][phase]
        ring = ["#247ca3", "#e87838", "#7cf0ff"][phase]
        p.rect(5, 5, 6, 6, "#162636")
        p.rect(6, 5, 4, 6, ring)
        p.rect(5, 6, 6, 4, ring)
        p.rect(7, 7, 2, 2, core)
        p.save(f"detonator-{phase}.svg")
    # Connected plasma tongues, not a text glyph or a floating plus sign.
    for phase in range(3):
        p = Canvas(16, 16, "Arc plasma burst")
        for x in range(16):
            spread = [3, 4, 5, 4][(x + phase) % 4]
            p.rect(x, 8 - spread, 1, spread * 2, "#c64e38")
            p.rect(x, 9 - spread, 1, spread * 2 - 2, "#f49946")
            p.rect(x, 7 + (x + phase) % 2, 1, 2, "#ffe5a0")
        p.save(f"blast-h-{phase}.svg")
        p.pixels = [list(line) for line in zip(*p.pixels)]
        p.save(f"blast-v-{phase}.svg")
    # Pixel shadow and floor scorch remain independent of actors' gait.
    p = Canvas(16, 16, "Ground shadow")
    p.rect(4, 12, 8, 3, "#0a1420")
    p.rect(2, 13, 12, 1, "#0a1420")
    p.save("shadow.svg")
    p = Canvas(16, 16, "Echo blast warning — not a pickup")
    for x, y, w, h in [(0, 0, 5, 2), (0, 0, 2, 5), (11, 0, 5, 2), (14, 0, 2, 5),
                        (0, 14, 5, 2), (0, 11, 2, 5), (11, 14, 5, 2), (14, 11, 2, 5)]:
        p.rect(x, y, w, h, "#ef9678")
    for x, y, w, h in [(5, 4, 6, 2), (9, 6, 2, 2), (5, 8, 6, 1), (5, 9, 2, 2), (5, 11, 6, 1)]:
        p.rect(x, y, w, h, "#f2bd66")
    p.save("echo-beacon.svg")


def actors():
    actor_dir = ART / "actors"
    if actor_dir.exists():
        for old in actor_dir.glob("*.svg"):
            old.unlink()
    rects = re.compile(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" fill="(#[0-9a-f]{6})"/>')
    for path in sorted(CAST.glob("*.svg")):
        src = Canvas(32, 32, path.stem)
        for x, y, w, h, color in rects.findall(path.read_text()):
            src.rect(int(x), int(y), int(w), int(h), color)
        if not any(any(row) for row in src.pixels):
            continue
        for facing in ("down", "up", "left", "right"):
            atlas = Canvas(96, 32, f"{path.stem} — {facing}: idle, left stride, right stride")
            # Back view keeps the character's head/cape palette, without front eyes.
            rear = src.pixels[7][10] or src.pixels[5][12] or "#3e5061"
            for phase in range(3):
                for y, line in enumerate(src.pixels):
                    for x, color in enumerate(line):
                        if color is None:
                            continue
                        xx, yy = x, y
                        # Swing lower legs and outer arms in opposing directions.
                        if phase and y >= 27 and 10 <= x <= 21:
                            leading = (x < 16) == (phase == 1)
                            yy = y - (1 if leading else 0)
                            xx += (-1 if x < 16 else 1) if leading else 0
                        if phase and 20 <= y <= 25 and (x < 11 or x > 20):
                            yy += (1 if x < 16 else -1) * (1 if phase == 1 else -1)
                        if facing == "up":
                            if 8 <= y <= 16 and 9 <= x <= 22 and color != INK:
                                color = rear
                            elif 10 <= y <= 15 and 10 <= x <= 21:
                                color = rear
                        if facing in ("left", "right"):
                            # Narrow silhouette and a slight profile, still on whole pixels.
                            xx = 16 + round((xx - 16) * 0.8)
                            if y < 18:
                                xx += 1
                        if facing == "left":
                            xx = 31 - xx
                        if 0 <= xx < 32 and 0 <= yy < 32:
                            atlas.rect(phase * 32 + xx, yy, 1, 1, color)
            atlas.save(f"actors/{path.stem}-{facing}.svg")


def overview(specs, destination):
    """Generated architecture overview, deliberately not an app screenshot."""
    sheet = Canvas(896, 524, "Bomb Run Avengers zone architecture")
    sheet.rect(0, 0, sheet.width, sheet.height, "#09131f")
    rects = re.compile(r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" fill="(#[0-9a-f]{6})"')
    def paste(name, x, y):
        for sx, sy, width, height, color in rects.findall((ART / name).read_text()):
            sheet.rect(x + int(sx), y + int(sy), int(width), int(height), color)
    for index, spec in enumerate(specs):
        left, top = 8 + index % 4 * 224, 12 + index // 4 * 260
        cursor = left
        for char in spec["name"].upper():
            if char not in FONT:
                continue
            glyph = FONT[char].split("/")
            for y, line in enumerate(glyph):
                for x, dot in enumerate(line):
                    if dot == "1":
                        sheet.rect(cursor + x * 2, top + y * 2, 2, 2, spec["accent"])
            cursor += (len(glyph[0]) + 1) * 2
        paste(f"deck-{spec['id']}.svg", left, top + 18)
        for y, line in enumerate(spec["layout"]):
            for x, kind in enumerate(line):
                if kind == "#" and 0 < x < 12 and 0 < y < 10:
                    paste(f"{spec['prop']}.svg", left + x * 16, top + 18 + (y + 2) * 16)
    sheet.png(destination)


def main(preview=None):
    ART.mkdir(parents=True, exist_ok=True)
    # Remove files from the earlier unused artwork prototype.
    for name in ("deck.svg", "ship-interior.svg", "bulkhead.svg", "conduit.svg", "blast-0.svg", "blast-1.svg", "blast-2.svg"):
        (ART / name).unlink(missing_ok=True)
    old_walk = ART / "walk"
    if old_walk.exists():
        for path in old_walk.glob("*.svg"):
            path.unlink()
        old_walk.rmdir()
    specs = json.loads((ROOT / "mods/doomsday-tabs/bomb-run-override.json").read_text())["decks"]
    for spec in specs:
        deck(spec)
    props()
    zone_props()
    pickups()
    actors()
    for text, name, color in [
        ("BOMB RUN", "title", "#e4d7b4"), ("CLEAR THE DECK", "mission", "#93b7b5"),
        ("ZONE SECURED", "victory", "#b8d5a5"), ("SIGNAL LOST", "defeat", "#dd9b86"),
        ("ON STANDBY", "paused", "#e4d7b4"),
    ]:
        lettering(text, name, color)
    if preview:
        overview(specs, preview)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ART, help="Destination for generated SVGs")
    parser.add_argument("--preview", type=Path, help="Optional eight-zone architecture PNG")
    args = parser.parse_args()
    ART = args.output
    main(args.preview)
