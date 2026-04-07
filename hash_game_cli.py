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
    print(f"  {C.WHT} NOTE:{C.RST} {C.DIM}There are {C.YLW}{C.BLD}104 unique challenges{C.RST}{C.DIM}, each with{C.RST}")
    print(f"  {C.DIM}  a {C.RED}{C.BLD}DIFFERENT{C.RST}{C.DIM} answer. Every question has its own number!{C.RST}")
    print()
    print(f"  {C.WHT} TIP:{C.RST} {C.DIM}Use Python's hashlib to brute-force each one.{C.RST}")
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
    print(f"  {C.CYN}  target = '<paste the hash from the game>'{C.RST}")
    print(f"  {C.CYN}  for i in range(1, 10000):{C.RST}")
    print(f"  {C.CYN}      text = f'Sentence here {{i}} rest here.'{C.RST}")
    print(f"  {C.CYN}      h = hashlib.md5(text.encode()).hexdigest(){C.RST}")
    print(f"  {C.CYN}      if h == target: print(f'Found: {{i}}'){C.RST}")
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
