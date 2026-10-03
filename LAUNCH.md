# Launch checklist

Moving drsannaaverbuchnd.com off Wix. Target: the new site live by about **Oct 27, 2026**.

## Timeline

| By | What |
| --- | --- |
| Oct 11 | Sanna reviews the preview and answers the open questions below. If she's in, she turns off auto-renew on the Wix **plan** (Wix renewals aren't refundable, and plans are billed up to 3 weeks before the purchase anniversary). |
| Oct 12–18 | Apply her edits and move her photos into `public/images/`. Open Porkbun and Cloudflare accounts in her name. Connect this repo to Cloudflare (see below). |
| Oct 20 | She requests the Wix transfer code; start the transfer at Porkbun. Then turn off auto-renew on the Wix **domain** (Wix bills domains 30 days before expiry, around Oct 28). |
| ~Oct 27 | The transfer completes. Switch the nameservers to Cloudflare and deploy; the site is live. |
| Early Nov | Export anything from Wix and unpublish the old site. |

Hard stop: the domain expires **Nov 27, 2026**.

## Open questions for Sanna

- Acupuncture and cupping are hands-on, but Jane only books virtual visits, and the old Wix search description mentions in-person visits in Stouffville. Keep them, drop them, or add a location?
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
2. **Prepare Cloudflare while the transfer runs.** Add the domain on the Free plan and note the two nameservers it gives you.
3. **Switch over.** At Porkbun, set the nameservers to Cloudflare's. Once Cloudflare shows the domain as active:
   - Uncomment `routes` in `wrangler.jsonc` and push. Workers Builds deploys it to `www.drsannaaverbuchnd.com`.
   - In Rules, add the "Redirect from root to WWW" redirect rule.
   - Check that `https://www.drsannaaverbuchnd.com/services-1` lands on `/services`.

   Bookings keep working throughout, because they happen on Jane.
4. **Free extras.**
   - Cloudflare Web Analytics: cookieless, no banner needed.
   - Email Routing (optional, receive-only): for example, `hello@drsannaaverbuchnd.com` forwards to her Gmail.
   - Google Search Console: verify the domain and submit `/sitemap.xml`.
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
