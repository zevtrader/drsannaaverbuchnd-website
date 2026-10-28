# Launch checklist

Moving drsannaaverbuchnd.com off Wix. Target: the new site live by about **Oct 27, 2026**.

## Timeline

| By | What |
| --- | --- |
| Oct 28 | Done: transfer requested at Wix (lock lifted 12:30 pm), paid at Porkbun with "Move DNS to Porkbun after the transfer", Cloudflare account created with the domain added (pending) and placeholder DNS records in place. |
| Now | She approves Porkbun's transfer email (and Wix's, if one arrives). Auto-renew off on the Wix **plan** (billed ~Nov 6, not refundable). Justin connects the repo to her Cloudflare account; she reviews the preview. |
| By ~Nov 4 | The transfer completes (Porkbun emails her). Same day: paste the nameservers into Porkbun; the site is live. |
| Mid Nov | Export anything from Wix and unpublish the old site. |

Hard stop: the domain expires **Nov 27, 2026**.

## Open questions for Sanna

- Acupuncture and cupping are hands-on, but Jane only books virtual visits, and the old Wix search description mentions in-person visits in Stouffville (AI search already repeats this). Keep them, drop them, or add a location? A real in-person address also makes her eligible for a Google Business Profile, which matters for "naturopath near me" answers.
- What is her CONO registration number, and the link to her public register entry? Showing both on the About page lets patients and AI assistants verify her registration.
- Is the pediatric assessment virtual or in person?
- Are the fees current?
- Is the "keep health details out of email" note on the contact page OK?

## Before launch

- [ ] Sanna reviews all copy. It is her Wix text, lightly edited for flow, plus the fees from her Jane page.
- [ ] Move photos off Wix. Download the originals from the Wix Media Manager into `public/images/`, compress them (for example with squoosh.app), and replace every `static.wixstatic.com` URL, including the `og:image` tags.
- [ ] Don't reuse the stock photos from the old services page (cupping, acupuncture, food). Wix licenses its free media for use on Wix sites only.

## Give Sanna access

1. She creates a free GitHub account.
2. Invite her with write access, either in the repo's Settings → Collaborators, or with:

   ```bash
   gh api -X PUT repos/zevtrader/drsannaaverbuchnd-website/collaborators/HER_USERNAME -f permission=push
   ```

3. Install the Claude GitHub App on your account, so Claude can reach this private repo:
   - Go to https://github.com/apps/claude/installations/new and choose `zevtrader`.
   - Under "Only select repositories", pick `drsannaaverbuchnd-website`.
4. She needs a Claude Pro plan or higher. Then she follows "Make a change with Claude" in README.md.

## Connect auto-deploy (Cloudflare Workers Builds)

Do this in her Cloudflare account. Afterwards, every push to `main` deploys automatically.

1. Go to Workers & Pages → Create application → Import a repository.
2. Authorize Cloudflare's GitHub app for `zevtrader/drsannaaverbuchnd-website`.
3. Name the Worker `drsannaaverbuchnd`. It must match `name` in `wrangler.jsonc`, or builds fail.
4. Leave the build command empty and set the deploy command to `npx wrangler deploy`. The production branch is `main`.

Until the domain is on Cloudflare, deploys succeed but nothing is public, because `workers_dev` is off and there is no route yet.

## Domain move

Wix does not let you change a Wix domain's nameservers, and Cloudflare's registrar only accepts domains already on Cloudflare nameservers. So the domain moves to Porkbun, and Cloudflare provides DNS and hosting for free.

1. **Transfer to Porkbun.**
   - In Wix, turn off Private Registration (Wix requires this first).
   - Don't edit the domain's contact details: a contact change locks transfers for 60 days.
   - Go to Domains → Domain Actions → "Transfer away from Wix". Wix emails the authorization (EPP) code to the domain's registrant email.
   - At Porkbun, start a transfer, enter the code, and pay US$11.08. This adds a year and includes WHOIS privacy.
   - It usually finishes within 7 days. When it does, Wix disconnects the old site, so switch over right away.
2. **Prepare Cloudflare while the transfer runs.** Done on Oct 28: the domain is added on the Free plan (status "Pending") with two placeholder records, `A @ 192.0.2.1` and `AAAA www 100::`, both proxied. Cloudflare's nameservers for this domain:

   ```
   dante.ns.cloudflare.com
   maeve.ns.cloudflare.com
   ```

   Also done on Oct 28, from Justin's Administrator login:
   - Workers Builds is connected to this repo. Worker `drsannaaverbuchnd`; every push to `main` deploys.
   - Preview address for review: https://drsannaaverbuchnd.sanna-averbuch-nd.workers.dev
   - Route `www.drsannaaverbuchnd.com/*` → the Worker (Worker → Domains).
   - Redirect rule "Redirect root to www" (301, keeps query strings) in Rules → Redirect Rules.
3. **Switch over, the day Porkbun says the transfer is complete.** At Porkbun → the domain → Nameservers, replace Porkbun's with the two above. Cloudflare emails when the domain is active, usually within an hour. Then:
   - Check `https://www.drsannaaverbuchnd.com` loads with a valid certificate, `https://drsannaaverbuchnd.com` redirects to it, and `/services-1` lands on `/services`.
   - AI Crawl Control (zone sidebar → AI Crawl Control → Security) only unlocks once the domain is active: set Search, Agent and Training to Allow (see VISIBILITY.md).
   - Set `workers_dev` to `false` in `wrangler.jsonc` and push, so the site isn't also served from the preview address.
   - Check that `https://www.drsannaaverbuchnd.com/services-1` lands on `/services`.

   Bookings keep working throughout, because they happen on Jane.
4. **Free extras.**
   - Cloudflare Web Analytics: cookieless, no banner needed.
   - Email Routing (optional, receive-only): for example, `hello@drsannaaverbuchnd.com` forwards to her Gmail.
   - Google Search Console and Bing Webmaster Tools: verify the domain and submit `/sitemap.xml`. Bing feeds Copilot and ChatGPT search.
   - The rest of the AI-visibility checklist (directory listings, monthly checks) is in VISIBILITY.md.
5. **Close out Wix.**
   - Export contacts and form submissions before the plan ends.
   - Unpublish the old site, so the free `wixsite.com` copy doesn't compete in search.

Optional, later: after 60 days at Porkbun, the domain could move to Cloudflare Registrar (at cost, about US$11.17/yr after Verisign's Nov 1, 2026 .com increase). That saves under $1 a year, so only do it if you want one fewer account.

## Running cost

| Item | Cost |
| --- | --- |
| Domain at Porkbun (.com, includes WHOIS privacy) | about US$11–12/yr |
| Hosting, DNS, SSL, redirects, analytics, email forwarding on Cloudflare | $0 |
| Booking (Jane App) | unchanged, billed separately |
| Claude, if she edits with it | her own Claude plan |

For comparison, Wix's cheapest plan that allows a custom domain (Light) is US$204/yr, and Wix renews a .com at US$21.35/yr.
