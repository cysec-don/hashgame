import hashlib
import random
import os
import sys

# ═══════════════════════════════════════════════════════════════
#   HASH CRACKER CHALLENGE v2 - CLI Edition
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
# Level 1: MD5 (Easy)    - need 3 correct to advance
# Level 2: SHA1 (Medium)  - need 5 correct to advance
# Level 3: SHA256 (Hard)  - need 7 correct to advance
# Level 4: SHA512 (Expert) - final level
level_config = {
    1: {"algo": "MD5",    "name": "EASY",    "needed": 3, "color": "\033[92m"},
    2: {"algo": "SHA1",   "name": "MEDIUM",  "needed": 5, "color": "\033[93m"},
    3: {"algo": "SHA256", "name": "HARD",    "needed": 7, "color": "\033[38;5;208m"},
    4: {"algo": "SHA512", "name": "EXPERT",  "needed": 999, "color": "\033[91m"},
}

hash_functions = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA512": hashlib.sha512
}

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
current_level = 1
level_correct = 0


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    cfg = level_config[current_level]
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
    print(f"  {C.WHT} DIFFICULTY:{C.RST} {cfg['color']}{C.BLD} Level {current_level} - {cfg['name']} ({cfg['algo']}){C.RST}")
    print(f"  {C.WHT} PROGRESS:{C.RST}  {C.YLW}{level_correct}{C.RST}/{cfg['needed']} correct to advance")
    print(f"  {C.WHT} SCORE:{C.RST}    {C.GRN}{score}{C.RST} total correct")
    print()
    print(f"  {C.DIM} OBJECTIVE: Crack the hash! Each question has a UNIQUE{C.RST}")
    print(f"  {C.DIM} answer — it could be a number, word, or phrase!{C.RST}")
    print(f"  {C.DIM} Answers get harder and hashes get longer as you level up.{C.RST}")
    print(f"  {C.CYN}{'─' * 62}{C.RST}")


def hash_sentence(sentence, algo):
    return hash_functions[algo](sentence.encode()).hexdigest()


def get_available_indices():
    """Get sentence indices matching current level."""
    return [i for i in range(len(plain_sentences)) if _levels[i] == current_level]


def generate_round():
    available = get_available_indices()
    idx = random.choice(available)
    sentence = plain_sentences[idx]
    algo = level_config[current_level]["algo"]
    correct_ans = _da(_ea[_im[idx]])
    filled = sentence.replace("-", correct_ans)
    h = hash_sentence(filled, algo)
    return sentence, algo, h, correct_ans


def display_round(sentence, algo, h):
    masked = sentence.replace("-", f"{C.RED}{C.BLD}_____{C.RST}")
    print()
    print(f"  {C.CYN}{C.BLD}Hash Type  :{C.RST} {C.WHT}{algo}{C.RST}")
    print(f"  {C.CYN}{C.BLD}Hash Value :{C.RST} {C.YLW}{h}{C.RST}")
    print()
    print(f"  {C.GRN}{C.BLD}Sentence   :{C.RST} {C.WHT}{C.BLD}{masked}{C.RST}")
    print(f"  {C.DIM}(Answer could be a number, word, or phrase!){C.RST}")
    print()


def check_answer(user_input, correct_ans):
    global score, total_rounds, current_level, level_correct
    total_rounds += 1

    mode = random.choice(["check", "check", "ignore", "chaos"])

    if mode == "check":
        # Case-insensitive comparison for word answers
        if user_input.lower().strip() == correct_ans.lower().strip():
            score += 1
            level_correct += 1
            print(f"\n  {C.GRN}{C.BLD}>> 200 OK - CORRECT!{C.RST} The hash matches!")
            print(f"  {C.GRN}   Answer: {correct_ans}{C.RST}")
            print(f"  {C.BLD}   Score: {score}/{total_rounds}{C.RST}")

            # Check level advancement
            cfg = level_config[current_level]
            if level_correct >= cfg["needed"] and current_level < 4:
                current_level += 1
                level_correct = 0
                new_cfg = level_config[current_level]
                print(f"\n  {C.BGMGN}{C.WHT}{C.BLD}  *** LEVEL UP! Now entering Level {current_level} - {new_cfg['name']} ({new_cfg['algo']}) ***{C.RST}")
                print(f"  {C.DIM}  Need {new_cfg['needed']} correct answers to advance.{C.RST}")
        else:
            print(f"\n  {C.RED}{C.BLD}>> 400 Bad Request - WRONG!{C.RST} Hash does not match.")
            print(f"  {C.RED}   Your input '{user_input}' did not produce the target hash.{C.RST}")
            print(f"  {C.YLW}   Remember: answer could be a word, phrase, or number!{C.RST}")
            print(f"  {C.BLD}   Score: {score}/{total_rounds}{C.RST}")

    elif mode == "ignore":
        code = random.choice(list(status_codes.values()))
        print(f"\n  {C.YLW}{C.BLD}>> {code}{C.RST}")
        print(f"  {C.DIM}   (Ambiguous server response - the hash doesn't lie!){C.RST}")
        print(f"  {C.BLD}   Score: {score}/{total_rounds}{C.RST}")

    else:
        code = random.choice(list(status_codes.values()))
        noise = (user_input * random.randint(1, 3))[:60]
        print(f"\n  {C.MGN}{C.BLD}>> {code} | Payload: {noise}{C.RST}")
        print(f"  {C.DIM}   (Network chaos detected - focus on the hash!){C.RST}")
        print(f"  {C.BLD}   Score: {score}/{total_rounds}{C.RST}")


def show_hint():
    print()
    print(f"  {C.YLW}{C.BLD}HINT:{C.RST}")
    print(f"  {C.WHT}  Each question has a UNIQUE answer!{C.RST}")
    print(f"  {C.WHT}  The answer could be a {C.GRN}number{C.RST}, {C.CYN}word{C.RST}, or {C.MGN}phrase{C.RST}!{C.RST}")
    print(f"  {C.WHT}  Case does not matter (answers are case-insensitive).{C.RST}")
    print()
    print(f"  {C.WHT}  Write a brute-force Python script:{C.RST}")
    print()
    print(f"  {C.CYN}  import hashlib{C.RST}")
    print(f"  {C.CYN}  target = '<paste the hash from the game>'{C.RST}")
    print(f"  {C.CYN}  for i in range(1, 10000):{C.RST}")
    print(f"  {C.CYN}      text = f'Sentence here {{i}} rest here.'{C.RST}")
    print(f"  {C.CYN}      h = hashlib.md5(text.encode()).hexdigest(){C.RST}")
    print(f"  {C.CYN}      if h == target: print(f'Found: {{i}}'){C.RST}")
    print()
    print(f"  {C.WHT}  For word answers, try common security words or tools!{C.RST}")
    print()


def main():
    global current_level, level_correct
    clear_screen()
    show_banner()

    while True:
        sentence, algo, h, correct_ans = generate_round()
        display_round(sentence, algo, h)

        print(f"  {C.DIM}Commands: your guess | 'hint' | 'level' | 'quit'{C.RST}")
        print()
        user_input = input(f"  {C.GRN}{C.BLD}Your guess:{C.RST} ").strip()

        if user_input.lower() in ('quit', 'exit', 'q'):
            clear_screen()
            print()
            print(f"  {C.BGBLK}{C.GRN}{C.BLD}{'─' * 58}{C.RST}")
            print(f"  {C.BGBLK}{C.GRN}{C.BLD}  FINAL SCORE: {score}/{total_rounds}{C.RST}")
            print(f"  {C.BGBLK}{C.GRN}{C.BLD}  Level reached: {current_level} - {level_config[current_level]['name']}{C.RST}")
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

        if user_input.lower() == 'level':
            cfg = level_config[current_level]
            print(f"\n  {C.CYN}{C.BLD}  Current Level: {current_level} - {cfg['name']} ({cfg['algo']}){C.RST}")
            print(f"  {C.WHT}  Progress: {level_correct}/{cfg['needed']} correct to advance{C.RST}")
            print(f"  {C.DIM}  Level 1: MD5 (Easy) -> Level 2: SHA1 (Medium) -> Level 3: SHA256 (Hard) -> Level 4: SHA512 (Expert){C.RST}")
            input(f"\n  {C.DIM}Press Enter to continue...{C.RST} ")
            clear_screen()
            show_banner()
            continue

        if not user_input:
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
