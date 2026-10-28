# CLAUDE.md

Website for Dr. Sanna Averbuch, ND, a naturopathic doctor offering virtual care across Ontario: https://www.drsannaaverbuchnd.com.
Plain HTML and CSS with no build step and no JavaScript, served by Cloudflare Workers static assets. Changes go live when they reach `main`.

## Who you're working with

Usually Sanna herself. She is not a developer.

- Use plain English: "page" not "HTML file", "publish" not "merge" or "deploy".
- Before changing wording about her care, show her the new text and get a yes.
- When done, say what changed and where, then walk her through publishing step by step:
  1. Click **Create PR**.
  2. Open the pull request on GitHub.
  3. Click **Merge pull request**. The site updates within a couple of minutes.
- If she asks for something that breaks the rules below, explain why and offer an alternative that fits.

## Structure

- `public/` is everything that is served: `index.html`, `about.html`, `services.html`, `contact.html`, `404.html`, `styles.css`, `_redirects`, `_headers`, `sitemap.xml`, `robots.txt`, `llms.txt`, `favicon.svg`.
- The header, footer and mobile booking bar (`.mobile-cta`) are repeated in every page. Change them identically everywhere; `scripts/check.py` fails if they drift.
- New page:
  - Copy an existing page's `<head>` and give it a unique `<title>`, meta description, canonical URL and `og:` tags.
  - Add it to the nav and footer in every page, and to `sitemap.xml`.
- Renamed or removed page: add a 301 to `public/_redirects`.
- Styling:
  - Use the colour and font tokens at the top of `styles.css`.
  - Keep body text contrast at 4.5:1 or better.
  - No frameworks, libraries, trackers or cookies.
- Images:
  - Put them in `public/images/`, at most about 1600px on the long edge and under 300 KB.
  - Always give them meaningful `alt` text and `width`/`height` attributes.
- Some photos still load from `static.wixstatic.com`. They must move into `public/images/` before Wix is cancelled (see LAUNCH.md).

## Booking (Jane App)

Booking happens on Jane, and Jane cannot be embedded. Buttons deep-link to `https://drsannaaverbuchnd.janeapp.com/` plus:

| Visit | Path |
| --- | --- |
| Free 15-min meet & greet | `#/staff_member/1/treatment/2` |
| Initial assessment, 75 min | `#/staff_member/1/treatment/1` |
| Pediatric initial assessment, 60 min | `#/staff_member/1/treatment/9` |
| Extended follow-up, 60 min | `#/staff_member/1/treatment/3` |
| Follow-up, 45 min | `#/staff_member/1/treatment/4` |
| Follow-up, 30 min | `#/staff_member/1/treatment/5` |
| Wait list | `wait_list/new?staff_member_id=1` |
| Gift cards | `online_gift_cards/new` |

Fees appear in `services.html` (Visits and fees) and in `index.html` (How it works). They must match Jane. When she changes a fee, update both places and remind her to change it in Jane too. Don't build booking forms.

## Rules: College of Naturopaths of Ontario advertising standard

Never add any of these:

- Testimonials, reviews, star ratings, patient stories or feedback, or links and widgets that show them (for example, Google reviews).
- Guarantees of results: "guaranteed", "will cure".
- Comparative or superlative claims: "best", "leading", "#1", "most effective".
- Package deals, discounts tied to bundles, or referral rewards.

Also:

- Keep "Dr." directly before her name, with ", ND" after it: "Dr. Sanna Averbuch, ND".
- Fees may be shown.
- Health claims should stay accurate and evidence-informed. When unsure, keep her existing wording and flag it.
- Privacy: the site collects no personal data and sets no cookies; keep it that way. No contact forms that could collect health details.

## Showing up in AI assistants and search

The goal is for ChatGPT, Claude, Perplexity, Gemini and Copilot to recommend her. VISIBILITY.md has the full plan.

- **Keep facts identical everywhere.** Fees, visit types, focus areas, credentials and location live in the pages, in `public/llms.txt`, and in the JSON-LD in `index.html` and `about.html`. When one changes, update every place, then remind her to match her Jane profile and directory listings. `scripts/check.py` verifies fees.
- **Update dates.** When you change a page, set its `<lastmod>` in `sitemap.xml` to today's date.
- **Write facts as plain sentences** in the page text, not only in images or JSON-LD, so assistants can quote them.
- **Keep `robots.txt` open** to every crawler.
- **Focus pages** (one per concern, such as acne, PMS and hormones, IBS, menopause):
  - File: `public/<concern>.html`, for example `public/acne.html`.
  - Title: "Naturopathic care for <concern> | Dr. Sanna Averbuch, ND". H1: "Naturopathic care for <concern>".
  - Sections:
    1. Who it's for: the symptoms she sees, using her wording.
    2. How Dr. Averbuch approaches it: ask her for this; don't invent clinical claims.
    3. What the first visit involves.
    4. Link to the fees on the services page.
    5. Booking button.
  - No promises of results.
  - Link it from the matching card in the home page's "Areas of focus" (not the nav), and add it to `sitemap.xml` and `llms.txt`.
- **New FAQ entries** go in the "Common questions" section of `services.html`. Use her real patients' questions and answers she approves.

## Before you finish

- Run `python3 scripts/check.py`. It must pass. It checks HTML structure, alt text, one `<h1>` per page, internal links, header and footer consistency, the sitemap, and flags wording the advertising rules forbid.
- In a cloud session you cannot load fonts or images, or see the page, so don't claim to have checked how it looks. Describe the change precisely instead.
- With a browser available, run `python3 serve.py` (http://localhost:8787) and look at the changed pages at desktop width and at 390px phone width. Check for no sideways scrolling, and that the booking bar shows on phones.
