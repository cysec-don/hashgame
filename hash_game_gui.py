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


# --- Encoded answers (XOR'd, stored as hex) ---
_ea = [
    "06030706", "04050701", "02030107", "03010503", "02060400",
    "0306000e", "040e0307", "01030f0e", "0f040505", "0107050e",
    "00070e03", "03040100", "0e050601", "02030205", "020f01",
    "020e0206", "02050206", "03070200", "020600", "03000207",
    "06060f01", "00060304", "050e0507", "00050e00", "04000005",
    "030e020e", "040502", "04070401", "04000f07", "04070e03",
    "060e0e01", "06000004", "03020405", "03010501", "03060101",
    "03000400", "0e060707", "00010001", "03050400", "02040300",
    "05010f07", "040e0600", "04010501", "01050e03", "04060104",
    "01030705", "0001060f", "0e070701", "000f0001", "03070500",
    "03060103", "05000403", "04050407", "05050103", "05070100",
    "000702", "00060e06", "02070301", "040603", "00020e06",
    "04030103", "06010703", "03050107", "00020607", "06050305",
    "0f03000e", "020f000f", "05040301", "020e0303", "020f0f06",
    "0e060400", "04050f00", "02020f05", "00050105", "020e0502",
    "04030104", "01010004", "02040106", "0f020e07", "0f030e0e",
    "02060604", "0f030f0f", "06000505", "0f040303", "06030f",
    "0e050504", "02070704", "01000706", "05070606", "03060004",
    "020f020f", "00010707", "04070704", "00000e00", "000106",
    "0f030500", "03070f06", "05040701", "06010205", "0602030f",
    "0f040606", "06050f0f", "0f050104", "06070104",
]

# --- Scrambled index map: sentence[i] uses _ea[_im[i]] ---
_im = [
    2, 38, 53, 21, 77, 60, 16, 22, 98, 30,
    63, 37, 5, 9, 55, 13, 34, 40, 59, 7,
    66, 97, 88, 43, 39, 74, 76, 70, 75, 52,
    72, 42, 64, 57, 81, 8, 27, 54, 17, 69,
    26, 87, 12, 0, 29, 6, 1, 92, 67, 95,
    71, 79, 46, 24, 68, 35, 32, 73, 47, 89,
    102, 84, 23, 91, 51, 96, 90, 85, 18, 50,
    48, 19, 4, 11, 80, 58, 44, 33, 99, 3,
    78, 28, 94, 15, 100, 61, 65, 25, 56, 10,
    41, 83, 86, 36, 31, 20, 93, 49, 62, 14,
    103, 101, 82, 45,
]

# --- 104 unique cybersecurity challenge sentences ---
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
    "Backup failed after - tries.",
    "WAF filtered - malicious payloads.",
    "Phishing email sent to - recipients.",
    "Brute force attack lasted - minutes.",
    "Encryption key rotated - times this month.",
    "DNS query resolved - domains.",
    "SSL certificate expires in - days.",
    "Proxy server handled - requests.",
    "Ransomware encrypted - files.",
    "Honeypot captured - attack attempts.",
    "Zero-day exploit affected - systems.",
    "Penetration test found - flaws.",
    "Load balancer distributed - connections.",
    "Cache hit rate was - percent.",
    "Packet loss reached - on the network.",
    "Latency spike lasted - milliseconds.",
    "Bandwidth usage peaked at - Mbps.",
    "Audit log stored - entries.",
    "Thread pool had - active workers.",
    "Webhook fired - times today.",
    "CI pipeline ran - builds.",
    "Container image is - MB in size.",
    "Deployment rollback happened - times.",
    "Swagger endpoint documented - routes.",
    "OAuth token refreshed - times.",
    "Session timeout set to - seconds.",
    "Rate limiter allows - requests per minute.",
    "Redis cache stored - keys.",
    "Kafka topic received - messages.",
    "Grafana dashboard tracks - metrics.",
    "Jenkins job failed - times this week.",
    "Docker container restarted - times.",
    "Kubernetes pod had - replicas.",
    "Lambda function ran for - ms.",
    "GraphQL query returned - fields.",
    "S3 bucket contains - objects.",
    "CDN edge served - assets.",
    "DNS lookup took - milliseconds.",
    "TCP handshake completed in - ms.",
    "TLS negotiation used - cipher suites.",
    "XSS payload tested - vectors.",
    "SQL injection attempted - times.",
    "CSRF token rotated - times.",
    "JWT token expired after - seconds.",
    "RBAC policy has - permission rules.",
    "MFA required for - admin accounts.",
    "Password policy enforced - complexity rules.",
    "Security header set - directives.",
    "Cookie flagged - security issues.",
    "Content Security Policy blocked - violations.",
    "CORS preflight rejected - origins.",
    "Subdomain takeover found - targets.",
    "Open port scan revealed - ports.",
    "Service enumeration found - services.",
    "Banner grabbing identified - servers.",
    "Directory bruteforce found - folders.",
    "Parameter tampering tested - variables.",
    "Race condition exploited - times.",
    "Buffer overflow triggered - crashes.",
    "Privilege escalation gained - levels.",
    "Lateral movement compromised - machines.",
    "Data exfiltration leaked - records.",
    "Incident response took - hours.",
    "Forensic analysis processed - artifacts.",
    "Threat intelligence found - indicators.",
    "Vulnerability scan ran for - minutes.",
    "Compliance audit checked - controls.",
    "Risk assessment scored - threats.",
    "Security training completed by - employees.",
    "Phishing simulation tricked - users.",
    "Patch management fixed - issues.",
    "Change management reviewed - deployments.",
    "Endpoint protection blocked - threats.",
    "Network segmentation created - zones.",
    "Log analysis flagged - events.",
    "SIEM collected - events per second.",
    "SOAR playbook automated - responses.",
    "Threat hunting found - suspicious activities.",
    "User behavior analytics detected - anomalies.",
    "Data loss prevention stopped - incidents.",
    "Cloud security posture found - misconfigs.",
    "Identity governance reviewed - accounts.",
    "Secrets scan found - exposed credentials.",
    "Container security scanned - images.",
    "API security tested - endpoints.",
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
    hint_window.geometry("480x300")
    hint_window.configure(bg="#1a1a2e")
    hint_window.resizable(False, False)

    tk.Label(
        hint_window,
        text="HINT",
        font=("Consolas", 16, "bold"),
        fg="#00ff88", bg="#1a1a2e"
    ).pack(pady=(15, 10))

    hint_text = (
        "Each question has a UNIQUE number answer!\n"
        "There are 104 different challenges.\n\n"
        "Write a Python script that hashes the sentence\n"
        "with different numbers and compares the result\n"
        "to the target hash.\n\n"
        "Example:\n"
        "import hashlib\n"
        "target = '<paste hash here>'\n"
        "for i in range(1, 10000):\n"
        "    h = hashlib.md5(\n"
        "        f'Sentence {i} here.'.encode()\n"
        "    ).hexdigest()\n"
        "    if h == target:\n"
        "        print(f'CRACKED: {i}')\n"
        "        break"
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
    text="104 Unique Challenges | Designed by Cysec Don",
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
