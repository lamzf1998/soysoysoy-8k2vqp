# SOYSOYSOY — a crab's crossing

A Crossy Road–style game starring Soy the crab. Cross 50 rows of beach highway,
tidal channels and a boardwalk tram line to reach the finish banner. Past it, a
red carpet leads into a game convention where Olaf deals a hand of solitaire —
win it and an envelope floats up with an invitation inside.

## The five acts

1. **The crossing** — 40 rows of traffic, water and trams, with the tide pushing behind you
2. **The convention** — Klondike solitaire, medium: draw one, unlimited redeals, dealt by
   a snowman who comments on everything. "New deal" reshuffles a cold hand, and after a
   while Olaf offers to wave you through
3. **The quiz** — five questions on a game-show stage, hosted by a sea otter.
   **A wrong answer sends you back to the solitaire tables** and restarts the quiz
4. **Wend** — the final round (see below)
5. **The invitation** — the envelope, and what's inside it

## The Wend grid

Wend's rule is that every letter in the grid is used exactly once, so the words have to
tile the board perfectly. Seven words — HAPPY, ANNIVERSARY, BABY, SOY, SAUCE, CRAB, TIME —
come to exactly 36 letters, which is exactly a 6×6 board:

```
E  A  I  Y  P  H
N  M  T  Y  A  P
V  N  R  E  S  U
I  E  S  A  C  A
B  R  Y  C  R  B
Y  A  B  O  S  A
```

Every word snakes (no straight-line freebies). Drag across neighbouring letters —
diagonals count — to spell one. **Clear** drops the current selection; **Hint** lights up
the first letter of a word you haven't found.

The layout came from `scratchpad/wend2.py`: a backtracking search that tiles the grid,
run a few hundred times with randomised ordering, keeping whichever solution bends the most.

## Playing

`index.html` is completely self-contained (no build step, no external files — the
photo is embedded as a data URI). Just double-click it, or open it in any browser.

- **Move**: arrow keys or WASD
- **Touch**: swipe in any direction, tap to hop forward, or use the on-screen D-pad
- Sound can be toggled with the `SND` button

Hazards: cars flatten you, open water drowns you (ride the driftwood and surfboards),
the tram is fast and only warns you with blinking lights, and if you dawdle the
incoming tide pushes the camera forward until a seagull takes you.

## Skipping ahead while testing

A dashed **Skip stage ▸** button sits in the bottom-right corner. Each press jumps
one stage forward: the crossing → the convention → the envelope → the invitation.
It's on by default.

To hide it in the version you actually send, append `?dev=0` to the link:

```
https://lamzf1998.github.io/soysoysoy-8k2vqp/?dev=0
```

No rebuild needed — the same page serves both.

## Hosting

Live at **https://lamzf1998.github.io/soysoysoy-8k2vqp/**

Served by GitHub Pages from the `main` branch of `lamzf1998/soysoysoy-8k2vqp`.
The repo name is deliberately unguessable, and `robots.txt` plus a `noindex` meta
tag ask search engines to stay away — but the URL is still technically public,
so treat it as "anyone with the link".

To update the live site: edit `index.html`, then

```
git add -A && git commit -m "..." && git push
```

Pages rebuilds in a minute or two.

Because it's a single static file, it also drops onto any other static host:

| Option | How |
| --- | --- |
| Netlify / Vercel | Drag the folder onto the dashboard |
| itch.io | Zip `index.html`, upload as an HTML project, tick "This file will be played in the browser" |
| Local network | `python -m http.server 8000` in this folder |

## Notes

- Rendered on a single 2D canvas, DPI-aware, resizes to any viewport
- Sound is synthesised with the Web Audio API — no audio assets
- Includes a `roundRect` polyfill for iOS Safari below version 16
