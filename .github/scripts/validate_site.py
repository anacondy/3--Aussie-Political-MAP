#!/usr/bin/env python3
"""Lightweight structural + marker validation for the static site.

This intentionally avoids third-party network dependencies so the CI check is
fast and reliable. It verifies:
  * required structural markers are present in index.html
  * the HTML tag nesting is balanced (script/style treated as raw text)
"""
import sys
import re
from html.parser import HTMLParser

REQUIRED = [
    '<!DOCTYPE html>',
    'id="map"',
    'id="sidebar"',
    'id="close-sidebar"',
    'id="drag-handle"',
    'Content-Security-Policy',
    'leaflet@1.9.4/dist/leaflet.js',
    'leaflet@1.9.4/dist/leaflet.css',
]

# Void/empty elements that never have a closing tag.
VOID = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr',
}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"Unexpected </{tag}> with empty stack")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
            return
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"Unclosed <{self.stack[-1]}> before </{tag}>")
                self.stack.pop()
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f"Stray </{tag}>")


def main():
    with open('index.html', encoding='utf-8') as fh:
        html = fh.read()

    missing = [m for m in REQUIRED if m not in html]
    if missing:
        print("FAIL: missing required markers:")
        for m in missing:
            print("  -", m)
        sys.exit(1)

    c = Checker()
    c.feed(html)
    if c.stack:
        print("WARN: unclosed tags remaining at EOF:", c.stack[-5:])
    if c.errors:
        print("FAIL: HTML structure errors:")
        for e in c.errors[:20]:
            print("  -", e)
        sys.exit(1)

    # Sanity: the embedded political data must be valid JSON-ish (keys present).
    if 'politicalData' not in html or 'New South Wales' not in html:
        print("FAIL: embedded politicalData appears incomplete")
        sys.exit(1)

    print("OK: HTML structure and required markers validated.")


if __name__ == '__main__':
    main()
