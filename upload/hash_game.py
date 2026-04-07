import tkinter as tk
import hashlib
import random

print("Designed by Cysec Don")

# 20 sentences
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

correct = "500"

# Hash functions
hash_functions = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA512": hashlib.sha512
}

status_codes = [
    "200 OK ✅",
    "400 Bad Request ❌",
    "401 Unauthorized 🔐",
    "403 Forbidden 🚫",
    "404 Not Found 🔍",
    "500 Internal Server Error 💥",
    "502 Bad Gateway 🌐",
    "503 Service Unavailable ⚠️"
]

def hash_sentence(sentence, algo):
    return hash_functions[algo](sentence.encode()).hexdigest()

def new_round():
    global current_sentence, current_hash, current_algo
    
    current_sentence = random.choice(plain_sentences)
    current_algo = random.choice(list(hash_functions.keys()))
    current_hash = hash_sentence(current_sentence, current_algo)

    algo_label.config(text=f"Hash Type: {current_algo}")
    hash_label.config(text=f"Hash: {current_hash}")
    sentence_label.config(text=current_sentence.replace("-", "_____"))
    result_label.config(text="")
    entry.delete(0, tk.END)

def check():
    user = entry.get()
    mode = random.choice(["check", "ignore", "chaos"])

    if mode == "check":
        if user == correct:
            result_label.config(text="200 OK ✅")
        else:
            result_label.config(text="400 Bad Request ❌")

    elif mode == "ignore":
        result_label.config(text=random.choice(status_codes))

    else:
        code = random.choice(status_codes)
        result_label.config(
            text=f"{code} | Payload: {user * random.randint(1,3)}"
        )

# GUI setup
root = tk.Tk()
root.title("Fuzzing Game (Multi-Hash) - Designed by Cysec Don")
root.geometry("600x300")

algo_label = tk.Label(root, text="", font=("Arial", 10))
algo_label.pack(pady=5)

hash_label = tk.Label(root, text="", font=("Arial", 9), wraplength=550)
hash_label.pack(pady=5)

sentence_label = tk.Label(root, text="", font=("Arial", 14))
sentence_label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=5)

tk.Button(root, text="Submit", command=check).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

tk.Button(root, text="Next", command=new_round).pack(pady=5)

footer = tk.Label(root, text="Designed by Cysec Don", font=("Arial", 8))
footer.pack(side="bottom", pady=5)

new_round()
root.mainloop()