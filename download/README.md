# 🔐 HashGame - Hash Brute-Force Trainer

A cybersecurity educational game that teaches students how hashing algorithms work through hands-on brute-force practice. Crack the hash, find the hidden answer, and learn real-world skills!

**Designed & Created by [Cysec Don](mailto:cysecdon@gmail.com)**

---

## Overview

Each round presents you with:
- A **sentence with a missing word or number** (shown as `___`)
- The **hash algorithm used** (from 50 different hash types)
- The **resulting hash value** of the answer
- The **difficulty level** (Beginner → Easy → Medium → Hard → Expert → Extreme → Nightmare → Insane)

Your mission: **figure out the hidden answer** that produces the given hash.

> **Important:** Each question has a **unique** answer — 250 are everyday words and 250 are numbers. You cannot reuse the same answer! This forces you to actually understand and practice hash cracking.

---

## Features

- **500 unique challenge questions** — each with a different hidden answer (words + numbers)
- **50 hash types** ranked from beginner to extremely hard
- **Progressive difficulty** — starts with simple checksums (CRC16, Adler-32) and advances to military-grade algorithms (Argon2id, Catena, Lyra2)
- **Answers hidden in source code** — XOR-encrypted and scrambled so students can't cheat
- **Score tracking** — tracks how many hashes you've cracked
- **Skip, hint, and quit** commands during gameplay
- **Two versions** — CLI (terminal) and GUI (graphical window)
- **Built-in hint system** — reveals answer length and first/last character

---

## 50 Hash Types (Ranked Easy → Extremely Hard)

### Beginner (Checksums & Non-Cryptographic)
| # | Hash Type | Questions |
|---|-----------|-----------|
| 1 | CRC16 | 1-10 |
| 2 | Adler-32 | 11-20 |
| 3 | CRC32 | 21-30 |
| 4 | FNV-1 (32-bit) | 31-40 |
| 5 | Jenkins (one-at-a-time) | 41-50 |

### Easy (Legacy Cryptographic)
| # | Hash Type | Questions |
|---|-----------|-----------|
| 6 | NTLM | 51-60 |
| 7 | MD4 | 61-70 |
| 8 | MD5 | 71-80 |
| 9 | SHA-0 | 81-90 |
| 10 | RIPEMD-128 | 91-100 |
| 11 | HAVAL-128 | 101-110 |
| 12 | Tiger-128 | 111-120 |
| 13 | Snefru-128 | 121-130 |
| 14 | GOST (old) | 131-140 |

### Medium (Standard Cryptographic)
| # | Hash Type | Questions |
|---|-----------|-----------|
| 15 | RIPEMD-160 | 141-150 |
| 16 | HAVAL-160 | 151-160 |
| 17 | Tiger-160 | 161-170 |
| 18 | SHA-1 | 171-180 |
| 19 | SHA-224 | 181-190 |
| 20 | Whirlpool | 191-200 |
| 21 | SHA-256 | 201-210 |
| 22 | SHA-384 | 211-220 |
| 23 | SHA-512 | 221-230 |
| 24 | SHA-512/224 | 231-240 |
| 25 | SHA-512/256 | 241-250 |

### Hard (Modern Cryptographic)
| # | Hash Type | Questions |
|---|-----------|-----------|
| 26 | SHA3-224 | 251-260 |
| 27 | SHA3-256 | 261-270 |
| 28 | SHA3-384 | 271-280 |
| 29 | SHA3-512 | 281-290 |
| 30 | BLAKE2s | 291-300 |
| 31 | BLAKE2b | 301-310 |
| 32 | BLAKE3 | 311-320 |
| 33 | Skein-256 | 321-330 |
| 34 | Skein-512 | 331-340 |
| 35 | Keccak-256 | 341-350 |

### Expert (Advanced)
| # | Hash Type | Questions |
|---|-----------|-----------|
| 36 | KangarooTwelve | 351-360 |
| 37 | ParallelHash | 361-370 |
| 38 | Haraka | 371-380 |
| 39 | Streebog-256 | 381-390 |
| 40 | Streebog-512 | 391-400 |

### Extreme to Insane (Password Hashing Functions)
| # | Hash Type | Questions |
|---|-----------|-----------|
| 41 | PBKDF2-HMAC-SHA256 | 401-410 |
| 42 | bcrypt | 411-420 |
| 43 | scrypt | 421-430 |
| 44 | Argon2d | 431-440 |
| 45 | Argon2i | 441-450 |
| 46 | Argon2id | 451-460 |
| 47 | Yescrypt | 461-470 |
| 48 | Balloon Hashing | 471-480 |
| 49 | Lyra2 | 481-490 |
| 50 | Catena | 491-500 |

---

## Prerequisites

- **Python 3.8 or higher** installed on your system

### Install Required Packages

```bash
pip install bcrypt argon2-cffi blake3 pycryptodome
```

### Additional Notes
- `tkinter` comes pre-installed with most Python distributions (needed for GUI version)
- `hashlib` and `zlib` are Python built-in libraries

> **Linux users:** If `tkinter` is not installed, run:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## Installation

### Option 1: Clone from GitHub (Recommended)

```bash
git clone https://github.com/cysec-don/hashgame.git
cd hashgame
pip install bcrypt argon2-cffi blake3 pycryptodome
```

### Option 2: Download Directly

1. Go to [https://github.com/cysec-don/hashgame](https://github.com/cysec-don/hashgame)
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file and install dependencies:
   ```bash
   pip install bcrypt argon2-cffi blake3 pycryptodome
   ```

---

## Usage

### CLI Version (Terminal)

Open your terminal and run:

```bash
python hash_game_cli.py
```

**How to play:**

1. A colorful welcome banner appears with credits
2. Press Enter to start the game
3. Each question shows:
   - Question number (e.g., "Question 42 of 500")
   - Hash type (e.g., "SHA-256")
   - Difficulty level (e.g., "Hard" with emoji indicator)
   - The question with `___` blank
   - The hash value to crack
4. Type your answer and press **Enter**
5. The game checks if your answer produces the target hash:
   - **Green "CORRECT!"** = You cracked the hash!
   - **Red "Incorrect"** = Wrong answer, the correct one is revealed
6. Continue through all 500 questions!

**Available commands during gameplay:**

| Command | Description |
|---------|-------------|
| `skip` | Skips the current question (reveals answer) |
| `hint` | Shows answer length, first and last character |
| `quit` or `exit` or `q` | Ends the game and shows final score |
| `credits` | Shows creator information |

---

### GUI Version (Graphical Window)

Run:

```bash
python hash_game_gui.py
```

**How to play:**

1. The game window opens with a dark hacker-themed interface
2. The hash type, difficulty, question, and target hash are displayed
3. Type your guess in the input field and click **SUBMIT** (or press **Enter**)
4. The result appears below:
   - **Green text** = Correct!
   - **Red text** = Wrong answer (correct one is revealed)
5. Click **NEXT** to proceed to the next question
6. Track your score and progress with the progress bar

**GUI Buttons:**

| Button | Description |
|--------|-------------|
| **SUBMIT** | Submits your answer guess |
| **HINT** | Shows answer length and first/last character |
| **SKIP** | Skips current question (reveals answer) |
| **QUIT** | Exits the game |
| **Credits** | Shows creator information |

---

## How to Actually Crack the Hash (Educational)

The whole point of this game is to learn **hash brute-forcing**. Here's how:

### Step 1: Understand the Problem

You have a question like `The encryption key length must be at least ___ bits.` and a hash. You need to find which word or number fills the blank.

### Step 2: Write a Brute-Force Script

Create a Python script that tries possibilities until it finds a match:

```python
import hashlib

target_hash = "c86d"  # The hash shown in the game (for CRC16)

# Try common words and numbers
wordlist = ["coffee", "dragon", "sunshine", "42", "256", "1337",
            "admin", "password", "guitar", "planet"]

for word in wordlist:
    h = hashlib.md5(word.encode()).hexdigest()
    if h == target_hash:
        print(f"CRACKED! The answer is: {word}")
        break
```

For number answers, use a range:

```python
for i in range(100, 10000):
    h = hashlib.md5(str(i).encode()).hexdigest()
    if h == target_hash:
        print(f"CRACKED! The number is: {i}")
        break
```

### Step 3: Enter the Answer

Once your script finds the answer, enter it in the game!

> **Real-world takeaway:** This is exactly how password cracking tools like Hashcat and John the Ripper work — they try millions of inputs until the hash matches. Now you understand the basics!

---

## Answer Types

The game uses a mix of answer types to keep things interesting:

- **Everyday words** (250 answers): coffee, dragon, sunshine, guitar, planet, thunder, castle, diamond, phoenix, raven, crystal, shadow, matrix, cipher, vector, kernel, module, proxy, socket, beacon, payload, rootkit, backdoor, etc.
- **Numbers** (250 answers): 15, 42, 77, 128, 256, 500, 1337, 2048, 4096, 9999, etc.

Every answer is **unique** — no duplicates across all 500 questions.

---

## File Structure

```
hashgame/
├── hash_game_cli.py      # CLI (terminal) version — 500 questions, 50 hash types
├── hash_game_gui.py      # GUI (graphical) version — same 500 questions
└── README.md             # This file
```

---

## Troubleshooting

### "No module named 'bcrypt'" / 'argon2' / 'blake3'
Install the required packages:
```bash
pip install bcrypt argon2-cffi blake3 pycryptodome
```

### "No module named tkinter" (Linux)
```bash
sudo apt-get install python3-tk
```

### "No module named tkinter" (macOS)
Tkinter comes bundled with macOS Python installations. If missing, reinstall Python from [python.org](https://www.python.org).

### CLI colors not showing on Windows
The CLI uses ANSI color codes. On older Windows versions, colors may not display correctly. Use the **GUI version** instead, or run in **Windows Terminal** which supports ANSI colors.

### Password hash questions are slow?
Password hash types (bcrypt, scrypt, Argon2, PBKDF2, etc.) use intentionally low work factors so the game remains playable. Each verification takes about 0.05-0.5 seconds.

---

## Credits

**Designed & Created by Cysec Don**
📧 Email: [cysecdon@gmail.com](mailto:cysecdon@gmail.com)
📁 GitHub: [cysec-don](https://github.com/cysec-don)

---

## License

This project is free to use for educational purposes. Please give credit to **Cysec Don** if you share or modify it.

---

*Learn hashing through play. Happy cracking!* 🔐
