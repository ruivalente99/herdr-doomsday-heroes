// Ship IDs are shared with the Fleet emblems and the generated background filenames.
export const FLEET = ["skyrunner", "arrowhawk", "nightglass", "bastion", "longbow", "dart", "eclipse-barge"];
export const SHIP_NAMES = {
  "skyrunner": "Quinjet", "arrowhawk": "Avenjet", "nightglass": "Royal Talon",
  "bastion": "Helicarrier", "longbow": "Benatar", "dart": "S.H.I.E.L.D. Dart",
  "eclipse-barge": "Latverian Barge",
};

export function shipBackground(ship, dark = true) {
  return FLEET.includes(ship) ? { image: `backgrounds/ships/${dark ? "eclipse" : "vanguard"}/${ship}.png`, fit: "cover" } : null;
}
