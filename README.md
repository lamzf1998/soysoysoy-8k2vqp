# SOYSOYSOY — a crab's crossing

A Crossy Road–style game starring Soy the crab. Cross 50 rows of beach highway,
tidal channels and a boardwalk tram line to reach the finish banner. Past it, a
red carpet leads to a locked convention door, and past that a game convention where
Olaf deals a hand of solitaire — win it and an envelope floats up with an invitation
inside.

## The six acts

1. **The crossing** — 40 rows of traffic, water and trams, with the tide pushing behind you
2. **The four-colour lock** — Mastermind on the convention door, refereed by a Psyduck
   with a migraine (see below)
3. **The convention** — Klondike solitaire: draw one, unlimited redeals, dealt by a
   snowman who comments on everything. Every hand is one a solver has already won, and
   **Hint** picks up the right card for you (see below). "New deal" reshuffles anyway,
   and after a while Olaf offers to wave you through
4. **The quiz** — five questions on a game-show stage, hosted by a sea otter.
   **A wrong answer sends you back to the solitaire tables** and restarts the quiz
5. **Wend** — the final round (see below)
6. **The invitation** — the envelope, and what's inside it

## Solitaire you can't get stuck on

Olaf never deals a hand that can't be won. Shuffles are run past a solver built into
`index.html` — a depth-first search over draw-one Klondike with a visited set, automatic
safe moves to the foundations, and a node budget — and only a shuffle the solver actually
beats gets dealt. A hand it finds *hard* is thrown away too, which is the point: the
budget quietly filters for gentle deals. Around half of shuffles survive, and they're
hunted in the background from the moment the page loads, so the search never lands on a
frame you can see.

**Hint** then works the board you're actually looking at. The route the solver used to
prove the deal is kept and becomes the opening plan, so the first hint costs nothing, and
the button hands the route over one move at a time, remembering which board each move
belongs to — ask again after playing one and you're a step further along. (Picking a good
move fresh each time instead is what makes hints loop: two moves that undo each other both
look fine in isolation.) A hint picks the card up for you; you tap the pile glowing gold.

Wander off the route and it solves again from wherever you've got to, with two wrinkles
worth knowing. If you've only been turning cards, the board is still on the route and just
the deck has been wound past it — that's spotted by matching the board while ignoring the
deck position, and the hint simply says keep turning. And when a search does stall, it
restarts with the move order shuffled rather than grinding the same bad order for longer,
which turns out to matter far more than searching longer does.

Careless play can still lose a winnable hand — that part is real solitaire, and Olaf's
giveaway button is the way out. But there's no such thing as a hand that was doomed from
the deal.

## The four-colour lock

Mastermind. A hidden code of four pegs drawn from five colours, repeats allowed, twenty
guesses. After each guess you get the standard pair of counts, rendered as dots on the
two edges of the row rather than as one cluster: **red dots against the left rail** for
pegs that are the right colour in the right hole, **white dots against the right rail**
for right colours in the wrong holes. Splitting them means neither count has to be read
by hue, and only the dots actually earned are drawn — an empty placeholder would read as
a count of its own once the two colours sit apart. Each peg is counted once, so four
whites means all four colours are present and every one is misplaced. That rule is
printed on the stage above the board, at a size you can read from a phone, because the
round is unplayable without it.

Every colour also carries a glyph — ● ▲ ■ ◆ ✚ — so the round never comes down to telling
two hues apart. The pink shell was cut when the palette came down to five: it sat too
close to the crab red, and dropping it leaves five colours nobody has to squint at.

Psyduck holds the code and can't bear to look at it. His headache is the guess counter:
the meter fills, the red haze behind his head thickens, and his shaking gets faster and
tighter through six stages, from "a dull throb" to "one more and he's gone". The stages
are spread proportionally across the round, with the last one held back for the very final
guess, so changing the guess limit re-paces the whole performance on its own. Spend all
twenty guesses and he faints — keels over sideways, greys out — then comes round, the lock
reshuffles itself, and you start again on a fresh code with your hints restored. There's
no way to lose the round permanently, which is the same promise the solitaire makes.

Two things keep it gentle:

- **Codes never contain three of a kind.** Shuffles with a triple are thrown away, which
  leaves 540 of the 625 possible codes. Triples are the ones that make the counts feel
  like they're lying to you
- **Hint tells the truth and pins it.** It reveals one hole's actual colour, rings it gold
  and locks it into every guess from then on, so you can't undo it by accident. Two hints
  per code

Twenty guesses is far more than enough, which is the intent — this round is a lap of
honour, not a wall. Playing the plainest possible strategy (always guess the first code
still consistent with every answer so far) the worst case across all 540 dealable codes is
**seven** guesses and the average is 4.5. And if the headache somehow wins anyway, Psyduck
offers to just tell you the code.

Twenty rows would otherwise push the pegs off a phone screen, so the history scrolls inside
its own pane and follows the newest guess down.

## The Wend grid

Wend's rule is that every letter in the grid is used exactly once, so the words have to
tile the board perfectly. Seven words — HAPPY, ANNIVERSARY, BABY, SOY, SAUCE, CRAB, TIME —
come to exactly 36 letters, which is exactly a 6×6 board:

```
M  E  C  R  S  O
I  T  Y  A  B  Y
P  A  R  A  E  V
P  H  E  S  R  I
Y  U  C  B  Y  N
S  A  B  A  A  N
```

Drag up, down, left or right across neighbouring letters — **no diagonals** — to spell a
word. Every word snakes, so there are no straight-line freebies. **Clear** drops the
current selection; **Hint** lights up the first letter of a word you haven't found.

`wend-solver.py` produced this layout. It backtracks to tile the grid, runs a few thousand
times with randomised ordering, and keeps the wiggliest result that also passes an
**unambiguity check**: every word must have exactly one possible path through the grid.
Without that check some grids let you spell, say, ANNIVERSARY along a second route, consume
letters another word needed, and strand the board with no way back.

## Playing

`index.html` is completely self-contained (no build step, no external files — the
photo is embedded as a data URI). Just double-click it, or open it in any browser.

- **Solitaire**: tap a card, then tap a green column. **Hint** if you'd rather not think
- **The lock**: tap a colour to drop it in the next hole, tap a placed peg to take it out,
  then **Guess**. On a keyboard, `1`–`5` place a colour, `Backspace` takes one back and
  `Enter` guesses
- **Move**: arrow keys or WASD
- **Touch**: swipe in any direction, tap to hop forward, or use the on-screen D-pad
- Sound can be toggled with the `SND` button

Hazards: cars flatten you, open water drowns you (ride the driftwood and surfboards),
the tram is fast and only warns you with blinking lights, and if you dawdle the
incoming tide pushes the camera forward until a seagull takes you.

## Skipping ahead while testing

A dashed **Skip stage ▸** button sits in the bottom-right corner. Each press jumps
one stage forward: the crossing → the lock → the convention → the quiz → Wend →
the envelope → the invitation. It's on by default.

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

- The character sprites arrived as RGB images with a transparency checkerboard painted
  into the pixels rather than a real alpha channel. `osha-decheckerboard.py` and
  `psyduck-decheckerboard.py` flood-fill the checkerboard from the image border, eat the
  lossy fringe, crop and save real alpha to `osha-cut.webp` / `psyduck-cut.webp`. A border
  flood fill is safe here because both characters' own white areas (eyes, beak) sit inside
  a dark outline, so the fill can't leak into them. The results are then inlined into
  `index.html` as base64 data URIs, which is why there's no build step
- Rendered on a single 2D canvas, DPI-aware, resizes to any viewport
- Sound is synthesised with the Web Audio API — no audio assets
- Includes a `roundRect` polyfill for iOS Safari below version 16
