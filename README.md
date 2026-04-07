# Hash Cracker Challenge v2

A cybersecurity educational game that teaches students how hashing algorithms work through hands-on brute-force practice. Crack the hash, find the hidden answer, and level up through progressively harder challenges!

**Designed & Created by [Cysec Don](mailto:cysecdon@gmail.com)**

---

## Overview

Each round presents you with:
- A **sentence with a missing answer** (shown as `_____`)
- The **hash algorithm used** (determined by your current level)
- The **resulting hash value** of the complete sentence

Your mission: **figure out the answer** that completes the sentence and produces the given hash.

> **Key Feature:** Answers are NOT just numbers! They can be **numbers** (e.g., "443"), **words** (e.g., "nmap"), or **phrases** (e.g., "zero day"). Every single question has a **unique** answer — no repeats!

---

## What's New in v2

| Feature | v1 | v2 |
|---------|----|----|
| **Answers** | Numbers only | Numbers, words, AND phrases |
| **Difficulty** | Same for all rounds | Progressive: MD5 → SHA1 → SHA256 → SHA512 |
| **Questions** | 104 random | 104 curated cybersecurity topics |
| **Level System** | None | 4 levels with advancement |
| **Answer Matching** | Exact | Case-insensitive |

---

## Progressive Difficulty System

The game features 4 difficulty levels. You must crack enough hashes to advance:

| Level | Algorithm | Name | Questions Needed | Answer Style |
|-------|-----------|------|-----------------|-------------|
| 1 | MD5 | EASY | 3 correct | Short numbers & everyday words (e.g., "root", "22") |
| 2 | SHA1 | MEDIUM | 5 correct | Medium numbers & security terms (e.g., "404", "nmap") |
| 3 | SHA256 | HARD | 7 correct | Two-word phrases & concepts (e.g., "zero day", "sql injection") |
| 4 | SHA512 | EXPERT | Endless | Complex phrases & mixed answers (e.g., "man in the middle", "zero trust") |

As you level up, hash digests get **longer and harder to crack**:
- MD5: 32 characters
- SHA1: 40 characters
- SHA256: 64 characters
- SHA512: 128 characters

---

## Answer Examples

Answers are diverse and unique across all 104 challenges:

| Type | Examples |
|------|----------|
| **Numbers** | "22", "443", "65535", "256", "64" |
| **Words** | "root", "nmap", "hashcat", "owasp", "kubernetes", "steganography" |
| **Phrases** | "ctrl c", "ip addr", "sql injection", "zero day", "man in the middle", "network segmentation" |

---

## Features

- **104 unique challenges** — each with a different answer
- **Mixed answer types** — numbers, single words, and multi-word phrases
- **Progressive difficulty** — hashes get longer and answers get harder
- **4 hash algorithms** — MD5, SHA1, SHA256, SHA512 unlocked by level
- **Answers hidden in source code** — XOR-encrypted with shuffled index mapping
- **All 520 hash computations verified** — every sentence × algorithm tested
- **HTTP-style status responses** — fuzzy server behavior adds realism
- **Score tracking** — tracks correct answers and current level
- **Two versions** — CLI (terminal) and GUI (graphical window)
- **Built-in hint system** — teaches brute-force techniques
- **Case-insensitive** — "Root", "ROOT", and "root" all work

---

## Challenge Topics by Level

### Level 1 — Easy (Everyday Tech)
Ports, file extensions, keyboard shortcuts, Linux commands, company names

### Level 2 — Medium (Security Basics)
HTTP status codes, security tools (nmap, hashcat, Wireshark), malware types, protocols

### Level 3 — Hard (Security Concepts)
SQL injection, phishing, steganography, Kubernetes, authentication, authorization

### Level 4 — Expert (Advanced Security)
Man-in-the-middle, lateral movement, zero trust, DNS tunneling, polymorphic malware, supply chain attacks

---

## Prerequisites

- **Python 3.6 or higher**
- No additional packages required (uses only built-in libraries: `tkinter`, `hashlib`, `random`, `os`, `sys`)

> **Linux users:** If `tkinter` is missing: `sudo apt-get install python3-tk`

---

## Installation

### Clone from GitHub
```bash
git clone https://github.com/cysec-don/hashgame.git
cd hashgame
```

### Download ZIP
Go to [github.com/cysec-don/hashgame](https://github.com/cysec-don/hashgame) → "Code" → "Download ZIP"

---

## Usage

### CLI Version
```bash
python hash_game_cli.py
```

- Type your answer (number, word, or phrase) and press Enter
- `hint` — Shows brute-force examples
- `level` — Shows current difficulty and progress
- `quit` — Exits with final score

### GUI Version
```bash
python hash_game_gui.py
```

- Type your answer and click SUBMIT (or press Enter)
- **NEXT ROUND** — New challenge
- **HINT** — Brute-force tips popup
- **CREDITS** — Creator info popup
- Level indicator bar changes color as you progress

---

## How to Crack the Hashes

### For Number Answers
```python
import hashlib
target = "<paste hash here>"
sentence = "Default SSH port is -."
for i in range(1, 100000):
    text = sentence.replace("-", str(i))
    h = hashlib.md5(text.encode()).hexdigest()
    if h == target:
        print(f"CRACKED: {i}")
        break
```

### For Word/Phrase Answers
Think about the topic! If the sentence mentions "network scanning," the answer might be "nmap." Try common cybersecurity terms and tools.

```python
import hashlib
target = "<paste hash here>"
sentence = "The tool used for network scanning is -."
wordlist = ["nmap", "wireshark", "hashcat", "burpsuite", "nikto"]
for word in wordlist:
    text = sentence.replace("-", word)
    h = hashlib.sha1(text.encode()).hexdigest()
    if h == target:
        print(f"CRACKED: {word}")
        break
```

---

## File Structure
```
hashgame/
├── hash_game_cli.py      # CLI (terminal) version
├── hash_game_gui.py      # GUI (graphical) version
└── README.md             # This file
```

---

## Credits

**Designed & Created by Cysec Don**
📧 [cysecdon@gmail.com](mailto:cysecdon@gmail.com)
📁 [github.com/cysec-don](https://github.com/cysec-don)

---

## License

Free to use for educational purposes. Please credit **Cysec Don** if you share or modify it.

---

*104 challenges, 4 levels, infinite learning — happy cracking!*
