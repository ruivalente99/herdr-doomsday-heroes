// How notifications look. Anything can post one with notify({ title, body,
// level, icon, action }); replace this mod to restyle them all. Click to
// run its action (e.g. go to the agent) and dismiss it.

import { View, div, image } from "gpui-kit";
import { v_flex, h_flex } from "gpui-base";
import { props, closeOverlay, run, theme, shared, exec, window, appHome, checking } from "herdr";

// Shared character assignments from the Doomsday Heroes Agents mod.
const CAST_KEY = "doomsday-agents.cast";
const HERO_ICON_SIZE = 28;
const AGENT_TOAST = /^(.+) (finished|needs you)$/;
const QUEST = {
  finished: { pose: "done", line: "completed the mission" },
  "needs you": { pose: "blocked", line: "needs backup" },
};
const HERO_NAMES = {
  doom: "Doctor Doom",
  ironman: "Iron Man",
  cap: "Captain America",
  thor: "Thor",
  hulk: "Hulk",
  widow: "Black Widow",
  hawkeye: "Hawkeye",
  spiderman: "Spider-Man",
  strange: "Doctor Strange",
  wanda: "Scarlet Witch",
  panther: "Black Panther",
  vision: "Vision",
  loki: "Loki",
  fury: "Nick Fury",
  doombot: "Doombot",
  sam: "Sam Wilson",
  antman: "Ant-Man",
  cassie: "Cassie Lang",
  shangchi: "Shang-Chi",
  mbaku: "M'Baku",
  falcon: "Falcon",
  peggy: "Peggy Carter",
  deadpool: "Deadpool",
  mrfantastic: "Mister Fantastic",
  invisiblewoman: "Invisible Woman",
  humantorch: "Human Torch",
  thing: "The Thing",
  yelena: "Yelena Belova",
  bucky: "Winter Soldier",
  usagent: "U.S. Agent",
  redguardian: "Red Guardian",
  sentry: "Sentry",
  ghost: "Ghost",
  professorx: "Professor X",
  magneto: "Magneto",
  cyclops: "Cyclops",
  beast: "Beast",
  gambit: "Gambit",
  mystique: "Mystique",
  nightcrawler: "Nightcrawler",
  namor: "Namor",
};
const HERO_LINES = {
  doom: {
    done: (name) => `${name}'s triumph was inevitable`,
    blocked: (name) => `${name} demands your immediate attention`,
  },
  ironman: {
    done: (name) => `${name} wrapped the build — Jarvis, queue the music`,
    blocked: (name) => `${name} needs a suit reboot`,
  },
  cap: {
    done: (name) => `${name} has completed the mission`,
    blocked: (name) => `${name} needs backup on the line`,
  },
  thor: {
    done: (name) => `${name} brings victory from Asgard`,
    blocked: (name) => `${name} calls for aid on the battlefield`,
  },
  hulk: {
    done: (name) => `${name} smashed the mission`,
    blocked: (name) => `${name} needs help — getting angry`,
  },
  widow: {
    done: (name) => `${name} cleared the ledger`,
    blocked: (name) => `${name} is calling for extraction`,
  },
  hawkeye: {
    done: (name) => `${name} hit the bullseye`,
    blocked: (name) => `${name} is out of arrows and needs backup`,
  },
  spiderman: {
    done: (name) => `${name} wrapped it up in webbing`,
    blocked: (name) => `${name}'s spider-sense is tingling — needs help`,
  },
  strange: {
    done: (name) => `${name} found the one winning outcome`,
    blocked: (name) => `${name} sees a timeline snag`,
  },
  wanda: {
    done: (name) => `${name} bent reality to finish`,
    blocked: (name) => `${name} needs backup to contain this`,
  },
  panther: {
    done: (name) => `${name} secured the objective`,
    blocked: (name) => `${name} requests reinforcements`,
  },
  vision: {
    done: (name) => `${name} calculated a successful mission`,
    blocked: (name) => `${name} reports an unexpected anomaly`,
  },
  loki: {
    done: (name) => `${name} achieved glorious purpose`,
    blocked: (name) => `${name} admits a minor complication`,
  },
  fury: {
    done: (name) => `${name} marks the operation complete`,
    blocked: (name) => `${name} needs you on deck immediately`,
  },
  doombot: {
    done: (name) => `${name} reports: directive complete`,
    blocked: (name) => `${name} lost uplink with Latveria`,
  },
  sam: {
    done: (name) => `${name} landed the mission on your left`,
    blocked: (name) => `${name} needs air support right now`,
  },
  antman: {
    done: (name) => `${name} finished — and barely shrank anything`,
    blocked: (name) => `${name} is stuck in the Quantum Realm — needs help`,
  },
  cassie: {
    done: (name) => `${name} nailed the quantum objective`,
    blocked: (name) => `${name} hit a Pym regulator snag`,
  },
  shangchi: {
    done: (name) => `${name} mastered the mission with the Ten Rings`,
    blocked: (name) => `${name} needs backup in the ring`,
  },
  mbaku: {
    done: (name) => `${name} claims victory for the Jabari`,
    blocked: (name) => `${name} calls for worthy reinforcements`,
  },
  falcon: {
    done: (name) => `${name} cleared the airspace`,
    blocked: (name) => `${name} lost Redwing telemetry — needs backup`,
  },
  peggy: {
    done: (name) => `${name} closed the SSR dossier cleanly`,
    blocked: (name) => `${name} requires your briefing immediately`,
  },
  deadpool: {
    done: (name) => `${name} finished — maximum effort!`,
    blocked: (name) => `${name} broke the fourth wall and needs you`,
  },
  mrfantastic: {
    done: (name) => `${name} solved the final variable`,
    blocked: (name) => `${name} stretched a hypothesis too far — needs input`,
  },
  invisiblewoman: {
    done: (name) => `${name} shielded the team through to completion`,
    blocked: (name) => `${name} is holding the force field — needs help`,
  },
  humantorch: {
    done: (name) => `${name} blazed through the mission`,
    blocked: (name) => `${name} needs a cooldown and backup`,
  },
  thing: {
    done: (name) => `${name} clobbered the whole task`,
    blocked: (name) => `${name} hit a brick wall — needs a hand`,
  },
  yelena: {
    done: (name) => `${name} wrapped the op without a scratch`,
    blocked: (name) => `${name} needs backup — and more pockets`,
  },
  bucky: {
    done: (name) => `${name} completed the objective`,
    blocked: (name) => `${name} is pinned down and needs support`,
  },
  usagent: {
    done: (name) => `${name} secured the perimeter`,
    blocked: (name) => `${name} requests immediate tactical backup`,
  },
  redguardian: {
    done: (name) => `${name} crushed the mission with glory!`,
    blocked: (name) => `${name} needs comrades on the front line`,
  },
  sentry: {
    done: (name) => `${name} finished in a flash of golden light`,
    blocked: (name) => `${name} needs grounding before things escalate`,
  },
  ghost: {
    done: (name) => `${name} phased past every obstacle`,
    blocked: (name) => `${name}'s containment field needs stabilization`,
  },
  professorx: {
    done: (name) => `${name} guided the mission to a peaceful close`,
    blocked: (name) => `${name} is calling for your focus`,
  },
  magneto: {
    done: (name) => `${name} bent every obstacle to his will`,
    blocked: (name) => `${name} requires your immediate intervention`,
  },
  cyclops: {
    done: (name) => `${name} executed the plan to the letter`,
    blocked: (name) => `${name} needs eyes on this sector`,
  },
  beast: {
    done: (name) => `${name} concluded the experiment with stars and garters`,
    blocked: (name) => `${name} encountered an unforeseen complication`,
  },
  gambit: {
    done: (name) => `${name} played the winning hand`,
    blocked: (name) => `${name} needs a fresh deal, mon ami`,
  },
  mystique: {
    done: (name) => `${name} slipped out with the objective secured`,
    blocked: (name) => `${name}'s cover is blown — needs extraction`,
  },
  nightcrawler: {
    done: (name) => `${name} bamfed across the finish line`,
    blocked: (name) => `${name} needs a clear landing zone`,
  },
  namor: {
    done: (name) => `${name} delivered victory from the deep`,
    blocked: (name) => `${name} demands counsel on deck`,
  },
};

// Only clicking a native banner should bring Herdr forward.
const HERDR_BUNDLE = "dev.herdr.app";

function reportFailure(tool) {
  return (r) => { if (r.code !== 0) console.error(`System notification failed (${tool} ${r.code}): ${r.stderr}`); };
}

// AppleScript banners can be attributed to Script Editor and open it when clicked.
// Never fall back to a script runner: keep the in-app toast if the native helper is unavailable.
function postToMacos(title, body, image) {
  const picture = image ? ["-contentImage", `${appHome()}/${image}`] : [];
  exec("terminal-notifier", ["-title", title, "-message", body || " ", "-activate", HERDR_BUNDLE, ...picture]).then(
    reportFailure("terminal-notifier"),
    (e) => console.warn(`Native macOS banner unavailable: ${e}. In-app alerts remain available. Install terminal-notifier (brew install terminal-notifier) to enable system banners.`),
  );
}

function postToLinux(title, body, image) {
  const icon = image ? ["-i", `${appHome()}/${image}`] : [];
  exec("notify-send", ["-a", "Herdr", ...icon, title, body]).then(
    reportFailure("notify-send"),
    (e) => console.error(`System notification failed (is notify-send installed?): ${e}`),
  );
}

// The in-app toast can't be seen from behind another app, so mirror it to the system's banners.
// Windows has no banner command to call, so there the in-app toast is all.
function postToSystem(platform, title, body, image) {
  if (platform === "macos") postToMacos(title, body, image);
  if (platform === "linux") postToLinux(title, body, image);
}

function heroOf(p) {
  const event = AGENT_TOAST.exec(p.title ?? "");
  const terminal = p.action?.name === "agent.focus" ? p.action.args?.terminal : null;
  const hero = terminal ? shared(CAST_KEY)?.[terminal] : null;
  if (!event || !hero || !HERO_NAMES[hero]) return null;
  const { pose, line } = QUEST[event[2]];
  const name = HERO_NAMES[hero];
  return {
    title: HERO_LINES[hero]?.[pose](name) ?? `${name} ${line}`,
    body: p.body ? `${event[1]} · ${p.body}` : event[1],
    icon: `mods/doomsday-agents/sprites/doomsday/${hero}.svg`,
    banner: null,
  };
}

const DOT = { error: "blocked", warning: "working", success: "done", info: "accent" };

export default class Toast extends View {
  // init, not render: from another macOS Space the window may not draw, so render may not run.
  init() {
    const w = window();
    if (checking() || !w || w.active) return;
    const raw = props() ?? {};
    const p = { ...raw, ...heroOf(raw) };
    postToSystem(w.platform, p.title ?? "Herdr", p.body ?? "", p.banner);
  }

  render(cx) {
    const t = theme();
    const raw = props() ?? {};
    const p = { ...raw, ...heroOf(raw) };
    const iconSize = p.icon === raw.icon ? 18 : HERO_ICON_SIZE;
    const login = /^([a-z0-9][a-z0-9_.-]{0,31}) needs login; run hc machine login \1$/.exec(p.body ?? "");
    const command = login ? `hc machine login ${login[1]}` : null;
    return h_flex()
      .id("toast")
      .size_full()
      .px(18)
      .gap(12)
      .items_center()
      .bg(t.popover)
      .cursor_pointer()
      .hover((s) => s.bg(t.hover))
      .on_click(() => {
        if (p.action?.name) run(p.action.name, p.action.args ?? {});
        closeOverlay(p.overlay);
      })
      .child(p.icon ? image(p.icon).w(iconSize).h(iconSize).flex_none() : div().size(8).rounded(4).flex_none().bg(t[DOT[p.level] ?? "accent"]))
      .child(
        v_flex()
          .flex_1()
          .overflow_hidden()
          .child(div().truncate().font_semibold().text_size(13).text_color(t.foreground).child(login ? `${login[1]} needs a login: run` : p.title ?? ""))
          .when(!login && Boolean(p.body), (el) => el.child(div().truncate().text_size(12).text_color(t.muted).child(p.body ?? "")))
          .when(Boolean(login), (el) => el.child(h_flex().gap(8).items_center()
            .child(div().flex_1().min_w(0).truncate().tooltip(command).text_size(12).text_color(t.muted).child(command))
            .child(div().id("toast-login-copy").flex_none().px(6).py(3).rounded(4).bg(t.raised)
              .text_size(12).text_color(t.foreground).cursor_pointer().hover(s => s.bg(t.hover))
              .on_click((_e, cx) => { cx.stop_propagation(); cx.write_to_clipboard(command); this.copied = true; cx.notify(); })
              .child(this.copied ? "Copied" : "Copy")))),
      );
  }
}
