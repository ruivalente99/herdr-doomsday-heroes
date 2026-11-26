// Pure training data: no host calls, real agent commands or random render-time state.
// Avengers & Doomsday cast for the Battle Simulator.
export const MELEE_WEAPONS = new Set(["shield", "mjolnir", "smash", "baton", "claw", "scepter"]);
export const ARCANE_WEAPONS = new Set(["eldritch", "chaos", "doom-magic"]);

export const HEROES = {
  ironman: { name: "Iron Man", weapon: "repulsor", style: "jetpack", line: "Suit at 400% capacity. Let's run it." },
  doom: { name: "Doctor Doom", weapon: "doom-magic", style: "heavy", line: "Every timeline ends under Doom's will." },
  cap: { name: "Capt. America", weapon: "shield", style: "duelist", line: "I can do this all day. Again, from the top." },
  thor: { name: "Thor", weapon: "mjolnir", style: "duelist", line: "Bring me a worthy sparring partner!" },
  hulk: { name: "Hulk", weapon: "smash", style: "heavy", line: "HULK SMASH TRAINING ROOM!" },
  widow: { name: "Black Widow", weapon: "baton", style: "dual", line: "Stay sharp. I don't miss twice." },
  hawkeye: { name: "Hawkeye", weapon: "arrow", style: "shooter", line: "Played eighteen, shot eighteen. Ready." },
  spiderman: { name: "Spider-Man", weapon: "web", style: "acrobat", line: "Hey everyone! Wait — is this a real drill?" },
  strange: { name: "Dr. Strange", weapon: "eldritch", style: "force", line: "I saw 14,000,605 simulations. Let's try one more." },
  wanda: { name: "Scarlet Witch", weapon: "chaos", style: "force", line: "Reality bends faster than this simulator." },
  panther: { name: "Black Panther", weapon: "claw", style: "dual", line: "Vibranium absorbs the strike. Return it twice as hard." },
  vision: { name: "Vision", weapon: "mind-beam", style: "shooter", line: "A fascinating exercise in tactical probability." },
  loki: { name: "Loki", weapon: "scepter", style: "duelist", line: "I am burdened with glorious training." },
  fury: { name: "Nick Fury", weapon: null, style: "support", line: "My eyes are on every terminal. Don't make me step in." },
  doombot: { name: "Doombot", weapon: "doom-blast", style: "shooter", line: "LATVERIAN PROTOCOL ACTIVE. TARGET LOCKED." },
};

export const PRESETS = {
  classic: { name: "Avengers", heroes: ["ironman", "doom", "cap", "thor", "widow", "hawkeye", "hulk", "doombot"] },
  doomsday: { name: "Doomsday", heroes: ["ironman", "doom", "strange", "wanda", "thor", "loki"] },
  strike: { name: "Strike team", heroes: ["cap", "panther", "widow", "hawkeye", "spiderman", "doombot"] },
  council: { name: "Council", heroes: ["fury", "strange", "wanda", "vision", "panther", "doom", "spiderman", "ironman"] },
};

// Avengers training banter. Each line names its speaker.
const CONVERSATIONS = [
  { pair: ["doom", "ironman"], lines: [["doom", "A tin suit against Latveria's sovereign? How quaint."], ["ironman", "Says the guy wearing a medieval cosplay helmet."], ["doom", "Doom does not cosplay, Stark."]] },
  { pair: ["cap", "ironman"], lines: [["ironman", "Big man in a suit of armor. Take that off, what are you?"], ["cap", "Still standing when the build breaks."], ["ironman", "Okay, fair. Next pass."]] },
  { pair: ["thor", "hulk"], lines: [["thor", "Strongest Avenger reporting in."], ["hulk", "Hulk strongest! Point break wrong!"], ["thor", "We are literally on the same team, banner-friend!"]] },
  { pair: ["thor", "loki"], lines: [["loki", "I have been falling for thirty minutes!"], ["thor", "Stop turning into snakes and help me deploy."], ["loki", "You always were so dramatic, brother."]] },
  { pair: ["widow", "hawkeye"], lines: [["widow", "Just like Budapest all over again."], ["hawkeye", "You and I remember Budapest very differently."], ["widow", "Keep your eyes on the flank, Barton."]] },
  { pair: ["spiderman", "ironman"], lines: [["spiderman", "Mr. Stark, I found a bug in the training sim!"], ["ironman", "Kid, stay on your feet and keep the webs off my visor."], ["spiderman", "Got it! Mostly!"]] },
  { pair: ["strange", "wanda"], lines: [["strange", "The multiverse is not a playground, Wanda."], ["wanda", "You break the rules and become a hero. I do it and it's a warning."], ["strange", "Not in this training room."]] },
  { pair: ["strange", "doom"], lines: [["doom", "Your mystic trinkets pale before Doom's sorcery."], ["strange", "I've bargained with worse than you, Victor."], ["doom", "Then let us test your wards."]] },
  { pair: ["cap", "panther"], lines: [["panther", "Your shield holds up well, Captain."], ["cap", "Wakanda makes good gear. Try not to scratch it."]] },
  { pair: ["wanda", "vision"], lines: [["vision", "Our odds improve markedly when we synchronize."], ["wanda", "Then stay close, Vis."]] },
  { pair: ["fury", "ironman"], lines: [["fury", "Stark, I need results, not sarcasm."], ["ironman", "You hired me for both, Director."]] },
  { pair: ["fury", "strange"], lines: [["fury", "Tell me we win this simulation, Doctor."], ["strange", "If I tell you what happens, it won't happen."]] },
  { pair: ["spiderman", "strange"], lines: [["spiderman", "Oh, we're using our made-up names! I'm Spider-Man."], ["strange", "Focus, Parker. Portal on your left."]] },
  { pair: ["doom", "cap"], lines: [["doom", "Kneel, Captain. Doomsday has already begun."], ["cap", "I can do this all day."], ["doom", "Defiance. How brief."]] },
  { pair: ["panther", "widow"], lines: [["widow", "Try to keep up, Your Highness."], ["panther", "I never freeze, Romanoff."]] },
  { pair: ["hawkeye", "doombot"], lines: [["hawkeye", "Ten arrows left. Ten tin cans."], ["doombot", "RECALIBRATING LATVERIAN DEFENSE MATRIX."]] },
  { pair: ["cap", "thor"], lines: [["cap", "On your left, Thor."], ["thor", "No, Captain — you take the little one."]] },
];

export function normalizeRoster(value) {
  if (!Array.isArray(value)) return [];
  const seen = new Set();
  return value.filter(hero => {
    if (typeof hero !== "string" || !Object.hasOwn(HEROES, hero)) return false;
    if (seen.has(hero) && hero !== "doombot") return false;
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
  if (weapons.every(weapon => MELEE_WEAPONS.has(weapon))) return "MELEE DUEL";
  if (weapons.some(weapon => ARCANE_WEAPONS.has(weapon))) return "ARCANE / MYSTIC";
  if (weapons.some(weapon => MELEE_WEAPONS.has(weapon))) return "DEFLECT / COUNTER";
  return "CROSS-FIRE";
}
