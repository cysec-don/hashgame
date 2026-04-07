# Hash Cracker Challenge

A cybersecurity educational game that teaches students how hashing algorithms work through hands-on brute-force practice. Crack the hash, find the hidden number, and learn real-world skills!

**Designed & Created by [Cysec Don](mailto:cysecdon@gmail.com)**

---

## Overview

Each round presents you with:
- A **sentence with a missing number** (shown as `_____`)
- The **hash algorithm used** (MD5, SHA1, SHA256, or SHA512)
- The **resulting hash value** of the complete sentence

Your mission: **figure out the hidden number** that completes the sentence and produces the given hash.

> **Important:** Each question has a **different** answer. You cannot guess the same number twice! This forces you to actually understand and practice hash cracking.

---

## Features

- **20 unique challenge sentences** — each with a different hidden number
- **4 hash algorithms** — MD5, SHA1, SHA256, SHA512 randomly selected per round
- **Answers hidden in source code** — XOR-encrypted and scrambled so students can't cheat by reading the code
- **HTTP-style status responses** — fuzzy server behavior adds realism (sometimes chaotic, sometimes accurate)
- **Score tracking** — tracks how many hashes you've cracked
- **Two versions** — CLI (terminal) and GUI (graphical window)
- **Built-in hint system** — teaches students the brute-force technique

---

## Prerequisites

- **Python 3.6 or higher** installed on your system
- No additional packages required! The game uses only Python's built-in libraries:
  - `tkinter` (comes pre-installed with most Python distributions)
  - `hashlib`
  - `random`
  - `os`
  - `sys`

> **Note for Linux users:** If `tkinter` is not installed, run:
> ```
> sudo apt-get install python3-tk
> ```

---

## Installation

### Option 1: Clone from GitHub (Recommended)

```bash
git clone https://github.com/cysec-don/hashgame.git
cd hashgame
```

### Option 2: Download Directly

1. Go to [https://github.com/cysec-don/hashgame](https://github.com/cysec-don/hashgame)
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your preferred location

---

## Usage

### CLI Version (Terminal)

Open your terminal and run:

```bash
python hash_game_cli.py
```

**How to play:**

1. A random challenge appears showing the hash algorithm, hash value, and a masked sentence
2. Type a number and press **Enter** to submit your guess
3. The game checks if your number produces the target hash:
   - **Green "200 OK"** = Correct! You cracked the hash!
   - **Red "400 Bad Request"** = Wrong! Try another number.
   - **Yellow/Orange** = Chaotic server response (the game simulates network fuzzing)
4. Press **Enter** to move to the next round

**Available commands during gameplay:**

| Command | Description |
|---------|-------------|
| `hint` | Shows a Python brute-force example |
| `quit` or `exit` or `q` | Ends the game and shows final score |
| Any number | Submits your guess |

**Example gameplay:**

```
  Hash Type  : MD5
  Hash Value : a1b2c3d4e5f6...

  Sentence   : I just paid _____ naira for coffee.

  Your guess: 100
  >> 400 Bad Request - WRONG! Hash does not match.
     Your input '100' did not produce the target hash.
     Try hashing different numbers!
```

---

### GUI Version (Graphical Window)

Run:

```bash
python hash_game_gui.py
```

**How to play:**

1. The game window opens with a dark hacker-themed interface
2. The hash algorithm, target hash, and masked sentence are displayed
3. Type your guess in the input field and click **SUBMIT** (or press **Enter**)
4. The result appears below:
   - **Green text** = Correct!
   - **Red text** = Wrong hash
   - **Yellow/Orange text** = Chaotic server response
5. Click **NEXT ROUND** to get a new challenge

**GUI Buttons:**

| Button | Description |
|--------|-------------|
| **SUBMIT** | Submits your number guess |
| **NEXT ROUND** | Generates a new challenge |
| **HINT** | Opens a popup with brute-force code example |
| **CREDITS** | Shows creator information |

---

## How to Actually Crack the Hash (Educational)

The whole point of this game is to learn **hash brute-forcing**. Here's how:

### Step 1: Understand the Problem

You have a sentence like `I just paid _____ naira for coffee.` and a hash. You need to find which number fills the blank.

### Step 2: Write a Brute-Force Script

Create a Python script that tries numbers until it finds a match:

```python
import hashlib

target_hash = "a1b2c3d4e5f6..."  # The hash shown in the game
algo = "md5"                      # The algorithm shown in the game

for i in range(1, 10000):
    sentence = f"I just paid {i} naira for coffee."
    if algo == "md5":
        h = hashlib.md5(sentence.encode()).hexdigest()
    elif algo == "sha1":
        h = hashlib.sha1(sentence.encode()).hexdigest()
    elif algo == "sha256":
        h = hashlib.sha256(sentence.encode()).hexdigest()
    elif algo == "sha512":
        h = hashlib.sha512(sentence.encode()).hexdigest()

    if h == target_hash:
        print(f"CRACKED! The number is: {i}")
        break
```

### Step 3: Enter the Answer

Once your script finds the number, enter it in the game!

> **Real-world takeaway:** This is exactly how password cracking tools like Hashcat and John the Ripper work — they try millions of inputs until the hash matches. Now you understand the basics!

---

## File Structure

```
hashgame/
├── hash_game_cli.py      # CLI (terminal) version of the game
├── hash_game_gui.py      # GUI (graphical) version of the game
└── README.md             # This file
```

---

## Troubleshooting

### "No module named tkinter" (Linux)
```bash
sudo apt-get install python3-tk
```

### "No module named tkinter" (macOS)
Tkinter comes bundled with macOS Python installations. If missing, reinstall Python from [python.org](https://www.python.org).

### CLI colors not showing on Windows
The CLI uses ANSI color codes. On older Windows versions, colors may not display correctly. Use the **GUI version** instead, or run in **Windows Terminal** which supports ANSI colors.

### Game feels too hard?
Click the **HINT** button (GUI) or type `hint` (CLI) for a brute-force code example. Remember — the answers are all integers, so you just need to try numbers!

---

## Credits

**Designed & Created by Cysec Don**
📧 Email: [cysecdon@gmail.com](mailto:cysecdon@gmail.com)
📁 GitHub: [cysec-don](https://github.com/cysec-don)

---

## License

This project is free to use for educational purposes. Please give credit to **Cysec Don** if you share or modify it.

---

*Learn hashing through play. Happy cracking!*
