# Design System — The Workshop (Direction B)

The Workshop is a builder's notebook: graph paper, dark bench ink,
safety-orange accents. Editorial serif headlines, monospace for anything
technical. Light mode by default, with a client-side dark-mode toggle.

## Tokens

| Token | Light | Dark | Use |
|---|---|---|---|
| `--ink` | `#1a1a1e` | `#f4efe6` | Header/nav background (light); text (dark) |
| `--paper` | `#f4efe6` | `#17171b` | Page background (ivory) |
| `--paper-soft` | `#efe8d8` | `#1e1e24` | Photo placeholders |
| `--card` | `#fbf8f1` | `#202027` | Card background |
| `--text` | `#221f1a` | `#ece7db` | Body text |
| `--muted` | `#6b655a` | `#a49d8f` | Secondary text, empty states |
| `--line` | `#d8d0bf` | `#3a3a42` | Borders, dividers |
| `--accent` | `#e85d04` | `#f07b2a` | Safety orange — links, rules, markers |
| `--accent-ink` | `#b64a02` | `#f07b2a` | Link text on paper |

All colours are CSS variables on `:root` / `html[data-theme="dark"]`
in `static/site.css`. The theme toggle in `static/site.js` stores the
choice in `localStorage` (`srspady-theme`); an inline script in
`base.html` applies it before first paint. Default is light.

## Type

- **Headlines:** Georgia / Charter system serif stack (`--serif`).
  `h1` scales with `clamp(2rem, 6vw, 3.4rem)`.
- **Body:** system sans stack (`--sans`).
- **Eyebrows / labels / technical details:** monospace (`--mono`),
  uppercase, letter-spaced (`0.14em`), small (`0.75rem`), accent colour.
- **Dates, codes, stats labels:** monospace.

## Background

Graph paper: two repeating `linear-gradient` layers at 28px, using
`--grid-line` (5.5% ink on light, 6% paper on dark). Subtle — it should
read as paper, not as a grid.

## Layout — mobile-first, genuinely responsive

- Single column on phones. `card-grid` goes 1 → 2 columns at 720px →
  3 at 1024px. `stat-grid` goes 2 → 3 → 4. `photo-grid` 1 → 2 → 3.
- No fixed-width mock frames, no fixed pixel containers: `.wrap` is
  `max-width: 72rem` with fluid `1rem` side padding.
- Header nav collapses to a Menu button below 720px; the group nav
  (sections by group) is hidden on phones and shown from 720px up.
- Footer columns stack on phones, 3 columns from 720px.

## Components

- **`.btn`** — solid safety-orange, monospace. **`.btn-ghost`** —
  transparent with orange outline.
- **`.card`** — paper card, 1px line border, 3px orange left rule.
- **`.empty-state`** — dashed border, centred, muted. Used everywhere
  a section has no records yet. Never replaced with invented content.
- **`.photo-placeholder`** — dashed border, "Photograph to be added"
  in monospace. No stock or generated photos anywhere on the site.
- **`.stat`** — big serif "—" value, monospace label. All 12 life
  numbers are empty states until calculated from real records.
- **`.farelune`** — dark bench-ink block with the Farelune heading,
  link and affiliate disclosure.
- **`.timeline-item`** — left orange rule with orange dot markers.
- **`.build`** — a built project: nine numbered steps (why, what,
  design, materials, process, challenges, result, lessons, future).
```

## Accessibility

- Skip-to-content link, `aria-current="page"` on active nav, labelled
  toggle buttons (`aria-expanded` on the menu button).
- Colour contrast: accent-on-paper passes for large text and UI; body
  links use the darker `--accent-ink` on light mode.
- Theme respects the stored choice; `color-scheme: light dark` is set so
  form controls follow the theme.
