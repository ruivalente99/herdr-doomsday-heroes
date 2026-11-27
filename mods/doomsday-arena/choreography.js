// Pure training data: no host calls, real agent commands or random render-time state.
// Avengers & Doomsday cast for the Battle Simulator.
export const MELEE_WEAPONS = new Set([
  "shield", "mjolnir", "smash", "baton", "claw", "scepter",
  "ten-rings", "jabari-staff", "katana", "elastic", "rock-smash",
  "metal-arm", "us-shield", "red-shield", "phase-strike", "beast-claw",
  "bamf-blade", "trident",
]);
export const ARCANE_WEAPONS = new Set([
  "eldritch", "chaos", "doom-magic",
  "force-field", "solar-flare", "psychic", "magnetism",
]);

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
  sam: { name: "Sam Wilson", weapon: "shield", style: "jetpack", line: "Vibranium wings hot and shield locked. On your left." },
  antman: { name: "Ant-Man", weapon: "pym-disc", style: "acrobat", line: "Going small, going big — either way, watch your ankles!" },
  cassie: { name: "Cassie Lang", weapon: "pym-disc", style: "acrobat", line: "Pym suit calibrated. Try keeping up, Dad." },
  shangchi: { name: "Shang-Chi", weapon: "ten-rings", style: "dual", line: "The Ten Rings answer to focus, not brute force." },
  mbaku: { name: "M'Baku", weapon: "jabari-staff", style: "heavy", line: "The Jabari do not train lightly! Show your strength!" },
  falcon: { name: "Falcon", weapon: "wing-blade", style: "jetpack", line: "EXO-7 wings online. Redwing has eyes on the deck." },
  peggy: { name: "Peggy Carter", weapon: "pistol", style: "shooter", line: "SSR discipline never goes out of style. Begin." },
  deadpool: { name: "Deadpool", weapon: "katana", style: "dual", line: "Maximum effort! Somebody tell the devs my sprite looks great." },
  mrfantastic: { name: "Mr. Fantastic", weapon: "elastic", style: "duelist", line: "Fascinating geometry. Let's stretch the parameters." },
  invisiblewoman: { name: "Sue Storm", weapon: "force-field", style: "force", line: "Force fields up. Nobody gets past this line." },
  humantorch: { name: "Human Torch", weapon: "flame", style: "jetpack", line: "Flame on! Try not to melt the training deck!" },
  thing: { name: "The Thing", weapon: "rock-smash", style: "heavy", line: "It's clobberin' time! Bring on the tin cans!" },
  yelena: { name: "Yelena", weapon: "baton", style: "dual", line: "Such a poser stance. Watch how a real Widow fights." },
  bucky: { name: "Bucky Barnes", weapon: "metal-arm", style: "heavy", line: "Keep the chatter down and hit your mark." },
  usagent: { name: "U.S. Agent", weapon: "us-shield", style: "duelist", line: "Shield up. Let's show them how it's done." },
  redguardian: { name: "Red Guardian", weapon: "red-shield", style: "heavy", line: "Ah! Finally, a real workout for the Red Guardian!" },
  sentry: { name: "Sentry", weapon: "solar-flare", style: "jetpack", line: "Trying to keep the output below a million suns." },
  ghost: { name: "Ghost", weapon: "phase-strike", style: "acrobat", line: "Blink and I'm already behind your guard." },
  professorx: { name: "Professor X", weapon: "psychic", style: "force", line: "Clear your mind. The true test begins within." },
  magneto: { name: "Magneto", weapon: "magnetism", style: "force", line: "Metal obeys only one master on this deck." },
  cyclops: { name: "Cyclops", weapon: "optic-blast", style: "shooter", line: "To me, my X-Men. Firing optic line on three." },
  beast: { name: "Beast", weapon: "beast-claw", style: "heavy", line: "Oh my stars and garters — let us test our agility!" },
  gambit: { name: "Gambit", weapon: "kinetic-card", style: "acrobat", line: "Pick a card, mon ami. Any card — they all blow up." },
  mystique: { name: "Mystique", weapon: "pistol", style: "acrobat", line: "Are you sure you're sparring with who you think?" },
  nightcrawler: { name: "Nightcrawler", weapon: "bamf-blade", style: "acrobat", line: "Bamf! Over here, mein Freund — en garde!" },
  namor: { name: "Namor", weapon: "trident", style: "jetpack", line: "Imperius Rex! Talokan bows to no surface throne." },
};

export const PRESETS = {
  classic: { name: "Avengers", heroes: ["ironman", "doom", "cap", "thor", "widow", "hawkeye", "hulk", "doombot"] },
  doomsday: { name: "Doomsday", heroes: ["sam", "doom", "mrfantastic", "sentry", "cyclops", "magneto", "thor", "loki"] },
  f4: { name: "Fantastic 4", heroes: ["mrfantastic", "doom", "invisiblewoman", "namor", "humantorch", "thing"] },
  thunderbolts: { name: "Thunderbolts", heroes: ["yelena", "bucky", "usagent", "redguardian", "sentry", "ghost"] },
  xmen: { name: "X-Men", heroes: ["professorx", "magneto", "cyclops", "beast", "gambit", "mystique", "nightcrawler", "deadpool"] },
};

// Avengers & Doomsday training banter. Each line names its speaker.
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
  { pair: ["doom", "mrfantastic"], lines: [["doom", "Richards! Your calculations fail before Doom's intellect."], ["mrfantastic", "Check your sign error, Victor. Every time."], ["doom", "Doom does not make sign errors!"]] },
  { pair: ["mrfantastic", "invisiblewoman"], lines: [["invisiblewoman", "Reed, less theory, more ducking."], ["mrfantastic", "Good point — expanding perimeter now!"]] },
  { pair: ["humantorch", "thing"], lines: [["humantorch", "Flame on! Try to keep up, rock-head!"], ["thing", "Watch the flame, Matchstick — it's clobberin' time!"], ["humantorch", "Classic Ben. Still the slowest on the roster."]] },
  { pair: ["invisiblewoman", "namor"], lines: [["namor", "Even your shields bend before the sea, Susan."], ["invisiblewoman", "Try pushing a little harder, Namor. You won't get through."]] },
  { pair: ["professorx", "magneto"], lines: [["magneto", "Still preaching patience while the world burns, Charles?"], ["professorx", "And you're still bending the hull plating, Erik."], ["magneto", "Old habits die hard, old friend."]] },
  { pair: ["cyclops", "magneto"], lines: [["cyclops", "Stand down, Magneto. This deck holds."], ["magneto", "Your visor cannot melt conviction, Summers."]] },
  { pair: ["cyclops", "gambit"], lines: [["cyclops", "Keep those charged cards off the console, Remy."], ["gambit", "Relax, Scott — Gambit always plays a clean hand."]] },
  { pair: ["beast", "nightcrawler"], lines: [["beast", "Extraordinary spatial displacement, Kurt!"], ["nightcrawler", "Bamf! Don't blink, Hank — behind you!"]] },
  { pair: ["magneto", "mystique"], lines: [["magneto", "Ready to turn the tide, Raven?"], ["mystique", "They won't know who threw the first punch."]] },
  { pair: ["yelena", "bucky"], lines: [["yelena", "Very dramatic entrance, Winter Soldier. Total poser."], ["bucky", "Just keep up, Belova."], ["yelena", "I'm already three steps ahead of you."]] },
  { pair: ["yelena", "redguardian"], lines: [["redguardian", "Behold! Red Guardian leads the Thunderbolts to glory!"], ["yelena", "Alexei, lower your voice — this is stealth ops."]] },
  { pair: ["usagent", "redguardian"], lines: [["usagent", "Two shields, one frontline. Don't get in my way."], ["redguardian", "Hah! My shield has twice the heart, little America!"]] },
  { pair: ["sentry", "ghost"], lines: [["ghost", "Keep the solar flare below blinding, Bob."], ["sentry", "Dialed back to one percent. Watch my flank."]] },
  { pair: ["sam", "doom"], lines: [["doom", "Another winged mortal carrying Rogers' trinket."], ["sam", "Vibranium wings and this shield say otherwise, Victor."]] },
  { pair: ["sam", "bucky"], lines: [["sam", "On your left, Bucky."], ["bucky", "Don't start with that again, Sam."]] },
  { pair: ["sam", "falcon"], lines: [["falcon", "Redwing's tracking hostiles across the deck, Cap!"], ["sam", "Good eyes, Joaquin. Take the high line."]] },
  { pair: ["cap", "peggy"], lines: [["peggy", "Try not to get reckless out there, Steve."], ["cap", "With you watching my six, Peggy? Never."]] },
  { pair: ["antman", "cassie"], lines: [["antman", "Wait — did you upgrade your regulator without telling me?"], ["cassie", "Relax, Dad. I fixed the wobble you kept complaining about."]] },
  { pair: ["panther", "mbaku"], lines: [["mbaku", "Stand aside, Princess — the Jabari lead the charge!"], ["panther", "Hold formation, M'Baku. Wakanda wins together."]] },
  { pair: ["panther", "namor"], lines: [["namor", "Do not mistake alliance for obedience, Shuri."], ["panther", "Then prove Talokan can match Wakanda's pace."]] },
  { pair: ["shangchi", "thor"], lines: [["shangchi", "Ten Rings against Mjolnir. Friendly spar?"], ["thor", "A glorious match! Show me your form!"]] },
  { pair: ["deadpool", "gambit"], lines: [["deadpool", "Ooh! I'm about to make a name for myself here!"], ["gambit", "Hey — dat's Gambit's line, Wade!"]] },
  { pair: ["deadpool", "doom"], lines: [["deadpool", "Wait — Tony?! Did the multiverse recast you?"], ["doom", "Speak one more jest and Doom erases your timeline."]] },
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
