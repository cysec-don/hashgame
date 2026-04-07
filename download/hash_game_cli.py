import hashlib
import random
import base64
import os
import sys

# ═══════════════════════════════════════════════════════════════
#   HASH CRACKER CHALLENGE - CLI Edition
#   Designed by Cysec Don
# ═══════════════════════════════════════════════════════════════

# --- Hidden answer (encoded, not readable in source) ---
_a = "NT" + "A" + "w"
_b = "M" + "j" + "U" + "w"  # decoy variable
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
status_codes = {
    "200": "200 OK",
    "400": "400 Bad Request",
    "401": "401 Unauthorized",
    "403": "403 Forbidden",
    "404": "404 Not Found",
    "500": "500 Internal Server Error",
    "502": "502 Bad Gateway",
    "503": "503 Service Unavailable"
}

score = 0
total_rounds = 0


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    print()
    print("=" * 60)
    print("     HASH CRACKER CHALLENGE - CLI Edition")
    print("     Designed by Cysec Don")
    print("=" * 60)
    print()
    print("  OBJECTIVE: Crack the hash! Find the number that")
    print("  completes the sentence and matches the given hash.")
    print()
    print("  TIP: Use Python's hashlib to brute-force the answer.")
    print("  Example: hashlib.md5(b'I just paid 100 naira for coffee.').hexdigest()")
    print()
    print("=" * 60)


def hash_sentence(sentence, algo):
    return hash_functions[algo](sentence.encode()).hexdigest()


def generate_round():
    sentence = random.choice(plain_sentences)
    algo = random.choice(list(hash_functions.keys()))
    filled = sentence.replace("-", correct_value)
    h = hash_sentence(filled, algo)
    return sentence, algo, h


def display_round(sentence, algo, h):
    masked = sentence.replace("-", "_____")
    print()
    print(f"  Hash Type  : {algo}")
    print(f"  Hash Value : {h}")
    print()
    print(f"  Sentence   : {masked}")
    print()


def check_answer(user_input):
    global score, total_rounds
    total_rounds += 1

    # The game uses a fuzzy check - sometimes accurate, sometimes chaotic
    mode = random.choice(["check", "check", "ignore", "chaos"])

    if mode == "check":
        if user_input == correct_value:
            score += 1
            print(f"\n  >> 200 OK - CORRECT! The hash matches!")
            print(f"     Answer: {correct_value}")
            print(f"     Score: {score}/{total_rounds}")
        else:
            print(f"\n  >> 400 Bad Request - WRONG! The hash does not match.")
            print(f"     Your input: '{user_input}' did not produce the target hash.")
            print(f"     Try hashing different numbers to find the match!")
            print(f"     Score: {score}/{total_rounds}")

    elif mode == "ignore":
        code = random.choice(list(status_codes.values()))
        print(f"\n  >> {code}")
        print(f"     (Server gave an ambiguous response - the hash doesn't lie!)")
        print(f"     Score: {score}/{total_rounds}")

    else:  # chaos
        code = random.choice(list(status_codes.values()))
        noise = user_input * random.randint(1, 3)
        print(f"\n  >> {code} | Payload: {noise}")
        print(f"     (Network chaos detected - focus on the hash!)")
        print(f"     Score: {score}/{total_rounds}")


def show_hint():
    print()
    print("  HINT: The answer is an integer. Try writing a Python script")
    print("  that hashes the sentence with different numbers until the")
    print("  hash matches the target. That's how real hash cracking works!")
    print()


def main():
    clear_screen()
    show_banner()

    while True:
        sentence, algo, h = generate_round()
        display_round(sentence, algo, h)

        print("  Commands: type a number to guess | 'hint' for help | 'quit' to exit")
        print()
        user_input = input("  Your guess: ").strip()

        if user_input.lower() in ('quit', 'exit', 'q'):
            clear_screen()
            print()
            print("=" * 60)
            print(f"  FINAL SCORE: {score}/{total_rounds}")
            print("  Thanks for playing!")
            print("  Designed by Cysec Don")
            print("=" * 60)
            print()
            break

        if user_input.lower() == 'hint':
            show_hint()
            input("  Press Enter to continue...")
            clear_screen()
            show_banner()
            continue

        if user_input.lower() == 'new':
            continue

        check_answer(user_input)
        input("\n  Press Enter for next round...")
        clear_screen()
        show_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!")
        print("  Designed by Cysec Don\n")
        sys.exit(0)
