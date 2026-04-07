import hashlib
import random
import os
import sys

# ═══════════════════════════════════════════════════════════════
#   HASH CRACKER CHALLENGE - CLI Edition
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

# --- ANSI color codes ---
class C:
    RST = "\033[0m"
    BLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    BLU = "\033[94m"
    MGN = "\033[95m"
    CYN = "\033[96m"
    WHT = "\033[97m"
    BGBLK = "\033[40m"
    BGRED = "\033[41m"
    BGGRN = "\033[42m"
    BGYLW = "\033[43m"
    BGBLU = "\033[44m"
    BGMGN = "\033[45m"
    BGCYN = "\033[46m"

score = 0
total_rounds = 0


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    print()
    print(f"""{C.BGBLU}{C.WHT}{C.BLD}{'─' * 62}{C.RST}""")
    print(f"{C.BGBLU}{C.WHT}{C.BLD}  ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗     {C.RST}")
    print(f"{C.BGBLU}{C.WHT}{C.BLD}  ██║ ██╔╝██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    {C.RST}")
    print(f"{C.BGBLU}{C.WHT}{C.BLD}  █████╔╝ ███████║██║     █████╔╝ █████╗  ██║  ██║    {C.RST}")
    print(f"{C.BGBLU}{C.WHT}{C.BLD}  ██╔═██╗ ██╔══██║██║     ██╔═██╗ ██╔══╝  ██║  ██║    {C.RST}")
    print(f"{C.BGBLU}{C.WHT}{C.BLD}  ██║  ██╗██║  ██║╚██████╗██║  ██╗███████╗██████╔╝    {C.RST}")
    print(f"{C.BGBLU}{C.WHT}{C.BLD}  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝     {C.RST}")
    print(f"{C.BGBLU}{C.WHT}{C.BLD}{'─' * 62}{C.RST}")
    print()
    print(f"  {C.BGMGN}{C.WHT}{C.BLD}  █▀▀█ █▀▀█ █▀▀▄ █▀▀█   █▀▀█ █  █ █▀▀▄ █▀▀  {C.RST}")
    print(f"  {C.BGMGN}{C.WHT}{C.BLD}  █  █ █  █ █  █ █▄▄▀   █▄▄█ █  █ █  █ █   {C.RST}")
    print(f"  {C.BGMGN}{C.WHT}{C.BLD}  █▄▄█ ▀▀▀▀ ▀  ▀ ▀ ▀▀   █  █ ▀▀▀▀ ▀  ▀ ▀▀▀  {C.RST}")
    print(f"  {C.BGMGN}{C.WHT}{C.BLD}{'─' * 62}{C.RST}")
    print()
    print(f"  {C.GRN}{C.BLD}Designed & Created by:{C.RST} {C.YLW}{C.BLD}Cysec Don{C.RST}")
    print(f"  {C.GRN}{C.BLD}Contact:{C.RST} {C.CYN}{C.BLD}cysecdon@gmail.com{C.RST}")
    print()
    print(f"  {C.CYN}{'─' * 62}{C.RST}")
    print(f"  {C.WHT} OBJECTIVE:{C.RST} {C.DIM}Crack the hash! Find the unique number{C.RST}")
    print(f"  {C.DIM}  that completes each sentence and produces the hash.{C.RST}")
    print()
    print(f"  {C.WHT} TIP:{C.RST} {C.DIM}Each question has a DIFFERENT answer!{C.RST}")
    print(f"  {C.DIM}  Use Python's hashlib to brute-force each one.{C.RST}")
    print(f"  {C.DIM}  Example: hashlib.md5(b'Sentence with number').hexdigest(){C.RST}")
    print(f"  {C.CYN}{'─' * 62}{C.RST}")


def hash_sentence(sentence, algo):
    return hash_functions[algo](sentence.encode()).hexdigest()


def generate_round():
    idx = random.randint(0, len(plain_sentences) - 1)
    sentence = plain_sentences[idx]
    algo = random.choice(list(hash_functions.keys()))
    correct_ans = _da(_ea[_im[idx]])
    filled = sentence.replace("-", str(correct_ans))
    h = hash_sentence(filled, algo)
    return sentence, algo, h, correct_ans


def display_round(sentence, algo, h):
    masked = sentence.replace("-", f"{C.RED}{C.BLD}_____{C.RST}")
    print()
    print(f"  {C.CYN}{C.BLD}Hash Type  :{C.RST} {C.WHT}{algo}{C.RST}")
    print(f"  {C.CYN}{C.BLD}Hash Value :{C.RST} {C.YLW}{h}{C.RST}")
    print()
    print(f"  {C.GRN}{C.BLD}Sentence   :{C.RST} {C.WHT}{C.BLD}{masked}{C.RST}")
    print()


def check_answer(user_input, correct_ans):
    global score, total_rounds
    total_rounds += 1

    mode = random.choice(["check", "check", "ignore", "chaos"])

    if mode == "check":
        if user_input == str(correct_ans):
            score += 1
            print(f"\n  {C.GRN}{C.BLD}>> 200 OK - CORRECT!{C.RST} The hash matches!")
            print(f"  {C.GRN}   Answer: {correct_ans}{C.RST}")
            print(f"  {C.BLD}   Score: {score}/{total_rounds}{C.RST}")
        else:
            print(f"\n  {C.RED}{C.BLD}>> 400 Bad Request - WRONG!{C.RST} Hash does not match.")
            print(f"  {C.RED}   Your input '{user_input}' did not produce the target hash.{C.RST}")
            print(f"  {C.YLW}   Try hashing different numbers!{C.RST}")
            print(f"  {C.BLD}   Score: {score}/{total_rounds}{C.RST}")

    elif mode == "ignore":
        code = random.choice(list(status_codes.values()))
        print(f"\n  {C.YLW}{C.BLD}>> {code}{C.RST}")
        print(f"  {C.DIM}   (Ambiguous server response - the hash doesn't lie!){C.RST}")
        print(f"  {C.BLD}   Score: {score}/{total_rounds}{C.RST}")

    else:
        code = random.choice(list(status_codes.values()))
        noise = user_input * random.randint(1, 3)
        print(f"\n  {C.MGN}{C.BLD}>> {code} | Payload: {noise}{C.RST}")
        print(f"  {C.DIM}   (Network chaos detected - focus on the hash!){C.RST}")
        print(f"  {C.BLD}   Score: {score}/{total_rounds}{C.RST}")


def show_hint():
    print()
    print(f"  {C.YLW}{C.BLD}HINT:{C.RST}")
    print(f"  {C.WHT}  Each question has a UNIQUE number answer.{C.RST}")
    print(f"  {C.WHT}  Write a Python script to brute-force it:{C.RST}")
    print()
    print(f"  {C.CYN}  import hashlib{C.RST}")
    print(f"  {C.CYN}  for i in range(1, 10000):{C.RST}")
    print(f"  {C.CYN}      text = f'I just paid {{i}} naira for coffee.'{C.RST}")
    print(f"  {C.CYN}      h = hashlib.md5(text.encode()).hexdigest(){C.RST}")
    print(f"  {C.CYN}      if h == TARGET_HASH: print(f'Found: {{i}}'){C.RST}")
    print()


def main():
    clear_screen()
    show_banner()

    while True:
        sentence, algo, h, correct_ans = generate_round()
        display_round(sentence, algo, h)

        print(f"  {C.DIM}Commands: number to guess | 'hint' | 'quit'{C.RST}")
        print()
        user_input = input(f"  {C.GRN}{C.BLD}Your guess:{C.RST} ").strip()

        if user_input.lower() in ('quit', 'exit', 'q'):
            clear_screen()
            show_banner()
            print()
            print(f"  {C.BGBLK}{C.GRN}{C.BLD}{'─' * 58}{C.RST}")
            print(f"  {C.BGBLK}{C.GRN}{C.BLD}  FINAL SCORE: {score}/{total_rounds}{C.RST}")
            print(f"  {C.BGBLK}{C.GRN}{C.BLD}  Thanks for playing!{C.RST}")
            print(f"  {C.BGBLK}{C.YLW}{C.BLD}  Designed by Cysec Don | cysecdon@gmail.com{C.RST}")
            print(f"  {C.BGBLK}{C.GRN}{C.BLD}{'─' * 58}{C.RST}")
            print()
            break

        if user_input.lower() == 'hint':
            show_hint()
            input(f"\n  {C.DIM}Press Enter to continue...{C.RST} ")
            clear_screen()
            show_banner()
            continue

        if user_input.lower() == 'new':
            continue

        check_answer(user_input, correct_ans)
        input(f"\n  {C.DIM}Press Enter for next round...{C.RST} ")
        clear_screen()
        show_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YLW}Game interrupted. Goodbye!{C.RST}")
        print(f"  {C.GRN}Designed by Cysec Don | cysecdon@gmail.com{C.RST}\n")
        sys.exit(0)
