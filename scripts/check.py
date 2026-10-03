#!/usr/bin/env python3
"""Sanity checks for the site. Run before publishing: python3 scripts/check.py

Errors (exit 1): broken HTML structure, missing alt text, not exactly one <h1>,
missing title/description/canonical, invalid JSON-LD, broken internal links,
header/footer/booking bar out of sync between pages, pages missing from the
sitemap, redirects to pages that don't exist.

Warnings: wording the College of Naturopaths of Ontario advertising standard
doesn't allow (testimonials, guarantees, superlatives). Review each one.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SHARED_BLOCKS = {
    "header": r'<header class="site-header">.*?</header>',
    "footer": r'<footer class="site-footer">.*?</footer>',
    "mobile booking bar": r'<div class="mobile-cta">.*?</div>',
}
RISKY_WORDING = re.compile(
    r"\b(testimonials?|reviews?|rated|5[- ]star|five[- ]star|guarantee[ds]?|cures?|cured|"
    r"best|leading|#1|number one|most effective|top-rated)\b",
    re.IGNORECASE,
)

errors, warnings = [], []


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.ids, self.links, self.problems = [], set(), [], []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.problems.append(f'duplicate id "{a["id"]}"')
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img" and not (a.get("alt") or "").strip():
            self.problems.append(f"image without alt text: {a.get('src', '')[:70]}")
        if tag == "h1":
            self.h1 += 1
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        self.problems.append(f"line {self.getpos()[0]}: unexpected </{tag}>")
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def page_for(path):
    """Map a site path like /about to its file, the way Cloudflare does."""
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return PUBLIC / "index.html"
    candidate = PUBLIC / path.lstrip("/")
    if candidate.suffix:
        return candidate
    return candidate.with_suffix(".html")


def normalize(block):
    block = block.replace(' aria-current="page"', "")
    return re.sub(r"\s+", " ", block).strip()


def visible_text(source):
    source = re.sub(r"<(script|style)\b.*?</\1>", " ", source, flags=re.S)
    source = re.sub(r"<[^>]+>", " ", source)
    return html.unescape(source)


pages = sorted(PUBLIC.glob("*.html"))
parsed = {}
for page in pages:
    source = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)
    parsed[page.name] = (source, parser)
    name = page.name
    for problem in parser.problems:
        errors.append(f"{name}: {problem}")
    if parser.stack:
        errors.append(f"{name}: unclosed tags {[t for t, _ in parser.stack]}")
    if parser.h1 != 1:
        errors.append(f"{name}: has {parser.h1} <h1> headings (needs exactly 1)")
    if name != "404.html":
        for label, pattern in {
            "<title>": r"<title>[^<]+</title>",
            "meta description": r'<meta name="description" content="[^"]+">',
            "canonical link": r'<link rel="canonical" href="https://www\.drsannaaverbuchnd\.com[^"]*">',
        }.items():
            if not re.search(pattern, source):
                errors.append(f"{name}: missing {label}")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            errors.append(f"{name}: structured data (JSON-LD) is invalid: {e}")
    for match in RISKY_WORDING.finditer(visible_text(source)):
        warnings.append(f'{name}: "{match.group(0)}" (check against the advertising rules)')

# Internal links and #anchors must resolve.
for name, (source, parser) in parsed.items():
    for href in parser.links:
        if not href.startswith("/"):
            continue
        target = page_for(href)
        if not target.exists():
            errors.append(f"{name}: link to {href} goes nowhere")
            continue
        if "#" in href and target.suffix == ".html":
            anchor = href.split("#", 1)[1]
            target_ids = parsed.get(target.name, (None, PageParser()))[1].ids
            if anchor and anchor not in target_ids:
                errors.append(f'{name}: link to {href} points at a missing section "#{anchor}"')

# Header, footer and booking bar must match on every page that has them.
reference_source = parsed["index.html"][0]
for label, pattern in SHARED_BLOCKS.items():
    reference = re.search(pattern, reference_source, re.S)
    for name, (source, _) in parsed.items():
        found = re.search(pattern, source, re.S)
        if not found:
            if name != "404.html":
                errors.append(f"{name}: missing the shared {label}")
            continue
        if normalize(found.group(0)) != normalize(reference.group(0)):
            errors.append(f"{name}: {label} differs from index.html (update every page the same way)")

# Every page (except 404) must be in the sitemap.
sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
for name, (source, _) in parsed.items():
    if name == "404.html":
        continue
    canonical = re.search(r'<link rel="canonical" href="([^"]+)">', source)
    if canonical and f"<loc>{canonical.group(1)}</loc>" not in sitemap:
        errors.append(f"sitemap.xml: missing {canonical.group(1)}")

# Redirects must point at real pages.
for line in (PUBLIC / "_redirects").read_text(encoding="utf-8").splitlines():
    parts = line.split()
    if len(parts) >= 2 and not parts[0].startswith("#") and parts[1].startswith("/"):
        if not page_for(parts[1]).exists():
            errors.append(f"_redirects: {parts[0]} -> {parts[1]} goes nowhere")

for warning in warnings:
    print(f"WARNING  {warning}")
for error in errors:
    print(f"ERROR    {error}")
print(f"\nChecked {len(pages)} pages: {len(errors)} errors, {len(warnings)} warnings.")
sys.exit(1 if errors else 0)
