# CPS Prestige Construction website

Complete editable source for a modern static website. No paid theme, framework subscription, or package installation is required. All HTML, CSS, JavaScript, downloaded original CPS photos, optimized WebP photos, favicon, metadata, sitemap and robots file are included.

## Edit and rebuild

- Edit page content and SEO fields in `build.py`.
- Edit appearance in `dist/styles.css`.
- Edit mobile navigation and quote email fallback behavior in `dist/main.js`.
- Run `python3 build.py` to regenerate HTML.
- Preview locally: `python3 -m http.server 8000 --directory dist`, then open http://localhost:8000.
- Do not open HTML by double-clicking; root-relative navigation needs a web server.

## Production domain

The private review copy uses its review domain. For the actual CPS domain, run:

```bash
SITE_URL=https://www.cpsremodeling.com python3 build.py
```

On Windows PowerShell:

```powershell
$env:SITE_URL="https://www.cpsremodeling.com"
python build.py
```

Upload the contents of `dist/` to a static host. The host must serve `/folder/index.html` for folder URLs and use `404.html` for unknown paths. HTTPS is required for launch. Leave the existing CPS website running until the replacement is verified. Sites registration details in `.openai/hosting.json` apply only to the private review host, not an independent hosting account.

## Quote requests

Phone and email links remain available in both modes. The **single missing destination is `QUOTE_FORM_URL`: the public HTTPS submission URL issued by CPS's chosen form handler**. No endpoint has been supplied or invented; the checked-in site continues to use the existing email fallback.

- Leave `QUOTE_FORM_URL` unset or empty: the form opens the visitor's email app with their details. They must review and press Send themselves. This website does not receive or store those entries.
- Set `QUOTE_FORM_URL` at build time: the generated form posts directly from the browser to that URL, including without JavaScript. The browser navigates to the handler's response page. It does not also open email or retry by email, so a request is not knowingly sent twice. The handler must display its own success/error result; this site does not claim inbox delivery.

For local or independent hosting, set the real URL as an environment variable and run `python3 build.py`. For GitHub Pages, add a repository Actions **variable** named `QUOTE_FORM_URL` under Settings → Secrets and variables → Actions → Variables, then run “Publish CPS website” (or push to main). The Pages workflow passes the variable to the build. Clearing the variable and rebuilding restores email mode. The URL must be absolute HTTPS, without embedded credentials or a fragment; invalid nonempty values fail the build instead of silently using email.

The handler must accept a standard `application/x-www-form-urlencoded` POST with fields `name`, `email`, `phone` (optional), `location`, `service` and `message`, and return a browser-readable confirmation/error page. A native form POST does not require browser fetch/CORS support. Choose and configure a handler that delivers requests to CPS; any spam controls, server validation, rate limits and retention settings belong at the handler. A JSON-only API or a service requiring a private browser authorization key is not compatible with this form contract.

`QUOTE_FORM_URL` is public: it appears in generated HTML. Supply only the public submission URL, never a secret API key, password, bearer token or private credential, including in its query string. Configure private credentials and the recipient mailbox on the handler's server/provider dashboard. No private credential is needed by this repository or browser code.

Run the isolated build checks with `python3 -m unittest discover -s tests -v` and the JavaScript behavior checks with `node --test tests/test_quote_behavior.cjs`. They use reserved test domains and never submit leads.

The build updates contact instructions, the submit button and privacy notice together. Email mode explains that details pass through the visitor's email provider. Direct mode identifies the form-service hostname, lists the submitted fields and explains that CPS and the service process the request and may retain submission/technical data. Once the real service is chosen, confirm its handling and retention policies and revise the notice for any additional provider-specific disclosures before launch. Rebuild and verify the generated contact/privacy pages and a real test request with the chosen handler; no live delivery can be verified until the URL is supplied.

## Verify business details before public launch

- Current source homepage/footer: 5515 Allatoona Gwty, Acworth.
- Current source contact page: 5515 Glade Rd SE, Acworth.
- Street address was intentionally omitted because these conflict. The new site uses Acworth, GA 30102. Confirm the correct address and add it to visible contact details and JSON-LD.
- Phone retained: 404-542-8325. Email retained: cpsprestigeconstruction@gmail.com.
- The original site states 22 years of experience; the new site attributes this statement. Confirm the current experience claim.
- Atlanta-area inquiries are targeted as requested. Confirm actual service boundaries before expanding city claims.
- No invented ratings, reviews, license numbers, certification claims, warranties, hours or project locations were added.
- Text explaining project steps was newly written; confirm it matches your process.

## Assets

The logo and every photo were downloaded from the existing CPS public website; original source URLs are in `asset-sources.json` in index order. Files `photo-0.png` through `photo-27.jpg` preserve those originals. Optimized WebP images include orientation correction. Confirm the company's rights to reuse stock inspiration photos and project photos. Images from Re-Bath and Magnet were not copied. Hero photo is original-site design inspiration, not represented as a CPS project. Project gallery uses original-site portfolio images, except the Interior framing in progress image, replaced at the user’s request with pexels-rstephens-33405084.jpg. Its original and optimized copies are included as interior-framing-original.jpg and interior-framing.webp.

## SEO included

- Unique server-readable titles and descriptions on 10 pages.
- Crawlable HTML service pages, headings and internal navigation.
- Canonical URLs, Open Graph text, mobile viewport and theme color.
- GeneralContractor business data, WebSite data and breadcrumbs.
- Actual phone and email; Acworth locality and Atlanta-area targeting.
- XML sitemap and robots.txt.
- Descriptive image alt text, WebP images and lazy loading below the hero.

SEO metadata does not guarantee ranking. The private review host cannot be indexed by Google. Launch on a public domain, verify it in Google Search Console, submit `/sitemap.xml`, and request indexing. Claim or verify the Google Business Profile, keep the company name/address/phone consistent, and add genuine project descriptions and customer reviews over time. Search Console and Business Profile were not configured by this build.

Official references:
https://developers.google.com/search/docs/appearance/title-link
https://developers.google.com/search/docs/appearance/snippet
https://developers.google.com/search/docs/appearance/structured-data/local-business
https://developers.google.com/search/docs/appearance/establish-business-details

## Migration

Keep or redirect existing URLs `/services`, `/remodeling`, `/painting-drywall`, `/about`, and `/contact` to their new trailing-slash equivalents. Review the original sitemap for other indexed URLs and add host-level permanent redirects individually. A full audit of the old Wix backend, private files, inbox or unpublished content was not available. This is complete new-site source, not an export of Wix's proprietary platform source.

The Atlanta service-area image beside “Tell us where your project is” was replaced with the user-supplied pexels-curtis-adams-1694007-7601163.jpg. Original and optimized copies are included as service-area-home-original.jpg and service-area-home.webp. This image is inspiration, not identified as a CPS project.

Painting & Drywall now uses both user-supplied images, pexels-planka-34046207.jpg and pexels-joaojesusdesign-8239799.jpg, side by side on all service cards and the service detail page. Originals and optimized WebP versions are included as painting-roller and painting-can assets.

## Owner review mockup additions

The Construction & Decks image is now a polished version of user-supplied pexels-chris-pennes-2148746480-32802992.jpg. It is inspiration imagery, not claimed as a CPS project. Hablamos Español is displayed in the header, contact information, footer and invoice page.

Pay invoice and Leave a review are working navigation links to explicitly labeled demo pages. Neither collects card details, charges payments, sends reviews, nor stores user entries. Invoice amounts are fictional examples. Both demo pages are excluded from the sitemap and use noindex. The owner must provide a secure payment portal and the exact Google review URL before making these operational. Set PAYMENT_URL and REVIEW_URL when running build.py to replace the demos with external provider links. Use HTTPS URLs; do not put secret keys in these values.

## Flooring & Tile update

Home is now an explicit header navigation link on every page. Flooring & Tile is the fourth service, with a dedicated /flooring-tile/ page, a five-photo inspiration gallery, a quote-form selection and sitemap entry. All five supplied Pexels photos are included as flooring-0 through flooring-4, with original JPEG and optimized WebP versions. They are described as inspiration rather than CPS project evidence. Written service descriptions should be confirmed by the owner before public launch.

## Metro Atlanta coverage and SEO update

The owner confirmed coverage of all metro Atlanta. Hero text, top bar, footer, contact information, about text, service pages and service-area copy now state this clearly. Acworth remains the actual business base; it is not the service limit.

Each core service has a distinct Atlanta-focused title and description. Business JSON-LD names the Atlanta metropolitan area and representative cities, the four service pages have Service JSON-LD, and the business offer catalog links to each service. No keyword meta tag is used because Google ignores it. Review/payment demos and 404 remain noindex. Titles, descriptions, canonical URLs, sitemap entries, schema and internal references are verified locally. This is source validation, not a Google Rich Results Test or Search Console indexing check.

PUBLIC LAUNCH STILL REQUIRED: The review host is owner-private. Its HTML tags cannot bypass that access requirement. On a public launch, rebuild with SITE_URL=https://www.cpsremodeling.com, deploy the site publicly, verify Search Console, submit sitemap.xml, and use URL Inspection. Update the Google Business Profile website and real service area; resolve the existing conflicting street addresses with the owner before adding a street address. Rankings are not guaranteed by any meta tag.

Hero kitchen photo edited with the built-in image-editing tool: preserve room composition and objects; improve balanced exposure, white cabinet luminosity, warm floor tones, natural light and crisp detail. Source image photo-2.jpg retained. Polished hero is separate from the original service-card photo.

The About CPS photo was replaced with user-supplied pexels-curtis-adams-1694007-4800176.jpg. Original and optimized versions are included as about-home-original.jpg and about-home.webp. This is inspiration imagery, not represented as a CPS project.

## Portfolio polish and sitemap
All ten Our Work images have professionally polished WebP versions named `gallery-*-polished.webp`. Original assets remain included. Image edits improve exposure, color and detail while preserving project conditions. Review image accuracy with the owner before public launch.

The footer links to `/sitemap/`, a visitor directory. `/sitemap.xml` lists every indexable page, including this directory; `robots.txt` points crawlers to it. Demo payment and review pages are excluded. Rebuild with the final public `SITE_URL` before launch and submit that domain’s XML sitemap in Google Search Console. A sitemap helps discovery but does not guarantee search ranking.
