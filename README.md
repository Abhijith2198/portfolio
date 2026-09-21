# Abhijith U — Design portfolio

A complete static portfolio in HTML, CSS and a small amount of JavaScript. No framework, package installation or build is required to host it.

## Pages

- Home: `index.html`
- Case studies: `repup.html`, `meridian.html`, `zomato.html`, `verge.html`
- `explorations.html`: selected details from the four projects
- `about.html`: background, experience, education, contact and resume
- `assets/Abhijith-U-Portfolio.pdf`: 20-page 16:9 portfolio
- `assets/Abhijith-U-Resume.pdf`: existing resume, preserved from the original website

## Editing the shared content

`content/portfolio.json` is the shared source for both formats. Update it, then run:

```
python -m pip install pillow reportlab
python build.py
python generate_pdf.py
```

The website uses static generated HTML; visitors do not need Python or JavaScript to read the case studies. JavaScript only adds the image viewer and restrained entrance motion. The PDF generator saves the standalone PDF one directory above this folder and updates the website download.

## GitHub Pages

Place this folder's contents at the repository root. Use GitHub Pages with the `main` branch and `/ (root)` source. `.nojekyll` is included. All internal URLs are relative; the canonical URLs point to `https://abhijith2198.github.io/`.

Preview locally with `python -m http.server 4173`, then open `http://localhost:4173/`.

## Sources and image quality

Content comes from the supplied Figma files, the existing website, and `Abhijith-U-Portfolio.pdf`. The lineup excludes confidential work and the later food-delivery project. Research figures are presented as findings from the project materials; onboarding speed and other design goals are not presented as measured outcomes.

RepUp Home was freshly rendered from Figma at 880 × 1,912 pixels through the connector after direct asset requests hit Figma's web security challenge. Other screens use existing full-size exports from the original portfolio. The editorial covers use the original RepUp, Meridian and Verge mockups exported from the supplied Figma files. Only empty transparent margins were trimmed; screen content was preserved. Phone images are shown at or below their native pixel width; larger diagrams can be opened in the image viewer. PDF text and recreated IA diagrams are vector-based. No AI-generated substitute screens or image enlargement was used.

## Showcase edition

`assets/css/portfolio.css` supplies the base layout and `assets/css/showcase.css` supplies the blue identity, oversized sans-serif headlines, rounded project stages and responsive compositions. The supplied Behance reference informed the visual direction. The project imagery, writing and layouts are specific to this portfolio.

The Field notes, case-study design-intent passages and selected `coverBackground` live in the shared JSON content. Both formats use the original device mockups from `assets/img/mockups/`. The sky and studio backdrops are original AI-generated backgrounds; no project screens or mockups were generated. See `DESIGN-NOTES.md` for the reference, asset provenance and generation prompts.

The seven pages were checked at 320, 390 and 768 pixels, with desktop visual checks, local link validation and a working enlarged-image gallery. All 20 PDF pages were rendered for visual review. The PDF uses native text and internal project navigation.

The packaged website is ready for GitHub Pages. It has not been published to the live repository.

Fonts: Archivo and Instrument Serif, both under the SIL Open Font License; license files are in `assets/fonts/`. Project photography and embedded design imagery retain their original ownership and are used as part of the supplied portfolio concepts.
