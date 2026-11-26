#!/usr/bin/env python3
"""Rebuild the fifteen 32×32 Avengers character sprites and weapon effects. Standard library only.

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


def write_preview(sprites, path):
    # Dependency-free PNG: rows are large nearest-neighbour art, then actual-size checks.
    backgrounds = [
        json.loads((ROOT / "themes" / f"{side}.json").read_text())["background"]
        for side in ["eclipse", "vanguard"]
    ]
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
        "doom": doom, "ironman": ironman, "cap": cap, "thor": thor,
        "hulk": hulk, "widow": widow, "hawkeye": hawkeye, "spiderman": spiderman,
        "strange": strange, "wanda": wanda, "panther": panther, "vision": vision,
        "loki": loki, "fury": fury, "doombot": doombot,
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
