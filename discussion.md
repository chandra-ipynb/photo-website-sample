# Project discussion

## Requested

- Replace the heavy Vistoriz export with a fast replica.
- Use lazy-loaded local images.
- Add Book Now, WhatsApp and call actions.
- Set studio details to Whizzteam19, `+91 99456 90520`, and the supplied Bengaluru address.
- Add a Python command for updating business details.
- Rename `vistoriz` to `sample`.
- Match Vistoriz's circular category hero and portfolio gallery behaviour.

## Implemented

- Responsive homepage: `index.html`.
- Clickable circular categories linking to matching sections in `portfolio.html`.
- First category opens a full-width horizontal “Portfolio Photoshoot Bangalore” gallery with arrow controls.
- Direct WhatsApp links open `web.whatsapp.com/send` for `919945690520` with a booking message, avoiding the `wa.me` landing screen on desktop.
- Floating WhatsApp and call buttons work on desktop and mobile.
- Business details are stored in `site-config.js`.

## Why all Vistoriz photos are not shown yet

- The `images` folder contains **348 files (76 MB)**, but many are different-size copies of the same photograph. After grouping those copies, there are approximately **122 distinct images**.
- The current homepage and portfolio reference only **21 unique image files**. I initially selected representative photos to reproduce the layout while keeping the first version fast.
- The old Wix/Vistoriz page used separate dynamic galleries and category pages. Rebuilding the page as lightweight static HTML did not automatically recreate those gallery assignments.
- Loading all 76 MB on one page would make mobile loading slow, consume unnecessary data, and work against the requested fast-loading behaviour.

## How the complete collection is shown

1. `build_gallery.py` inventories the archive and removes duplicate resolution copies.
2. Branding and unusable Wix preview placeholders are excluded, leaving **107 usable photographs**.
3. All 107 photographs are visually assigned to portfolio, headshots, portraits, family, matrimonial, couples, maternity, or baby.
4. The generated `gallery-data.js` uses one web-sized copy per photograph.
5. `portfolio.html` renders every categorized photograph. Images below the first visible pair use native lazy loading.
6. Desktop visitors get horizontal navigation for the featured portfolio and responsive grids for other categories; mobile visitors can swipe and scroll.
7. The homepage remains fast because it loads only the circular category covers.
8. Portfolio category tabs now behave like separate Vistoriz galleries: clicking one hides the other categories, shows only related photographs, highlights the selection, and updates the URL hash for direct linking.
9. The homepage category area now matches the reference layout more closely: five large circles on the first desktop row, three on the second, no extra heading above them, and new category-specific cover photographs.

To rebuild the gallery after changing `images/`, run `python3 build_gallery.py` and review any newly reported, unclassified photographs.

## Update command

```bash
cd "/Users/apple/Downloads/Business/3. AI Websites/Website Templates/Photography/sample"
python3 update_site.py --studio "My Studio" --phone "+919999999999" --address "My address"
```
