// Pure training data: no host calls, real agent commands or random render-time state.
// Original cast: every hero, villain and line here is invented for this project.
export const HEROES = {
  meridian: { name: "Meridian", weapon: "blade-green", style: "duelist", line: "Ready when you are. Again, from the top." },
  umbra: { name: "King Umbra", weapon: "blade-red", style: "heavy", line: "Every timeline ends in my shadow." },
  vesper: { name: "Vesper", weapon: "pulse", style: "shooter", line: "Comms are up. Somebody has to hold this line." },
  rook: { name: "Rook", weapon: "pulse", style: "shooter", line: "It's a drill. What's the worst that could happen?" },
  basalt: { name: "Basalt", weapon: "launcher", style: "heavy", line: "Stand behind the rock. I am the rock." },
  husk: { name: "Husk drone", weapon: "pulse", style: "shooter", line: "TARGET ACQUIRED. PROBABLY." },
  cog: { name: "Cog", weapon: "arc-zap", style: "droid", line: "Bzzt! Whirr-click!" },
  aldric: { name: "Aldric", weapon: "blade-blue", style: "duelist", line: "Patience. Read the second strike, not the first." },
  pip: { name: "Pip", weapon: "blade-green", style: "acrobat", line: "Small wings, big swing!" },
  kestrel: { name: "Kestrel", weapon: "pulse", style: "jetpack", line: "Eyes in the sky. Nothing gets past me." },
  juno: { name: "Juno", weapon: null, style: "support", line: "Recalculating odds. They are not encouraging." },
  vale: { name: "Dr. Vale", weapon: null, style: "support", line: "Nobody gets hurt on my shift. Nobody." },
  nyx: { name: "Nyx", weapon: "blade-white", style: "dual", line: "Two blades, half the time." },
  hexa: { name: "Hexa", weapon: "blade-purple", style: "duelist", line: "Every sigil has a price. I pay early." },
  morrow: { name: "Morrow", weapon: "void-bolt", style: "force", line: "Let us see how much this simulator can bear." },
};

export const PRESETS = {
  classic: { name: "Classic", heroes: ["meridian", "umbra", "rook", "kestrel", "vesper", "husk", "basalt", "cog"] },
  doomsday: { name: "Doomsday", heroes: ["aldric", "umbra", "nyx", "hexa", "pip", "morrow"] },
  strike: { name: "Strike team", heroes: ["rook", "kestrel", "basalt", "husk", "vesper", "cog"] },
  council: { name: "Council", heroes: ["vale", "morrow", "hexa", "umbra", "juno", "cog", "pip", "kestrel"] },
};

// Original training banter. Each line names its speaker.
const CONVERSATIONS = [
  { pair: ["umbra", "meridian"], lines: [["umbra", "Kneel, Captain. The last day has already begun."], ["meridian", "Then I'll spend all of it standing."], ["umbra", "Defiance. How brief."]] },
  { pair: ["meridian", "pip"], lines: [["pip", "You swing like you're carrying the whole sky."], ["meridian", "Some days I am."], ["pip", "Then let me carry a corner!"]] },
  { pair: ["rook", "basalt"], lines: [["rook", "Basalt, cover me. Again."], ["basalt", "I am always covering you."], ["rook", "Fine. You take the next hit."]] },
  { pair: ["vesper", "cog"], lines: [["vesper", "Cog, patch me into every channel we've got."], ["cog", "Bzzt! Channels open."], ["vesper", "And this time, encrypt them."]] },
  { pair: ["aldric", "umbra"], lines: [["aldric", "I knew you before the crown, Umbra."], ["umbra", "That man burned with his kingdom."], ["aldric", "Then let the steel do the talking."]] },
  { pair: ["aldric", "nyx"], lines: [["aldric", "Who taught you that entrance?"], ["nyx", "You did. I just skipped the speech after."]] },
  { pair: ["pip", "morrow"], lines: [["pip", "Your void is very loud for something empty."], ["morrow", "The simulator is merely warming up."]] },
  { pair: ["hexa", "morrow"], lines: [["hexa", "Your sigils are borrowed, Morrow."], ["morrow", "Everything is borrowed. I simply never return it."], ["hexa", "Not in this training room."]] },
  { pair: ["rook", "kestrel"], lines: [["kestrel", "Calder. You owe me a glider."], ["rook", "Send the bill to the end of the world."]] },
  { pair: ["nyx", "umbra"], lines: [["nyx", "I don't take orders from crowns."], ["umbra", "Then this should be an interesting exercise."]] },
  { pair: ["vale", "juno"], lines: [["vale", "Juno, open a channel to their side."], ["juno", "At last. A task with an acceptable survival rate."]] },
  { pair: ["juno", "cog"], lines: [["juno", "Cog, do not plug into strange consoles."], ["cog", "Whirr. Already plugged in."], ["juno", "We are going to be recalibrated."]] },
  { pair: ["vale", "morrow"], lines: [["vale", "We came to talk, Morrow."], ["morrow", "Of course, Doctor. A perfectly peaceful simulation."]] },
  { pair: ["nyx", "hexa"], lines: [["hexa", "Show me your guard."], ["nyx", "Try to keep up, witch."]] },
  { pair: ["kestrel", "husk"], lines: [["kestrel", "Aim first. Then fire."], ["husk", "RECALIBRATING PRIORITIES."]] },
  { pair: ["aldric", "meridian"], lines: [["aldric", "Whatever comes on the last day, you won't face it alone."], ["meridian", "Then let's take another pass."]] },
];

export function normalizeRoster(value) {
  if (!Array.isArray(value)) return [];
  const seen = new Set();
  return value.filter(hero => {
    if (typeof hero !== "string" || !Object.hasOwn(HEROES, hero)) return false;
    if (seen.has(hero) && hero !== "husk") return false;
    seen.add(hero);
    return true;
  }).slice(0, 8);
}

export function frontsFor(roster) {
  const heroes = normalizeRoster(roster);
  return Array.from({ length: Math.ceil(heroes.length / 2) }, (_, index) => heroes.slice(index * 2, index * 2 + 2));
}

export function dialogueLines(roster) {
  const heroes = normalizeRoster(roster);
  const present = new Set(heroes);
  const lines = CONVERSATIONS.filter(({ pair }) => pair.every(hero => present.has(hero)))
    .flatMap(({ pair, lines }) => lines.map(([speaker, text]) => ({ speaker, text, pair })));
  return lines.length ? lines : heroes.map(speaker => ({ speaker, text: HEROES[speaker].line, pair: heroes.slice(0, 2) }));
}

export function exchange(roster, turn = 0) {
  const lines = dialogueLines(roster);
  return lines.length ? lines[((turn % lines.length) + lines.length) % lines.length] : null;
}

export function frontStyle(pair) {
  if (pair.length < 2) return "STANDBY";
  const weapons = pair.map(hero => HEROES[hero].weapon);
  if (weapons.includes(null)) return "ESCORT / SUPPORT";
  if (weapons.every(weapon => weapon.startsWith("blade-"))) return "BLADE DUEL";
  if (weapons.includes("void-bolt") || weapons.includes("arc-zap")) return "VOID / TECH";
  if (weapons.some(weapon => weapon.startsWith("blade-"))) return "DEFLECT / COUNTER";
  return "CROSS-FIRE";
}
