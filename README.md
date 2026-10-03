# Your website

This is the code for **www.drsannaaverbuchnd.com**. You don't need to know code to change it: ask Claude.

Status: getting ready to launch in late October 2026. Until then, changes are saved here but not yet public.

## Make a change with Claude

You need a Claude Pro plan or higher.

**First time only**

1. Go to [claude.ai/code](https://claude.ai/code) and sign in.
2. Connect GitHub when asked, then choose this repository: `drsannaaverbuchnd-website`.

**Every time**

1. Open [claude.ai/code](https://claude.ai/code) and pick the `drsannaaverbuchnd-website` repository.
2. Describe what you want in plain English, for example:
   - "Change the 45-minute follow-up fee to $180."
   - "Add thyroid health to my areas of focus."
   - "Make the cupping description shorter."
3. Claude makes the change and explains it. Ask for tweaks until it's right.
4. To publish:
   - Click **Create PR**.
   - Open the pull request on GitHub.
   - Click **Merge pull request**. The live site updates within a couple of minutes.

Claude already knows your site's rules (below) and will tell you if a request would break them.

## Quick text fixes without Claude

1. On github.com, open the `public` folder, then the page you want:

   | Page | File |
   | --- | --- |
   | Home | `public/index.html` |
   | About | `public/about.html` |
   | Services & fees | `public/services.html` |
   | Contact | `public/contact.html` |

2. Click the pencil icon, change the words, and click **Commit changes**.
3. Change only the words between the `<` `>` tags; don't delete the tags themselves.

The header and footer appear on every page, so a change there has to be made in each file. That one is easier to ask Claude for.

## Rules for your website

These come from the College of Naturopaths of Ontario advertising standard:

- No testimonials. That includes reviews, patient stories or feedback, and links or widgets that show them.
- No guarantees of results.
- No comparisons or superlatives such as "best" or "leading".
- Fees are fine to show.
- "Dr." goes directly before your name, with ND after it.

## If something goes wrong

Nothing is ever lost. Every change is kept in the history, and Cloudflare keeps every earlier version of the site, so any change can be undone. Ask Claude to "undo my last change", or ask Justin.

## Technical notes

- Plain HTML and CSS in `public/`. No build step, no JavaScript.
- Preview locally with `python3 serve.py`, then open http://localhost:8787.
- Check before publishing with `python3 scripts/check.py`. GitHub runs it on every pull request too.
- Once Cloudflare Workers Builds is connected (see LAUNCH.md), pushes to `main` deploy automatically.
- `public/_redirects` keeps the old Wix URLs (`/services-1`, `/contact-3`) working.
- Launch checklist and domain move: [LAUNCH.md](LAUNCH.md). Instructions for Claude: [CLAUDE.md](CLAUDE.md).
