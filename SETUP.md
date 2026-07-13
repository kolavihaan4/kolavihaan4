# How to use this profile repo

This is a terminal / neofetch–style GitHub profile README.

## Files
- `README.md` .............. the profile (shows on your GitHub page)
- `vihaan-ascii.svg` ....... left panel: ASCII name banner
- `info-card.svg` .......... right panel: neofetch info card
- `contrib-heatmap.svg` .... contribution graph (auto-refreshes daily)
- `scripts/` ............... generators for the SVGs
- `.github/workflows/` ..... daily job that refreshes the contribution graph

## To publish
1. Put ALL of these files in your `kolavihaan4/kolavihaan4` repo (keep the folder structure).
2. Commit. Your profile updates immediately.
3. The contribution graph refreshes itself daily via GitHub Actions — no token needed.
   (First refresh happens on your next push, or the daily 06:17 UTC run.)

## To change the profile picture
The pfp is ASCII art rendered from `ascii-art.txt`:
1. Generate ASCII art from any image on a site like generator-ascii.art or inkmeascii.com
   (width ~200-300 chars gives good detail). Save the text.
2. Replace the contents of `ascii-art.txt` with your new art.
3. `python scripts/make_ascii_svg.py`  (regenerates vihaan-ascii.svg with the boot animation)

## To edit the text later
- Change role/stack/highlights: edit `scripts/make_info_card.py`, then run
  `python scripts/make_info_card.py`
- Change the banner/subtitle: edit `scripts/make_ascii_svg.py`, then run
  `python scripts/make_ascii_svg.py`
- Requirements to run locally: `pip install pyfiglet` (banner) and
  `pip install -r scripts/requirements.txt` (graph).
