# Showing up in AI assistants

Goal: when someone asks ChatGPT, Claude, Perplexity, Gemini or Copilot for a naturopathic doctor in Ontario, Dr. Averbuch is one of the names that comes up. No one can guarantee a spot in AI answers, but these are the levers that matter.

## How assistants pick who to mention

- **With web search**, an assistant looks things up in search indexes (Google, Bing) or with its own crawler (OpenAI, Anthropic and Perplexity each run one). It then quotes pages that answer the question plainly.
- **Agreement across sources** builds confidence. Assistants trust facts that match across several places: her site, the regulator and association directories, her booking page and her social profiles.
- **Without web search**, they rely on training data, which lags by months.

## Already done on the site

- Plain HTML that crawlers read without running JavaScript. The Wix site needs about 87 scripts to show anything.
- `robots.txt` welcomes every crawler, including AI ones.
- `llms.txt`: a plain-text summary of the practice, her credentials, and the visits and fees.
- Structured data for search engines: the practice, plus her degree, her College of Naturopaths of Ontario registration, her OAND/CAND memberships and her areas of focus.
- An "At a glance" facts box on About, and "Common questions" on Services & fees, phrased the way people ask.
- A sitemap with last-modified dates.
- Removed an outdated claim. The Wix search description says she sees patients in person in Stouffville, and AI search already repeats it. The new site leaves it out until she confirms.

## Launch day (about 30 minutes)

1. **Cloudflare AI crawler settings.**
   - Cloudflare sorts AI bots into Search, Agent and Training. For domains added after Sept 15, 2026, it blocks Agent and Training by default on pages that show ads.
   - Her site has no ads, but check anyway: in AI Crawl Control, set all three categories to **Allow**.
   - A week later, look at the Crawlers tab to confirm nothing is being blocked.
2. **Google Search Console.** Verify the domain and submit `/sitemap.xml`. This covers Google Search, AI Overviews and Gemini.
3. **Bing Webmaster Tools.** Import the site from Search Console and submit the sitemap. Bing's index powers Copilot and is one of the sources behind ChatGPT search.
4. **Optional: Crawler Hints.** Turn it on in Cloudflare under Caching → Configuration. It notifies Bing and other IndexNow engines when pages change.

## Listings: the biggest lever after launch

Use the same facts everywhere: **Dr. Sanna Averbuch, ND · Naturopathic doctor · Virtual care across Ontario · www.drsannaaverbuchnd.com**.

- [ ] **College of Naturopaths of Ontario public register:** check that her practice details are current, and add the website if the register allows it. Then link her register entry from the About page, so patients and AI assistants can verify her registration.
- [ ] **OAND "Find a Naturopathic Doctor" directory** (a member benefit): fill in the profile completely, with focus areas, virtual care and the website link.
- [ ] **CAND directory:** same.
- [ ] **Instagram @cycleofbeauty:** the bio says "Naturopathic Doctor (ND) · Virtual care across Ontario" and links to the website, not only to Linktree.
- [ ] **LinkedIn:** same name, credentials and link.
- [ ] **Jane profile bio:** same focus areas, plus a link to the website.
- [ ] **In-person location (if she has one):** add a Google Business Profile and a Bing Places listing for it. These drive "naturopath near me" answers in Gemini, Google Maps and Copilot. A virtual-only practice isn't eligible for a Google Business Profile.
- [ ] **Mentions on other sites:** she was a guest on the *Your Health Minute* podcast in June 2024, while still a student. Ask the host to update the show notes with her current title and website. More podcasts, guest articles and local news help in the same way.

## Content that gets quoted

- **Focus pages:** one page per main concern, such as acne, PMS and hormones, IBS and bloating, and menopause. The Ontario naturopaths that currently appear in AI answers for these searches have pages like this.
  - Each page covers who it's for, her approach in her own words, what a first visit involves, and a booking link.
  - No promises of results.
  - To make one, she can ask Claude: "Create a focus page on acne. Here's how I approach it: ...". CLAUDE.md has the template.
- **The FAQ:** keep adding real questions patients ask her.

## Check once a month

Ask each assistant the same questions and note whether she appears:

- "Can you recommend a naturopathic doctor in Ontario who offers virtual visits for hormone issues?"
- "Virtual naturopath in Ontario for acne"
- "Who is Dr. Sanna Averbuch?"
- "How much is an initial assessment with Dr. Sanna Averbuch?"

Also look at Cloudflare's AI Crawl Control to see which AI crawlers are visiting.

Expect a few weeks after launch for search-backed answers to pick her up, and months for anything that depends on model training.

## Don't

- Buy "AI SEO" packages, directory spam or fake listings.
- Add testimonials, reviews or review widgets. The College of Naturopaths of Ontario doesn't allow them.
- Hide text or stuff keywords for bots. Assistants quote what people can read.
