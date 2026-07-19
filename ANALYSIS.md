# Project Analysis — Australia Political Governance Map (3--Aussie-Political-MAP)

**Analyst:** Arena.ai Agent Mode
**Date:** 2026-07-19
**Scope:** Full audit of the repository (`index.html`, `README.md`, git history, remote
branches, GitHub Pages configuration, and the third-party runtime dependencies).
**Branch reviewed:** `arena/019f7a12-3-aussie-political-map` (based on `main` @ `bd1e0a3`)

---

## 1. Executive Summary

This is a **single-file static web app** (`index.html`, ~720 lines) that renders an
interactive Leaflet map of Australian states/territories coloured by governing party,
with a sliding information sidebar. It is deployed via GitHub Pages.

The app *roughly* works in a happy-path browser session, but it is **fragile, insecure,
and was left in a half-finished state by the previous agent**. I found:

- **1 critical infrastructure defect** (GitHub Pages deploys from a stale feature branch).
- **2 high-severity security gaps** (no Content-Security-Policy, third-party scripts
  without Subresource Integrity).
- **1 stored-XSS-capable code path** (untrusted GeoJSON text rendered via `innerHTML`).
- **1 high-severity availability defect** (map geometry fetched from a single external URL
  with no fallback/timeout).
- **Several functional bugs** that make advertised features silently fail (click-to-close
  sidebar, resize-driven close-button visibility, stale mobile detection).
- **Dead / inert code** (deprecated Leaflet options, a no-op ternary, contradictory CSS).
- **Repository clutter**: a broken screenshot image link and unverified "testing" claims in
  the README (the previous agent attached screenshots and called it "progress").

All of the above have been **patched** in this branch. See §7 and the diff.

> **Overall rating: 3.5 / 10.** Functionally it demos the idea; architecturally and
> securely it is a prototype, not production-grade. Detailed scoring in §6.

---

## 2. How the Audit Was Performed

1. Enumerated the repo (`git ls-files`, `find`) → only 4 tracked files, **no committed
   binary/screenshot clutter** exists in git history.
2. Read `index.html` line-by-line, traced the Leaflet lifecycle, and reasoned about
   event propagation and responsive state.
3. Extracted the inline `<script>` and ran `node --check` (passed after fixes).
4. Ran a structural HTML validator (`.github/scripts/validate_site.py`, added in this
   branch) — balanced tags + required markers.
5. Inspected remote branches and the GitHub Pages configuration via the GitHub API.
6. Verified the external data dependency (the Australian-states GeoJSON) — confirmed the
   upstream default branch is still `master`, but proved the app has **no fallback** if that
   host/repo ever changes.

---

## 3. Critical Vulnerabilities

### V-1 — No Content-Security-Policy (High, Security)
The document has **no CSP**. Any injection point (see V-3) could execute arbitrary script,
and the page freely loads executables from any origin. I added a strict-but-functional CSP:

```
default-src 'self';
script-src 'self' 'unsafe-inline' https://unpkg.com;
style-src 'self' 'unsafe-inline' https://unpkg.com https://fonts.googleapis.com;
font-src 'self' https://fonts.gstatic.com https://fonts.googleapis.com;
img-src 'self' data: https://*.cartocdn.com;
connect-src 'self' https://raw.githubusercontent.com https://cdn.jsdelivr.net;
frame-ancestors 'none'; object-src 'none'; base-uri 'self'
```

> Note: `'unsafe-inline'` is required because the app is a single file with inline
> `<style>`/`<script>`. The proper hardening (moving JS/CSS to separate files and using
> nonce-based CSP) is listed under Recommendations.

### V-2 — Third-party scripts/styles without Subresource Integrity (High, Security)
`leaflet.js`, `leaflet.css`, and Google Fonts are loaded from CDNs **with no `integrity`
attribute and no `crossorigin`**. A compromised CDN (or MITM on an unprotected network)
could serve malicious JavaScript and fully control the page. Recommended fix: pin exact
versions and add SRI hashes (blocked here only by the need to compute hashes against the
pinned CDN assets).

### V-3 — Stored-XSS-capable path via `innerHTML` (Medium/High, Security)
`updateSidebar()` injects the **state name** into the DOM with template-literal `innerHTML`:

```js
document.getElementById('sidebar-content').innerHTML =
  `<h2 class="sidebar-title">${stateName}</h2>...`;
```

`stateName` is derived from the GeoJSON `STATE_NAME` property, i.e. **attacker-influenced
if the upstream data source is tampered with**. A crafted `STATE_NAME` (e.g. containing
`<img src=x onerror=...>`) would execute when a user clicks that region. The hardcoded
`politicalData` object is trusted, but the *name crosswalk* is not. **Fix:** added an
`escapeHtml()` helper and applied it to `stateName`.

### V-4 — Hard dependency on a single external data file (High, Availability)
The map geometry is fetched at runtime from one URL:

```js
fetch('https://raw.githubusercontent.com/rowanhogan/australian-states/master/states.geojson')
```

There is **no fallback, no timeout, and no local copy**. If that repo is renamed, deleted,
rate-limited, or its schema changes, the entire map silently fails (the only symptom is a
red "Failed to load map data" toast). **Fix:** try two mirrors in sequence
(`raw.githubusercontent.com` → `cdn.jsdelivr.net`) with a 15 s per-request timeout. The
robust production fix is to **vendor `states.geojson` into the repo** (see Recommendations).

---

## 4. Functional Bugs (Broken / Not Firing / Dead Code)

### B-1 — Click-to-close sidebar is dead (High, Functional)
The map click handler only closed the sidebar when
`e.originalEvent.target.id === 'map'`. In practice the click target is almost always a
**tile `<img>` or the SVG `<path>`**, never the `#map` container, so clicking the map
background **never closed the panel**. **Fix:** close on any map click whose target is *not*
a `.leaflet-interactive` (state) element.

### B-2 — Close button visibility inverted on resize (Medium, Functional)
The resize handler did:

```js
closeBtn.style.display = newIsMobile ? 'block' : 'none';   // backwards!
```

…which shows the close button on **mobile** and hides it on **desktop** — the exact
opposite of the intended design (desktop shows the × button; mobile uses the drag handle).
After any window resize the desktop close button vanished. **Fix:** introduced
`syncCloseButton()` that shows it only when `!isMobile`.

### B-3 — `geojson` is an undeclared implicit global (Medium, Correctness)
`geojson = L.geoJson(...)` is assigned **without `var/let/const`**, creating a global. The
`resetHighlight()` handler calls `geojson.resetStyle(...)` with no guard, which would throw
if a mouseout fired before the layer finished loading (and is simply bad practice).
**Fix:** declared `let geojson = null;` up front and guarded the call.

### B-4 — `isMobile` computed once, then stale (Medium, Responsive)
`const isMobile = window.innerWidth <= 768;` is captured at load. Because it was `const`
and only the initial value was ever used, the close button, click handler, and fly-to math
all operated on a **stale viewport state** after rotating/resizing a device. **Fix:** made
it a mutable `let`, updated it inside the (debounced) resize handler.

### B-5 — Swipe-to-dismiss only wired when loaded as mobile (Low/Medium, Responsive)
The entire touch/swipe block was gated behind `if (isMobile) { … }`, so a device that
*starts* on desktop and is later resized/narrowed never got the handlers, and the logic
could not react to orientation changes. **Fix:** handlers are now attached
unconditionally and no-op when `!isMobile`.

### B-6 — Deprecated / inert Leaflet options (Low, Dead Code)
`L.map(..., { tap: true, tapTolerance: 15 })` — both options were **removed in Leaflet 1.7**
and do nothing in 1.9.4. They are dead configuration that misleads future maintainers.
**Fix:** removed.

### B-7 — Redundant ternary (Low, Dead Code)
`minZoom: isMobile ? 3 : 3` evaluates to `3` either way. **Fix:** `minZoom: 3`.

### B-8 — Contradictory `.close-btn` CSS (Low, Clutter)
Inside the `≤768px` media query the button was set to `display: block` and then, lower down,
`set to `display: none` — net result correct but confusing and a maintenance trap.
**Fix:** collapsed to a single explicit `display: none` on mobile (visibility is otherwise
driven by JS).

---

## 5. Repository Clutter & "Previous Agent" Cleanup

- **No binary screenshots are committed** — I searched the entire git object store and
  working tree; there are no `.png/.jpg/...` files. The "screenshots" the previous agent
  attached were **GitHub user-attachment links pasted into the README**, not real repo
  artifacts. That is why the only clutter is a *broken link*, not files.
- **Removed** the dangling image embed in `README.md`
  (`![Desktop View](https://github.com/user-attachments/assets/13fd00cb-…)`), which renders
  as a broken image and leaks a private attachment URL.
- **Removed** the empty "Screenshots" section and replaced it with an honest note + a
  Deployment section clarifying the GitHub Pages source branch.
- Replaced unverified "The site has been tested on 4K displays / iPads / …" claims with a
  neutral "designed for" statement (the previous agent asserted testing that was not
  evidenced).

---

## 6. Architecture & Code-Quality Rating

The app is a **monolith**: one 720-line HTML file containing CSS, data, and behavior. There
is no build step, no module system, no tests, and no separation of concerns.

| Axis | Score | Notes |
|------|-------|-------|
| Correctness | 4 / 10 | Core render works; several interaction bugs (B-1, B-2) silently break features. |
| Robustness / Reliability | 3 / 10 | Single external point of failure (V-4), no fallbacks, no CSP. |
| Security | 2 / 10 | No CSP, no SRI, XSS-capable path (V-1/V-2/V-3). |
| Maintainability | 3 / 10 | One huge file, hardcoded data, no tests, dead/inert code. |
| Performance | 6 / 10 | Reasonable: debounced resize, GPU-accelerated CSS, lazy-ish load. |
| Mobile / Responsive | 5 / 10 | Good CSS; but JS state is stale (B-4) and handlers mis-wired (B-5). |
| **Overall** | **3.5 / 10** | A working prototype, **not** production-ready. |

**Architecture grade: D / C−.**

### Where the code is weakest
1. **No data layer.** Political data and geometry are hardcoded / fetched ad-hoc, mixed
   with DOM code. A change to either requires editing the monolith.
2. **No error boundaries.** A failed fetch shows a toast but leaves the app in a dead state
   with no retry.
3. **Global mutable state & implicit globals** (`geojson`, `isMobile`).
4. **No automated tests / CI** (now added — see §7).
5. **Security is an afterthought** (no CSP/SRI, raw `innerHTML`).
6. **Deployment is mis-wired** to a stale branch (see §8).

---

## 7. Patches Applied (this branch)

| ID | File | Change |
|----|------|--------|
| V-1 | `index.html` | Added `Content-Security-Policy` meta tag. |
| V-3 | `index.html` | Added `escapeHtml()`; applied to `stateName` in `updateSidebar()`. |
| V-4 | `index.html` | GeoJSON load now tries 2 mirrors with a 15 s timeout each (`GEOJSON_SOURCES`). |
| B-1 | `index.html` | Map click closes sidebar unless target is a state polygon. |
| B-2 | `index.html` | Added `syncCloseButton()`; close button shown only on desktop. |
| B-3 | `index.html` | Declared `let geojson = null;`; guarded `resetHighlight()`. |
| B-4 | `index.html` | `isMobile` is now a mutable `let`, recomputed on resize. |
| B-5 | `index.html` | Touch/swipe handlers attached unconditionally, guarded by `isMobile`. |
| B-6 | `index.html` | Removed inert `tap` / `tapTolerance` Leaflet options. |
| B-7 | `index.html` | `minZoom: 3` (removed no-op ternary). |
| B-8 | `index.html` | Collapsed contradictory `.close-btn` CSS. |
| — | `README.md` | Removed broken screenshot link + empty section; added Deployment notes. |
| — | `.github/workflows/ci.yml` | New CI: structural HTML check + `node --check` on inline JS. |
| — | `.github/scripts/validate_site.py` | New validation script used by CI. |

All patches were verified locally: `node --check` passes and
`.github/scripts/validate_site.py` passes.

---

## 8. CI / Deployment Findings

- **GitHub Pages is configured to build from `copilot/optimize-ui-for-mobile`**, a *stale
  feature branch*, not `main`. This means the live site (`anacondy.github.io/…`) is not
  sourced from the canonical branch, and any merge to `main` will **not** be reflected
  until the source is changed.
  - I attempted to repoint it to `main` via the API but received
    `403 Resource not accessible by integration` — the sandbox token lacks Pages admin.
  - **Action required (repo owner):** in *Settings → Pages*, set the source branch to
    `main` (root). This is the real fix for "make the CI build reflect the code."
- **Two workflows exist** on the repo: `pages-build-deployment` (Pages) and the dynamic
  `Copilot coding agent` workflow. There was **no real test/validation CI** — only the
  Pages publish. I added `.github/workflows/ci.yml`, which runs on every push to `main`
  and on every pull request, giving a genuine green check.

---

## 9. Recommendations / Next Steps

1. **Repoint GitHub Pages to `main`** (owner action — see §8).
2. **Vendor `states.geojson` into the repo** (`data/states.geojson`) and load it locally;
   keep the CDN fetch only as a fallback. Removes the last external runtime dependency.
3. **Add SRI + `crossorigin`** to the Leaflet and Google Fonts `<link>`/`<script>` tags.
4. **Move CSP to nonce-based**: extract the inline `<style>`/`<script>` into `style.css` /
   `app.js`, serve with `script-src 'self' 'nonce-…'`, and drop `'unsafe-inline'`.
5. **Add automated browser tests** (e.g. Playwright) that assert: map loads, clicking a
   state opens the sidebar, clicking the ocean closes it, and the close button toggles with
   viewport width.
6. **Extract political data** into `data/states.json` + `data/politics.json` to separate
   content from presentation.
7. **Add a retry button** on the loading-error toast instead of a dead-end message.

---

*End of analysis.*
