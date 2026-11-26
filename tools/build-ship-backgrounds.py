#!/usr/bin/env python3
"""Build seven Avengers pixel-art ship emblems and cockpits in dark/light variants.

Usage: python3 tools/build-ship-backgrounds.py [--preview /tmp/fleet-backgrounds.png]
PNG files are used by Herdr; matching SVG files are editable/exportable sources.
"""

import argparse
from html import escape
import json
from pathlib import Path
import random
import struct
import xml.etree.ElementTree as ET
import zlib

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "backgrounds/ships"
FLEET = {
    "skyrunner": ("Quinjet", "#58a6d8"),
    "arrowhawk": ("Avenjet", "#d85a5a"),
    "nightglass": ("Royal Talon", "#9f78d8"),
    "bastion": ("Helicarrier", "#78a4b8"),
    "longbow": ("Benatar", "#d89a52"),
    "dart": ("S.H.I.E.L.D. Dart", "#62b5a8"),
    "eclipse-barge": ("Latverian Barge", "#4eb872"),
}
W, H = 320, 180


def rgb(color):
    return tuple(bytes.fromhex(color.lstrip("#")))


def blend(a, b, amount):
    return "#" + "".join(f"{round(x * (1 - amount) + y * amount):02x}" for x, y in zip(rgb(a), rgb(b)))


def png(path, pixels, scale=1):
    height, width = len(pixels), len(pixels[0])
    rows = []
    for row in pixels:
        scan = b"\0" + b"".join(bytes(rgb(color)) * scale for color in row)
        rows.extend([scan] * scale)

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    header = struct.pack(">2I5B", width * scale, height * scale, 8, 2, 0, 0, 0)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                           + chunk(b"IDAT", zlib.compress(b"".join(rows))) + chunk(b"IEND", b""))


class Scene:
    def __init__(self, dark, accent):
        # The two theme files are the only source of interface/cockpit colors.
        side = "eclipse" if dark else "vanguard"
        theme = json.loads((ROOT / "themes" / f"{side}.json").read_text())
        colors = theme["colors"]
        self.dark = dark
        self.colors = {
            "sky": theme["background"], "deep": colors["canvas"], "planet": colors["hover"],
            "horizon": blend(colors["hover"], theme["background"], 0.35),
            "city": blend(colors["border"], theme["background"], 0.55 if dark else 0.60),
            "star": blend(colors["dim"], theme["background"], 0.35),
            "frame": colors["border"], "hull": blend(colors["input"], theme["background"], 0.72),
            "edge": colors["input"], "panel": colors["surface"], "glass": colors["selected"],
            "light": colors["muted"],
        }
        self.colors["accent"] = blend(accent, self.colors["sky"], 0.18 if dark else 0.45)
        self.colors["glow"] = blend(accent, self.colors["sky"], 0.42 if dark else 0.65)
        self.pixels = [[self.colors["sky"]] * W for _ in range(H)]

    def rect(self, x, y, width, height, color):
        color = self.colors.get(color, color)
        for yy in range(max(0, y), min(H, y + height)):
            self.pixels[yy][max(0, x):min(W, x + width)] = [color] * max(0, min(W, x + width) - max(0, x))

    def poly(self, points, color):
        for y in range(max(0, min(p[1] for p in points)), min(H, max(p[1] for p in points))):
            hits = []
            for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
                if min(y1, y2) <= y + 0.5 < max(y1, y2):
                    hits.append(x1 + (y + 0.5 - y1) * (x2 - x1) / (y2 - y1))
            hits.sort()
            for x1, x2 in zip(hits[::2], hits[1::2]):
                left, right = round(x1), round(x2)
                self.rect(left, y, right - left, 1, color)

    def line(self, x1, y1, x2, y2, width, color):
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for step in range(steps + 1):
            x, y = round(x1 + (x2 - x1) * step / steps), round(y1 + (y2 - y1) * step / steps)
            self.rect(x - width // 2, y - width // 2, width, width, color)

    def disc(self, cx, cy, radius, color):
        for y in range(max(0, cy - radius), min(H, cy + radius + 1)):
            half = int(max(0, radius ** 2 - (y - cy) ** 2) ** 0.5)
            self.rect(cx - half, y, 2 * half + 1, 1, color)

    def ring(self, cx, cy, outer, inner, color):
        for y in range(max(0, cy - outer), min(H, cy + outer + 1)):
            for x in range(max(0, cx - outer), min(W, cx + outer + 1)):
                d2 = (x - cx) ** 2 + (y - cy) ** 2
                if inner ** 2 <= d2 <= outer ** 2:
                    self.pixels[y][x] = self.colors.get(color, color)

    def window(self, points, rim=None):
        space = self.pixels
        self.pixels = [[self.colors["frame"]] * W for _ in range(H)]
        if rim:
            self.poly(rim, "hull")
        self.poly(points, "sky")
        for y, row in enumerate(self.pixels):
            for x, color in enumerate(row):
                if color == self.colors["sky"]:
                    row[x] = space[y][x]

    def instruments(self, x, y, width, height, seed):
        self.rect(x, y, width, height, "deep")
        self.rect(x + 2, y + 2, width - 4, height - 4, "panel")
        randomizer = random.Random(seed)
        for yy in range(y + 5, y + height - 3, 5):
            for xx in range(x + 5, x + width - 4, 7):
                self.rect(xx, yy, randomizer.choice([2, 3, 4]), 1,
                          randomizer.choice(["glass", "glass", "edge", "accent"]))

    def svg(self, title):
        out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" '
               'width="640" height="360" shape-rendering="crispEdges">',
               f"  <title>{escape(title)} cockpit — pixel art</title>"]
        for y, row in enumerate(self.pixels):
            x = 0
            while x < W:
                end = x + 1
                while end < W and row[end] == row[x]:
                    end += 1
                out.append(f'<rect x="{x}" y="{y}" width="{end - x}" height="1" fill="{row[x]}"/>')
                x = end
        return "\n".join([*out, "</svg>", ""])


EMBLEM_INK = {
    "K": "#1a2430", "S": "#b8c7d4", "s": "#718291", "G": "#ebc04d",
    "C": "#58d4f0", "R": "#d64545", "V": "#a970ff", "E": "#4ee680",
}

# 16x16 Avengers fleet emblems: Quinjet, Avenjet, Royal Talon, Helicarrier, Benatar, S.H.I.E.L.D. Dart, Latverian Barge.
EMBLEMS = {
    # Quinjet: twin-rotor Avengers VTOL jet.
    "skyrunner": [
        ".......KK.......",
        "......KSSK......",
        "......KCCK......",
        ".....KSCCSK.....",
        "....KSSSSSSK....",
        "..KKSSsSSsSSKK..",
        ".KSSKCKSSKCKSSK.",
        "KSSKCCKSSKCCKSSK",
        "KSSSKCKSSKCKSSSK",
        "KKKKSSsSSsSSKKKK",
        "...KSSsSSsSSK...",
        "..KSSKSSSSKSSK..",
        "..KCK.KGGK.KCK..",
        "..KK..K..K..KK..",
        "................",
        "................",
    ],
    # Avenjet: Stark red/gold delta interceptor with glowing Arc core.
    "arrowhawk": [
        ".......KK.......",
        "......KRRK......",
        ".....KRGGRK.....",
        ".....KRCCRK.....",
        "....KRRCCRRK....",
        "...KRRRRRRRRK...",
        "..KRRKCCCCKRRK..",
        ".KRRKCCGGCCKRRK.",
        "KRRGKRCCCCKRGRRK",
        "KKKKRRRRRRRRKKKK",
        "...KRRKRRKRRK...",
        "..KGGK.KK.KGGK..",
        "..KCCK....KCCK..",
        "...KK......KK...",
        "................",
        "................",
    ],
    # Royal Talon Fighter: Wakandan horned mask-shaped royal craft with violet vibranium engines.
    "nightglass": [
        "...KK......KK...",
        "..KSSK....KSSK..",
        "..KSSKK..KKSSK..",
        ".KSSsKKKKKKsSSK.",
        ".KSSKVVssVVKSSK.",
        "KSSKVVGGGGVVKSSK",
        "KSSKVVGssGVVKSsK",
        "KSSsKKGGGGKKsSSK",
        ".KSSsKSSSSKsSSK.",
        ".KSSKKSVVSKKSSK.",
        "..KK..KVVKK.KK..",
        "......KVVKK.....",
        ".......KK.......",
        "................",
        "................",
        "................",
    ],
    # Helicarrier: S.H.I.E.L.D. airborne aircraft carrier with 4 corner turbines & runway.
    "bastion": [
        "......KKKK......",
        ".KKK.KSSSSK.KKK.",
        "KCCCKKSssSKKCCCK",
        "KCSCKKSSSSKKCSCK",
        ".KKKKSsGGsSKKKK.",
        "...KSSsSSsSSK...",
        "...KSSsCCsSSK...",
        "...KSSsSSsSSK...",
        "...KSSsGGsSSK...",
        ".KKKKSsSSsSKKKK.",
        "KCSCKKSSSSKKCSCK",
        "KCCCKKssssKKCCCK",
        ".KKK..KCCK..KKK.",
        "......KKKK......",
        "................",
        "................",
    ],
    # Benatar: swept orange-gold Guardians starship with feathered wing blades.
    "longbow": [
        ".......KK.......",
        "......KGGK......",
        ".....KGCCGK.....",
        ".KK..KGCCGK..KK.",
        "KGGK.KGGGGK.KGGK",
        ".KGGKKGssGKKGGK.",
        "..KGGKGGGGKGGK..",
        "KKGGGGsSSsGGGGKK",
        ".KKGGGsSSsGGGKK.",
        "..KKGGKGGKGGKK..",
        "...KGGKCCKGGK...",
        "....KKKCCKKK....",
        "......K..K......",
        "................",
        "................",
        "................",
    ],
    # S.H.I.E.L.D. Dart: sleek stealth needle interceptor with swept cyan wings.
    "dart": [
        ".......KK.......",
        "......KSSK......",
        "......KCCK......",
        ".....KSSSSK.....",
        "....KSSCCSSK....",
        "...KSSsSSsSSK...",
        "..KSSsKSSKsSSK..",
        ".KSSsKSSSSKsSSK.",
        "KCCsKSSSSSSKsCCK",
        "KKKK.KSSSSK.KKKK",
        ".....KSSsSK.....",
        "....KCK..KCK....",
        "....KK....KK....",
        "................",
        "................",
        "................",
    ],
    # Latverian Barge: Doctor Doom's gothic armored dreadnought with emerald arcane core.
    "eclipse-barge": [
        "..KK........KK..",
        ".KSSK..KK..KSSK.",
        ".KSSKKGEEGKKSSK.",
        "KSSsKKEEEKKEsSSK",
        "KSSsKKEssEKsSSSK",
        "KSSsKKEEEKKEsSSK",
        ".KSSsKGGGGKsSSK.",
        ".KSSsKSSSSKsSSK.",
        "..KSSKsEEsKSSK..",
        "..KSSKsEEsKSSK..",
        "...KSSKSSKSSK...",
        "...KEEK..KEEK...",
        "....KK....KK....",
        "................",
        "................",
        "................",
    ],
}


def emblems():
    folder = ROOT / "mods/doomsday-systems/ships"
    for ship, rows in EMBLEMS.items():
        assert len(rows) == 16 and all(len(row) == 16 for row in rows), ship
        rects = []
        for y, row in enumerate(rows):
            x = 0
            while x < 16:
                end = x + 1
                while end < 16 and row[end] == row[x]:
                    end += 1
                if row[x] != ".":
                    rects.append(f'<rect x="{x}" y="{y}" width="{end - x}" height="1" fill="{EMBLEM_INK[row[x]]}"/>')
                x = end
        (folder / f"{ship}.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="32" height="32" '
            f'shape-rendering="crispEdges"><title>{escape(FLEET[ship][0])}</title>{"".join(rects)}</svg>', encoding="utf-8")


def draw_avengers_a(s, cx, cy, color):
    # Subtle pixel-art Avengers 'A' crest inside a circular ring.
    s.ring(cx, cy, 24, 21, color)
    s.line(cx - 12, cy + 16, cx + 2, cy - 18, 4, color)
    s.line(cx + 2, cy - 18, cx + 10, cy + 16, 4, color)
    s.line(cx - 8, cy + 4, cx + 14, cy + 4, 3, color)


def draw_vista(ship, dark):
    """Per-craft Marvel/Avengers exterior vista + subtle tactical ship projection."""
    s = Scene(dark, FLEET[ship][1])
    rng = random.Random(705 + sum(ord(c) for c in ship))
    for _ in range(75):
        s.rect(rng.randrange(W), rng.randrange(132), 1, 1, "star")

    if ship == "skyrunner":
        # Quinjet: Manhattan dusk skyline & Avengers Tower spire on the horizon.
        for bx, bw, bh in [(18, 22, 42), (44, 18, 56), (68, 24, 38), (98, 20, 48),
                           (124, 16, 36), (178, 22, 44), (206, 26, 52), (240, 20, 40), (266, 28, 46)]:
            s.rect(bx, 152 - bh, bw, bh, "city")
        # Iconic Avengers Tower silhouette in center-right skyline.
        s.poly([(144, 152), (144, 72), (168, 60), (174, 86), (166, 86), (166, 152)], "horizon")
        s.rect(152, 66, 10, 4, "glow")
        s.rect(156, 76, 4, 12, "glow")
        s.rect(0, 146, W, 34, "horizon")
    elif ship == "arrowhawk":
        # Avenjet: Upper atmosphere Earth curvature + subtle Avengers 'A' HUD crest.
        s.disc(160, 295, 195, "horizon")
        s.ring(160, 295, 197, 194, "glow")
        draw_avengers_a(s, 238, 68, "glow")
    elif ship == "nightglass":
        # Royal Talon: Wakandan mountains & Golden City spires.
        s.poly([(0, 148), (42, 92), (88, 122), (138, 84), (190, 118), (248, 86), (320, 126), (320, 180), (0, 180)], "city")
        for tx, tw, th in [(118, 10, 44), (134, 14, 58), (154, 12, 48), (172, 10, 38)]:
            s.rect(tx, 148 - th, tw, th, "horizon")
            s.rect(tx + 2, 148 - th + 6, tw - 4, 2, "glow")
            s.rect(tx + 2, 148 - th + 14, tw - 4, 2, "glow")
        s.ring(240, 62, 22, 19, "glow")
    elif ship == "bastion":
        # Helicarrier: Above-the-clouds horizon with twin wing-mounted rotor housings outside.
        for cx, cy, r in [(42, 116, 26), (82, 122, 22), (128, 118, 28), (186, 120, 26), (242, 114, 30), (288, 122, 24)]:
            s.disc(cx, cy, r, "horizon")
        s.rect(0, 116, W, 64, "horizon")
        # Outer Helicarrier turbine rings visible on left & right wings.
        s.ring(52, 96, 20, 14, "city")
        s.ring(268, 96, 20, 14, "city")
    elif ship == "longbow":
        # Benatar: Cosmic deep space with ringed planet (Titan/Knowhere vibe) & distant nebula clouds.
        s.disc(236, 64, 30, "planet")
        s.disc(246, 58, 27, "sky")
        s.line(192, 76, 282, 48, 3, "glow")
        s.disc(82, 54, 14, "horizon")
    elif ship == "dart":
        # S.H.I.E.L.D. Dart: High-altitude stratosphere arc & tactical speed markers.
        s.disc(160, 310, 205, "horizon")
        s.ring(160, 310, 207, 205, "glow")
        for x, y in [(26, 32), (48, 72), (278, 36), (264, 84)]:
            s.line(x, y, x + (16 if x > 160 else -16), y - 6, 1, "glow")
    else:
        # Latverian Barge: Castle Doom mountain crags, gothic spires & eclipsed moon.
        s.disc(246, 54, 28, "planet")
        s.disc(254, 50, 25, "sky")
        s.poly([(0, 150), (36, 98), (78, 134), (118, 86), (156, 124), (204, 92), (258, 132), (320, 96), (320, 180), (0, 180)], "city")
        # Castle Doom gothic towers silhouette.
        for sx, sh in [(110, 56), (122, 68), (134, 52)]:
            s.rect(sx, 140 - sh, 8, sh, "horizon")
            s.poly([(sx - 1, 140 - sh), (sx + 4, 126 - sh), (sx + 9, 140 - sh)], "horizon")
            s.rect(sx + 3, 146 - sh, 2, 5, "glow")

    # Subtle ship emblem hologram in upper right (except Avenjet which shows the Avengers 'A').
    if ship != "arrowhawk":
        emblem = ET.parse(ROOT / f"mods/doomsday-systems/ships/{ship}.svg").getroot()
        for rect in emblem.findall("{http://www.w3.org/2000/svg}rect"):
            x, y, w, h = (int(rect.attrib[k]) for k in ["x", "y", "width", "height"])
            ink = blend(rect.attrib["fill"], s.colors["sky"], 0.68 if dark else 0.74)
            s.rect(214 + x * 4, 36 + y * 4, w * 4, h * 4, ink)
    return s


def draw(ship, dark=True):
    s = draw_vista(ship, dark)
    if ship == "skyrunner":
        # Quinjet: angular tactical Avengers stealth canopy & twin flight consoles.
        s.window([(36, 18), (284, 18), (310, 52), (310, 126), (282, 148), (38, 148), (10, 126), (10, 52)],
                 rim=[(28, 12), (292, 12), (318, 48), (318, 132), (286, 156), (34, 156), (2, 132), (2, 48)])
        for a, b in [((68, 14), (88, 150)), ((252, 14), (232, 150)), ((160, 14), (160, 44))]:
            s.line(*a, *b, 5, "frame")
            s.line(*a, *b, 1, "edge")
        s.rect(0, 152, 320, 28, "hull")
        s.line(0, 152, 320, 152, 2, "accent")
        s.instruments(14, 158, 86, 20, 1)
        s.instruments(108, 155, 104, 24, 2)
        s.instruments(220, 158, 86, 20, 3)
    elif ship == "nightglass":
        # Royal Talon: geometric Wakandan angular viewport & vibranium Kimoyo dash.
        s.window([(66, 14), (160, 6), (254, 14), (304, 62), (292, 134), (242, 156), (78, 156), (28, 134), (16, 62)])
        for a, b in [((66, 14), (96, 156)), ((254, 14), (224, 156))]:
            s.line(*a, *b, 4, "frame")
            s.line(*a, *b, 1, "accent")
        s.poly([(0, 150), (320, 150), (320, 180), (0, 180)], "hull")
        s.line(78, 151, 242, 151, 2, "accent")
        s.instruments(20, 156, 84, 22, 4)
        s.instruments(216, 156, 84, 22, 5)
        s.ring(160, 166, 10, 7, "accent")
    elif ship == "bastion":
        # Helicarrier Command Bridge: wide slanted carrier glass & S.H.I.E.L.D. tactical deck.
        s.poly([(0, 0), (320, 0), (320, 18), (0, 18)], "frame")
        s.poly([(0, 130), (320, 130), (320, 180), (0, 180)], "hull")
        for x in [24, 92, 158, 224, 290]:
            s.poly([(x, 16), (x + 6, 16), (x + 14, 130), (x + 8, 130)], "frame")
            s.line(x + 3, 20, x + 11, 126, 1, "edge")
        s.rect(0, 128, 320, 3, "accent")
        s.instruments(10, 140, 114, 36, 6)
        s.instruments(196, 140, 114, 36, 7)
        s.poly([(136, 136), (184, 136), (196, 180), (124, 180)], "panel")
        s.rect(144, 146, 32, 3, "accent")
    elif ship == "eclipse-barge":
        # Latverian Barge: gothic iron-ribbed arched viewport & emerald arcane plinth.
        s.poly([(0, 0), (320, 0), (320, 26), (0, 26)], "hull")
        for points in [[(0, 0), (32, 0), (68, 146), (38, 154), (0, 82)],
                       [(320, 0), (288, 0), (252, 146), (282, 154), (320, 82)],
                       [(154, 0), (166, 0), (170, 148), (150, 148)]]:
            s.poly(points, "frame")
        s.rect(158, 22, 4, 122, "accent")
        s.poly([(0, 146), (320, 146), (320, 180), (0, 180)], "hull")
        s.line(0, 146, 320, 146, 2, "accent")
        s.instruments(28, 152, 114, 24, 8)
        s.instruments(178, 152, 114, 24, 9)
    else:
        # Avenjet, Benatar & S.H.I.E.L.D. Dart: distinct Stark / Guardians / S.H.I.E.L.D. canopies.
        if ship == "arrowhawk":
            ribs = [((22, 0), (84, 148)), ((298, 0), (236, 148))]
            # Subtle Stark HUD corner brackets.
            s.rect(24, 24, 16, 2, "accent")
            s.rect(24, 24, 2, 14, "accent")
            s.rect(280, 24, 16, 2, "accent")
            s.rect(294, 24, 2, 14, "accent")
        elif ship == "longbow":
            ribs = [((44, 0), (62, 150)), ((276, 0), (258, 150)), ((112, 0), (112, 143)), ((208, 0), (208, 143))]
            s.rect(30, 52, 12, 82, "panel")
            s.rect(278, 52, 12, 82, "panel")
            s.rect(32, 63, 8, 45, "accent")
            s.rect(280, 63, 8, 45, "accent")
        else:  # S.H.I.E.L.D. Dart sharp stealth canopy.
            ribs = [((0, 16), (116, 148)), ((320, 16), (204, 148)), ((116, 0), (144, 148)), ((204, 0), (176, 148))]
        s.rect(0, 0, 320, 8, "frame")
        for a, b in ribs:
            s.line(*a, *b, 7, "frame")
            s.line(*a, *b, 2, "edge")
        s.poly([(0, 143), (112, 149), (160, 139), (208, 149), (320, 143), (320, 180), (0, 180)], "hull")
        s.line(0, 146, 105, 154, 3, "accent")
        s.line(215, 154, 320, 146, 3, "accent")
        s.instruments(19, 157, 76, 22, 10)
        s.instruments(111, 150, 98, 30, 11)
        s.instruments(225, 157, 76, 22, 12)
        s.rect(149, 153, 22, 12, "glass")
        s.ring(160, 159, 4, 2, "accent")
    return s


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()
    emblems()
    DEST.mkdir(parents=True, exist_ok=True)
    scenes = []
    for ship, (title, _) in FLEET.items():
        for dark in [True, False]:
            scene = draw(ship, dark)
            target = DEST / ("eclipse" if dark else "vanguard")
            target.mkdir(parents=True, exist_ok=True)
            (target / f"{ship}.svg").write_text(scene.svg(title), encoding="utf-8")
            png(target / f"{ship}.png", scene.pixels, scale=2)
            if dark:
                scenes.append(scene)
    if args.preview:
        background = Scene(True, FLEET["skyrunner"][1]).colors["sky"]
        sheet = [[background] * (W * 2) for _ in range(H * 4)]
        for index, scene in enumerate(scenes):
            x, y = (index % 2) * W, (index // 2) * H
            for yy, row in enumerate(scene.pixels):
                sheet[y + yy][x:x + W] = row
        png(args.preview, sheet)
        print(f"Preview: {args.preview}")
    print(f"Built {len(FLEET) * 2} Avengers cockpit backgrounds (PNG + SVG) in {DEST}")


if __name__ == "__main__":
    main()
