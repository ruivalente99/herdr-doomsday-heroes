// Ship IDs are shared with the Fleet emblems and the generated background filenames.
export const FLEET = ["skyrunner", "arrowhawk", "nightglass", "bastion", "longbow", "dart", "eclipse-barge"];
export const SHIP_NAMES = {
  "skyrunner": "Skyrunner", "arrowhawk": "Arrowhawk", "nightglass": "Nightglass",
  "bastion": "Bastion", "longbow": "Longbow", "dart": "Dart",
  "eclipse-barge": "Eclipse Barge",
};

export function shipBackground(ship, dark = true) {
  return FLEET.includes(ship) ? { image: `backgrounds/ships/${dark ? "eclipse" : "vanguard"}/${ship}.png`, fit: "cover" } : null;
}
