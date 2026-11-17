#!/usr/bin/env python3
"""Validate internal links, anchors, referenced assets and portfolio invariants."""
from __future__ import annotations
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1] / "docs"
PAGES = ("index.html", "about.html", "expertise.html", "projects.html", "gallery.html", "credentials.html", "contact.html", "solutions.html")
ACTIVE = PAGES[:-1]
ISSUES = []

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []
        self.current = []
        self.menu = 0
        self.nav = 0
        self.active = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.append(d["id"])
        if tag == "nav" and d.get("id") == "navigation":
            self.nav += 1
        if tag == "a" and d.get("aria-current") == "page":
            self.active += 1
        if tag == "button":
            if d.get("type") != "button":
                ISSUES.append("Button missing explicit type")
            if "menu-button" in d.get("class", "").split():
                self.menu += 1
        if tag == "img":
            if "alt" not in d:
                ISSUES.append("Image missing alt")
            if "width" not in d or "height" not in d:
                ISSUES.append("Image missing width/height")
        for attr in ("src", "href", "poster", "action"):
            if d.get(attr):
                self.refs.append((tag, attr, d[attr]))
        if d.get("srcset"):
            for part in d["srcset"].split(","):
                self.refs.append((tag, "srcset", part.strip().split()[0]))
        for attr in ("aria-labelledby", "aria-controls"):
            if d.get(attr):
                for value in d[attr].split():
                    self.current.append(value)

scans = {}
for file in PAGES:
    path = ROOT / file
    scan = Scan()
    scan.feed(path.read_text(encoding="utf-8"))
    scans[file] = scan
    duplicate = [x for x, n in Counter(scan.ids).items() if n > 1]
    if duplicate:
        ISSUES.append(f"{file}: duplicate IDs {duplicate}")
    if file in ACTIVE and (scan.nav != 1 or scan.active != 1 or scan.menu != 1):
        ISSUES.append(f"{file}: navigation/menu/active state invalid")
    for idref in scan.current:
        if idref not in scan.ids:
            ISSUES.append(f"{file}: missing accessibility target #{idref}")

for page, scan in scans.items():
    for tag, attr, url in scan.refs:
        if url.startswith(("mailto:", "tel:", "data:", "https:", "http:")):
            continue
        parsed = urlsplit(url)
        if not parsed.path and not parsed.fragment:
            continue
        if parsed.path:
            target = (ROOT / unquote(parsed.path.lstrip("/"))).resolve()
            if not target.is_relative_to(ROOT.resolve()):
                ISSUES.append(f"{page}: link outside docs: {url}")
                continue
        else:
            target = ROOT / page
        if not target.is_file():
            ISSUES.append(f"{page}: missing local asset: {url}")
            continue
        if parsed.fragment and target.suffix == ".html":
            target_name = str(target.relative_to(ROOT))
            if target_name in scans and unquote(parsed.fragment) not in scans[target_name].ids:
                ISSUES.append(f"{page}: missing anchor: {url}")

expertise = (ROOT / "expertise.html").read_text(encoding="utf-8")
start = expertise.find('id="agri-indices"')
end = expertise.find("</section>", start)
section = expertise[start:end]
if section.count('class="index-name-card"') != 12:
    ISSUES.append("Expertise must contain 12 full-name indices")
if any(word in section.lower() for word in ("formula", "<code", "<table", "sentinel", "landsat", "satellite")):
    ISSUES.append("Index cards must not contain formulas or satellite names")
for file in ACTIVE:
    s=(ROOT/file).read_text(encoding="utf-8")
    if any(word in s.lower() for word in ("sentinel-1", "sar backscatter", "vv / vh", "sar-rice")):
        ISSUES.append(file+": removed radar analysis reintroduced")
if "prefers-reduced-motion:reduce" not in (ROOT/"assets/style.css").read_text(encoding="utf-8"):
    ISSUES.append("Floating icons missing reduced-motion support")
if "url=gallery.html" not in (ROOT/"solutions.html").read_text(encoding="utf-8"):
    ISSUES.append("Legacy gallery redirect missing")

if ISSUES:
    for issue in ISSUES:
        print("FAIL: "+issue)
    sys.exit(1)
print(f"PASS: {len(PAGES)} pages; all local references, accessible IDs and portfolio invariants verified")
