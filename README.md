# MiniWord — Embeddable Daily Word Game

MiniWord is a lightweight, embeddable Wordle-style daily game built to be hosted on GitHub Pages (or any static host) and embedded in an iframe.

Features
- Standard Wordle rules: 5-letter words, 6 guesses
- Daily word (same for everyone) determined by UTC date (changes every 24 hours)
- Original Wordle list behavior: separate answers list (solutions) and allowed-guesses list (validation)
- Loads open-source word lists from public raw URLs (or local files if you host `answers.txt` and `allowed.txt` in the repo root)
- Local stats: games played, win rate, current & best streak (saved to `localStorage`)
- Shareable emoji result (copy to clipboard)
- Embeddable via iframe

Included files
- `index.html` — single-file web app. It fetches full word lists at runtime but will fall back to a built-in sample list if fetching fails.
- `LICENSE` — MIT license.

Deployment (GitHub Pages)
1. Create a new repository (or use an existing one).
2. Add `index.html` (and optionally `answers.txt` and `allowed.txt` if you want local copies of the lists) to the repository root.
   - If you prefer hosting your own copies of the lists, create `answers.txt` and `allowed.txt` (one word per line, lowercase) in the repo root — index.html will try local files first.
3. In the repository Settings → Pages, set Source to your branch (e.g., `main`) and folder to `/ (root)`.
4. Wait a moment while GitHub publishes the site. Your site will be available at `https://<username>.github.io/<repo>/`.
5. Embed the game in another page with:
   <iframe src="https://<username>.github.io/<repo>/index.html" width="560" height="760" style="border:0"></iframe>

Customizing the word lists
- The app tries public raw URLs (mirrors) first. If you want full control, add `answers.txt` and `allowed.txt` (one word per line, 5-letter words, lowercase) to the repo root to override remote fetches.
- For the "original Wordle list behavior", use a smaller `answers.txt` for solutions and a larger `allowed.txt` for guesses.
- Recommended public sources (examples):
  - `https://raw.githubusercontent.com/tabatkins/wordle-list/main/answers.txt`
  - `https://raw.githubusercontent.com/tabatkins/wordle-list/main/allowed-guesses.txt`
  (Index.html already attempts these URLs by default.)

Embedding & iframe tips
- The game is responsive but adjust iframe width/height to taste.
- Example:
  <iframe src="https://<username>.github.io/<repo>/index.html" width="630" height="760" style="border:0"></iframe>

Want me to:
- Create the GitHub repository and push these files for you? If yes, tell me the repository name and owner (e.g., clariteegroup/miniworld) and I will push the files.
- Or produce a ZIP containing all files ready to upload?
- Or add features like hard mode, daily countdown, result history export/import, or a custom theme?

I can also produce `answers.txt` and `allowed.txt` files directly in this chat if you want them included in the repo rather than fetched at runtime.
