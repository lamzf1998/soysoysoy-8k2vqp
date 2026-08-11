# SOYSOYSOY — a crab's crossing

A Crossy Road–style game starring Soy the crab. Cross 30 rows of beach highway,
tidal channels and a boardwalk tram line to reach the finish banner — then Soy
dives into a river of soy sauce and an envelope floats up with an invitation inside.

## Playing

`index.html` is completely self-contained (no build step, no external files — the
photo is embedded as a data URI). Just double-click it, or open it in any browser.

- **Move**: arrow keys or WASD
- **Touch**: swipe in any direction, tap to hop forward, or use the on-screen D-pad
- Sound can be toggled with the `SND` button

Hazards: cars flatten you, open water drowns you (ride the driftwood and surfboards),
the tram is fast and only warns you with blinking lights, and if you dawdle the
incoming tide pushes the camera forward until a seagull takes you.

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
