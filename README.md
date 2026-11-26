<h1 align="center">Doomsday Heroes for Herdr</h1>

<p align="center">
  <strong>An Avengers: Doomsday command center for your coding agents.</strong><br>
  Pixel-art Avengers sprites, ship cockpits and live agent status — inside <a href="https://herdr.dev">Herdr</a>.
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#choose-your-side">Choose your side</a> ·
  <a href="#the-cast">Meet the cast</a> ·
  <a href="#battle-simulator">Battle Simulator</a> ·
  <a href="#bomb-run">Bomb Run</a> ·
  <a href="#customize-and-test">Customize</a> ·
  <a href="RECIPE.md">Recipe</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/characters-15-6eaa8f?style=flat-square" alt="15 characters">
  <img src="https://img.shields.io/badge/ships-7-a8875a?style=flat-square" alt="7 ships">
  <img src="https://img.shields.io/badge/appearances-2-4c96b5?style=flat-square" alt="2 appearances">
</p>

<p align="center">
  <img src="docs/images/overview.svg" alt="Illustrated Vanguard and Eclipse workspaces with the project's character sprites, agent cards and cockpit artwork" width="1200">
  <br>
  <sub>Illustrated overview using the actual project artwork and theme colors. Not a screenshot.</sub>
</p>

Your agents become the cast. Your spaces get their own ships. Keep real work in view, with a little more end-of-the-world energy around it.

| Track your squad | Fly your fleet | Train between missions |
| --- | --- | --- |
| Character cards, live statuses, model and context details, pinning and sub-agent trees. | Seven ship identities, matching cockpit backgrounds, Git branch and upstream status. | Multi-front battles, custom squads and character conversations in a separate training Arena. |

## Install

You need the [Herdr desktop app](https://herdr.dev) installed, with `herdr-app` available in your shell. From the repository root, run:

```sh
./install.sh
```

The installer backs up replaced Doomsday Heroes files under `backups/doomsday-<timestamp>/`, validates all seven custom mods, then tries to select the layout. It leaves unrelated layouts, mods and settings untouched. The default destination is `~/.config/herdr-app`; set `HERDR_APP_HOME` to use another app home. If Herdr is not running, the files are still installed and you can select the layout from Herdr later.

To return to your previous workspace appearance, switch layouts in Herdr. Keep Herdr's built-in mods installed: this layout uses `workspace-chrome`, `pane`, `files` and `changes`. The top bar is `doomsday-tabs`, a copy of Herdr's `tabs` with a Bomb Run button added.

## Choose your side

One layout, two coordinated appearances:

| Vanguard | Eclipse |
| --- | --- |
| Ivory surfaces, blue accents and warm cockpit lighting. | Charcoal surfaces, muted red accents and darker cockpits. |
| 14 available Avengers & Doombots. | The same roster, with Doctor Doom joining the cast. |

The layout follows system appearance until you select a side. Use **Doomsday Heroes: Vanguard** or **Doomsday Heroes: Eclipse** in the command palette, or run:

```sh
herdr-app do doomsday-systems.light
herdr-app do doomsday-systems.dark
```

These commands change both appearance and palette while preserving unrelated settings. Herdr's `app.theme` command changes the palette only. Return to automatic switching with **Settings → Look → System**.

<details>
<summary>Explore the cockpit artwork</summary>

<table>
  <tr>
    <th>Vanguard · Avenjet</th>
    <th>Eclipse · Quinjet</th>
  </tr>
  <tr>
    <td><img src="backgrounds/ships/vanguard/arrowhawk.png" alt="Vanguard Avenjet cockpit" width="100%"></td>
    <td><img src="backgrounds/ships/eclipse/skyrunner.png" alt="Eclipse Quinjet cockpit" width="100%"></td>
  </tr>
</table>

Every ship has both appearances: **Quinjet, Avenjet, Royal Talon, Helicarrier, Benatar, S.H.I.E.L.D. Dart** and **Latverian Barge**. Each space keeps a stable ship identity; its cockpit follows that space and the active appearance.

</details>

## The cast

<p align="center">
  <img src="mods/doomsday-agents/sprites/doomsday/ironman.svg" alt="Iron Man" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/cap.svg" alt="Captain America" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/thor.svg" alt="Thor" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/hulk.svg" alt="Hulk" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/widow.svg" alt="Black Widow" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/hawkeye.svg" alt="Hawkeye" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/spiderman.svg" alt="Spider-Man" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/strange.svg" alt="Doctor Strange" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/wanda.svg" alt="Scarlet Witch" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/panther.svg" alt="Black Panther" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/vision.svg" alt="Vision" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/loki.svg" alt="Loki" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/fury.svg" alt="Nick Fury" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/doombot.svg" alt="Doombot" width="40">
  <img src="mods/doomsday-agents/sprites/doomsday/doom.svg" alt="Doctor Doom" width="40">
</p>

Iron Man, Captain America, Thor, Hulk, Black Widow, Hawkeye, Spider-Man, Doctor Strange, Scarlet Witch, Black Panther, Vision, Loki, Nick Fury and Doombot are available in both appearances. Doctor Doom joins on the Eclipse.

Characters stay unique across agents; extra agents receive Doombots after the other available characters are assigned.

| Agent status | In your workspace |
| --- | --- |
| **Working** | On mission. Long-running work progresses through **Holding the line**, **Front line** and **Last stand**. |
| **Blocked** | Needs backup, with a visible `!` indicator. |
| **Done** | Mission complete, with a completion marker. |
| **Idle** | On standby. |

Pin agents, fold groups, or inspect live sub-agent trees. Cards show model and context details when detected. Character-aware alerts and the status bar highlight agents that need attention.

### Mini battles

Two or more agents in the same space appear over that space's cockpit. Working characters attack, blocked characters hold position, and done characters celebrate. Dialogue alternates between speakers, with pair-specific quotes and status-aware lines.

Each space has its own **Pause** control. Use **Squad** to page through larger groups and **Expand** to open the visible squad in the Arena. Speech bubbles point toward the speaker and keep their own row below the characters, not over their heads.

## Battle Simulator

A separate training scene, with no commands sent to real agents.

1. **Build a matchup.** Choose **Avengers**, **Doomsday**, **Strike team** or **Council**, or pick **Custom** and select 2–8 fighters from the full cast. Selection order defines pairs; an odd fighter stays on standby.
2. **Follow the action.** Up to four fronts run at once, with Captain America's Vibranium Shield, Thor's Mjolnir, Iron Man's repulsors & thrusters, Hulk's gamma smash, Spider-Man's webs & leaps, Black Widow's twin batons, Black Panther's twin claws, Doctor Strange's eldritch magic, Scarlet Witch's chaos hexes and Doctor Doom's arcane bolts. Nick Fury remains unarmed on tactical support.
3. **Tune the conversation.** Click a fighter to hear that front; click again to return to squad comms. Use **Next line** to advance or **Replay** to restart the conversation. Current and previous lines appear in separate speech bubbles with speaker portraits and Avengers training banter.
4. **Set the pace.** Choose **0.5× / 1× / 2×**, **Pause / Resume**, or **Motion: reduced** to keep comms without moving or pulsing effects. Close with **Close** or Escape.

Open **Doomsday Heroes: Battle Simulator** from the command palette, use **Expand** in a mini battle, or run:

```sh
herdr-app do mod.open --name doomsday-arena
```

Expanded battles keep their source space's cockpit, even when another space is active. Selection and playback settings reset when the overlay is reopened. Native animations stop when not drawn; dialogue pauses with the simulation or when the app window is hidden.

<details>
<summary>See the Arena</summary>

<p align="center">
  <img src="docs/images/arena.svg" alt="Illustrated Battle Simulator with the Doomsday preset: Iron Man and Doctor Doom, Doctor Strange and Scarlet Witch, and Thor and Loki on three training fronts" width="840">
  <br>
  <sub>Illustration built from the project artwork. Not a screenshot.</sub>
</p>

</details>

## Bomb Run

A small Bomberman-style arcade game. Open it from the command palette or from the **Bomb Run** button in the top bar, next to Files and Changes. A second click hides it again. Don't want the game? Run **Doomsday Heroes: Toggle Bomb Run** from the command palette to remove the button (run it again to bring it back); the setting is saved. To open it directly:

```sh
herdr-app do mod.open --name doomsday-bomb-run
```

A dedicated pixel-art deck, with space visible through the forward windows, wall consoles, destructible coolant cells and thermal detonators. A single icon toolbar, inline counters and a small pilot strip use Herdr's theme; the map keeps its own pixel palette. Start, pause and defeat messages appear in a compact lower ribbon rather than covering the center of the arena. The **sliders icon** opens mission options and the upgrade list; on-screen directional controls are optional and hidden by default. Your pilot uses the character assigned to an open agent, with three-pose walking atlases in four directions — no floating avatar or whole-body bounce.

Click **Start mission** or press **Enter** to play. Hold **WASD / arrow keys** to walk, and press **Space** to plant a charge. **P / Escape** pauses; **Enter** resumes; **R** restarts the current deck without losing pilot upgrades. The **×** at the far right of the toolbar always closes the game panel or overlay. Escape from the start, defeat or pause screen also closes it. Switching tabs, leaving the game or hiding Herdr automatically pauses the run. The pilot arrows load another agent's progress; **↗** opens a separate larger game. This is a local training game: it never commands real agents.

**Characters stay unique, including your pilot.** Only Doombots can repeat. Clearing a zone unlocks **Next deck**. Eight Avengers zones each have their own solid-wall maps, props, palettes and architecture: **Stark Arc Core, Helicarrier Deck, Hydra Siberia Lab, Wakanda Vault, Sanctum Sanctorum, Avengers Tower, The Raft and Castle Doom Foundry**. Later sectors revisit these zones with new energy cell placements and opposing rosters. Patrols get faster and the squad grows from four to eight hostiles.

**Your agent's pilot evolves through milestones, not loot.** Coolant cells give 5 XP, hostiles 40 XP, and clearing a deck another 75 XP. XP and the highest unlocked deck are saved locally per agent, including after defeat or reopening. Ranks track XP, while combat upgrades require **both** a minimum deck and total XP. There are no floor modules, random drops or stackable buffs.

| Upgrade | Requires | Effect |
| --- | --- | --- |
| **Blast extender** | Deck 2 + 200 XP | 3-tile reach; 4 at deck 5 + 1,200 XP, 5 at deck 8 + 2,200 XP |
| **Extra magazine** | Deck 3 + 600 XP | 2 charges; 3 at deck 8 + 2,200 XP |
| **Line launcher** | Deck 5 + 900 XP | **Q / Line** plants a facing row using available charges, stopping at obstacles |
| **Nova payload** | Deck 6 + 1,400 XP | Optional three-tile-wide blast lanes |
| **Sprint boots** | Deck 7 + 1,800 XP | One speed improvement: 160 → 120 ms per tile (1.33×) |
| **Echo charge** | Deck 8 + 2,400 XP | Optional second explosion after one second, marked by warning beacons |

**E** cycles unlocked payloads: Standard, Nova or Echo. **Nova and Echo cannot be combined.** Range is capped at five tiles, capacity at three charges, and speed has only one upgrade. The upgrade list in Mission options shows locked/unlocked milestones; hover for requirements and effects. Retries keep XP and unlocks, but start with the Standard payload. Consoles still block damage, coolant cells stop a ray after breaking, and planted charges snapshot their payload. Echo never repeats recursively, and a deck cannot finish with pending charges or echoes.

**Optional: Thinking only.** Use the **link icon** in the toolbar, or the descriptive switch in Mission options, to play only while the **selected pilot's agent** reports `working`. Idle, done, blocked, unknown and disconnected agents freeze the entire game: patrols, fuses, echoes, time, XP and gameplay inputs. A waiting screen explains the block. When the agent works again, an already running game continues without resetting or replaying held keys; manual/focus pauses still require Resume. The switch is saved locally, defaults to Off, and never commands the agent.

<details>
<summary>See Bomb Run</summary>

<p align="center">
  <img src="docs/images/bomb-run.svg" alt="Illustrated Bomb Run on the Helicarrier Deck with energy cells, a Stark Arc charge, a blast lane and the Avengers cast" width="440">
  <br>
  <sub>Illustration built from the game's own pixel art. Not a screenshot.</sub>
</p>

</details>

<details>
<summary>Explore all eight deck layouts</summary>

<img src="docs/images/bomb-run-decks.png" alt="Pixel-art layout overview of Stark Arc Core, Helicarrier Deck, Hydra Siberia Lab, Wakanda Vault, Sanctum Sanctorum, Avengers Tower, The Raft and Castle Doom Foundry zones" width="896">

Generated artwork and fixed wall layouts, not an app screenshot. Energy cells and characters are omitted so each zone’s architecture is visible.

</details>

## Model and context details

Model and context values are inferred from terminal output every 15 seconds, not provided directly by Herdr. If no supported value is found, the card omits it.

<details>
<summary>Supported status-line formats</summary>

- **Claude Code:** `ctx 27%`, a percentage bar, or `Context left until auto-compact: 73%`.
- **pi:** footer formats such as `12.6%/500k` and `(provider) model • medium`.
- **Other agents:** model names such as `gpt-*` and lines like `85% context left`.

Claude Code does not show a status line by default. Configure one to print model and context usage if you want these details on its card.

</details>

## Notifications

In-app alerts work without extra tools. System banners use:

| Platform | Optional system integration |
| --- | --- |
| **macOS** | `terminal-notifier` (`brew install terminal-notifier`). Clicking its banner activates Herdr. |
| **Linux** | `notify-send` from `libnotify`. |
| **Windows** | In-app alerts only. |

Notification permissions may also need to be enabled in the operating system. If the helper is missing or fails, the in-app alert remains the fallback. macOS notifications never fall back to AppleScript, because those banners can open Script Editor instead of Herdr.

## Customize and test

| Change | Edit |
| --- | --- |
| Interface colors and cockpit palettes | `themes/vanguard.json`, `themes/eclipse.json` |
| Character pixels and palettes | `tools/build-sprites.py` |
| Arena presets, character profiles and dialogue | `mods/doomsday-arena/choreography.js` |
| Bomb Run compact chrome and options drawer | `mods/doomsday-bomb-run/ui.js` |
| Bomb Run grid, buffs and game rules | `mods/doomsday-bomb-run/game.js` |
| Bomb Run zone identities and wall maps | `mods/doomsday-bomb-run/decks.js` |
| Bomb Run deck, props, bitmap labels and walking atlases | `tools/build-bomb-run-art.py` |
| Mini-battle dialogue and presentation | `mods/doomsday-agents/battle.js` |
| README illustrations and `preview.png` | `tools/build-readme-art.py` |

Rebuild artwork after changing its source:

```sh
python3 tools/build-sprites.py --preview /tmp/doomsday-sprites.png
python3 tools/build-ship-backgrounds.py --preview /tmp/fleet-backgrounds.png
python3 tools/build-readme-art.py
# preview.png is the overview illustration rendered at 2x, e.g. with headless Chrome:
# chrome --headless=new --force-device-scale-factor=2 --window-size=1440,760 --screenshot=preview.png docs/images/overview.svg
python3 tools/build-bomb-run-art.py --preview docs/images/bomb-run-decks.png
```

The builders use Python's standard library. Run the regression suite with Node's built-in test runner:

```sh
node --test tools/*.test.mjs
```

The tests cover theme contrast, local assets, both battle appearances, custom rosters, dialogue, squad paging, per-space controls, pause, speed and reduced motion. Validate changed mods with `herdr-app check mods/<mod-name>` as well.

For the implementation map, see [Architecture](docs/architecture.md).

## Herdr gallery

This repository is a [Herdr community layout](https://herdr.dev/layouts): the root holds `layouts/doomsday.json`, its `mods/`, the [`RECIPE.md`](RECIPE.md) brief and `preview.png`, and the repo carries the `herdr-layout` topic.

## Inspiration and credits

Inspired by [Herdr Middle-earth](https://github.com/joaovitorwoliveira/herdr-middle-earth), particularly its character-driven approach to a Herdr workspace.

General Herdr behavior is adapted from the `agents`, `toast`, `workspace-status` and `spaces` mods. Their source lineage is recorded in each mod's `cloned_from` metadata. See [Inspiration and credits](docs/inspiration.md) for more context.

---

Fan-made pixel-art tribute project for Herdr. Not affiliated with or endorsed by Marvel Studios or Disney.
