import tkinter as tk
from tkinter import font as tkfont
import hashlib
import random
import base64

# ═══════════════════════════════════════════════════════════════
#   HASH CRACKER CHALLENGE - GUI Edition
#   Designed by Cysec Don
# ═══════════════════════════════════════════════════════════════

# --- Hidden answer (encoded, not readable in source) ---
_a = "NT" + "A" + "w"
correct_value = base64.b64decode(_a.encode()).decode()

# --- Sentence pool ---
plain_sentences = [
    "I just paid - naira for coffee.",
    "The system crashed after receiving - requests.",
    "My account was charged - times by mistake.",
    "Error: you owe - dollars immediately.",
    "Server responded with - errors today.",
    "The hacker sent - packets to the target.",
    "Login failed after - attempts.",
    "Firewall blocked - connections.",
    "Database returned - results.",
    "User made - requests per second.",
    "System logged - warnings.",
    "API returned - responses.",
    "Bot generated - inputs.",
    "Process consumed - MB memory.",
    "Script executed - times.",
    "Scanner found - vulnerabilities.",
    "Admin reset password - times.",
    "Malware triggered - alerts.",
    "IDS detected - anomalies.",
    "Backup failed after - tries."
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


def hash_sentence(sentence, algo):
    return hash_functions[algo](sentence.encode()).hexdigest()


def new_round():
    global current_algo, current_hash, current_sentence, score, total_rounds

    current_sentence = random.choice(plain_sentences)
    current_algo = random.choice(list(hash_functions.keys()))
    filled = current_sentence.replace("-", correct_value)
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
        if user == correct_value:
            score += 1
            result_label.config(
                text="200 OK - CORRECT! Hash matched!",
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
    hint_window.geometry("450x220")
    hint_window.configure(bg="#1a1a2e")
    hint_window.resizable(False, False)

    tk.Label(
        hint_window,
        text="HINT",
        font=("Consolas", 16, "bold"),
        fg="#00ff88", bg="#1a1a2e"
    ).pack(pady=(15, 10))

    hint_text = (
        "The answer is an integer.\n\n"
        "Write a Python script that hashes the sentence\n"
        "with different numbers and compares the result\n"
        "to the target hash.\n\n"
        "Example:\n"
        "hashlib.md5(b'I just paid 100 naira for coffee.')\n"
        "    .hexdigest()"
    )
    tk.Label(
        hint_window,
        text=hint_text,
        font=("Consolas", 9),
        fg="#cccccc", bg="#1a1a2e",
        justify="left"
    ).pack(pady=(0, 15))


# ═══════════════════════════════════════════════════════════════
#   GUI SETUP
# ═══════════════════════════════════════════════════════════════

root = tk.Tk()
root.title("Hash Cracker Challenge - Designed by Cysec Don")
root.geometry("700x520")
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
    font=("Consolas", 9),
    fg="#888888", bg="#16213e"
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

# --- Footer ---
tk.Label(
    root,
    text="Designed by Cysec Don | Learn Hashing Through Play",
    font=("Consolas", 8),
    fg="#555555", bg="#0f0f23"
).pack(side="bottom", pady=8)

# --- Start first round ---
new_round()
root.mainloop()
