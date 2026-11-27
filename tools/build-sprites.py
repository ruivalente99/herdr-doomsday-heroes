#!/usr/bin/env python3
"""Rebuild the 41 32×32 Avengers: Doomsday character sprites and weapon effects. Standard library only.

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
WEAPONS_DEST = DEST / "weapons"
INK = "#11151f"


class Sprite:
    def __init__(self, title, palette, width=SIZE, height=SIZE):
        self.title = title
        self.width = width
        self.height = height
        self.palette = {"K": INK, **palette}
        self.pixels = [[None] * width for _ in range(height)]

    def rect(self, x, y, w, h, color):
        assert color in self.palette, (self.title, color)
        assert 0 <= x < x + w <= self.width and 0 <= y < y + h <= self.height, (
            self.title, x, y, w, h, self.width, self.height
        )
        for row in self.pixels[y:y + h]:
            row[x:x + w] = [self.palette[color]] * w

    def stamp(self, x, y, rows):
        for dy, row in enumerate(rows):
            for dx, color in enumerate(row):
                if color != ".":
                    self.rect(x + dx, y + dy, 1, 1, color)

    def svg(self, display_w=36, display_h=36, mirror=False):
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" '
            f'width="{display_w}" height="{display_h}" shape-rendering="crispEdges">',
            f"  <title>{escape(self.title)} — pixel art</title>",
        ]
        for y, row in enumerate(self.pixels):
            active = list(reversed(row)) if mirror else row
            x = 0
            while x < self.width:
                color = active[x]
                end = x + 1
                while end < self.width and active[end] == color:
                    end += 1
                if color:
                    lines.append(
                        f'  <rect x="{x}" y="{y}" width="{end - x}" '
                        f'height="1" fill="{color}"/>'
                    )
                x = end
        return "\n".join([*lines, "</svg>", ""])


BASE = {"F": "#e8ae80", "s": "#bf805a", "W": "#f6f5ef"}


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


def ironman():
    # Mark armor: crimson plates, gold faceplate/biceps/thighs, glowing cyan Arc Reactor & eye slits.
    p = body("Iron Man", {
        "A": "#c8232c", "a": "#8e161e", "T": "#e8b938", "L": "#c8232c", "B": "#9e1922",
        "G": "#f4c542", "g": "#c49122", "E": "#5ce6ff", "e": "#d9fbff", "F": "#c8232c",
    }, head=False)
    # Helmet with iconic gold faceplate and forehead red crest.
    box(p, 10, 3, 12, 12, "A")
    p.rect(11, 4, 1, 10, "a")
    p.rect(12, 5, 8, 9, "G")
    p.rect(12, 5, 1, 9, "g")
    p.rect(14, 4, 4, 2, "A")
    p.rect(15, 5, 2, 1, "a")
    # Glowing cyan visor eyes & jaw slit.
    p.rect(12, 8, 3, 2, "K")
    p.rect(17, 8, 3, 2, "K")
    p.rect(12, 8, 3, 1, "E")
    p.rect(17, 8, 3, 1, "E")
    p.rect(13, 8, 1, 1, "e")
    p.rect(18, 8, 1, 1, "e")
    p.rect(14, 12, 4, 1, "K")
    # Gold biceps, thigh plates, and glowing Arc Reactor on chest.
    p.rect(7, 18, 3, 3, "G")
    p.rect(22, 18, 3, 3, "G")
    p.rect(7, 23, 3, 2, "G")
    p.rect(22, 23, 3, 2, "G")
    p.rect(11, 25, 4, 3, "G")
    p.rect(17, 25, 4, 3, "G")
    p.rect(12, 16, 8, 6, "A")
    p.stamp(14, 17, [".KK.", "KEeK", "KeEK", ".KK."])
    p.rect(10, 22, 12, 1, "g")
    return p


def cap():
    # Captain America: cobalt cowl with white A & wings, chest star, red/white stripes, red gloves/boots.
    p = body("Captain America", {
        "A": "#1f54a3", "a": "#143970", "T": "#6e4326", "L": "#1b498c", "B": "#c62828",
        "R": "#c62828", "r": "#8c1a1a", "U": "#2a66bd",
    })
    # Blue helmet covering top half of head + side wings + crisp forehead 'A'.
    p.rect(10, 2, 12, 8, "K")
    p.rect(11, 3, 10, 6, "A")
    p.rect(11, 3, 2, 6, "a")
    p.stamp(14, 4, [".W..", "W.W.", "WWW.", "W.W."])
    p.rect(9, 5, 1, 3, "W")
    p.rect(22, 5, 1, 3, "W")
    # Eyes peeking through cowl + chinstrap.
    p.rect(12, 9, 8, 2, "F")
    p.rect(13, 9, 2, 2, "K")
    p.rect(18, 9, 2, 2, "K")
    p.rect(13, 9, 1, 1, "W")
    p.rect(18, 9, 1, 1, "W")
    p.rect(11, 10, 1, 4, "A")
    p.rect(20, 10, 1, 4, "A")
    # Red gloves and boots.
    p.rect(7, 22, 3, 3, "R")
    p.rect(22, 22, 3, 3, "R")
    p.rect(11, 27, 4, 3, "R")
    p.rect(17, 27, 4, 3, "R")
    # White star on chest + crisp red & white vertical abdominal stripes.
    p.stamp(14, 16, [".WW.", "WWWW", ".WW.", "W..W"])
    for idx, x in enumerate(range(11, 21, 2)):
        p.rect(x, 21, 2, 2, "R" if idx % 2 == 0 else "W")
    p.rect(15, 23, 2, 1, "W")
    return p


def thor():
    # Thor: winged silver helm, golden blonde hair & beard, crimson cape, silver chest discs.
    p = body("Thor", {
        "A": "#2a3342", "a": "#1a202b", "T": "#8c6230", "L": "#242c38", "B": "#3d2d22",
        "C": "#c4232c", "c": "#87141c", "H": "#f0c84b", "h": "#c49725", "M": "#cfd8e3", "m": "#8e9ba8",
    }, cape=True)
    # Flowing golden hair + silver winged helmet.
    p.stamp(8, 2, [
        "..KKKKKKKKKKKK..",
        "KKKMMMMMMMMMMKKK",
        "KWWKMMMMMMMMKWWK",
        "KWWKmmmmmmmmKWWK",
        ".KKKHHHHHHHHKKK.",
    ])
    p.rect(9, 7, 2, 8, "H")
    p.rect(21, 7, 2, 8, "H")
    p.rect(10, 7, 1, 8, "h")
    # Blonde beard framing jaw.
    p.stamp(11, 11, ["HH......HH", "HHHHsHHHHH", ".HHhHHhHH.", "..HHHHHH.."])
    # Silver Asgardian chest armor discs and bracers.
    for x in (12, 18):
        for y in (16, 19, 21):
            p.rect(x, y, 2, 2 if y < 21 else 1, "M")
    p.rect(7, 21, 3, 3, "M")
    p.rect(22, 21, 3, 3, "M")
    return p


def hulk():
    # Hulk: massive wide muscular gamma-green brute, ragged black hair, tattered purple shorts.
    p = Sprite("Hulk", {
        **BASE, "A": "#4ea83c", "a": "#337826", "l": "#78cf60", "H": "#181c22", "h": "#2f3640",
        "P": "#6f3c9c", "p": "#4b246e",
    })
    # Wide muscular torso & huge arms.
    box(p, 3, 10, 26, 16, "A")
    box(p, 9, 24, 6, 7, "A")
    box(p, 17, 24, 6, 7, "A")
    box(p, 10, 3, 12, 10, "A")
    # Muscle highlights on shoulders, chest and biceps.
    p.rect(4, 11, 6, 3, "l")
    p.rect(22, 11, 6, 3, "l")
    p.rect(11, 13, 4, 4, "l")
    p.rect(17, 13, 4, 4, "l")
    p.rect(15, 13, 2, 5, "a")
    p.rect(4, 15, 2, 7, "a")
    p.rect(26, 15, 2, 7, "a")
    # Ragged black hair + furrowed angry brow + gritted teeth.
    p.stamp(9, 1, [
        "..KKKKKKKKKK..",
        ".KHHhHHHHhHHK.",
        "KHHHHHHHHHHHHK",
        "KHH.HHHHHH.HHK",
        "KH..........HK",
    ])
    p.rect(12, 7, 8, 1, "K")
    p.rect(13, 8, 2, 1, "W")
    p.rect(17, 8, 2, 1, "W")
    p.rect(13, 8, 1, 1, "K")
    p.rect(18, 8, 1, 1, "K")
    p.rect(13, 10, 6, 2, "K")
    p.rect(14, 10, 4, 1, "W")
    # Tattered purple shorts.
    p.rect(9, 21, 14, 4, "P")
    p.rect(10, 22, 2, 3, "p")
    p.rect(10, 25, 4, 2, "P")
    p.rect(18, 25, 4, 2, "P")
    p.rect(11, 26, 2, 1, "A")
    p.rect(19, 26, 1, 1, "A")
    # Huge fists & feet.
    p.rect(4, 22, 4, 3, "a")
    p.rect(24, 22, 4, 3, "a")
    p.rect(10, 29, 4, 1, "a")
    p.rect(18, 29, 4, 1, "a")
    return p


def widow():
    # Black Widow: slate-obsidian catsuit, fiery red wavy hair, red hourglass belt, cyan Widow's Bite cuffs.
    p = body("Black Widow", {
        "F": "#f0bba0", "s": "#c98d74", "A": "#2c3240", "a": "#1b1f29", "T": "#454e63",
        "L": "#242936", "B": "#181c24", "H": "#c93f22", "h": "#eb6938", "R": "#e32929", "C": "#5ce3ff",
    })
    # Flowing red hair framing face and shoulders.
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHhHHHHHK",
        "KHH......HHK",
        "KHH......HHK",
        "KH........HK",
    ])
    p.stamp(8, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", "KHK", "KK."])
    p.stamp(21, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", "KHK", ".KK"])
    # Tactical zipper line, glowing cyan wrist stingers, red hourglass buckle.
    p.rect(15, 16, 2, 6, "T")
    p.rect(7, 22, 3, 2, "C")
    p.rect(22, 22, 3, 2, "C")
    p.stamp(14, 22, ["RRRR", ".RR.", "RRRR"])
    return p


def hawkeye():
    # Hawkeye: charcoal & purple tactical vest, spiky brown hair, purple shades, shoulder arrow quiver.
    p = body("Hawkeye", {
        "A": "#242630", "a": "#161820", "T": "#4d4f5c", "L": "#1e2029", "B": "#161820",
        "P": "#7b43b8", "p": "#51287d", "V": "#b87cff", "H": "#6b472e", "h": "#946542",
    })
    # Arrow quiver peeking behind left shoulder with purple fletchings.
    p.stamp(6, 9, ["KVK.", "KPK.", "KPKK", "KaaK", "KaaK", "KaaK"])
    # Spiky brown hair.
    hair(p, [
        ".K.KK.KK.K..",
        ".KHKHHhKHK..",
        "KHHhHHHHHHHK",
        "KHHHHHHHHHHK",
        "KH........HK",
    ])
    # Iconic purple tactical visor/shades.
    p.rect(11, 8, 10, 3, "K")
    p.rect(12, 9, 3, 1, "V")
    p.rect(17, 9, 3, 1, "V")
    p.rect(15, 9, 2, 1, "P")
    # Purple chest chevron and harness strap.
    p.rect(11, 16, 10, 3, "P")
    p.rect(12, 17, 8, 1, "V")
    p.rect(11, 19, 3, 4, "p")
    p.rect(18, 19, 3, 4, "p")
    p.rect(22, 18, 3, 5, "F")
    p.rect(22, 22, 3, 2, "P")
    return p


def spiderman():
    # Spider-Man: bright red & cobalt blue suit, iconic big white angular lenses, black chest spider.
    p = body("Spider-Man", {
        "A": "#d9232e", "a": "#9e1520", "T": "#d9232e", "L": "#1c4ea8", "B": "#d9232e",
        "U": "#1c4ea8", "u": "#123475", "F": "#d9232e",
    }, head=False)
    # Full red mask with iconic symmetric large angled white Spider-Man lenses.
    box(p, 10, 3, 12, 12, "A")
    p.rect(11, 4, 1, 10, "a")
    p.stamp(11, 6, [
        "KK......KK",
        "KWWK..KWWK",
        "KWWKKKKWWK",
        ".KWWKKWWK.",
        "..KKKKKK..",
    ])
    # Blue sides, blue forearm stripes, red gloves, red boots, black chest spider.
    p.rect(7, 19, 3, 3, "U")
    p.rect(22, 19, 3, 3, "U")
    p.rect(10, 19, 2, 5, "U")
    p.rect(20, 19, 2, 5, "U")
    p.rect(11, 27, 4, 3, "A")
    p.rect(17, 27, 4, 3, "A")
    p.stamp(14, 17, ["K..K", ".KK.", "KKKK", "K..K"])
    return p


def strange():
    # Doctor Strange: crimson Cloak of Levitation with tall popped collar, silver temples, Eye of Agamotto.
    p = body("Doctor Strange", {
        "A": "#203b6b", "a": "#15284a", "T": "#8a5a2b", "L": "#182c50", "B": "#2b221e",
        "C": "#c9242e", "c": "#8c151d", "G": "#ebc046", "E": "#52eb87", "H": "#201e24", "h": "#d8dee8",
    }, cape=True)
    # High popped Cloak of Levitation collar flanking head.
    p.stamp(7, 8, ["KK.", "KCK", "KCK", "KcK", "KCK", "KCK", "KGK"])
    p.stamp(22, 8, [".KK", "KCK", "KCK", "KcK", "KCK", "KCK", "KGK"])
    # Dark hair with iconic silver-white temples & neat goatee.
    hair(p, [
        "..KKKKKKKK..",
        ".KHHHHHHHHK.",
        "KHHHHHHHHHHK",
        "KhH......HhK",
        "Kh........hK",
    ])
    p.stamp(14, 12, ["HHHH", ".HH."])
    # Gold Eye of Agamotto medallion with glowing emerald core.
    p.stamp(14, 16, [".GG.", "GEEG", ".GG."])
    p.rect(11, 21, 10, 2, "c")
    p.rect(15, 19, 2, 5, "G")
    return p


def wanda():
    # Scarlet Witch: iconic crimson horned tiara, auburn hair, crimson suit & coat, glowing chaos hands.
    p = body("Scarlet Witch", {
        "F": "#f0bda4", "s": "#c78e74", "A": "#b51c36", "a": "#7d1024", "T": "#591020",
        "L": "#47111e", "B": "#2b0b13", "C": "#99172e", "c": "#660d1d",
        "H": "#6e2e26", "h": "#9c4738", "R": "#eb2d4b", "E": "#ff638a",
    }, cape=True)
    # Long flowing auburn hair.
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
        "KHH......HHK",
        "KH........HK",
    ])
    p.stamp(8, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", "KHK", "KHK", ".K."])
    p.stamp(21, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", "KHK", "KHK", ".K."])
    # Unmistakable crimson horned Scarlet Witch tiara/crown!
    p.stamp(10, 1, [
        ".KK......KK.",
        "KRRK....KRRK",
        "KRRKK..KKRRK",
        ".KRRRRRRRRK.",
        "..KKRKKRKK..",
    ])
    # Glowing scarlet chaos hands & chest diamond.
    p.rect(7, 23, 3, 2, "E")
    p.rect(22, 23, 3, 2, "E")
    p.stamp(14, 17, [".RR.", "REER", ".RR."])
    return p


def panther():
    # Black Panther: obsidian vibranium suit, symmetric pointed cat ears, white eye slits, silver-violet necklace.
    p = body("Black Panther", {
        "A": "#282c38", "a": "#191c24", "T": "#454c61", "L": "#222630", "B": "#171a22",
        "V": "#b075ff", "v": "#e2c7ff", "S": "#cfd7e8", "F": "#282c38",
    }, head=False)
    # Symmetric pointed panther ears + sleek vibranium cowl.
    p.stamp(10, 1, ["KK........KK", "KAK......KAK"])
    box(p, 10, 3, 12, 12, "A")
    p.rect(11, 4, 1, 10, "a")
    # Sharp white panther eye slits + subtle silver brow lines.
    p.rect(12, 8, 3, 1, "W")
    p.rect(17, 8, 3, 1, "W")
    p.rect(15, 5, 2, 3, "T")
    # Iconic silver & glowing violet kinetic claw necklace + chest kinetic lines.
    p.stamp(11, 16, ["S.V.S..S.V.S", ".S.V.SS.V.S."])
    p.rect(12, 19, 2, 3, "V")
    p.rect(18, 19, 2, 3, "V")
    p.rect(7, 22, 3, 1, "V")
    p.rect(22, 22, 3, 1, "V")
    return p


def vision():
    # Vision: crimson synthezoid face, glowing yellow Mind Stone gem, teal armor, bright golden cape.
    p = body("Vision", {
        "F": "#b8324c", "s": "#872035", "A": "#2a7d6a", "a": "#1b5447", "T": "#e8bc3c",
        "L": "#256e5d", "B": "#e8bc3c", "C": "#ebc03d", "c": "#b88c1d", "G": "#ffe766", "R": "#b8324c",
    }, cape=True)
    # Head markings + iconic bright yellow Mind Stone gem on forehead.
    p.rect(11, 4, 10, 2, "A")
    p.rect(15, 5, 2, 2, "G")
    p.rect(15, 5, 1, 1, "W")
    p.rect(11, 11, 1, 3, "A")
    p.rect(20, 11, 1, 3, "A")
    # Crimson chest panels, golden cape collar & diamond crest.
    p.rect(10, 15, 12, 2, "C")
    p.rect(12, 18, 8, 4, "R")
    p.stamp(14, 18, [".GG.", "GGGG", ".GG."])
    p.rect(7, 17, 3, 4, "R")
    p.rect(22, 17, 3, 4, "R")
    p.rect(7, 23, 3, 2, "C")
    p.rect(22, 23, 3, 2, "C")
    return p


def loki():
    # Loki: tall sweeping golden horned crown, emerald cape, green & gold Asgardian tunic.
    p = body("Loki", {
        "F": "#efd0b6", "s": "#c49c7e", "A": "#216b3e", "a": "#144728", "T": "#e6ba3c",
        "L": "#183324", "B": "#1c1f22", "C": "#1e6338", "c": "#124024",
        "G": "#ecc03d", "g": "#b58b1b", "H": "#181b21",
    }, cape=True)
    # Sweeping golden horns curving high above the head!
    p.stamp(7, 0, [
        "KK..............KK",
        "KGK............KGK",
        ".KGK..........KGK.",
        "..KGKKKKKKKKKKGK..",
        "..KGGGGGGGGGGGGK..",
        "..KggHHHHHHHHggK..",
    ])
    p.rect(10, 6, 2, 8, "H")
    p.rect(20, 6, 2, 8, "H")
    # Gold Asgardian chest chevrons & shoulder pauldrons.
    p.rect(10, 15, 3, 2, "G")
    p.rect(19, 15, 3, 2, "G")
    p.stamp(13, 17, ["G....G", ".G..G.", "..GG..", ".G..G."])
    p.rect(7, 23, 3, 2, "G")
    p.rect(22, 23, 3, 2, "G")
    return p


def fury():
    # Nick Fury: bald head, black eyepatch & strap, stern goatee, black S.H.I.E.L.D. leather trench coat.
    p = body("Nick Fury", {
        "F": "#734730", "s": "#523120", "A": "#2c313b", "a": "#1b1e26", "T": "#4d5566",
        "L": "#232730", "B": "#171a21", "S": "#b0bac9", "h": "#946144",
    })
    # Subtle bald head highlight + iconic eyepatch & diagonal strap over left eye.
    p.rect(13, 4, 4, 1, "h")
    p.stamp(15, 5, [
        ".....KK",
        "....KK.",
        "...KK..",
        "..KKKK.",
        "..KKKK.",
    ])
    # Neat dark goatee.
    p.stamp(14, 12, ["KKKK", ".KK."])
    # Trench coat lapels, turtleneck & S.H.I.E.L.D. silver badge.
    p.rect(13, 15, 6, 8, "a")
    p.rect(14, 15, 4, 2, "T")
    p.rect(11, 16, 2, 6, "T")
    p.rect(19, 16, 2, 6, "T")
    p.rect(12, 18, 2, 2, "S")
    return p


def doombot():
    # Doombot: repeatable Latverian robotic drone — steel faceplate, green hood/plates, glowing green visor.
    p = body("Doombot", {
        "A": "#6f7a85", "a": "#4a535c", "T": "#264d33", "L": "#56606b", "B": "#384047",
        "M": "#8a96a3", "m": "#5d6873", "G": "#2b5c3c", "E": "#4dff7a", "e": "#ccffd8", "F": "#6f7a85",
    }, head=False)
    # Green drone hood over brushed steel faceplate.
    box(p, 9, 2, 14, 13, "G")
    box(p, 11, 5, 10, 10, "M")
    p.rect(12, 6, 1, 8, "m")
    # Single glowing neon-green robot visor + grill lines.
    p.rect(12, 8, 8, 3, "K")
    p.rect(12, 9, 8, 1, "E")
    p.rect(15, 9, 2, 1, "e")
    p.rect(14, 12, 4, 1, "m")
    # Green chest tabard & mechanical vents.
    p.rect(12, 16, 8, 7, "G")
    p.rect(15, 18, 2, 2, "E")
    for y in (21,):
        p.rect(13, y, 6, 1, "a")
    return p


def doom():
    # Doctor Doom: iconic deep emerald hooded cloak, riveted iron mask, gold clasps, steel armor & glowing eyes.
    p = body("Doctor Doom", {
        "A": "#8e9ba8", "a": "#5d6873", "T": "#6e4526", "L": "#7a8794", "B": "#4d5661",
        "C": "#1e6b3a", "c": "#114524", "G": "#ecc042", "g": "#b58b1f",
        "M": "#a6b3bf", "m": "#717e8a", "E": "#6eff9c", "F": "#8e9ba8",
    }, cape=True, head=False)
    # Deep emerald hood framing the shadowed iron mask.
    box(p, 8, 1, 16, 15, "C")
    p.rect(9, 2, 2, 13, "c")
    p.rect(21, 2, 2, 13, "c")
    box(p, 11, 5, 10, 10, "M")
    p.rect(12, 6, 1, 8, "m")
    # Deep shadowed eye sockets with piercing glowing green eyes + iron mask mouth grille.
    p.rect(12, 8, 3, 2, "K")
    p.rect(17, 8, 3, 2, "K")
    p.rect(13, 9, 2, 1, "E")
    p.rect(17, 9, 2, 1, "E")
    p.rect(13, 12, 6, 2, "K")
    for x in (14, 16, 18):
        p.rect(x, 12, 1, 2, "m")
    # Emerald tunic over steel plate + iconic twin gold cloak medallions + gold belt buckle.
    p.rect(11, 15, 10, 9, "C")
    p.rect(12, 16, 1, 7, "c")
    p.rect(10, 15, 2, 2, "G")
    p.rect(20, 15, 2, 2, "G")
    p.rect(15, 23, 2, 1, "G")
    p.rect(12, 24, 8, 2, "C")
    return p


def sam():
    # Sam Wilson / Captain America: white & cobalt vibranium suit, red goggles, twin vibranium wingtips.
    p = body("Sam Wilson", {
        "F": "#7c4b30", "s": "#593420", "A": "#eef2f7", "a": "#bcc7d6", "T": "#1e52a3",
        "L": "#1c4a91", "B": "#252b36", "U": "#1e52a3", "R": "#d62b34", "S": "#9fb0c4", "m": "#667587",
        "H": "#191c22",
    })
    # Vibranium wingtips rising cleanly behind shoulders.
    p.stamp(1, 11, ["KK....", "KSSK..", ".KSSK.", "..KSmK", "..KSmK", "...KUK", "...KUK", "....KK"])
    p.stamp(25, 11, ["....KK", "..KSSK", ".KSSK.", "KmSK..", "KmSK..", "KUK...", "KUK...", "KK...."])
    # Short dark hair + white cowl side-pieces + iconic crimson-lensed tactical goggles.
    p.rect(11, 3, 10, 3, "H")
    p.rect(10, 6, 2, 8, "A")
    p.rect(20, 6, 2, 8, "A")
    p.rect(11, 8, 10, 3, "K")
    p.rect(12, 9, 3, 1, "R")
    p.rect(17, 9, 3, 1, "R")
    p.rect(15, 9, 2, 1, "S")
    # Blue shoulders, crimson chest stripes & crisp silver/blue star emblem.
    p.rect(7, 17, 3, 4, "U")
    p.rect(22, 17, 3, 4, "U")
    p.rect(10, 16, 12, 2, "U")
    p.rect(10, 21, 12, 2, "R")
    p.stamp(14, 17, [".UU.", "UWWU", ".UU.", "U..U"])
    p.rect(7, 23, 3, 2, "R")
    p.rect(22, 23, 3, 2, "R")
    return p


def antman():
    # Scott Lang / Ant-Man: silver Pym helmet, glowing red visor & antennae, red/black tactical suit.
    p = body("Ant-Man", {
        "A": "#b8232d", "a": "#7d151d", "T": "#9ea9b5", "L": "#262a33", "B": "#22262e",
        "D": "#262a33", "M": "#c2ccd6", "m": "#828e99", "R": "#e02b38", "E": "#ff7882", "F": "#c2ccd6",
    }, head=False)
    # Brushed steel helmet with antennae tips, red lenses and breather grille.
    p.stamp(10, 1, [".K........K.", ".K........K."])
    box(p, 10, 3, 12, 12, "M")
    p.rect(11, 4, 1, 10, "m")
    p.rect(14, 4, 4, 2, "R")
    p.rect(11, 7, 10, 3, "K")
    p.rect(12, 8, 3, 1, "R")
    p.rect(17, 8, 3, 1, "R")
    p.rect(13, 8, 1, 1, "E")
    p.rect(18, 8, 1, 1, "E")
    p.rect(13, 11, 6, 3, "D")
    p.rect(15, 11, 2, 3, "m")
    # Black side panels, silver Pym piping, red center & glowing regulator buckle.
    p.rect(7, 17, 3, 6, "D")
    p.rect(22, 17, 3, 6, "D")
    p.rect(10, 16, 2, 7, "D")
    p.rect(20, 16, 2, 7, "D")
    p.rect(14, 16, 4, 7, "M")
    p.rect(15, 17, 2, 5, "A")
    p.rect(15, 23, 2, 1, "E")
    return p


def cassie():
    # Cassie Lang: purple & silver Quantum Pym helmet & suit with glowing violet visor.
    p = body("Cassie Lang", {
        "A": "#7b42b8", "a": "#502680", "T": "#b8c3cf", "L": "#422469", "B": "#2a2038",
        "M": "#c4ced9", "m": "#84909e", "V": "#d494ff", "E": "#f0d4ff", "D": "#2d2538", "F": "#c4ced9",
    }, head=False)
    # Sleek purple-and-silver Pym helmet with antennae & glowing lavender visor.
    p.stamp(10, 1, [".K........K.", ".K........K."])
    box(p, 10, 3, 12, 12, "A")
    p.rect(11, 4, 1, 10, "a")
    p.rect(14, 4, 4, 2, "M")
    p.rect(11, 7, 10, 3, "K")
    p.rect(12, 8, 8, 1, "V")
    p.rect(13, 8, 2, 1, "E")
    p.rect(17, 8, 2, 1, "E")
    p.rect(13, 11, 6, 3, "M")
    p.rect(15, 12, 2, 2, "m")
    # Silver chest harness, dark side panels, glowing violet Pym core.
    p.rect(7, 18, 3, 5, "D")
    p.rect(22, 18, 3, 5, "D")
    p.rect(11, 16, 2, 7, "M")
    p.rect(19, 16, 2, 7, "M")
    p.rect(15, 18, 2, 2, "V")
    p.rect(15, 23, 2, 1, "V")
    return p


def shangchi():
    # Shang-Chi: crimson dragon-scale combat tunic, black sleeves, glowing golden Ten Rings on forearms.
    p = body("Shang-Chi", {
        "F": "#e8b48a", "s": "#be865e", "A": "#b8242c", "a": "#7d161c", "T": "#23262e",
        "L": "#23262e", "B": "#17191f", "D": "#23262e", "H": "#1a1d24", "h": "#393e4d",
        "G": "#ffd048", "g": "#e0951f",
    })
    # Swept dark hair.
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
        "KH........HK",
    ])
    # Black sleeves with glowing stacked golden Ten Rings on both forearms!
    p.rect(7, 17, 3, 7, "D")
    p.rect(22, 17, 3, 7, "D")
    for y in (20, 22):
        p.rect(7, y, 3, 1, "G")
        p.rect(22, y, 3, 1, "G")
    p.rect(7, 21, 3, 1, "g")
    p.rect(22, 21, 3, 1, "g")
    # Diagonal black/crimson dragon-scale chest armor & subtle gold collar trim.
    p.rect(10, 16, 2, 7, "D")
    p.rect(20, 16, 2, 7, "D")
    p.stamp(13, 16, ["D....D", ".D..D.", "..DD..", ".G..G.", "D....D"])
    return p


def mbaku():
    # M'Baku: Jabari leader with fluffy white fur mantle, dark wood/bronze armor & full beard.
    p = body("M'Baku", {
        "F": "#6b3e26", "s": "#4a2918", "A": "#543625", "a": "#382216", "T": "#c99642",
        "L": "#3d281c", "B": "#2b1c14", "H": "#181a1f", "G": "#c99642", "W": "#f2f0e6", "w": "#c7c3b4",
    })
    # Cropped black hair & bold Jabari beard.
    p.rect(11, 3, 10, 3, "H")
    p.stamp(11, 11, ["HH......HH", "HHHHsHHHHH", ".HHHHHHHH.", "..HHHHHH.."])
    # Wide iconic white Jabari gorilla-fur shoulder mantle!
    box(p, 5, 14, 22, 6, "W")
    p.rect(6, 15, 2, 4, "w")
    p.rect(24, 15, 2, 4, "w")
    p.rect(12, 16, 8, 3, "A")
    # Bronze/gold pectoral bands & bracers.
    p.rect(12, 17, 8, 1, "G")
    p.rect(14, 19, 4, 4, "G")
    p.rect(7, 21, 3, 2, "G")
    p.rect(22, 21, 3, 2, "G")
    return p


def falcon():
    # Joaquin Torres / Falcon: olive-green & gunmetal winged EXO-7 suit with bright amber goggles.
    p = body("Falcon", {
        "F": "#c98b63", "s": "#9c6544", "A": "#3d6b47", "a": "#26472e", "T": "#4a535e",
        "L": "#2b4732", "B": "#22272e", "M": "#9aa6b2", "G": "#f5b83d", "g": "#ffe999", "H": "#1e1a18",
    })
    # Olive & silver wings rising cleanly behind shoulders.
    p.stamp(1, 11, ["KK....", "KAMK..", ".KAMK.", "..KaaK", "..KaaK", "...KAK", "...KAK", "....KK"])
    p.stamp(25, 11, ["....KK", "..KMAK", ".KMAK.", "KaaK..", "KaaK..", "KAK...", "KAK...", "KK...."])
    # Short dark hair + iconic amber tactical visor goggles.
    p.rect(11, 3, 10, 3, "H")
    p.rect(11, 8, 10, 3, "K")
    p.rect(12, 9, 3, 1, "G")
    p.rect(17, 9, 3, 1, "G")
    p.rect(13, 9, 1, 1, "g")
    p.rect(18, 9, 1, 1, "g")
    p.rect(15, 9, 2, 1, "M")
    # Silver chest chevron & shoulder plates.
    p.stamp(12, 16, ["M......M", ".M....M.", "..M..M..", "...MM..."])
    p.rect(7, 17, 3, 3, "M")
    p.rect(22, 17, 3, 3, "M")
    return p


def peggy():
    # Peggy Carter: iconic 1940s crimson fedora hat, wavy chestnut hair, navy SSR coat & red tie.
    p = body("Peggy Carter", {
        "F": "#f0bba0", "s": "#c98e73", "A": "#1e3a6e", "a": "#13264a", "T": "#8c1a22",
        "L": "#182f59", "B": "#2b1c18", "U": "#1e3a6e", "R": "#c9242e", "r": "#8c151d", "H": "#59321e", "h": "#824c30",
    })
    # Iconic wide-brimmed crimson fedora hat with navy band!
    p.stamp(7, 1, [
        "....KKKKKKKK....",
        "...KRRRRRRRRK...",
        "..KRRrRRRRrRRK..",
        ".KRUUUUUUUUUURK.",
        "KRRRRRRRRRRRRRRK",
        ".KKKKKKKKKKKKKK.",
    ])
    # Wavy chestnut hair framing face.
    p.stamp(9, 7, ["KH", "KH", "Kh", "KH", "KH", "KH", "KK"])
    p.stamp(21, 7, ["HK", "HK", "hK", "HK", "HK", "HK", "KK"])
    p.rect(15, 12, 3, 1, "R")
    # White shirt collar, crimson tie & brass SSR lapel buttons.
    p.rect(13, 15, 6, 4, "W")
    p.rect(15, 16, 2, 6, "R")
    p.rect(12, 19, 1, 1, "T")
    p.rect(19, 19, 1, 1, "T")
    return p


def deadpool():
    # Deadpool: red & black mask with expressive asymmetric white eyes, crossed twin katana hilts behind back.
    p = body("Deadpool", {
        "A": "#c9202b", "a": "#8c131c", "T": "#593928", "L": "#20232b", "B": "#181a20",
        "D": "#20232b", "M": "#aeb8c4", "F": "#c9202b",
    }, head=False)
    # Crossed katana hilts peeking over both shoulders!
    p.stamp(6, 10, ["KK..", "KMK.", ".KDK", "..KD"])
    p.stamp(22, 10, ["..KK", ".KMK", "KDK.", "DK.."])
    # Full crimson mask with black eye patches and asymmetric expressive white eyes!
    box(p, 10, 3, 12, 12, "A")
    p.rect(11, 4, 1, 10, "a")
    p.stamp(11, 7, [
        ".KK....KK.",
        "KWWK..KWWK",
        "KWWK..KKKK",
        ".KK....KK.",
    ])
    # Tactical black shoulders, forearm wraps, red chest/belt buckle.
    p.rect(7, 17, 3, 3, "D")
    p.rect(22, 17, 3, 3, "D")
    p.rect(7, 22, 3, 3, "D")
    p.rect(22, 22, 3, 3, "D")
    p.rect(10, 16, 2, 7, "D")
    p.rect(20, 16, 2, 7, "D")
    p.rect(14, 16, 4, 6, "A")
    p.rect(15, 22, 2, 2, "A")
    p.rect(11, 25, 4, 2, "A")
    p.rect(17, 25, 4, 2, "A")
    return p


def mrfantastic():
    # Mister Fantastic (Reed Richards): F4 sky-blue & white suit with "4" chest emblem, silver temples & goatee.
    p = body("Mister Fantastic", {
        "F": "#e8ae84", "s": "#bd825b", "A": "#2b7de0", "a": "#1c58a6", "T": "#f2f5fa",
        "L": "#2b7de0", "B": "#f2f5fa", "H": "#4d3629", "h": "#cfd8e3", "W": "#f2f5fa",
    })
    # Brown hair with iconic silver-white temples & neat goatee/moustache.
    hair(p, [
        "..KKKKKKKK..",
        ".KHHHHHHHHK.",
        "KHHHHHHHHHHK",
        "KhH......HhK",
        "Kh........hK",
    ])
    p.stamp(14, 12, ["HHHH", ".HH."])
    # Retro-futuristic F4 white collar, white gloves, white boots & circular "4" chest badge.
    p.rect(11, 15, 10, 2, "W")
    p.rect(7, 22, 3, 3, "W")
    p.rect(22, 22, 3, 3, "W")
    p.stamp(14, 18, ["WWWW", "WAWW", "WAAW", "WWWW"])
    p.rect(15, 19, 2, 1, "a")
    return p


def invisiblewoman():
    # Invisible Woman (Sue Storm): F4 sky-blue & white suit, golden blonde hair, glowing cyan psionic hands.
    p = body("Invisible Woman", {
        "F": "#f2bfa4", "s": "#c99277", "A": "#2b7de0", "a": "#1c58a6", "T": "#f2f5fa",
        "L": "#2b7de0", "B": "#f2f5fa", "H": "#ebd06c", "h": "#c4a33b", "C": "#7ceeff", "c": "#d9fcff",
    })
    # Flowing blonde hair framing face and shoulders.
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
        "KHH......HHK",
        "KH........HK",
    ])
    p.stamp(8, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", "KHK", "KK."])
    p.stamp(21, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", "KHK", ".KK"])
    # White F4 collar, chest badge, glowing translucent cyan psionic energy hands!
    p.rect(11, 15, 10, 2, "W")
    p.stamp(14, 18, ["WWWW", "WAWW", "WAAW", "WWWW"])
    p.rect(7, 22, 3, 3, "C")
    p.rect(22, 22, 3, 3, "C")
    p.rect(8, 23, 1, 1, "c")
    p.rect(23, 23, 1, 1, "c")
    return p


def humantorch():
    # Human Torch (Johnny Storm): FLAME ON! Blazing yellow-orange-red fiery aura, white-hot eyes & flames.
    p = body("Human Torch", {
        "A": "#f26b1d", "a": "#c43814", "T": "#ffd84d", "L": "#e04c18", "B": "#b82914",
        "Y": "#ffe85c", "O": "#ff8824", "R": "#d92e18", "E": "#fffde6", "F": "#ff8824",
    }, head=False)
    # Roaring crown of flames licking above head!
    p.stamp(10, 0, [
        "..K..KK..K..",
        ".KRKKYYKKRK.",
        "KROYYYYYYORK",
    ])
    box(p, 10, 3, 12, 12, "Y")
    p.rect(11, 4, 1, 10, "O")
    p.rect(20, 4, 1, 10, "O")
    # Blazing white-hot eyes & fiery grin.
    p.rect(12, 8, 3, 2, "R")
    p.rect(17, 8, 3, 2, "R")
    p.rect(13, 8, 2, 1, "E")
    p.rect(17, 8, 2, 1, "E")
    p.rect(14, 12, 4, 1, "O")
    # Supernova chest glow & flame hands.
    p.rect(12, 16, 8, 6, "O")
    p.stamp(14, 17, [".YY.", "YEEY", "YEEY", ".YY."])
    p.rect(7, 22, 3, 3, "Y")
    p.rect(22, 22, 3, 3, "Y")
    p.rect(8, 23, 1, 1, "E")
    p.rect(23, 23, 1, 1, "E")
    return p


def thing():
    # The Thing (Ben Grimm): massive wide rocky orange crag physique, heavy brow, blue eyes, F4 blue trunks.
    p = Sprite("The Thing", {
        **BASE, "A": "#d9752b", "a": "#a64f17", "l": "#f2a450", "d": "#75330c",
        "U": "#2b7de0", "u": "#1c58a6", "E": "#6bc4ff",
    })
    # Wide muscular rocky torso, huge arms & heavy head.
    box(p, 3, 10, 26, 16, "A")
    box(p, 9, 24, 6, 7, "A")
    box(p, 17, 24, 6, 7, "A")
    box(p, 10, 3, 12, 10, "A")
    # Craggy rock plate seams & warm highlights on shoulders, chest and brow.
    p.rect(4, 11, 6, 3, "l")
    p.rect(22, 11, 6, 3, "l")
    p.rect(11, 13, 4, 4, "l")
    p.rect(17, 13, 4, 4, "l")
    for x, y, w, h in [(15, 12, 2, 7), (4, 16, 4, 1), (24, 16, 4, 1), (11, 17, 10, 1), (13, 5, 6, 1)]:
        p.rect(x, y, w, h, "d")
    # Heavy rocky brow, bright blue eyes & determined frown.
    p.rect(11, 7, 10, 1, "d")
    p.rect(12, 8, 3, 1, "W")
    p.rect(17, 8, 3, 1, "W")
    p.rect(13, 8, 1, 1, "E")
    p.rect(18, 8, 1, 1, "E")
    p.rect(13, 11, 6, 1, "d")
    # Classic Fantastic Four blue shorts & crisp white belt!
    p.rect(9, 21, 14, 4, "U")
    p.rect(9, 21, 14, 1, "W")
    p.rect(10, 22, 2, 3, "u")
    p.rect(10, 25, 4, 2, "U")
    p.rect(18, 25, 4, 2, "U")
    # Huge rocky fists & feet.
    p.rect(4, 22, 4, 3, "a")
    p.rect(24, 22, 4, 3, "a")
    p.rect(10, 29, 4, 1, "a")
    p.rect(18, 29, 4, 1, "a")
    return p


def yelena():
    # Yelena Belova: crisp white tactical suit, dark olive pocketed utility vest, blonde hair, blue stingers.
    p = body("Yelena Belova", {
        "F": "#f2bfa6", "s": "#c99177", "A": "#e8edf5", "a": "#b5c0cf", "T": "#333d38",
        "L": "#dce3ed", "B": "#22262e", "V": "#333d38", "v": "#1f2622", "H": "#ebd786", "h": "#c4ad54",
        "C": "#6be6ff",
    })
    # Platinum blonde hair framing face.
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
        "KHH......HHK",
        "KH........HK",
    ])
    p.stamp(8, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", "KK."])
    p.stamp(21, 6, ["KHK", "KHK", "KhK", "KHK", "KHK", ".KK"])
    # Iconic dark olive utility vest with pockets over white suit!
    p.rect(10, 16, 12, 7, "V")
    p.rect(11, 17, 4, 2, "v")
    p.rect(17, 17, 4, 2, "v")
    p.rect(11, 20, 4, 2, "v")
    p.rect(17, 20, 4, 2, "v")
    p.rect(15, 16, 2, 7, "a")
    # Glowing cyan Widow wrist cuffs.
    p.rect(7, 22, 3, 2, "C")
    p.rect(22, 22, 3, 2, "C")
    return p


def bucky():
    # Bucky Barnes / Winter Soldier: dark tactical combat jacket, swept brown hair, gleaming Vibranium bionic arm!
    p = body("Winter Soldier", {
        "F": "#ebb48c", "s": "#bf8762", "A": "#2a303d", "a": "#1a1e26", "T": "#4c5466",
        "L": "#222733", "B": "#171a22", "H": "#3d2a1f", "h": "#614433",
        "M": "#7b8799", "m": "#4a5361", "G": "#ecc042",
    })
    # Swept brown hair & rugged beard/stubble.
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
        "KH........HK",
    ])
    p.stamp(9, 7, ["KH", "KH", "KH", "KK"])
    p.stamp(21, 7, ["HK", "HK", "HK", "KK"])
    p.stamp(13, 12, ["HHHHHH", ".HHHH."])
    # Iconic Vibranium bionic left arm (viewer's right) with Wakandan gold filigree lines!
    p.rect(22, 17, 3, 8, "M")
    p.rect(22, 17, 1, 8, "m")
    p.rect(22, 18, 3, 1, "G")
    p.rect(22, 21, 3, 1, "G")
    p.rect(22, 24, 3, 1, "m")
    # Tactical chest harness & buckle.
    p.rect(12, 16, 2, 7, "T")
    p.rect(18, 16, 2, 7, "T")
    p.rect(14, 18, 4, 2, "a")
    return p


def usagent():
    # John Walker / U.S. Agent: matte-black tactical Cap helmet & armor with bold crimson-and-white stripes.
    p = body("U.S. Agent", {
        "A": "#242936", "a": "#161922", "T": "#4a3326", "L": "#1e232e", "B": "#2b1c1c",
        "R": "#c9242b", "r": "#8c151b", "W": "#eef2f7",
    })
    # Matte black helmet with white 'A' & chinstrap.
    p.rect(10, 2, 12, 8, "K")
    p.rect(11, 3, 10, 6, "A")
    p.rect(11, 3, 2, 6, "a")
    p.stamp(14, 4, [".W..", "W.W.", "WWW.", "W.W."])
    p.rect(12, 9, 8, 2, "F")
    p.rect(13, 9, 2, 2, "K")
    p.rect(18, 9, 2, 2, "K")
    p.rect(13, 9, 1, 1, "W")
    p.rect(18, 9, 1, 1, "W")
    p.rect(11, 10, 1, 4, "A")
    p.rect(20, 10, 1, 4, "A")
    # Bold red & white tactical chest stripes & star.
    p.rect(11, 16, 10, 3, "R")
    p.stamp(14, 16, [".WW.", "WWWW", ".WW."])
    for idx, x in enumerate(range(11, 21, 2)):
        p.rect(x, 20, 2, 3, "W" if idx % 2 == 0 else "R")
    p.rect(7, 22, 3, 3, "R")
    p.rect(22, 22, 3, 3, "R")
    return p


def redguardian():
    # Alexei Shostakov / Red Guardian: bold crimson super-soldier suit, helmet with star, bushy brown beard.
    p = body("Red Guardian", {
        "A": "#c42228", "a": "#871419", "T": "#593826", "L": "#9e1b20", "B": "#291c18",
        "W": "#f2f0e6", "H": "#633d24", "h": "#8c5b3a",
    })
    # Crimson Soviet helmet with crisp white star!
    p.rect(10, 2, 12, 8, "K")
    p.rect(11, 3, 10, 6, "A")
    p.rect(11, 3, 2, 6, "a")
    p.stamp(14, 4, [".WW.", "WWWW", ".WW."])
    p.rect(12, 9, 8, 2, "F")
    p.rect(13, 9, 2, 2, "K")
    p.rect(18, 9, 2, 2, "K")
    p.rect(13, 9, 1, 1, "W")
    p.rect(18, 9, 1, 1, "W")
    # Big bushy brown beard framing jaw!
    p.stamp(10, 11, ["HHH....HHH", "HHHHssHHHH", ".HHhHHhHH.", "..HHHHHH.."])
    # Bold white shoulder stripes & big white Soviet chest star!
    p.rect(7, 17, 3, 2, "W")
    p.rect(22, 17, 3, 2, "W")
    p.stamp(14, 17, [".WW.", "WWWW", ".WW.", "W..W"])
    p.rect(10, 21, 12, 2, "W")
    return p


def sentry():
    # Bob Reynolds / Sentry: radiant golden-yellow suit, deep navy cape, flowing golden hair & bold 'S' belt.
    p = body("Sentry", {
        "F": "#f0bc94", "s": "#c48d68", "A": "#f0c230", "a": "#bf8f18", "T": "#1b3678",
        "L": "#e6b525", "B": "#1b3678", "C": "#1b3678", "c": "#10224f",
        "H": "#f5d76e", "h": "#cfa736", "G": "#fff08a", "E": "#fffbe0",
    }, cape=True)
    # Flowing golden hair!
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
        "KHH......HHK",
        "KH........HK",
    ])
    p.stamp(8, 6, ["KHK", "KHK", "KhK", "KHK", "KK."])
    p.stamp(21, 6, ["KHK", "KHK", "KhK", "KHK", ".KK"])
    # Glowing solar eyes!
    p.rect(13, 9, 2, 1, "E")
    p.rect(18, 9, 2, 1, "E")
    # Navy gloves, blue shoulder clasps, bright gold radiant chest & iconic gold 'S' buckle.
    p.rect(7, 22, 3, 3, "C")
    p.rect(22, 22, 3, 3, "C")
    p.rect(10, 15, 2, 2, "C")
    p.rect(20, 15, 2, 2, "C")
    p.rect(13, 17, 6, 4, "G")
    p.rect(14, 22, 4, 2, "G")
    p.rect(15, 22, 2, 2, "C")
    return p


def ghost():
    # Ava Starr / Ghost: white & silver quantum stealth hood, dark faceplate with glowing red sensor cluster.
    p = body("Ghost", {
        "A": "#e3e8f0", "a": "#a8b3c2", "T": "#2c323d", "L": "#cfd7e3", "B": "#242933",
        "C": "#dde3ec", "c": "#9ea9b8", "D": "#242933", "R": "#ff334b", "E": "#ff99a8", "F": "#e3e8f0",
    }, cape=True, head=False)
    # White quantum stealth hood framing dark multi-lens visor mask!
    box(p, 8, 2, 16, 14, "C")
    p.rect(9, 3, 2, 12, "c")
    p.rect(21, 3, 2, 12, "c")
    box(p, 11, 5, 10, 10, "D")
    # Iconic cluster of glowing crimson quantum optical sensors!
    p.rect(12, 8, 2, 2, "R")
    p.rect(15, 7, 2, 2, "R")
    p.rect(18, 8, 2, 2, "R")
    p.rect(13, 8, 1, 1, "E")
    p.rect(15, 7, 1, 1, "E")
    p.rect(18, 8, 1, 1, "E")
    p.rect(14, 11, 4, 1, "a")
    # Charcoal quantum harness seams & chest core.
    p.rect(10, 16, 2, 7, "D")
    p.rect(20, 16, 2, 7, "D")
    p.rect(14, 17, 4, 4, "D")
    p.rect(15, 18, 2, 2, "R")
    return p


def professorx():
    # Professor X (Charles Xavier): bald head, tailored navy suit, iconic golden hoverchair frame & X-badge.
    p = body("Professor X", {
        "F": "#ecc09d", "s": "#c2916e", "A": "#2a384f", "a": "#1b2536", "T": "#1a202b",
        "L": "#222c3d", "B": "#171b24", "C": "#e8ba38", "c": "#b3881b", "h": "#fae0c8",
        "U": "#366cc4", "R": "#d62828", "G": "#ffe36e",
    }, cape=True)
    # Iconic bald head shine + gentle eyebrows.
    p.rect(13, 4, 4, 1, "h")
    p.rect(12, 8, 3, 1, "s")
    p.rect(17, 8, 3, 1, "s")
    # Golden hoverchair high side armrests & control lights!
    p.rect(5, 16, 2, 10, "C")
    p.rect(25, 16, 2, 10, "C")
    p.rect(6, 17, 1, 8, "c")
    p.rect(25, 17, 1, 8, "c")
    # Crisp white dress shirt, cobalt tie & red-gold X-emblem!
    p.rect(13, 15, 6, 6, "W")
    p.rect(15, 16, 2, 6, "U")
    p.rect(11, 17, 2, 2, "C")
    p.rect(11, 17, 1, 1, "R")
    return p


def magneto():
    # Magneto: iconic crimson winged helmet, purple cape, crimson & purple armor, silver brows.
    p = body("Magneto", {
        "F": "#edd0b8", "s": "#c49c7e", "A": "#b81d30", "a": "#7d101e", "T": "#66287d",
        "L": "#961627", "B": "#66287d", "C": "#66287d", "c": "#421554",
        "R": "#c92236", "r": "#871120", "P": "#7b3499", "E": "#e66eff",
    }, cape=True)
    # Unmistakable Magneto crimson helmet with curved cheek guards & central forehead crest!
    p.stamp(9, 1, [
        "..KKKKKKKKKK..",
        ".KRRRRRRRRRRK.",
        "KRRrRRRRRRrRRK",
        "KRRrRRKKRRrRRK",
        "KRRrRKKKKRrRRK",
    ])
    p.rect(10, 6, 2, 8, "R")
    p.rect(20, 6, 2, 8, "R")
    p.rect(15, 6, 2, 3, "R")
    p.rect(11, 12, 2, 2, "R")
    p.rect(19, 12, 2, 2, "R")
    # Purple cape collar, chest trim, gauntlets & glowing magenta magnetic palms!
    p.rect(10, 15, 12, 2, "P")
    p.rect(12, 18, 8, 3, "P")
    p.rect(7, 21, 3, 4, "P")
    p.rect(22, 21, 3, 4, "P")
    p.rect(8, 23, 1, 1, "E")
    p.rect(23, 23, 1, 1, "E")
    return p


def cyclops():
    # Scott Summers / Cyclops: classic blue & yellow X-Men suit, brown hair, iconic golden ruby-quartz visor!
    p = body("Cyclops", {
        "A": "#1f54a3", "a": "#13366e", "T": "#f2c636", "L": "#1c4a91", "B": "#f2c636",
        "Y": "#f2c636", "y": "#bf941b", "R": "#ff2a3c", "E": "#ff99a3", "H": "#6b432a", "h": "#94613f",
    })
    # Blue X-Men head cowl with spiky brown hair exposed on top!
    p.rect(10, 4, 12, 10, "A")
    p.rect(11, 5, 1, 8, "a")
    p.rect(12, 10, 8, 4, "F")
    p.rect(15, 12, 3, 1, "s")
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
    ])
    # Unmistakable golden ruby-quartz visor with glowing crimson optic slit!
    p.rect(10, 7, 12, 4, "K")
    p.rect(11, 8, 10, 2, "Y")
    p.rect(11, 8, 10, 1, "R")
    p.rect(14, 8, 4, 1, "E")
    # Iconic yellow X-chest harness, yellow gloves & red X-buckle!
    p.stamp(11, 16, ["YY......YY", ".YY....YY.", "..YY..YY..", "...YYYY..."])
    p.rect(15, 22, 2, 2, "R")
    p.rect(7, 22, 3, 3, "Y")
    p.rect(22, 22, 3, 3, "Y")
    return p


def beast():
    # Hank McCoy / Beast: wide bulky sapphire-blue furred mutant, twin-peaked dark mane, glasses & X-belt.
    p = Sprite("Beast", {
        **BASE, "A": "#245ea8", "a": "#163d73", "l": "#4a8ce0", "H": "#132e59",
        "Y": "#f0c230", "D": "#1e2430", "R": "#d62828", "G": "#d9c275",
    })
    # Wide muscular furry torso, huge arms & furry head.
    box(p, 3, 10, 26, 16, "A")
    box(p, 9, 24, 6, 7, "A")
    box(p, 17, 24, 6, 7, "A")
    box(p, 10, 3, 12, 10, "A")
    # Fur highlights on shoulders and chest.
    p.rect(4, 11, 6, 3, "l")
    p.rect(22, 11, 6, 3, "l")
    p.rect(11, 13, 4, 4, "l")
    p.rect(17, 13, 4, 4, "l")
    p.rect(15, 13, 2, 5, "a")
    # Iconic twin-peaked Beast dark-blue mane!
    p.stamp(8, 1, [
        ".KK..........KK.",
        "KHHKKKKKKKKKKHHK",
        "KHHHHHHHHHHHHHHK",
        "KHH..HHHHHH..HHK",
        "KH............HK",
    ])
    # Classic rectangular reading glasses + intelligent brow & fangs hint!
    p.rect(11, 7, 10, 3, "K")
    p.rect(12, 8, 3, 1, "W")
    p.rect(17, 8, 3, 1, "W")
    p.rect(15, 8, 2, 1, "G")
    p.rect(13, 11, 6, 1, "H")
    p.rect(14, 11, 1, 1, "W")
    p.rect(17, 11, 1, 1, "W")
    # Classic X-Men dark trunks with yellow belt & red X-buckle!
    p.rect(9, 21, 14, 4, "D")
    p.rect(9, 21, 14, 1, "Y")
    p.rect(15, 21, 2, 2, "R")
    p.rect(10, 25, 4, 2, "D")
    p.rect(18, 25, 4, 2, "D")
    p.rect(4, 22, 4, 3, "a")
    p.rect(24, 22, 4, 3, "a")
    p.rect(10, 29, 4, 1, "a")
    p.rect(18, 29, 4, 1, "a")
    return p


def gambit():
    # Remy LeBeau / Gambit: brown duster trench coat, dark steel head-cowl, magenta chest armor & pink card!
    p = body("Gambit", {
        "F": "#ebb48c", "s": "#bf8762", "A": "#282c36", "a": "#1a1d24", "T": "#4a5261",
        "L": "#222630", "B": "#242830", "C": "#8f5c38", "c": "#5e3a20",
        "H": "#693e26", "h": "#945a3a", "M": "#d6337c", "m": "#8c1d4c", "P": "#ff70b8", "R": "#ff3b52",
    }, cape=True)
    # Dark head-cowl framing face + tousled brown hair on top!
    p.rect(10, 5, 2, 9, "A")
    p.rect(20, 5, 2, 9, "A")
    p.rect(12, 13, 8, 1, "A")
    hair(p, [
        ".K.KK.KK.K..",
        ".KHHhHHHhK..",
        "KHHHHHHHHHHK",
        "KHH......HHK",
    ])
    # Iconic glowing crimson-on-black eyes!
    p.rect(13, 9, 2, 2, "K")
    p.rect(18, 9, 2, 2, "K")
    p.rect(13, 9, 1, 1, "R")
    p.rect(18, 9, 1, 1, "R")
    # Iconic magenta-pink armored chest plate, brown coat sleeves & glowing kinetic card in hand!
    p.rect(7, 17, 3, 6, "C")
    p.rect(22, 17, 3, 6, "C")
    p.rect(11, 16, 10, 7, "M")
    p.rect(12, 17, 1, 5, "m")
    for y in (18, 20):
        p.rect(13, y, 6, 1, "m")
    p.rect(22, 23, 3, 2, "P")
    p.rect(23, 23, 1, 2, "W")
    return p


def mystique():
    # Raven Darkhölme / Mystique: cerulean-blue scaly skin, swept fiery crimson hair, golden eyes & white sash.
    p = body("Mystique", {
        "F": "#2b7cd6", "s": "#1b559c", "A": "#2b7cd6", "a": "#1b559c", "T": "#ebc042",
        "L": "#256ec2", "B": "#eef2f7", "H": "#c92228", "h": "#f04838", "Y": "#ffe042",
        "W": "#eef2f7", "w": "#bcc7d6",
    })
    # Swept fiery crimson hair!
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
        "KH........HK",
    ])
    p.stamp(8, 6, ["KHK", "KhK", "KHK", "KK."])
    p.stamp(21, 6, ["KHK", "KhK", "KHK", ".KK"])
    # Piercing golden-yellow mutant eyes!
    p.rect(13, 9, 2, 2, "K")
    p.rect(18, 9, 2, 2, "K")
    p.rect(13, 9, 2, 1, "Y")
    p.rect(18, 9, 2, 1, "Y")
    # Classic white draped combat tunic & gold skull-belt accent!
    p.rect(11, 16, 10, 7, "W")
    p.rect(12, 17, 1, 5, "w")
    p.rect(13, 24, 6, 2, "W")
    p.rect(7, 22, 3, 3, "W")
    p.rect(22, 22, 3, 3, "W")
    return p


def nightcrawler():
    # Nightcrawler (Kurt Wagner): indigo-blue skin, pointed ears, golden eyes, red/black X-suit & pointed tail!
    p = body("Nightcrawler", {
        "F": "#2a3b8f", "s": "#1a2663", "A": "#1c1f29", "a": "#12141c", "T": "#c4202b",
        "L": "#1c1f29", "B": "#eef2f7", "H": "#141b45", "h": "#2b3982",
        "R": "#c9222e", "r": "#87141c", "Y": "#ffe44d", "W": "#eef2f7",
    })
    # Pointed elfin ears + tousled dark indigo hair!
    p.stamp(8, 7, [".KK", "KFK", "KFK", ".KK"])
    p.stamp(21, 7, ["KK.", "KFK", "KFK", "KK."])
    hair(p, [
        ".K.KK.KK.K..",
        ".KHHhHHHhK..",
        "KHHHHHHHHHHK",
        "KHH......HHK",
    ])
    # Glowing golden eyes!
    p.rect(13, 9, 2, 2, "K")
    p.rect(18, 9, 2, 2, "K")
    p.rect(13, 9, 2, 1, "Y")
    p.rect(18, 9, 2, 1, "Y")
    # Iconic crimson V-chest & puffed crimson shoulders, white acrobatic gloves & boots!
    p.rect(7, 16, 3, 4, "R")
    p.rect(22, 16, 3, 4, "R")
    p.stamp(11, 16, ["RRRRRRRRRR", ".RRRRRRRR.", "..RRRRRR..", "...RRRR...", "....RR...."])
    p.rect(7, 23, 3, 2, "W")
    p.rect(22, 23, 3, 2, "W")
    # Iconic pointed indigo devil tail curling out to the right!
    p.stamp(25, 22, ["..KK", ".KFK", "KFFK", "KFK.", "KK.."])
    return p


def namor():
    # Namor: bronze skin, pointed ears, sleek black hair, ornate emerald-jade & gold Talokan collar, ankle wings!
    p = body("Namor", {
        "F": "#b87a52", "s": "#8a5636", "A": "#b87a52", "a": "#8a5636", "T": "#ebc03d",
        "L": "#b87a52", "B": "#b87a52", "H": "#181b22", "h": "#333947",
        "G": "#ebc03d", "g": "#b3871b", "J": "#249964", "j": "#156340", "W": "#f2f5fa",
    })
    # Pointed Talokan ears + sleek dark hair!
    p.rect(9, 8, 1, 2, "F")
    p.rect(22, 8, 1, 2, "F")
    hair(p, [
        "..KKKKKKKK..",
        ".KHHhHHHhHK.",
        "KHHHHHHHHHHK",
        "KHH......HHK",
    ])
    p.stamp(14, 12, ["HHHH", ".HH."])
    # Ornate golden & emerald-jade Mesoamerican feathered collar + gold arm bracers!
    p.rect(10, 15, 12, 3, "G")
    p.rect(11, 16, 10, 1, "J")
    p.rect(14, 15, 4, 3, "J")
    p.rect(15, 16, 2, 1, "G")
    p.rect(7, 21, 3, 2, "G")
    p.rect(22, 21, 3, 2, "G")
    # Emerald-green Talokan scaled trunks & iconic white ankle wings!
    p.rect(10, 22, 12, 3, "J")
    p.rect(10, 22, 12, 1, "G")
    p.rect(11, 25, 4, 2, "J")
    p.rect(17, 25, 4, 2, "J")
    p.rect(8, 28, 2, 2, "W")
    p.rect(22, 28, 2, 2, "W")
    return p


def build_weapons():
    """Build crisp 24×12 Avengers weapon & power effect SVGs (left + right pairs)."""
    WEAPONS_DEST.mkdir(parents=True, exist_ok=True)
    for old in WEAPONS_DEST.glob("*.svg"):
        old.unlink()

    def make(name, palette, rows):
        assert len(rows) == 12 and all(len(r) == 24 for r in rows), name
        for facing, mirror in (("right", False), ("left", True)):
            s = Sprite(f"{name} {facing}", palette, width=24, height=12)
            s.stamp(0, 0, rows)
            (WEAPONS_DEST / f"{name}-{facing}.svg").write_text(
                s.svg(display_w=48, display_h=24, mirror=mirror), encoding="utf-8"
            )

    # Captain America's Vibranium Shield (red/white/blue concentric circle with star).
    make("shield", {"R": "#d62828", "W": "#f6f7f2", "B": "#1f54a3", "S": "#9eb5cf"}, [
        "........KKKKKK..........",
        "......KKRRRRRRKK........",
        ".....KRRWWWWWWWRK.......",
        "....KRWWBBBBBBWWRK......",
        "...KRWBBWWBWWBBWRK......",
        "...KRWBBWWWWWBWWRK......",
        "...KRWBBWWWWWBWWRK......",
        "...KRWBBWWBWWBBWRK......",
        "....KRWWBBBBBBWWRK......",
        ".....KRRWWWWWWWRK.......",
        "......KKRRRRRRKK........",
        "........KKKKKK..........",
    ])

    # Thor's Mjolnir hammer with crackling blue-white lightning.
    make("mjolnir", {"H": "#7a5130", "M": "#b6c2cf", "m": "#788594", "L": "#58d4ff", "W": "#e6faff"}, [
        "..............LL........",
        "..........KKKKKKLL......",
        ".........KMMMMMMKWL.....",
        ".........KMmmmmMK.LL....",
        "..KKKKKKKMMMMMMMKW.L....",
        ".KHHHHHHHMmmmmMMK.LL....",
        ".KHHHHHHHMmmmmMMKWL.....",
        "..KKKKKKKMMMMMMMK.LL....",
        ".........KMmmmmMK..L....",
        ".........KMMMMMMKL......",
        "..........KKKKKK........",
        "..............LL........",
    ])

    # Iron Man's Repulsor blast (red/gold gauntlet + bright cyan-white beam).
    make("repulsor", {"R": "#c8232c", "G": "#f4c542", "C": "#4de2ff", "W": "#e8fdff"}, [
        "........................",
        "........................",
        "......CC..CC............",
        ".KKKKKCWCCWCCCCCCCCCC...",
        "KRRGGKCWWWWWWWWWWWWWWCC.",
        "KRRGGKWWWWWWWWWWWWWWWWWC",
        "KRRGGKWWWWWWWWWWWWWWWWWC",
        "KRRGGKCWWWWWWWWWWWWWWCC.",
        ".KKKKKCWCCWCCCCCCCCCC...",
        "......CC..CC............",
        "........................",
        "........................",
    ])

    # Hulk's Gamma Smash shockwave.
    make("smash", {"G": "#4ea83c", "g": "#2d6b22", "L": "#96ff70", "W": "#e8ffe0"}, [
        "..........LL............",
        ".......LLLWWLL..........",
        ".....LLGGGGGGLL..LL.....",
        "...LLGGLLLLLLGGLLWWL....",
        "..LGGLLWWWWWWLLGGGGGL...",
        ".LGGLWWGGGGGGWWLLWWGL...",
        ".LGGLWWGGGGGGWWLLWWGL...",
        "..LGGLLWWWWWWLLGGGGGL...",
        "...LLGGLLLLLLGGLLWWL....",
        ".....LLGGGGGGLL..LL.....",
        ".......LLLWWLL..........",
        "..........LL............",
    ])

    # Black Widow's electric blue Widow's Bite baton.
    make("baton", {"D": "#2a3140", "S": "#8d99a8", "C": "#48d9ff", "W": "#e0faff"}, [
        "........................",
        "........................",
        "...........CC....CC.....",
        "......CCCCCCCCCCCCCCCC..",
        ".KKKKKCWWWWWWWWWWWWWWCK.",
        "KDDSSKCWWWWWWWWWWWWWWCWK",
        "KDDSSKCWWWWWWWWWWWWWWCWK",
        ".KKKKKCWWWWWWWWWWWWWWCK.",
        "......CCCCCCCCCCCCCCCC..",
        "..............CC........",
        "........................",
        "........................",
    ])

    # Hawkeye's recurve bow & purple trick arrow.
    make("arrow", {"B": "#2b2e3a", "P": "#9d5cff", "W": "#ead6ff", "S": "#9aa4b2"}, [
        "...KK...................",
        "..KBBK..................",
        "...KBBK.................",
        "....KBBK............PP..",
        ".....KBK...........KPPK.",
        "..KPPKSSKKKKKKKKKKKWWWWK",
        "..KPPKSSKKKKKKKKKKKWWWWK",
        ".....KBK...........KPPK.",
        "....KBBK............PP..",
        "...KBBK.................",
        "..KBBK..................",
        "...KK...................",
    ])

    # Spider-Man's white web-shooter line.
    make("web", {"W": "#f6f8fc", "S": "#a6b8cc", "R": "#d9232e"}, [
        "........................",
        "............S...........",
        "......S....WWS.....S....",
        ".....WWS...W.W....WWS...",
        ".KKK.W.WWWWWWWWWWWWWWWW.",
        "KRRRKWWWWWWWWWWWWWWWWWWW",
        "KRRRKWWWWWWWWWWWWWWWWWWW",
        ".KKK.W.WWWWWWWWWWWWWWWW.",
        ".....WWS...W.W....WWS...",
        "......S....WWS.....S....",
        "............S...........",
        "........................",
    ])

    # Doctor Strange's glowing orange-gold Eldritch mandala & arcane whip.
    make("eldritch", {"O": "#ff8c24", "G": "#ffd154", "W": "#fff7d6"}, [
        "....OOOO................",
        "..OOGGGGOO..............",
        ".OGGWWWWGGO....OOO......",
        ".OGW....WGO..OOGGGOO....",
        "OGW..GG..WGOOGWWWWWGOOO.",
        "OGW.GWWG.WGOGWWWWWWWWGGO",
        "OGW.GWWG.WGOGWWWWWWWWGGO",
        "OGW..GG..WGOOGWWWWWGOOO.",
        ".OGW....WGO..OOGGGOO....",
        ".OGGWWWWGGO....OOO......",
        "..OOGGGGOO..............",
        "....OOOO................",
    ])

    # Scarlet Witch's crimson chaos magic hex bolt.
    make("chaos", {"R": "#d91c3e", "P": "#ff5c8a", "W": "#ffdbe6"}, [
        "........................",
        ".....RRR.....RRR........",
        "...RRPPPRR.RRPPPRR......",
        "..RPPWWWPPPPPWWWPPPRR...",
        ".RPWWWRRWWWWWRRWWWWPPR..",
        "RPWWPPPRRPPPPRRPPPWWPPR.",
        "RPWWPPPRRPPPPRRPPPWWPPR.",
        ".RPWWWRRWWWWWRRWWWWPPR..",
        "..RPPWWWPPPPPWWWPPPRR...",
        "...RRPPPRR.RRPPPRR......",
        ".....RRR.....RRR........",
        "........................",
    ])

    # Black Panther's glowing violet vibranium energy claws.
    make("claw", {"V": "#9c59ff", "L": "#d9b5ff", "W": "#f7ecff"}, [
        "........................",
        ".....VVVVVVVVVV.........",
        "....VLLLLLLLLLLVVV......",
        "...VLWWWWWWWWWWWLLV.....",
        "......VVVVVVVVVVVVVV....",
        "....VVLLLLLLLLLLLLLLVV..",
        "...VLWWWWWWWWWWWWWWLLV..",
        "......VVVVVVVVVVVVVV....",
        "...VLWWWWWWWWWWWLLV.....",
        "....VLLLLLLLLLLVVV......",
        ".....VVVVVVVVVV.........",
        "........................",
    ])

    # Vision's golden Mind Stone solar beam.
    make("mind-beam", {"G": "#f5bd2a", "L": "#ffe96b", "W": "#fffbe0"}, [
        "........................",
        "........................",
        "....GG..................",
        "..GGLLGGGGGGGGGGGGGGGG..",
        ".GLLWWWWWWWWWWWWWWWWWWG.",
        "GLWWWWWWWWWWWWWWWWWWWWWL",
        "GLWWWWWWWWWWWWWWWWWWWWWL",
        ".GLLWWWWWWWWWWWWWWWWWWG.",
        "..GGLLGGGGGGGGGGGGGGGG..",
        "....GG..................",
        "........................",
        "........................",
    ])

    # Loki's golden Asgardian scepter with glowing emerald-cyan gem.
    make("scepter", {"G": "#ebc03d", "g": "#b58b1f", "C": "#48f0c0", "W": "#e0fff7"}, [
        "........................",
        "................KKKK....",
        "..............KKGGGGK...",
        ".............KGGCCCCGK..",
        ".KKKKKKKKKKKKGKCWWWWCGK.",
        "KggggggggGGGGGGCWWWWCGK.",
        "KggggggggGGGGGGCWWWWCGK.",
        ".KKKKKKKKKKKKGKCWWWWCGK.",
        ".............KGGCCCCGK..",
        "..............KKGGGGK...",
        "................KKKK....",
        "........................",
    ])

    # Doombot's neon-green Latverian plasma blaster.
    make("doom-blast", {"M": "#788594", "D": "#384047", "G": "#36d96a", "W": "#d4ffe0"}, [
        "........................",
        "........................",
        "........................",
        ".KKKKKKKKKK...GGGGG.....",
        "KMMMMDDDDMMKGGGGGGGGGG..",
        "KMMDDDDDDMMKWWWWWWWWWWG.",
        "KMMDDDDDDMMKWWWWWWWWWWG.",
        "KMMMMDDDDMMKGGGGGGGGGG..",
        ".KKKKKKKKKK...GGGGG.....",
        "....KDDK................",
        "....KKKK................",
        "........................",
    ])

    # Doctor Doom's emerald arcane lightning bolt.
    make("doom-magic", {"G": "#1fb852", "L": "#6eff9c", "W": "#e6ffed"}, [
        "........................",
        "......GG........GG......",
        "....GGLLGG....GGLLGG....",
        "..GGLLWWLLGGGGLLWWLLGG..",
        "GGLLWWWWWWLLLLWWWWWWLLG.",
        "GLLWWWWWWWWWWWWWWWWWWLLG",
        "GLLWWWWWWWWWWWWWWWWWWLLG",
        "GGLLWWWWWWLLLLWWWWWWLLG.",
        "..GGLLWWLLGGGGLLWWLLGG..",
        "....GGLLGG....GGLLGG....",
        "......GG........GG......",
        "........................",
    ])

    # Shang-Chi's glowing golden Ten Rings energy rings.
    make("ten-rings", {"G": "#f5b82e", "L": "#ffe57a", "W": "#fffbe0"}, [
        "........................",
        "....GGGG....GGGG........",
        "..GGLLLLGGGGLLLLGG......",
        ".GLLWWWWGLLGWWWWLLGG....",
        ".GLWW..GLLWGL..WWLLGG...",
        "GLW....GLLWG....WWLLWGG.",
        "GLW....GLLWG....WWLLWGG.",
        ".GLWW..GLLWGL..WWLLGG...",
        ".GLLWWWWGLLGWWWWLLGG....",
        "..GGLLLLGGGGLLLLGG......",
        "....GGGG....GGGG........",
        "........................",
    ])

    # M'Baku's carved Jabari wood & bronze war club/staff.
    make("jabari-staff", {"W": "#6e462b", "w": "#452916", "G": "#d9a443", "L": "#ffe296"}, [
        "........................",
        "...............KKKKKK...",
        "..............KGGWWGGK..",
        ".............KGWWWWWWGK.",
        ".KKKKKKKKKKKKKWWLLLLWWK.",
        "KWWWWwwwwWWWWWWLWWWWWWGK",
        "KWWWWwwwwWWWWWWLWWWWWWGK",
        ".KKKKKKKKKKKKKWWLLLLWWK.",
        ".............KGWWWWWWGK.",
        "..............KGGWWGGK..",
        "...............KKKKKK...",
        "........................",
    ])

    # Deadpool's twin steel katanas with crimson-wrapped hilt.
    make("katana", {"R": "#c9202b", "D": "#20232b", "M": "#d9e2ec", "m": "#8d9ba8", "W": "#ffffff"}, [
        "........................",
        "........................",
        "........................",
        "......KK................",
        ".KKKKKDKMMMMMMMMMMMMMK..",
        "KRDRDRDKWWWWWWWWWWWWWWK.",
        "KRDRDRDKmmmmmmmmmmmmmmMK",
        ".KKKKKDKMMMMMMMMMMMMK...",
        "......KK................",
        "........................",
        "........................",
        "........................",
    ])

    # Ant-Man & Cassie Lang's red/blue Pym Particle growth/shrink disc burst.
    make("pym-disc", {"R": "#e02b38", "B": "#2b82e0", "C": "#7ce6ff", "W": "#f6f8fc"}, [
        "........................",
        "........BB..............",
        ".....BBBCCBB....RR......",
        "...BBCCWWWWCCBRRWWWR....",
        "..BCWWWWWWWWWWWWWWWWWR..",
        ".BCWWWWBBBBWWWWWWWWWWWR.",
        ".BCWWWWBBBBWWWWWWWWWWWR.",
        "..BCWWWWWWWWWWWWWWWWWR..",
        "...BBCCWWWWCCBRRWWWR....",
        ".....BBBCCBB....RR......",
        "........BB..............",
        "........................",
    ])

    # Falcon's EXO-7 Redwing vibranium wing-blade & laser dart.
    make("wing-blade", {"G": "#3d6b47", "M": "#b4c2d4", "L": "#ffe066", "W": "#fffbe0"}, [
        "........................",
        ".....KKKK...............",
        "...KKGGGGKK.............",
        "..KGGMMMMGGKK....LL.....",
        ".KGMMWWWWMMMMKKLLWWLL...",
        "KMMWWWWWWWWWWWWWWWWWWWL.",
        "KMMWWWWWWWWWWWWWWWWWWWL.",
        ".KGMMWWWWMMMMKKLLWWLL...",
        "..KGGMMMMGGKK....LL.....",
        "...KKGGGGKK.............",
        ".....KKKK...............",
        "........................",
    ])

    # Mister Fantastic's elastic stretched super-punch fist.
    make("elastic", {"B": "#2b7de0", "b": "#1c58a6", "W": "#f2f5fa", "F": "#e8ae84"}, [
        "........................",
        "........................",
        "...............KKKKKK...",
        "..............KWWWWWWK..",
        ".KKKKKKKKKKKKKWWWWWWWWK.",
        "KBBBBBBBBBBBBKWWWWWWWWWK",
        "KbbbbbbbbbbbbKWWWWWWWWWK",
        ".KKKKKKKKKKKKKWWWWWWWWK.",
        "..............KWWWWWWK..",
        "...............KKKKKK...",
        "........................",
        "........................",
    ])

    # Invisible Woman's translucent cyan psionic force-field pulse.
    make("force-field", {"B": "#36a8e8", "C": "#7ceeff", "W": "#e8fdff"}, [
        "........CCCC............",
        "......CCWWWWCC..........",
        "....CCWWBBBBWWCC...CC...",
        "...CWWBBCCCCBBWWCCWWWC..",
        "..CWWBCWWWWWWCBWWCWWWWC.",
        "..CWBCWWCCCCWWCBWCWWWWWC",
        "..CWBCWWCCCCWWCBWCWWWWWC",
        "..CWWBCWWWWWWCBWWCWWWWC.",
        "...CWWBBCCCCBBWWCCWWWC..",
        "....CCWWBBBBWWCC...CC...",
        "......CCWWWWCC..........",
        "........CCCC............",
    ])

    # Human Torch's roaring supernova fireball.
    make("flame", {"R": "#d92e18", "O": "#ff8824", "Y": "#ffe85c", "W": "#fffde6"}, [
        "..........RR............",
        ".......RRROORR..........",
        ".....RROOYYYYOORR..RR...",
        "...RROOYYWWWWYYOORROOR..",
        "..ROOYWWWWWWWWWWYYOOOOR.",
        ".ROYWWWWWWWWWWWWWWYYOOOR",
        ".ROYWWWWWWWWWWWWWWYYOOOR",
        "..ROOYWWWWWWWWWWYYOOOOR.",
        "...RROOYYWWWWYYOORROOR..",
        ".....RROOYYYYOORR..RR...",
        ".......RRROORR..........",
        "..........RR............",
    ])

    # The Thing's craggy rocky clobberin' shockwave.
    make("rock-smash", {"O": "#d9752b", "d": "#8c3d11", "L": "#f5b062", "W": "#fff2d9"}, [
        "..........LL............",
        ".......LLLOOLL..........",
        ".....LLOOOOOOLL..LL.....",
        "...LLOOLLLLLLOOLLWWL....",
        "..LOOLLWWWWWWLLOOOOOL...",
        ".LOOLWWddOOOOddLLWWOL...",
        ".LOOLWWddOOOOddLLWWOL...",
        "..LOOLLWWWWWWLLOOOOOL...",
        "...LLOOLLLLLLOOLLWWL....",
        ".....LLOOOOOOLL..LL.....",
        ".......LLLOOLL..........",
        "..........LL............",
    ])

    # Winter Soldier's Vibranium cybernetic bionic punch shockwave.
    make("metal-arm", {"M": "#7b8799", "D": "#38404d", "G": "#f0c230", "W": "#fff6cf"}, [
        "........................",
        "...........GG...........",
        ".........GGWWGG.........",
        ".KKKKKKK.GWWWWGG..GG....",
        "KMMGGMMMKWWMMWWWGWWWG...",
        "KDDGGDDDKWMMMMWWWWWWWG..",
        "KDDGGDDDKWMMMMWWWWWWWG..",
        "KMMGGMMMKWWMMWWWGWWWG...",
        ".KKKKKKK.GWWWWGG..GG....",
        ".........GGWWGG.........",
        "...........GG...........",
        "........................",
    ])

    # U.S. Agent's black, crimson & silver tactical shield.
    make("us-shield", {"R": "#c9242b", "W": "#eef2f7", "D": "#242936", "S": "#9aa6b2"}, [
        "........KKKKKK..........",
        "......KKRRRRRRKK........",
        ".....KRRWWWWWWWRK.......",
        "....KRWWDDDDDDWWRK......",
        "...KRWDDWWDWWDDWRK......",
        "...KRWDDWWWWWDWWRK......",
        "...KRWDDWWWWWDWWRK......",
        "...KRWDDWWDWWDDWRK......",
        "....KRWWDDDDDDWWRK......",
        ".....KRRWWWWWWWRK.......",
        "......KKRRRRRRKK........",
        "........KKKKKK..........",
    ])

    # Red Guardian's crimson & white Soviet star shield.
    make("red-shield", {"R": "#c42228", "r": "#871419", "W": "#f2f0e6"}, [
        "........KKKKKK..........",
        "......KKRRRRRRKK........",
        ".....KRRWWWWWWWRK.......",
        "....KRWWRRRRRRWWRK......",
        "...KRWRRWWRWWRRWRK......",
        "...KRWRRWWWWWRWWRK......",
        "...KRWRRWWWWWRWWRK......",
        "...KRWRRWWRWWRRWRK......",
        "....KRWWRRRRRRWWRK......",
        ".....KRRWWWWWWWRK.......",
        "......KKRRRRRRKK........",
        "........KKKKKK..........",
    ])

    # Sentry's million-exploding-suns golden solar flare wave.
    make("solar-flare", {"G": "#f0b818", "Y": "#ffe866", "W": "#fffde8"}, [
        "........................",
        "......GG........GG......",
        "....GGYYGG....GGYYGG....",
        "..GGYYWWYYGGGGYYWWYYGG..",
        "GGYYWWWWWWYYYYWWWWWWYYG.",
        "GYYWWWWWWWWWWWWWWWWWWYYG",
        "GYYWWWWWWWWWWWWWWWWWWYYG",
        "GGYYWWWWWWYYYYWWWWWWYYG.",
        "..GGYYWWYYGGGGYYWWYYGG..",
        "....GGYYGG....GGYYGG....",
        "......GG........GG......",
        "........................",
    ])

    # Ghost's quantum phase-distortion strike slash.
    make("phase-strike", {"W": "#eef2f7", "S": "#9aa6b2", "R": "#ff334b", "P": "#ffa3b0"}, [
        "........................",
        ".....SSSSWWWWWW.........",
        "...SSWWWWPPPPWWWRR......",
        "..SWWPPWWWWWWWWPPWRR....",
        "....SSWWWWWWWWWWWWPRR...",
        "..SSWWPPWWWWWWWWWWPPWR..",
        "..SSWWPPWWWWWWWWWWPPWR..",
        "....SSWWWWWWWWWWWWPRR...",
        "..SWWPPWWWWWWWWPPWRR....",
        "...SSWWWWPPPPWWWRR......",
        ".....SSSSWWWWWW.........",
        "........................",
    ])

    # Professor X's golden-violet concentric telepathic mind-wave rings.
    make("psychic", {"P": "#9d5cff", "G": "#f5cc4c", "W": "#fff8d6"}, [
        "....GGGG................",
        "..GGPPPPGG....PPPP......",
        ".GPPWWWWPPGGPPWWWWPP....",
        ".GPW....WPGPW......WP...",
        "GPW..GG..WGW...GG...WP..",
        "GPW.GWWG.WGW..GWWG..WWP.",
        "GPW.GWWG.WGW..GWWG..WWP.",
        "GPW..GG..WGW...GG...WP..",
        ".GPW....WPGPW......WP...",
        ".GPPWWWWPPGGPPWWWWPP....",
        "..GGPPPPGG....PPPP......",
        "....GGGG................",
    ])

    # Magneto's crackling magenta-purple electromagnetic wave & orbiting metal shards.
    make("magnetism", {"P": "#7b2cbf", "M": "#e056fd", "W": "#fae6ff", "S": "#cfd8e3"}, [
        "......SS........SS......",
        ".....PPP.......PPP......",
        "...PPMMMPP...PPMMMPP....",
        "..PMMWWWMMMPPMMWWWMMMP..",
        ".PMWWPPWWWWMMWWWWPPWWMP.",
        "PMWWMMMPPPWWWWPPPMMMWWMP",
        "PMWWMMMPPPWWWWPPPMMMWWMP",
        ".PMWWPPWWWWMMWWWWPPWWMP.",
        "..PMMWWWMMMPPMMWWWMMMP..",
        "...PPMMMPP...PPMMMPP....",
        ".....PPP.......PPP......",
        "......SS........SS......",
    ])

    # Cyclops' intense ruby-quartz concussive optic blast beam!
    make("optic-blast", {"R": "#d91424", "L": "#ff4d5a", "W": "#ffe6e8", "Y": "#f2c636"}, [
        "........................",
        "........................",
        "......RR................",
        ".KKKKRLLRRRRRRRRRRRRRRR.",
        "KYYYYRWWWWWWWWWWWWWWWWWR",
        "KRRRRWWWWWWWWWWWWWWWWWWW",
        "KRRRRWWWWWWWWWWWWWWWWWWW",
        "KYYYYRWWWWWWWWWWWWWWWWWR",
        ".KKKKRLLRRRRRRRRRRRRRRR.",
        "......RR................",
        "........................",
        "........................",
    ])

    # Beast's ferocious blue-silver acrobatic claw slash!
    make("beast-claw", {"B": "#245ea8", "L": "#6bb3ff", "W": "#ebf5ff"}, [
        "........................",
        ".....BBBBBBBBBB.........",
        "....BLLLLLLLLLLBBB......",
        "...BLWWWWWWWWWWWLLB.....",
        "......BBBBBBBBBBBBBB....",
        "....BBLLLLLLLLLLLLLLBB..",
        "...BLWWWWWWWWWWWWWWLLB..",
        "......BBBBBBBBBBBBBB....",
        "...BLWWWWWWWWWWWLLB.....",
        "....BLLLLLLLLLLBBB......",
        ".....BBBBBBBBBB.........",
        "........................",
    ])

    # Gambit's glowing hot-pink kinetically charged playing cards!
    make("kinetic-card", {"P": "#d62976", "L": "#ff70b8", "W": "#fff0f7"}, [
        "........................",
        ".........PPPPP..........",
        "........PLWWWLP...PPPPP.",
        "....PP..PLWPWLP..PLWWWLP",
        "..PPLLPPPLWWWLP..PLWPWLP",
        ".PLWWWWLPPPPP....PLWWWLP",
        ".PLWPWWLP........PLWWWLP",
        "..PLWWLLPPPPP....PPPPP..",
        "....PP..PLWWWLP.........",
        "........PLWPWLP.........",
        "........PLWWWLP.........",
        ".........PPPPP..........",
    ])

    # Nightcrawler's violet BAMF teleport puff & pirate cutlass!
    make("bamf-blade", {"P": "#6b2db8", "L": "#b57aff", "M": "#d9e2ec", "G": "#ebc03d", "W": "#ffffff"}, [
        "........................",
        "...PPP..................",
        "..PLLLPP................",
        ".PLPPPPLP.KK............",
        "..PLPPKKKGKMMMMMMMMMK...",
        "..PPKKGGGKKWWWWWWWWWWWK.",
        "..PPKKGGGKKMMMMMMMMMMMK.",
        "..PLPPKKKGKMMMMMMMMMK...",
        ".PLPPPPLP.KK............",
        "..PLLLPP................",
        "...PPP..................",
        "........................",
    ])

    # Namor's golden-jade Talokan vibranium spear/trident!
    make("trident", {"G": "#ebc03d", "g": "#b3871b", "J": "#249964", "L": "#7cf2be", "W": "#e6fff4"}, [
        "........................",
        "................KKKK....",
        "...............KGGGGK...",
        "..............KGGLLGGK..",
        ".KKKKKKKKKKKKKGJWWWWWGK.",
        "KggggggggGGGGGGJWWWWWWGK",
        "KggggggggGGGGGGJWWWWWWGK",
        ".KKKKKKKKKKKKKGJWWWWWGK.",
        "..............KGGLLGGK..",
        "...............KGGGGK...",
        "................KKKK....",
        "........................",
    ])

    # Peggy Carter & Mystique's tactical sidearm muzzle blast!
    make("pistol", {"D": "#2c3240", "M": "#8d99a8", "G": "#ffaa2b", "W": "#fff5cc"}, [
        "........................",
        "........................",
        "...............GG.......",
        ".KKKKKKKKKK..GGWWGG.....",
        "KMMMMDDDDMMKGWWWWWWGGG..",
        "KMMDDDDDDMMKWWWWWWWWWWG.",
        "KMMDDDDDDMMKWWWWWWWWWWG.",
        "KMMMMDDDDMMKGWWWWWWGGG..",
        ".KKKKKKKKKK..GGWWGG.....",
        "...KDDK........GG.......",
        "...KKKK.................",
        "........................",
    ])


def write_preview(sprites, path):
    # Dependency-free PNG: grid rows of large nearest-neighbour art + actual-size checks, dark then light.
    backgrounds = [
        json.loads((ROOT / "themes" / f"{side}.json").read_text())["background"]
        for side in ["eclipse", "vanguard"]
    ]
    cols = min(len(sprites), 11)
    band_rows = (len(sprites) + cols - 1) // cols
    cell_w, cell_h = 144, 212
    half_h = band_rows * cell_h
    width, height = cols * cell_w, half_h * 2
    rgb = lambda color: bytes.fromhex(color.lstrip("#"))
    rows = []
    for y in range(height):
        bg = backgrounds[y // half_h]
        row = bytearray(rgb(bg) * width)
        band_y = y % half_h
        grid_row = band_y // cell_h
        local_y = band_y % cell_h
        for col in range(cols):
            index = grid_row * cols + col
            if index >= len(sprites):
                break
            sprite = sprites[index]
            for scale, top in [(4, 8), (1.125, 160)]:
                size = round(SIZE * scale)
                if not top <= local_y < top + size:
                    continue
                sy = int((local_y - top) / scale)
                left = col * cell_w + (cell_w - size) // 2
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
        # Classic Avengers & Doomsday core
        "doom": doom, "ironman": ironman, "cap": cap, "thor": thor,
        "hulk": hulk, "widow": widow, "hawkeye": hawkeye, "spiderman": spiderman,
        "strange": strange, "wanda": wanda, "panther": panther, "vision": vision,
        "loki": loki, "fury": fury, "doombot": doombot,
        # Doomsday Avengers & Allies
        "sam": sam, "antman": antman, "cassie": cassie, "shangchi": shangchi,
        "mbaku": mbaku, "falcon": falcon, "peggy": peggy, "deadpool": deadpool,
        # Fantastic Four
        "mrfantastic": mrfantastic, "invisiblewoman": invisiblewoman,
        "humantorch": humantorch, "thing": thing,
        # Thunderbolts
        "yelena": yelena, "bucky": bucky, "usagent": usagent,
        "redguardian": redguardian, "sentry": sentry, "ghost": ghost,
        # X-Men & Mutants
        "professorx": professorx, "magneto": magneto, "cyclops": cyclops,
        "beast": beast, "gambit": gambit, "mystique": mystique, "nightcrawler": nightcrawler,
        # Other Doomsday Cast
        "namor": namor,
    }
    DEST.mkdir(parents=True, exist_ok=True)
    for old in DEST.glob("*.svg"):
        old.unlink()
    characters = {name: draw() for name, draw in drawings.items()}
    for name, sprite in characters.items():
        (DEST / f"{name}.svg").write_text(sprite.svg(), encoding="utf-8")
    build_weapons()
    print(f"Built {len(characters)} Avengers character sprites and weapon effects in {DEST}")
    if args.preview:
        write_preview(list(characters.values()), args.preview)
        print(f"Preview: {args.preview}")


if __name__ == "__main__":
    main()
