#!/usr/bin/env python3
"""
Generate answers.txt and allowed.txt from user_words.txt and a fallback list.
- Normalizes to lowercase
- Deduplicates
- Deterministic shuffle with seed=42
- Fills to 365 words from fallback if needed
"""
import random
from pathlib import Path

SEED = 42
TARGET = 365

# Small fallback pool (extra words to fill if needed)
FALLBACK = [
"arise","civic","baker","badge","bloom","brave","brain","bring","brown",
"candy","carry","cause","chain","chair","chart","charm","chase","cheap","cheer",
"chest","chief","child","china","choir","civil","claim","class","clean","clear",
"climb","clock","close","coach","coast","count","court","cover","crane","crate",
"crazy","cream","crime","cross","crowd","crown","dance","dairy","delay","demon",
"depth","doubt","dozen","draft","drama","dream","dress","drink","drive","dwell",
"eager","early","earth","eight","elite","entry","equal","error","event","every",
"exact","exist","extra","faith","false","favor","fence","ferry","field","fight",
"final","first","flash","fleet","fling","float","floor","focus","force","frame",
"fresh","front","fruit","funny","future","gauge","ghost","giant","globe","glory",
"grace","grade","grand","grant","grasp","grass","grave","great","green","greet",
"group","guide","habit","handy","happy","harsh","heart","heavy","honey","honor",
"horse","hotel","house","human","ideal","image","imply","index","inner","input",
"issue","joint","judge","juice","jelly","known","label","labor","large","laser",
"later","laugh","layer","learn","leave","level","light","limit","local","logic",
"loyal","lucky","lumen","major","maker","march","match","maybe","metal","meter",
"merry","might","minor","model","money","month","moral","motor","mount","mouse",
"mouth","movie","music","naive","nasty","naval","noble","noise","north","novel",
"nurse","occur","ocean","often","older","olive","order","organ","other","outer",
"owner","paint","panel","panic","paper","party","peace","phase","phone","photo",
"piano","piece","pilot","pitch","place","plain","plane","plant","plate","point",
"pride","prime","prize","proof","proud","pulse","punch","queen","quick","quiet",
"radio","raise","rally","range","rapid","ratio","reach","react","ready"
]

ROOT = Path(__file__).resolve().parents[1]
USER_FILE = ROOT / 'user_words.txt'
ANS_FILE = ROOT / 'answers.txt'
ALLOWED_FILE = ROOT / 'allowed.txt'

def load_user_words():
    if not USER_FILE.exists():
        print(f"user_words.txt not found at {USER_FILE}")
        return []
    lines = [l.strip() for l in USER_FILE.read_text(encoding='utf-8').splitlines()]
    words = []
    for line in lines:
        if not line:
            continue
        w = ''.join(ch for ch in line if ch.isalpha())
        w = w.lower()
        if len(w) == 5:
            words.append(w)
    return words

def main():
    raw = load_user_words()
    # dedupe preserving order
    seen = set()
    unique = []
    for w in raw:
        if w in seen:
            continue
        seen.add(w)
        unique.append(w)

    # deterministic shuffle of unique list
    rnd = random.Random(SEED)
    pool = unique[:]
    rnd.shuffle(pool)

    # fill from fallback if needed
    fallback_pool = [w for w in FALLBACK if w not in pool]
    idx = 0
    while len(pool) < TARGET:
        if idx >= len(fallback_pool):
            # reuse fallback in deterministic order if necessary
            fallback_pool = [w for w in FALLBACK if w not in pool]
            if not fallback_pool:
                raise SystemExit("Not enough words to fill answers.txt")
        pool.append(fallback_pool[idx % len(fallback_pool)])
        idx += 1

    pool = pool[:TARGET]

    # write answers.txt
    ANS_FILE.write_text('\n'.join(pool) + '\n', encoding='utf-8')
    print(f"Wrote {len(pool)} answers to {ANS_FILE}")

    # allowed.txt: merge existing allowed (if present) with answers
    existing_allowed = []
    if ALLOWED_FILE.exists():
        existing_allowed = [l.strip().lower() for l in ALLOWED_FILE.read_text(encoding='utf-8').splitlines() if l.strip()]
    allowed_set = []
    seen = set()
    for w in existing_allowed + pool:
        if w not in seen:
            seen.add(w)
            allowed_set.append(w)
    ALLOWED_FILE.write_text('\n'.join(allowed_set) + '\n', encoding='utf-8')
    print(f"Wrote {len(allowed_set)} allowed words to {ALLOWED_FILE}")

if __name__ == '__main__':
    main()
