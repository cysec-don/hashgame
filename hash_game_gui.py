import tkinter as tk
from tkinter import font as tkfont
import hashlib
import random

# ═══════════════════════════════════════════════════════════════
#   HASH CRACKER CHALLENGE v2 - GUI Edition
#   Designed by Cysec Don | cysecdon@gmail.com
#   Features: 104 unique challenges, mixed answers (numbers,
#   words, phrases), progressive difficulty (MD5 → SHA512)
# ═══════════════════════════════════════════════════════════════

# --- XOR key for answer decoding ---
_XK = 0x37


def _da(hx):
    """Decode XOR'd hex answer back to string."""
    raw = bytes.fromhex(hx)
    return ''.join(chr(b ^ _XK) for b in raw)


# --- Encoded answers (XOR'd, stored as hex) ---
_ea = [
    "5659445e555b5217475b564e5558585c", "444e4443525a54435b", "5443455b1741", "564743",
    "544552535259435e565b1745584356435e5859", "4147591743425959525b", "0f07",
    "5a425b435e17515654435845175642435f", "445a56454317545859434556544317524f475b585e43",
    "515e455a405645521743565a4752455e5950", "47455e415e5b52505217524454565b56435e5859", "444e445b5850",
    "4e425a", "5f58444344", "5e59434542445e5859175352435254435e5859", "5c425552455952435244",
    "44465b175e595d5254435e5859", "475f5e445f5e595017445e4352", "595a5647", "050201",
    "4458545e565b175259505e595252455e5950", "59524f431750525917515e455240565b5b",
    "5642435f58455e4d56435e5859", "030703", "445a5e445f5e5950", "5d44", "5f435a5b",
    "5642435f5259435e5456435e5859", "405e515e", "4458514340564552175352475259535259545e5244", "5840564447",
    "405e4552445f56455c", "51424d4d5e5950", "56475e1744525442455e434e17435244435e5950", "0103",
    "4f44441756434356545c", "455347", "53535844", "5642435f58455e4d5253685c524e44",
    "5e59545e5352594317455244475859445217475b5659", "47525917435244435e5950",
    "545b584253174758444342455217545f52545c", "5453", "544152", "03", "5352594e17565b5b", "445f56020605",
    "5647575b52", "5a5659175e5917435f52175a5e53535b52", "0502", "5e471756535345", "474e", "5f56445f545643",
    "55454243521751584554521756434356545c", "5545424352175158455452", "030304", "564756545f52",
    "5443455b1744", "585642435f", "47545e17534444", "5b56435245565b175a5841525a525943", "44514347",
    "45585843", "525954454e47435e5859", "435f45525643175e5943525b5b5e5052595452",
    "47585b4e5a5845475f5e54175a565b40564552", "5f56445f5e5950", "535643561747585e4458595e5950", "5b5e594244",
    "5a5e595e5a425a17565454524444", "4459584543", "5359441743425959525b5e5950", "5d5641564454455e4743",
    "0505", "445e525a17475b56435158455a", "44435250565958504556475f4e", "52415e5b1743405e59",
    "544552535259435e565b1744434251515e5950", "5952434058455c174452505a52594356435e5859", "425542594342",
    "56475e175056435240564e", "435f45525643175f4259435e5950", "545251175158455a5643",
    "47504717525954454e47435e5859", "020707", "030706", "4345585d5659175f58454452",
    "445254455243175a56595650525a525943", "0204", "54455859175d5855", "4058455a", "5b44", "4d5245581753564e",
    "4d524558174345424443", "47455e5943", "5542515152451758415245515b5840", "5a5e54455844585143", "030704",
    "0102020402", "45565944585a40564552", "535944175f5e5d56545c5e5950", "0506", "5443455b1754",
    "455858435c5e43",
]

# --- Scrambled index map: sentence[i] uses _ea[_im[i]] ---
_im = [
    73, 6, 55, 101, 88, 49, 62, 51, 25, 3,
    12, 91, 42, 94, 102, 2, 57, 96, 47, 68,
    72, 26, 61, 44, 50, 79, 23, 85, 97, 84,
    19, 98, 28, 18, 52, 99, 43, 30, 58, 45,
    46, 13, 1, 70, 31, 36, 54, 38, 63, 37,
    34, 56, 16, 77, 89, 40, 17, 75, 5, 24,
    21, 59, 35, 27, 83, 0, 15, 14, 20, 92,
    66, 80, 22, 7, 69, 90, 11, 82, 48, 10,
    60, 103, 32, 29, 53, 67, 93, 81, 41, 71,
    8, 86, 78, 64, 100, 65, 33, 76, 4, 74,
    95, 87, 39, 9,
]

# --- Difficulty level for each sentence ---
_levels = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4,
]

# --- 104 unique cybersecurity challenge sentences ---
plain_sentences = [
    "Default SSH port is -.",
    "HTTP uses port -.",
    "HTTPS uses port -.",
    "FTP uses port -.",
    "DNS uses port -.",
    "SMTP uses port -.",
    "The common username for admin is -.",
    "The file extension for Python is -.",
    "The file extension for JavaScript is -.",
    "Linux package manager on Debian is -.",
    "Linux package manager on RedHat is -.",
    "The command to list files in Linux is -.",
    "The command to change directory in Linux is -.",
    "The command to print text in Python is -.",
    "The shortcut to copy is -.",
    "The shortcut to paste is -.",
    "The shortcut to save is -.",
    "The company that makes Windows is -.",
    "The company that makes macOS is -.",
    "The founder of Linux is -.",
    "A popular programming language for web is -.",
    "The file extension for HTML is -.",
    "The protocol for secure file transfer is -.",
    "Ping sends - packets by default on Linux.",
    "The command to check IP address is -.",
    "A popular Linux distribution is -.",
    "HTTP status code for Not Found is -.",
    "HTTP status code for Unauthorized is -.",
    "HTTP status code for Forbidden is -.",
    "HTTP status code for Server Error is -.",
    "AES encryption key size is - bits.",
    "The maximum TCP port number is -.",
    "The most common Wi-Fi protocol is -.",
    "The tool used for network scanning is -.",
    "The tool used for password cracking is -.",
    "A type of malware that encrypts files is -.",
    "A software vulnerability database is -.",
    "The standard for security headers is -.",
    "The authentication protocol using tokens is -.",
    "A firewall rule that blocks all traffic is called -.",
    "The hash function used for passwords in Linux is -.",
    "The file that stores DNS locally is -.",
    "The command to restart a service in Linux is -.",
    "A popular intrusion detection system is -.",
    "The tool for packet analysis is -.",
    "The protocol for remote desktop is -.",
    "A method to bypass authentication is called -.",
    "The file containing SSH keys is -.",
    "The process of encoding data is called -.",
    "A type of attack that floods a server is called -.",
    "The default TTL value is -.",
    "A web server made by Apache is called -.",
    "The attack that targets SQL databases is -.",
    "The attack that steals login credentials is -.",
    "A script that runs automatically is called -.",
    "The process of finding vulnerabilities is called -.",
    "A fake website to steal passwords is called -.",
    "The method of hiding data in images is -.",
    "A proxy that hides your IP is called -.",
    "The attack targeting mobile phones is -.",
    "A network device that filters traffic is -.",
    "The security standard for payment cards is -.",
    "A type of attack using crafted URLs is -.",
    "The process of verifying user identity is -.",
    "A protocol for secure email is called -.",
    "The tool for managing configurations is -.",
    "The framework for container management is -.",
    "A system that detects intrusions is -.",
    "The practice of tricking users into revealing secrets is -.",
    "A vulnerability before it is publicly known is called -.",
    "The method of encoding passwords irreversibly is -.",
    "A server that handles API requests is called -.",
    "The process of giving access permissions is called -.",
    "A security measure requiring multiple proofs is called -.",
    "The concept of least privilege means -.",
    "A type of malware that spreads without user action is -.",
    "The file that logs all system events is -.",
    "The standard format for security logs is -.",
    "The attack that intercepts network traffic is called -.",
    "A privilege escalation technique is called -.",
    "The process of moving through a network is called -.",
    "A type of malware that stays hidden is -.",
    "The technique of testing input boundaries is -.",
    "A supply chain attack targets -.",
    "The method of breaking encryption by trying all keys is -.",
    "An attack using poisoned data is called -.",
    "The security model that verifies everything is -.",
    "The practice of hunting for hidden threats is called -.",
    "A cloud security misconfiguration scanner is -.",
    "The technique of encoding data in DNS queries is -.",
    "A type of attack on blockchain is called -.",
    "The method of hiding malicious code in apps is called -.",
    "A defense strategy that isolates compromised systems is -.",
    "The process of collecting threat information is called -.",
    "An attack that targets domain name systems is -.",
    "A technique to evade antivirus detection is called -.",
    "The method of testing API security is -.",
    "A type of attack using fake wireless access points is -.",
    "The practice of rotating credentials automatically is -.",
    "A system that manages security events centrally is -.",
    "The technique of exploiting buffer boundaries is -.",
    "A method to securely store secrets is -.",
    "The framework for incident response is -.",
    "An attack using modified firmware is called -.",
]

# --- Level configuration ---
level_config = {
    1: {"algo": "MD5",    "name": "EASY",    "needed": 3, "color": "#00ff88", "bg": "#0a2e1a"},
    2: {"algo": "SHA1",   "name": "MEDIUM",  "needed": 5, "color": "#ffaa00", "bg": "#2e2a0a"},
    3: {"algo": "SHA256", "name": "HARD",    "needed": 7, "color": "#ff6600", "bg": "#2e1a0a"},
    4: {"algo": "SHA512", "name": "EXPERT",  "needed": 999, "color": "#ff2244", "bg": "#2e0a0a"},
}

hash_functions = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA512": hashlib.sha512
}

status_codes = [
    "200 OK", "400 Bad Request", "401 Unauthorized", "403 Forbidden",
    "404 Not Found", "500 Internal Server Error", "502 Bad Gateway",
    "503 Service Unavailable"
]

score = 0
total_rounds = 0
current_level = 1
level_correct = 0
current_algo = ""
current_hash = ""
current_sentence = ""
current_correct = ""


def hash_sentence(sentence, algo):
    return hash_functions[algo](sentence.encode()).hexdigest()


def get_available_indices():
    return [i for i in range(len(plain_sentences)) if _levels[i] == current_level]


def update_level_display():
    cfg = level_config[current_level]
    level_label.config(
        text=f"Level {current_level}: {cfg['name']} ({cfg['algo']})  |  "
             f"Progress: {level_correct}/{cfg['needed']} to advance",
        fg=cfg["color"]
    )
    # Color the level bar
    level_bar.config(bg=cfg["bg"])


def new_round():
    global current_algo, current_hash, current_sentence, current_correct

    available = get_available_indices()
    if not available:
        result_label.config(
            text="All levels completed! You've mastered all hash algorithms!",
            fg="#00ff88"
        )
        return

    idx = random.choice(available)
    current_sentence = plain_sentences[idx]
    current_algo = level_config[current_level]["algo"]
    current_correct = _da(_ea[_im[idx]])

    filled = current_sentence.replace("-", current_correct)
    current_hash = hash_sentence(filled, current_algo)

    masked = current_sentence.replace("-", "_____")

    algo_label.config(text=f"Hash Algorithm: {current_algo}")
    hash_label.config(text=f"{current_hash}")
    sentence_label.config(text=masked)
    result_label.config(text="")
    result_label.config(fg="#cccccc")
    hint_label.config(text="(Answer could be a number, word, or phrase!)", fg="#666666")
    entry.delete(0, tk.END)
    entry.focus_set()
    update_level_display()


def check():
    global score, total_rounds, current_level, level_correct
    user = entry.get().strip()
    if not user:
        result_label.config(text="Enter your answer to crack the hash!", fg="#ffaa00")
        return

    total_rounds += 1
    mode = random.choice(["check", "check", "ignore", "chaos"])

    if mode == "check":
        if user.lower() == current_correct.lower():
            score += 1
            level_correct += 1
            result_label.config(
                text=f"200 OK - CORRECT! Answer: {current_correct}",
                fg="#00ff88"
            )

            # Check level advancement
            cfg = level_config[current_level]
            if level_correct >= cfg["needed"] and current_level < 4:
                current_level += 1
                level_correct = 0
                new_cfg = level_config[current_level]
                result_label.config(
                    text=f"*** LEVEL UP! Now Level {current_level} - {new_cfg['name']} ({new_cfg['algo']}) ***",
                    fg="#ff44ff"
                )
        else:
            result_label.config(
                text="400 Bad Request - Hash mismatch! Try a different word or number.",
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
        noise = (user * random.randint(1, 3))[:60]
        result_label.config(
            text=f"{code} | Payload: {noise}",
            fg="#ff6600"
        )

    score_label.config(text=f"Score: {score}/{total_rounds}")
    update_level_display()


def show_hint():
    hint_window = tk.Toplevel(root)
    hint_window.title("Hint - Hash Cracker Challenge")
    hint_window.geometry("500x320")
    hint_window.configure(bg="#1a1a2e")
    hint_window.resizable(False, False)

    tk.Label(
        hint_window, text="HINT", font=("Consolas", 16, "bold"),
        fg="#00ff88", bg="#1a1a2e"
    ).pack(pady=(15, 10))

    hint_text = (
        "Each question has a UNIQUE answer!\n"
        "The answer could be:\n"
        "  - A NUMBER (e.g., '22', '443')\n"
        "  - A WORD (e.g., 'nmap', 'root')\n"
        "  - A PHRASE (e.g., 'zero day')\n\n"
        "Case does NOT matter (case-insensitive).\n\n"
        "For numbers, write a brute-force script:\n"
        "  for i in range(1, 10000):\n"
        "      h = hashlib.md5(f'Sentence {i} here.'.encode())\n"
        "          .hexdigest()\n"
        "      if h == target: print(f'CRACKED: {i}')\n\n"
        "For words, think about the topic of the sentence\n"
        "and try common security/tech terms!"
    )
    tk.Label(
        hint_window, text=hint_text, font=("Consolas", 9),
        fg="#cccccc", bg="#1a1a2e", justify="left"
    ).pack(pady=(0, 15))


def show_credits():
    cred_window = tk.Toplevel(root)
    cred_window.title("Credits - Hash Cracker Challenge")
    cred_window.geometry("400x180")
    cred_window.configure(bg="#1a1a2e")
    cred_window.resizable(False, False)

    tk.Label(
        cred_window, text="CREDITS", font=("Consolas", 16, "bold"),
        fg="#00ff88", bg="#1a1a2e"
    ).pack(pady=(15, 10))
    tk.Label(
        cred_window, text="Designed & Created by:", font=("Consolas", 10),
        fg="#888888", bg="#1a1a2e"
    ).pack(pady=(5, 2))
    tk.Label(
        cred_window, text="Cysec Don", font=("Consolas", 14, "bold"),
        fg="#00ccff", bg="#1a1a2e"
    ).pack(pady=(0, 5))
    tk.Label(
        cred_window, text="cysecdon@gmail.com", font=("Consolas", 10),
        fg="#ffaa00", bg="#1a1a2e"
    ).pack(pady=(0, 10))


# ═══════════════════════════════════════════════════════════════
#   GUI SETUP
# ═══════════════════════════════════════════════════════════════

root = tk.Tk()
root.title("Hash Cracker Challenge v2 - Designed by Cysec Don")
root.geometry("720x600")
root.configure(bg="#0f0f23")
root.resizable(False, False)

# --- Title bar ---
title_frame = tk.Frame(root, bg="#16213e")
title_frame.pack(fill="x")
tk.Label(
    title_frame, text="HASH CRACKER CHALLENGE v2",
    font=("Consolas", 18, "bold"), fg="#00ff88", bg="#16213e"
).pack(pady=(12, 2))
tk.Label(
    title_frame, text="104 Unique Challenges | Mixed Answers | Progressive Difficulty",
    font=("Consolas", 9, "bold"), fg="#00ccff", bg="#16213e"
).pack(pady=(0, 1))
tk.Label(
    title_frame, text="Designed by Cysec Don | cysecdon@gmail.com",
    font=("Consolas", 9), fg="#ffaa00", bg="#16213e"
).pack(pady=(0, 10))

# --- Level bar ---
level_bar = tk.Frame(root, bg="#0a2e1a")
level_bar.pack(fill="x")
level_label = tk.Label(
    level_bar, text="",
    font=("Consolas", 11, "bold"), fg="#00ff88", bg="#0a2e1a"
)
level_label.pack(pady=6)

# --- Score ---
score_label = tk.Label(
    root, text="Score: 0/0", font=("Consolas", 12, "bold"),
    fg="#00ff88", bg="#0f0f23"
)
score_label.pack(pady=(8, 6))

# --- Algorithm display ---
algo_label = tk.Label(
    root, text="", font=("Consolas", 12, "bold"),
    fg="#00ccff", bg="#0f0f23"
)
algo_label.pack(pady=4)

# --- Hash display ---
hash_frame = tk.Frame(root, bg="#1a1a2e", bd=2, relief="groove")
hash_frame.pack(padx=40, pady=6, fill="x")
tk.Label(
    hash_frame, text="Target Hash:", font=("Consolas", 9),
    fg="#888888", bg="#1a1a2e"
).pack(anchor="w", padx=8, pady=(6, 0))
hash_label = tk.Label(
    hash_frame, text="", font=("Consolas", 10),
    fg="#ffffff", bg="#1a1a2e", wraplength=620, justify="left"
)
hash_label.pack(anchor="w", padx=8, pady=(2, 8))

# --- Sentence display ---
tk.Label(
    root, text="Crack this sentence:", font=("Consolas", 9),
    fg="#888888", bg="#0f0f23"
).pack(pady=(8, 2))
sentence_label = tk.Label(
    root, text="", font=("Consolas", 15, "bold"),
    fg="#ffffff", bg="#0f0f23"
)
sentence_label.pack(pady=4)

hint_label = tk.Label(
    root, text="", font=("Consolas", 9),
    fg="#666666", bg="#0f0f23"
)
hint_label.pack(pady=(0, 4))

# --- Input ---
input_frame = tk.Frame(root, bg="#0f0f23")
input_frame.pack(pady=8)
entry = tk.Entry(
    input_frame, font=("Consolas", 14), width=25,
    bg="#1a1a2e", fg="#ffffff", insertbackground="#00ff88",
    bd=2, relief="groove"
)
entry.pack(side="left", padx=4)
entry.bind("<Return>", lambda e: check())

tk.Button(
    input_frame, text="SUBMIT", font=("Consolas", 11, "bold"),
    bg="#00ff88", fg="#0f0f23", activebackground="#00cc66",
    bd=0, padx=15, pady=4, command=check
).pack(side="left", padx=4)

# --- Result display ---
result_label = tk.Label(
    root, text="", font=("Consolas", 12),
    fg="#cccccc", bg="#0f0f23"
)
result_label.pack(pady=8)

# --- Buttons row ---
btn_frame = tk.Frame(root, bg="#0f0f23")
btn_frame.pack(pady=8)

tk.Button(
    btn_frame, text="NEXT ROUND", font=("Consolas", 10, "bold"),
    bg="#16213e", fg="#00ccff", activebackground="#1a3a5c",
    bd=0, padx=12, pady=4, command=new_round
).pack(side="left", padx=6)

tk.Button(
    btn_frame, text="HINT", font=("Consolas", 10, "bold"),
    bg="#16213e", fg="#ffaa00", activebackground="#1a3a5c",
    bd=0, padx=12, pady=4, command=show_hint
).pack(side="left", padx=6)

tk.Button(
    btn_frame, text="CREDITS", font=("Consolas", 10, "bold"),
    bg="#16213e", fg="#ff44ff", activebackground="#1a3a5c",
    bd=0, padx=12, pady=4, command=show_credits
).pack(side="left", padx=6)

# --- Level legend ---
legend_frame = tk.Frame(root, bg="#0f0f23")
legend_frame.pack(pady=(4, 0))
tk.Label(
    legend_frame, text="Lv1: MD5 (Easy)  →  Lv2: SHA1 (Medium)  →  Lv3: SHA256 (Hard)  →  Lv4: SHA512 (Expert)",
    font=("Consolas", 8), fg="#444444", bg="#0f0f23"
).pack()

# --- Footer ---
footer_frame = tk.Frame(root, bg="#0f0f23")
footer_frame.pack(side="bottom", pady=8)
tk.Label(
    footer_frame, text="Designed by Cysec Don",
    font=("Consolas", 8), fg="#555555", bg="#0f0f23"
).pack()
tk.Label(
    footer_frame, text="cysecdon@gmail.com | Learn Hashing Through Play",
    font=("Consolas", 8), fg="#555555", bg="#0f0f23"
).pack()

# --- Start first round ---
new_round()
root.mainloop()
