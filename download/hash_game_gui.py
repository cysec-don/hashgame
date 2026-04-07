import tkinter as tk
from tkinter import font as tkfont
import hashlib
import random

# ═══════════════════════════════════════════════════════════════
#   HASH CRACKER CHALLENGE - GUI Edition
#   Designed by Cysec Don | cysecdon@gmail.com
# ═══════════════════════════════════════════════════════════════

# --- XOR key for answer decoding ---
_XK = 0x37


def _da(hx):
    """Decode XOR'd hex answer back to integer."""
    raw = bytes.fromhex(hx)
    return int(''.join(chr(b ^ _XK) for b in raw))


# --- Encoded answers (XOR'd, stored as hex fragments) ---
# Index mapping: sentence[i] -> _ea[_im[i]]
_ea = [
    "06" + "0207",       # idx 0  -> 150
    "05" + "070f0f",     # idx 1  -> 2048
    "00",                # idx 2  -> 7
    "0e" + "0e0e",       # idx 3  -> 999
    "0f" + "05",         # idx 4  -> 42
    "06" + "040400",     # idx 5  -> 1337
    "04",                # idx 6  -> 3
    "05" + "0201",       # idx 7  -> 256
    "06" + "07050f",     # idx 8  -> 1024
    "02" + "0707",       # idx 9  -> 500
    "0f" + "0f",         # idx 10 -> 88
    "0f" + "070f",       # idx 11 -> 404
    "06" + "070707",     # idx 12 -> 1000
    "02" + "0605",       # idx 13 -> 512
    "00" + "00",         # idx 14 -> 77
    "06" + "0f",         # idx 15 -> 14
    "02",                # idx 16 -> 5
    "04" + "06",         # idx 17 -> 31
    "01" + "0e",         # idx 18 -> 69
    "0e",                # idx 19 -> 9
]

# --- Scrambled index map: sentence[i] uses _ea[_im[i]] ---
_im = [13, 3, 19, 7, 16, 9, 14, 1, 17, 11, 4, 6, 8, 15, 18, 2, 10, 0, 5, 12]

# --- Sentence pool (each paired with a UNIQUE hidden answer) ---
plain_sentences = [
    "I just paid - naira for coffee.",            # 150
    "The system crashed after receiving - requests.",  # 2048
    "My account was charged - times by mistake.",  # 7
    "Error: you owe - dollars immediately.",       # 999
    "Server responded with - errors today.",       # 42
    "The hacker sent - packets to the target.",    # 1337
    "Login failed after - attempts.",              # 3
    "Firewall blocked - connections.",             # 256
    "Database returned - results.",                # 1024
    "User made - requests per second.",            # 500
    "System logged - warnings.",                   # 88
    "API returned - responses.",                   # 404
    "Bot generated - inputs.",                     # 1000
    "Process consumed - MB memory.",               # 512
    "Script executed - times.",                    # 77
    "Scanner found - vulnerabilities.",            # 14
    "Admin reset password - times.",               # 5
    "Malware triggered - alerts.",                 # 31
    "IDS detected - anomalies.",                   # 69
    "Backup failed after - tries.",                # 9
]

# --- Hash algorithms ---
hash_functions = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA512": hashlib.sha512
}

# --- HTTP-style status responses ---
status_codes = [
    "200 OK",
    "400 Bad Request",
    "401 Unauthorized",
    "403 Forbidden",
    "404 Not Found",
    "500 Internal Server Error",
    "502 Bad Gateway",
    "503 Service Unavailable"
]

score = 0
total_rounds = 0
current_algo = ""
current_hash = ""
current_sentence = ""
current_correct = 0


def hash_sentence(sentence, algo):
    return hash_functions[algo](sentence.encode()).hexdigest()


def new_round():
    global current_algo, current_hash, current_sentence, current_correct

    idx = random.randint(0, len(plain_sentences) - 1)
    current_sentence = plain_sentences[idx]
    current_algo = random.choice(list(hash_functions.keys()))
    current_correct = _da(_ea[_im[idx]])

    filled = current_sentence.replace("-", str(current_correct))
    current_hash = hash_sentence(filled, current_algo)

    masked = current_sentence.replace("-", "_____")

    algo_label.config(text=f"Hash Algorithm: {current_algo}")
    hash_label.config(text=f"{current_hash}")
    sentence_label.config(text=masked)
    result_label.config(text="")
    result_label.config(fg="#cccccc")
    entry.delete(0, tk.END)
    entry.focus_set()


def check():
    global score, total_rounds
    user = entry.get().strip()
    if not user:
        result_label.config(text="Enter a number to crack the hash!", fg="#ffaa00")
        return

    total_rounds += 1
    mode = random.choice(["check", "check", "ignore", "chaos"])

    if mode == "check":
        if user == str(current_correct):
            score += 1
            result_label.config(
                text=f"200 OK - CORRECT! Answer: {current_correct}",
                fg="#00ff88"
            )
        else:
            result_label.config(
                text="400 Bad Request - Hash mismatch! Try another number.",
                fg="#ff4444"
            )

    elif mode == "ignore":
        code = random.choice(status_codes)
        result_label.config(
            text=f"{code} - Ambiguous server response. Trust the hash!",
            fg="#ffaa00"
        )

    else:
        code = random.choice(status_codes)
        noise = user * random.randint(1, 3)
        result_label.config(
            text=f"{code} | Payload: {noise}",
            fg="#ff6600"
        )

    score_label.config(text=f"Score: {score}/{total_rounds}")


def show_hint():
    hint_window = tk.Toplevel(root)
    hint_window.title("Hint - Hash Cracker Challenge")
    hint_window.geometry("480x280")
    hint_window.configure(bg="#1a1a2e")
    hint_window.resizable(False, False)

    tk.Label(
        hint_window,
        text="HINT",
        font=("Consolas", 16, "bold"),
        fg="#00ff88", bg="#1a1a2e"
    ).pack(pady=(15, 10))

    hint_text = (
        "Each question has a UNIQUE number answer!\n\n"
        "Write a Python script that hashes the sentence\n"
        "with different numbers and compares the result\n"
        "to the target hash.\n\n"
        "Example:\n"
        "import hashlib\n"
        "for i in range(1, 10000):\n"
        "    h = hashlib.md5(\n"
        "        f'I just paid {i} naira for coffee.'.encode()\n"
        "    ).hexdigest()\n"
        "    if h == TARGET: print(f'Found: {i}')"
    )
    tk.Label(
        hint_window,
        text=hint_text,
        font=("Consolas", 9),
        fg="#cccccc", bg="#1a1a2e",
        justify="left"
    ).pack(pady=(0, 15))


def show_credits():
    cred_window = tk.Toplevel(root)
    cred_window.title("Credits - Hash Cracker Challenge")
    cred_window.geometry("400x180")
    cred_window.configure(bg="#1a1a2e")
    cred_window.resizable(False, False)

    tk.Label(
        cred_window,
        text="CREDITS",
        font=("Consolas", 16, "bold"),
        fg="#00ff88", bg="#1a1a2e"
    ).pack(pady=(15, 10))

    tk.Label(
        cred_window,
        text="Designed & Created by:",
        font=("Consolas", 10),
        fg="#888888", bg="#1a1a2e"
    ).pack(pady=(5, 2))

    tk.Label(
        cred_window,
        text="Cysec Don",
        font=("Consolas", 14, "bold"),
        fg="#00ccff", bg="#1a1a2e"
    ).pack(pady=(0, 5))

    tk.Label(
        cred_window,
        text="cysecdon@gmail.com",
        font=("Consolas", 10),
        fg="#ffaa00", bg="#1a1a2e"
    ).pack(pady=(0, 10))


# ═══════════════════════════════════════════════════════════════
#   GUI SETUP
# ═══════════════════════════════════════════════════════════════

root = tk.Tk()
root.title("Hash Cracker Challenge - Designed by Cysec Don")
root.geometry("700x560")
root.configure(bg="#0f0f23")
root.resizable(False, False)

# --- Title bar ---
title_frame = tk.Frame(root, bg="#16213e")
title_frame.pack(fill="x")
tk.Label(
    title_frame,
    text="HASH CRACKER CHALLENGE",
    font=("Consolas", 18, "bold"),
    fg="#00ff88", bg="#16213e"
).pack(pady=(12, 2))
tk.Label(
    title_frame,
    text="Designed by Cysec Don",
    font=("Consolas", 10, "bold"),
    fg="#00ccff", bg="#16213e"
).pack(pady=(0, 1))
tk.Label(
    title_frame,
    text="cysecdon@gmail.com",
    font=("Consolas", 9),
    fg="#ffaa00", bg="#16213e"
).pack(pady=(0, 10))

# --- Score ---
score_label = tk.Label(
    root, text="Score: 0/0",
    font=("Consolas", 12, "bold"),
    fg="#00ff88", bg="#0f0f23"
)
score_label.pack(pady=(12, 8))

# --- Algorithm display ---
algo_label = tk.Label(
    root, text="",
    font=("Consolas", 12, "bold"),
    fg="#00ccff", bg="#0f0f23"
)
algo_label.pack(pady=4)

# --- Hash display ---
hash_frame = tk.Frame(root, bg="#1a1a2e", bd=2, relief="groove")
hash_frame.pack(padx=40, pady=6, fill="x")
tk.Label(
    hash_frame,
    text="Target Hash:",
    font=("Consolas", 9),
    fg="#888888", bg="#1a1a2e"
).pack(anchor="w", padx=8, pady=(6, 0))
hash_label = tk.Label(
    hash_frame,
    text="",
    font=("Consolas", 10),
    fg="#ffffff", bg="#1a1a2e",
    wraplength=600, justify="left"
)
hash_label.pack(anchor="w", padx=8, pady=(2, 8))

# --- Sentence display ---
tk.Label(
    root, text="Crack this sentence:",
    font=("Consolas", 9),
    fg="#888888", bg="#0f0f23"
).pack(pady=(10, 2))
sentence_label = tk.Label(
    root, text="",
    font=("Consolas", 15, "bold"),
    fg="#ffffff", bg="#0f0f23"
)
sentence_label.pack(pady=4)

# --- Input ---
input_frame = tk.Frame(root, bg="#0f0f23")
input_frame.pack(pady=10)
entry = tk.Entry(
    input_frame,
    font=("Consolas", 14),
    width=20,
    bg="#1a1a2e", fg="#ffffff",
    insertbackground="#00ff88",
    bd=2, relief="groove"
)
entry.pack(side="left", padx=4)
entry.bind("<Return>", lambda e: check())

tk.Button(
    input_frame, text="SUBMIT",
    font=("Consolas", 11, "bold"),
    bg="#00ff88", fg="#0f0f23",
    activebackground="#00cc66",
    bd=0, padx=15, pady=4,
    command=check
).pack(side="left", padx=4)

# --- Result display ---
result_label = tk.Label(
    root, text="",
    font=("Consolas", 12),
    fg="#cccccc", bg="#0f0f23"
)
result_label.pack(pady=8)

# --- Buttons row ---
btn_frame = tk.Frame(root, bg="#0f0f23")
btn_frame.pack(pady=8)

tk.Button(
    btn_frame, text="NEXT ROUND",
    font=("Consolas", 10, "bold"),
    bg="#16213e", fg="#00ccff",
    activebackground="#1a3a5c",
    bd=0, padx=12, pady=4,
    command=new_round
).pack(side="left", padx=6)

tk.Button(
    btn_frame, text="HINT",
    font=("Consolas", 10, "bold"),
    bg="#16213e", fg="#ffaa00",
    activebackground="#1a3a5c",
    bd=0, padx=12, pady=4,
    command=show_hint
).pack(side="left", padx=6)

tk.Button(
    btn_frame, text="CREDITS",
    font=("Consolas", 10, "bold"),
    bg="#16213e", fg="#ff44ff",
    activebackground="#1a3a5c",
    bd=0, padx=12, pady=4,
    command=show_credits
).pack(side="left", padx=6)

# --- Footer ---
footer_frame = tk.Frame(root, bg="#0f0f23")
footer_frame.pack(side="bottom", pady=8)
tk.Label(
    footer_frame,
    text="Designed by Cysec Don",
    font=("Consolas", 8),
    fg="#555555", bg="#0f0f23"
).pack()
tk.Label(
    footer_frame,
    text="cysecdon@gmail.com | Learn Hashing Through Play",
    font=("Consolas", 8),
    fg="#555555", bg="#0f0f23"
).pack()

# --- Start first round ---
new_round()
root.mainloop()
