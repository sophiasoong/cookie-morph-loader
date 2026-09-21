# Cookie Morph Loader

A loading indicator that springs through six shapes while it spins, in the style of the Material 3 Expressive loading indicator.

**Live demo:** https://sophiasoong.github.io/cookie-morph-loader/

Sequence (loops): 12-sided cookie → 9-sided cookie → 7-sided cookie → 6-sided cookie → 4-sided cookie → circle

## Files

| Path | What it is |
| --- | --- |
| `index.html` | Demo page: loader at 24/38/64px and a large size, playback (pause, 0.5×, 2×), shape size and color settings, recent colors |
| `cookie-morph-loader.svg` | Standalone animated SVG (380×380, `#6750A4`). Plays anywhere SVG animation runs, no JavaScript needed |
| `shapes/` | The six source shapes |
| `scripts/generate_svg.py` | Rebuilds `cookie-morph-loader.svg` from `shapes/` |

## Motion

| | |
| --- | --- |
| Time per shape | 650 ms |
| Morph | spring, stiffness 1000, damping ratio 0.6 (slight overshoot) |
| Turn per morph | +90°, on the same spring |
| Constant rotation | 360° every 4666 ms |

Every shape is resampled as 240 radii around the center (190, 190), so shapes with different side counts blend point-for-point. The keyframes are precomputed into native SVG animation (SMIL), so the loader plays even where scripts are blocked. JavaScript in the demo page only adds the controls.

## Regenerate the SVG

```bash
python3 scripts/generate_svg.py
```

Change the timing constants at the top of the script (`INTERVAL`, `STIFF`, `ZETA`, `K`) to tune the motion. The demo page embeds the same keyframes inline, so update `index.html` too if you change them.
