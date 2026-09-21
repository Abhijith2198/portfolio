# Portfolio design notes

## Direction

The user-supplied [Creative portfolio / web, graphic, ux/ui](https://www.behance.net/gallery/254984081/Creative-portfolio-web-graphic-uxui) reference by Katsiaryna Tretsiakova informed the large sans-serif typography, compact identity badge, rounded image stages and generous white space. No images, portrait, project content or code were taken from that reference.

The cover uses a sunlit plaster studio photograph, dark typography and a shared display platform for the original Meridian laptop and Verge phone mockups. The phone is smaller in proportion to the laptop, and both stand along a common baseline with space between them. The platform is drawn with HTML/CSS/SVG on the website and vector shapes in the PDF. Both formats read the chosen backdrop from `coverBackground` in the shared JSON. The sky remains in the footer and contact page.

The design pairs this visual treatment with Abhijith's original RepUp, Meridian and Verge mockups, a recreated vector Zomato IA composition, and case-study content drawn from the supplied portfolio sources. The website and 20-page, 16:9 PDF share `content/portfolio.json`.

## Project imagery

- RepUp, Meridian and Verge device mockups are original exports from the supplied Figma files. `assets/img/mockups/sources.json` records their provenance. Empty transparent margins were trimmed without altering screen content.
- RepUp Home was freshly exported through the Figma connector at 880 × 1,912 pixels. Other project screens retain the supplied full-size exports.
- Images preserve their aspect ratios. Detailed screens and boards can be enlarged from the case-study pages.
- Research findings are attributed to project materials. Design intentions and proposed validation are kept distinct from measured results.
- Confidential client work and the later food-delivery project are excluded.

## Generated backgrounds

The atmospheric sky and two architectural studio backdrops were generated using the built-in image generation tool. The sky appears with a darker overlay in the website footer and PDF contact page. No local image-generation CLI or API key was used. All devices and project screens remain original supplied assets.

The sunlit plaster studio is the selected cover background. Its natural light, restrained warmth and fine texture complement the project screens. A cooler gallery backdrop was also reviewed in the cover and retained as an alternative.

- Selected: [studio-sunlit.png](assets/img/identity/studio-sunlit.png) and [studio-sunlit.webp](assets/img/identity/studio-sunlit.webp).
- Alternative: [studio-gallery.png](assets/img/identity/studio-gallery.png) and [studio-gallery.webp](assets/img/identity/studio-gallery.webp).
- Both originals are 1,672 × 941 pixels. Their WebP versions preserve those dimensions, encoded at quality 96, with no enlargement or sharpening.
- Exact prompts, generation mode and saved asset paths are recorded in [background-sources.json](assets/img/identity/background-sources.json).

Sky assets:

- `assets/img/identity/sky-cover.png` — original generated PNG, 1,672 × 941 pixels.
- `assets/img/identity/sky-cover.webp` — same dimensions, encoded at quality 96 for the website and PDF. No enlargement or artificial sharpening was applied.

The requested resolution was higher than the tool's actual output; the delivered dimensions above are the verified dimensions.

Final generation prompt:

> Use case: photorealistic-natural. Asset type: original wide website portfolio cover background, also used in a 16:9 PDF. Create a crisp high-resolution photographic blue sky seen looking upward, with beautifully defined sunlit white cumulus clouds around the left and right edges and in the lower corners. Medium rich cornflower-blue to clear azure daylight, contemporary editorial fashion-magazine atmosphere. Panoramic landscape 16:9 composition, open uncluttered blue space through the central 65% and upper middle for real product mockups and oversized white HTML typography to be added separately. Realistic cloud texture, clean luminous daylight, refined color grading. The sky fills the entire frame; no horizon, no land, no buildings, no people, no objects, no typography, no logo, no watermark. Produce at the highest available resolution, ideally 3840 by 2160. This is a standalone atmospheric background, not a website screenshot or interface.

## Delivery

The site is static and ready for GitHub Pages. It includes relative links, bundled fonts, a resume download and portfolio PDF. Publishing has not changed the existing live website; these files are the completed local deliverables.
