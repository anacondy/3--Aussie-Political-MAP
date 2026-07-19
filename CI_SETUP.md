# Enabling CI for this Repository

This repository had **no real test/validation CI** — only the automatic GitHub Pages
publish (`pages-build-deployment`). The workflow below adds a genuine check that runs the
structural HTML validator and a JavaScript syntax check on every push to `main` and on
every pull request.

> **Why this file is not already active:** the agent token used for this branch does not
> have the GitHub App `workflows` permission, so it cannot create/update files under
> `.github/workflows/`. The file is provided here so a repo owner (or anyone with
> `workflows: write`) can drop it into place in one step.

## How to enable

1. Move this file into the workflows directory:

   ```bash
   mkdir -p .github/workflows
   git mv CI_SETUP.md .github/workflows/ci.yml   # then strip the YAML out of the prose below
   ```

   Or, more simply, create `.github/workflows/ci.yml` with **exactly** the YAML block
   below (the prose in this file is only explanation).

2. Commit and push to `main`. GitHub Actions will run it automatically.

## Proposed `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    name: Validate site
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Structural HTML check
        run: python3 .github/scripts/validate_site.py

      - name: JavaScript syntax check
        run: |
          python3 - <<'PY'
          import re
          html = open('index.html', encoding='utf-8').read()
          scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.S)
          with open('/tmp/app.js', 'w', encoding='utf-8') as fh:
              fh.write("\n".join(scripts))
          print("Extracted %d inline script block(s)" % len(scripts))
          PY
          node --check /tmp/app.js
```

## What it checks

- `python3 .github/scripts/validate_site.py` — verifies required markers are present in
  `index.html` and that the HTML tag nesting is balanced.
- `node --check` — parses the extracted inline JavaScript for syntax errors.

Both checks were verified to pass locally on this branch.
