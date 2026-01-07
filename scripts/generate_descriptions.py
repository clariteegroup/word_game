#!/usr/bin/env python3
"""
Query dictionaryapi.dev for short definitions of words in answers.txt and write descriptions.json.
- Writes a simple mapping: word -> first available short definition (string).
- Sleeps briefly between requests to be polite to the API.
"""
import json
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
ANS_FILE = ROOT / "answers.txt"
DESC_FILE = ROOT / "descriptions.json"

API_BASE = "https://api.dictionaryapi.dev/api/v2/entries/en/"

HEADERS = {
    "User-Agent": "clariteegroup-word-game/1.0 (+https://github.com/clariteegroup/word_game)"
}


def get_definition(word: str) -> str:
    url = API_BASE + word
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code != 200:
            return ""
        data = resp.json()
        # data is typically a list of entries; extract the first definition available
        if isinstance(data, list) and data:
            entry = data[0]
            meanings = entry.get("meanings", [])
            if meanings:
                defs = meanings[0].get("definitions", [])
                if defs:
                    d = defs[0].get("definition", "")
                    # keep it short (one sentence) if possible
                    if isinstance(d, str):
                        return d.strip()
        return ""
    except Exception:
        return ""


def main():
    if not ANS_FILE.exists():
        print("answers.txt not found — run generate_answers.py first or ensure answers.txt exists.")
        return

    words = [l.strip() for l in ANS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    out = {}

    for i, w in enumerate(words, start=1):
        print(f"[{i}/{len(words)}] fetching definition for: {w}")
        d = get_definition(w)
        out[w] = d or ""
        # polite pause to avoid hammering the public API
        time.sleep(0.5)

    DESC_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(out)} definitions to {DESC_FILE}")


if __name__ == "__main__":
    main()
