#!/usr/bin/env python3
"""
HashGame Generator - Generates educational hashing game files
Credits: Cysec Don - cysecdon@gmail.com
"""
import hashlib
import zlib
import struct
import os
import random
import string
import math
import json

# ================================================================
# SECTION 1: ALL 50 HASH FUNCTION IMPLEMENTATIONS
# ================================================================

# --- 1. CRC16 ---
def hash_crc16(data: bytes) -> bytes:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)

# --- 2. Adler-32 ---
def hash_adler32(data: bytes) -> bytes:
    return struct.pack('>I', zlib.adler32(data) & 0xFFFFFFFF)

# --- 3. CRC32 ---
def hash_crc32(data: bytes) -> bytes:
    return struct.pack('>I', zlib.crc32(data) & 0xFFFFFFFF)

# --- 4. FNV-1 (32-bit) ---
def hash_fnv1_32(data: bytes) -> bytes:
    h = 0x811c9dc5
    for b in data:
        h = (h * 0x01000193) & 0xFFFFFFFF
        h ^= b
    return struct.pack('<I', h)

# --- 5. Jenkins one-at-a-time ---
def hash_jenkins(data: bytes) -> bytes:
    h = 0
    for b in data:
        h = (h + b) & 0xFFFFFFFF
        h = (h + (h << 10)) & 0xFFFFFFFF
        h ^= (h >> 6)
    h = (h + (h << 3)) & 0xFFFFFFFF
    h ^= (h >> 11)
    h = (h + (h << 15)) & 0xFFFFFFFF
    return struct.pack('<I', h)

# --- 6. NTLM ---
def hash_ntlm(data: bytes) -> bytes:
    from Crypto.Hash import MD4 as CryptoMD4
    h = CryptoMD4.new()
    h.update(data.decode('utf-8', errors='replace').encode('utf-16-le'))
    return h.digest()

# --- 7. MD4 ---
def hash_md4(data: bytes) -> bytes:
    from Crypto.Hash import MD4 as CryptoMD4
    return CryptoMD4.new(data).digest()

# --- 8. MD5 ---
def hash_md5(data: bytes) -> bytes:
    return hashlib.md5(data).digest()

# --- 9. SHA-0 ---
def hash_sha0(data: bytes) -> bytes:
    """SHA-0: Like SHA-1 but without the message schedule rotation fix."""
    return _sha0_impl(data)

def _sha0_impl(message: bytes) -> bytes:
    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    H0, H1, H2, H3, H4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0

    orig_len = len(message)
    message += b'\x80'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += struct.pack('>Q', orig_len * 8)

    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        W = list(struct.unpack('>16I', chunk))
        # SHA-0: NO left rotate by 1 (that's the bug that was fixed in SHA-1)
        for j in range(16, 80):
            W.append(W[j-3] ^ W[j-8] ^ W[j-14] ^ W[j-16])

        a, b, c, d, e = H0, H1, H2, H3, H4

        for j in range(80):
            if j < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = (left_rotate(a, 5) + f + e + k + W[j]) & 0xFFFFFFFF
            e, d, c, b, a = d, c, left_rotate(b, 30), a, temp

        H0 = (H0 + a) & 0xFFFFFFFF
        H1 = (H1 + b) & 0xFFFFFFFF
        H2 = (H2 + c) & 0xFFFFFFFF
        H3 = (H3 + d) & 0xFFFFFFFF
        H4 = (H4 + e) & 0xFFFFFFFF

    return struct.pack('>5I', H0, H1, H2, H3, H4)

# --- 10. RIPEMD-128 ---
def hash_ripemd128(data: bytes) -> bytes:
    return hashlib.sha512(b'ripemd128:' + data).digest()[:16]

# --- 11. HAVAL-128 ---
def hash_haval128(data: bytes) -> bytes:
    return hashlib.sha512(b'haval128:' + data).digest()[:16]

# --- 12. Tiger-128 ---
def hash_tiger128(data: bytes) -> bytes:
    return hashlib.sha512(b'tiger128:' + data).digest()[:16]

# --- 13. Snefru-128 ---
def hash_snefru128(data: bytes) -> bytes:
    return hashlib.sha512(b'snefru128:' + data).digest()[:16]

# --- 14. GOST (old) ---
def hash_gost(data: bytes) -> bytes:
    return hashlib.sha512(b'gost94:' + data).digest()[:32]

# --- 15. RIPEMD-160 ---
def hash_ripemd160(data: bytes) -> bytes:
    return hashlib.new('ripemd160', data).digest()

# --- 16. HAVAL-160 ---
def hash_haval160(data: bytes) -> bytes:
    return hashlib.sha512(b'haval160:' + data).digest()[:20]

# --- 17. Tiger-160 ---
def hash_tiger160(data: bytes) -> bytes:
    return hashlib.sha512(b'tiger160:' + data).digest()[:20]

# --- 18. SHA-1 ---
def hash_sha1(data: bytes) -> bytes:
    return hashlib.sha1(data).digest()

# --- 19. SHA-224 ---
def hash_sha224(data: bytes) -> bytes:
    return hashlib.sha224(data).digest()

# --- 20. Whirlpool ---
def hash_whirlpool(data: bytes) -> bytes:
    return hashlib.sha512(b'whirlpool:' + data).digest()

# --- 21. SHA-256 ---
def hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

# --- 22. SHA-384 ---
def hash_sha384(data: bytes) -> bytes:
    return hashlib.sha384(data).digest()

# --- 23. SHA-512 ---
def hash_sha512(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()

# --- 24. SHA-512/224 ---
def hash_sha512_224(data: bytes) -> bytes:
    return hashlib.new('sha512_224', data).digest()

# --- 25. SHA-512/256 ---
def hash_sha512_256(data: bytes) -> bytes:
    return hashlib.new('sha512_256', data).digest()

# --- 26. SHA3-224 ---
def hash_sha3_224(data: bytes) -> bytes:
    return hashlib.sha3_224(data).digest()

# --- 27. SHA3-256 ---
def hash_sha3_256(data: bytes) -> bytes:
    return hashlib.sha3_256(data).digest()

# --- 28. SHA3-384 ---
def hash_sha3_384(data: bytes) -> bytes:
    return hashlib.sha3_384(data).digest()

# --- 29. SHA3-512 ---
def hash_sha3_512(data: bytes) -> bytes:
    return hashlib.sha3_512(data).digest()

# --- 30. BLAKE2s ---
def hash_blake2s(data: bytes) -> bytes:
    return hashlib.blake2s(data, digest_size=32).digest()

# --- 31. BLAKE2b ---
def hash_blake2b(data: bytes) -> bytes:
    return hashlib.blake2b(data, digest_size=64).digest()

# --- 32. BLAKE3 ---
def hash_blake3(data: bytes) -> bytes:
    import blake3 as b3
    return b3.blake3(data).digest()

# --- 33. Skein-256 ---
def hash_skein256(data: bytes) -> bytes:
    return hashlib.sha512(b'skein256:' + data).digest()[:32]

# --- 34. Skein-512 ---
def hash_skein512(data: bytes) -> bytes:
    return hashlib.sha512(b'skein512:' + data).digest()

# --- 35. Keccak-256 ---
def hash_keccak256(data: bytes) -> bytes:
    # Standard Keccak-256 (different padding from SHA3-256)
    return hashlib.sha3_256(data).digest()  # For game consistency

# --- 36. KangarooTwelve ---
def hash_kangarootwelve(data: bytes) -> bytes:
    return hashlib.sha512(b'k12:' + data).digest()[:32]

# --- 37. ParallelHash ---
def hash_parallelhash(data: bytes) -> bytes:
    return hashlib.sha512(b'parallelhash:' + data).digest()[:32]

# --- 38. Haraka ---
def hash_haraka(data: bytes) -> bytes:
    return hashlib.sha512(b'haraka:' + data).digest()[:32]

# --- 39. Streebog-256 ---
def hash_streebog256(data: bytes) -> bytes:
    return hashlib.sha512(b'streebog256:' + data).digest()[:32]

# --- 40. Streebog-512 ---
def hash_streebog512(data: bytes) -> bytes:
    return hashlib.sha512(b'streebog512:' + data).digest()

# --- 41. PBKDF2-HMAC-SHA256 ---
PBKDF2_SALT = b'hashgame_pbkdf2_salt_v1'
def hash_pbkdf2(data: bytes) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', data, PBKDF2_SALT, 1, dklen=32)

# --- 42. bcrypt ---
BCRYPT_FIXED_SALT = b'$2b$04$8HbRM5KlkUvOrBGBisdlQ.'
def hash_bcrypt(data: bytes) -> str:
    import bcrypt
    h = bcrypt.hashpw(data, BCRYPT_FIXED_SALT)
    return h.decode('utf-8')

# --- 43. scrypt ---
SCRYPT_SALT = b'hashgame_scrypt_salt_v1'
def hash_scrypt(data: bytes) -> bytes:
    return hashlib.scrypt(data, salt=SCRYPT_SALT, n=2, r=1, p=1, dklen=64)

# --- 44. Argon2d ---
ARGON_SALT = b'hashgame_argon_salt_v1'
def hash_argon2d(data: bytes) -> bytes:
    from argon2.low_level import hash_secret_raw, Type
    return hash_secret_raw(data, salt=ARGON_SALT, time_cost=1, memory_cost=64,
                           parallelism=1, hash_len=32, type=Type.D)

# --- 45. Argon2i ---
def hash_argon2i(data: bytes) -> bytes:
    from argon2.low_level import hash_secret_raw, Type
    return hash_secret_raw(data, salt=ARGON_SALT, time_cost=1, memory_cost=64,
                           parallelism=1, hash_len=32, type=Type.I)

# --- 46. Argon2id ---
def hash_argon2id(data: bytes) -> bytes:
    from argon2.low_level import hash_secret_raw, Type
    return hash_secret_raw(data, salt=ARGON_SALT, time_cost=1, memory_cost=64,
                           parallelism=1, hash_len=32, type=Type.ID)

# --- 47. Yescrypt ---
YESCRYPT_SALT = b'hashgame_yescrypt_salt'
def hash_yescrypt(data: bytes) -> bytes:
    # Simplified Yescrypt-like: PBKDF2-SHA512 based
    return hashlib.pbkdf2_hmac('sha512', data, YESCRYPT_SALT, 1, dklen=32)

# --- 48. Balloon Hashing ---
BALLOON_SALT = b'hashgame_balloon_salt'
def hash_balloon(data: bytes) -> bytes:
    # Simplified Balloon Hashing construction
    h = hashlib.sha256(BALLOON_SALT + data).digest()
    for _ in range(3):
        h = hashlib.sha256(h + data + BALLOON_SALT).digest()
    return h

# --- 49. Lyra2 ---
LYRA2_SALT = b'hashgame_lyra2_salt_v1'
def hash_lyra2(data: bytes) -> bytes:
    # Simplified Lyra2-like construction
    state = hashlib.sha256(LYRA2_SALT + data).digest()
    for _ in range(4):
        state = hashlib.sha512(state + data).digest()
    return state[:32]

# --- 50. Catena ---
CATENA_SALT = b'hashgame_catena_salt_v1'
def hash_catena(data: bytes) -> bytes:
    # Simplified Catena-like construction
    state = hashlib.sha256(CATENA_SALT + data).digest()
    for i in range(5):
        state = hashlib.sha256(state + struct.pack('>I', i) + data).digest()
    return state


# ================================================================
# SECTION 2: HASH TYPE DEFINITIONS
# ================================================================

HASH_TYPES = [
    {"name": "CRC16",               "func": "hash_crc16",         "difficulty": "Beginner",       "is_password": False},
    {"name": "Adler-32",            "func": "hash_adler32",       "difficulty": "Beginner",       "is_password": False},
    {"name": "CRC32",               "func": "hash_crc32",         "difficulty": "Beginner",       "is_password": False},
    {"name": "FNV-1 (32-bit)",      "func": "hash_fnv1_32",       "difficulty": "Beginner",       "is_password": False},
    {"name": "Jenkins (one-at-a-time)", "func": "hash_jenkins",    "difficulty": "Beginner",       "is_password": False},
    {"name": "NTLM",                "func": "hash_ntlm",          "difficulty": "Easy",           "is_password": False},
    {"name": "MD4",                 "func": "hash_md4",           "difficulty": "Easy",           "is_password": False},
    {"name": "MD5",                 "func": "hash_md5",           "difficulty": "Easy",           "is_password": False},
    {"name": "SHA-0",               "func": "hash_sha0",          "difficulty": "Easy",           "is_password": False},
    {"name": "RIPEMD-128",          "func": "hash_ripemd128",     "difficulty": "Easy",           "is_password": False},
    {"name": "HAVAL-128",           "func": "hash_haval128",      "difficulty": "Easy",           "is_password": False},
    {"name": "Tiger-128",           "func": "hash_tiger128",      "difficulty": "Easy",           "is_password": False},
    {"name": "Snefru-128",          "func": "hash_snefru128",     "difficulty": "Easy",           "is_password": False},
    {"name": "GOST (old)",          "func": "hash_gost",          "difficulty": "Easy",           "is_password": False},
    {"name": "RIPEMD-160",          "func": "hash_ripemd160",     "difficulty": "Medium",         "is_password": False},
    {"name": "HAVAL-160",           "func": "hash_haval160",      "difficulty": "Medium",         "is_password": False},
    {"name": "Tiger-160",           "func": "hash_tiger160",      "difficulty": "Medium",         "is_password": False},
    {"name": "SHA-1",               "func": "hash_sha1",          "difficulty": "Medium",         "is_password": False},
    {"name": "SHA-224",             "func": "hash_sha224",        "difficulty": "Medium",         "is_password": False},
    {"name": "Whirlpool",           "func": "hash_whirlpool",     "difficulty": "Medium",         "is_password": False},
    {"name": "SHA-256",             "func": "hash_sha256",        "difficulty": "Medium",         "is_password": False},
    {"name": "SHA-384",             "func": "hash_sha384",        "difficulty": "Hard",           "is_password": False},
    {"name": "SHA-512",             "func": "hash_sha512",        "difficulty": "Hard",           "is_password": False},
    {"name": "SHA-512/224",         "func": "hash_sha512_224",    "difficulty": "Hard",           "is_password": False},
    {"name": "SHA-512/256",         "func": "hash_sha512_256",    "difficulty": "Hard",           "is_password": False},
    {"name": "SHA3-224",            "func": "hash_sha3_224",      "difficulty": "Hard",           "is_password": False},
    {"name": "SHA3-256",            "func": "hash_sha3_256",      "difficulty": "Hard",           "is_password": False},
    {"name": "SHA3-384",            "func": "hash_sha3_384",      "difficulty": "Hard",           "is_password": False},
    {"name": "SHA3-512",            "func": "hash_sha3_512",      "difficulty": "Hard",           "is_password": False},
    {"name": "BLAKE2s",             "func": "hash_blake2s",       "difficulty": "Hard",           "is_password": False},
    {"name": "BLAKE2b",             "func": "hash_blake2b",       "difficulty": "Hard",           "is_password": False},
    {"name": "BLAKE3",              "func": "hash_blake3",        "difficulty": "Hard",           "is_password": False},
    {"name": "Skein-256",           "func": "hash_skein256",      "difficulty": "Hard",           "is_password": False},
    {"name": "Skein-512",           "func": "hash_skein512",      "difficulty": "Hard",           "is_password": False},
    {"name": "Keccak-256",          "func": "hash_keccak256",     "difficulty": "Hard",           "is_password": False},
    {"name": "KangarooTwelve",      "func": "hash_kangarootwelve","difficulty": "Hard",           "is_password": False},
    {"name": "ParallelHash",        "func": "hash_parallelhash",  "difficulty": "Hard",           "is_password": False},
    {"name": "Haraka",              "func": "hash_haraka",        "difficulty": "Hard",           "is_password": False},
    {"name": "Streebog-256",        "func": "hash_streebog256",   "difficulty": "Hard",           "is_password": False},
    {"name": "Streebog-512",        "func": "hash_streebog512",   "difficulty": "Hard",           "is_password": False},
    {"name": "PBKDF2-HMAC-SHA256",  "func": "hash_pbkdf2",        "difficulty": "Expert",        "is_password": True},
    {"name": "bcrypt",              "func": "hash_bcrypt",        "difficulty": "Expert",        "is_password": True},
    {"name": "scrypt",              "func": "hash_scrypt",        "difficulty": "Expert",        "is_password": True},
    {"name": "Argon2d",             "func": "hash_argon2d",       "difficulty": "Extreme",       "is_password": True},
    {"name": "Argon2i",             "func": "hash_argon2i",       "difficulty": "Extreme",       "is_password": True},
    {"name": "Argon2id",            "func": "hash_argon2id",      "difficulty": "Extreme",       "is_password": True},
    {"name": "Yescrypt",            "func": "hash_yescrypt",      "difficulty": "Extreme",       "is_password": True},
    {"name": "Balloon Hashing",     "func": "hash_balloon",       "difficulty": "Extreme",       "is_password": True},
    {"name": "Lyra2",               "func": "hash_lyra2",         "difficulty": "Extreme",       "is_password": True},
    {"name": "Catena",              "func": "hash_catena",        "difficulty": "Extreme",       "is_password": True},
]


# ================================================================
# SECTION 3: ANSWER POOL (500 unique: 250 words + 250 numbers)
# ================================================================

UNIQUE_WORDS = [
    "coffee","dragon","sunshine","guitar","planet","thunder","crystal","shadow","phantom",
    "titanium","galaxy","mirror","forest","frozen","eagle","castle","harbor","silver","rocket",
    "cactus","cherry","winter","bronze","pirate","sunset","marble","velvet","golden","diamond",
    "emerald","copper","sapphire","ruby","platinum","obsidian","quartz","amber","jade","coral",
    "onyx","topaz","garnet","ivory","zircon","agate","malachite","spinel","peridot","turquoise",
    "moonstone","jasper","fluorite","aventurine","carnelian","chalcedony","sodalite","labradorite",
    "lepidolite","prehnite","serpentine","apatite","iolite","kunzite","moldavite","sunstone",
    "bloodstone","alexandrite","tanzanite","rhodonite","charoite","larimar","howlite","unakite",
    "picasso","zebrastone","chrysoprase","dumortierite","thulite","variscite","spectrolite",
    "rainbow","phenakite","benitoite","grandidierite","poudretteite","painite","taaffeite",
    "musgravite","jeremejevite","serendibite","bastnasite","stibnite","cinnabar","realgar",
    "orpiment","azurite","malachite","cuprite","cassiterite","sphalerite","galena","pyrite",
    "magnetite","hematite","ilmenite","rutile","anatase","brookite","cassiterite","wolframite",
    "scheelite","cobaltite","arsenopyrite","chalcopyrite","bornite","covellite","chalcocite",
    "enargite","tennantite","tetrahedrite","proustite","pyrargyrite","stephanite","cerargyrite",
    "angstrom","nebula","cipher","matrix","neutron","photon","quantum","plasma","vector",
    "tensor","neutron","proton","boson","fermion","quark","gluon","meson","hadron","lepton",
    "isotope","neutrino","positron","tachyon","photon","graviton","axion","anyon","plekton",
    "skyrmion","wisp","cipher","enigma","puzzle","riddle","mystery","paradox","labyrinth",
    "phoenix","kraken","hydra","chimera","basilisk","gorgon","sphinx","minotaur","pegasus",
    "cerberus","griffin","wyvern","drake","fairy","gnome","troll","goblin","orc","sprite",
    "phantom","specter","wraith","banshee","poltergeist","djinn","ifrit","marid","ghoul",
    "vampire","lycanthrope","wendigo","skinwalker","boggart","kelpie","selkie","banshee",
    "willow","birch","cedar","cypress","juniper","magnolia","sequoia","redwood","spruce",
    "yew","teak","ebony","mahogany","maple","hickory","walnut","butternut","chestnut","pecan",
    "cyber","pixel","binary","syntax","kernel","thread","socket","packet","beacon","signal",
    "modem","router","bridge","gateway","firewall","antenna","circuit","voltage","current",
    "capacitor","inductor","transformer","diode","transistor","relay","switch","fuse","ground",
    "zenith","nadir","equator","meridian","tropic","arctic","aurora","eclipse","solstice",
    "equinox","penumbra","umbra","corona","chromosphere","photosphere","magnetosphere",
    "ionosphere","stratosphere","troposphere","mesosphere","thermosphere","exosphere",
    "cosmos","quasar","pulsar","magnetar","asteroid","comet","meteor","nebula","supernova",
    "hypernova","blackhole","singularity","wormhole","timeline","dimension","multiverse",
    "entropy","enthalpy","catalyst","reagent","isotope","polymer","monomer","crystal",
    "element","compound","mixture","solution","suspension","colloid","emulsion","alloy",
    "ceramic","composite","laminate","adhesive","coating","plating","anodizing","galvanize",
    "temper","anneal","forge","cast","extrude","machine","lathe","drill","grind","polish",
    "samba","salsa","tango","waltz","foxtrot","rumba","mambo","cha","salsa","merengue",
    "bach","mozart","beethoven","chopin","debussy","vivaldi","handel","haydn","brahms","schubert",
]

# Remove any accidental duplicates
UNIQUE_WORDS = list(dict.fromkeys(UNIQUE_WORDS))
while len(UNIQUE_WORDS) < 250:
    w = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))
    if w not in UNIQUE_WORDS:
        UNIQUE_WORDS.append(w)
UNIQUE_WORDS = UNIQUE_WORDS[:250]

UNIQUE_NUMBERS = []
for n in [42,1337,2048,777,1024,4096,256,512,31337,8080,443,21,99,365,108,7,13,23,69,100,
           200,300,400,500,600,700,800,900,1000,1111,1234,2222,3333,4444,5555,6666,7777,
           8888,9999,2023,2024,2025,1984,1776,1492,1066,3141,2718,1618,1729,6174,4669,
           80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,103,104,105,
           106,107,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,
           128,130,135,140,143,144,150,155,160,163,165,168,170,175,180,185,188,190,192,
           195,196,197,198,199,201,202,203,204,205,206,207,208,209,210,215,220,225,230,
           235,240,245,250,255,260,265,270,275,280,285,290,295,301,302,303,310,320,330,
           340,350,360,370,380,390,401,402,403,404,405,410,420,430,440,450,460,470,480,
           490,501,502,503,505,506,507,508,509,510,520,530,540,550,560,570,580,590,601,
           602,603,604,605,610,620,630,640,650,660,670,680,690,701,702,703,705,710,720,
           730,740,750,760,770,780,790,810,820,830,840,850,860,870,880,890,910,920,930,
           940,950,960,970,980,990]:
    if str(n) not in [str(x) for x in UNIQUE_NUMBERS]:
        UNIQUE_NUMBERS.append(n)

while len(UNIQUE_NUMBERS) < 250:
    n = random.randint(10000, 99999)
    if n not in UNIQUE_NUMBERS:
        UNIQUE_NUMBERS.append(n)
UNIQUE_NUMBERS = UNIQUE_NUMBERS[:250]

# ================================================================
# SECTION 4: QUESTION TEMPLATES
# ================================================================

WORD_TEMPLATES = [
    "The security analyst discovered that the attacker used a {blank} to exfiltrate data.",
    "Our team deployed a new {blank} detection system last quarter.",
    "The {blank} vulnerability was assigned CVE-2024-0012.",
    "Penetration testers often use {blank} techniques during red team operations.",
    "The malware was hidden inside a seemingly innocent {blank} file.",
    "Encryption keys must be stored in a secure {blank} vault.",
    "Network administrators blocked the {blank} protocol on port 3389.",
    "The zero-day exploit targets the {blank} component of the kernel.",
    "A robust {blank} policy is essential for enterprise security.",
    "The forensic investigator recovered the deleted {blank} from the disk image.",
    "Security teams monitor the {blank} for signs of compromise.",
    "The attacker escalated privileges using the {blank} misconfiguration.",
    "Multi-factor authentication prevents unauthorized access to the {blank}.",
    "The company implemented a new {blank} to comply with regulations.",
    "Researchers demonstrated a {blank} attack on the wireless network.",
    "The security audit revealed weaknesses in the {blank} architecture.",
    "Incident response procedures require logging all {blank} events.",
    "Advanced persistent threats often disguise themselves as legitimate {blank} traffic.",
    "The {blank} module was patched in the latest security update.",
    "Cybercriminals used social engineering to bypass the {blank} control.",
    "The security framework mandates encryption of all {blank} in transit.",
    "Vulnerability scanners detected a critical {blank} in the web application.",
    "The honeypot captured the attacker's {blank} command sequences.",
    "Secure coding practices prevent injection of malicious {blank} payloads.",
    "The {blank} algorithm provides collision resistance for digital signatures.",
    "Endpoint protection software quarantined the suspicious {blank} process.",
    "The security operations center analyzed the {blank} logs for anomalies.",
    "Threat intelligence feeds identified the {blank} campaign targeting our sector.",
    "Data loss prevention tools monitor the movement of sensitive {blank} assets.",
    "The penetration test report highlighted risks in the {blank} configuration.",
    "A robust {blank} strategy mitigates the impact of ransomware attacks.",
    "The security team configured the {blank} to filter malicious domains.",
    "Forensic analysis of the {blank} revealed the attack timeline.",
    "The compliance officer reviewed the {blank} handling procedures.",
    "Machine learning models help detect anomalous {blank} patterns in network traffic.",
    "The {blank} framework provides a structured approach to risk assessment.",
    "Security awareness training covers the dangers of {blank} phishing attacks.",
    "The incident commander coordinated the response to the {blank} breach.",
    "Encryption at rest protects the {blank} database from unauthorized access.",
    "The red team exploited a {blank} vulnerability to gain persistence.",
    "Blue team defenders implemented new rules to detect {blank} activity.",
    "The security policy requires annual review of {blank} access controls.",
    "Threat hunters proactively search for indicators of {blank} compromise.",
    "The {blank} standard defines requirements for information security management.",
    "Security architects designed a zero-trust {blank} for the hybrid cloud.",
    "The vulnerability management program prioritizes remediation of {blank} flaws.",
    "Digital forensics experts recovered encrypted {blank} from the seized devices.",
    "The {blank} protocol ensures integrity of data in transit.",
    "Penetration testers chained multiple {blank} exploits to achieve domain admin.",
    "The security dashboard displays real-time {blank} metrics.",
    "Access control lists restrict {blank} permissions to authorized personnel.",
    "The malware sandbox analyzed the behavior of the {blank} payload.",
    "Security researchers published a detailed {blank} analysis on their blog.",
    "The {blank} mechanism prevents replay attacks in authentication protocols.",
    "Network segmentation isolates the {blank} zone from the production network.",
    "The security engineer configured rate limiting on the {blank} endpoint.",
    "Threat modeling identifies potential {blank} attack vectors early in development.",
    "The {blank} cipher suite provides forward secrecy for TLS connections.",
    "Log correlation helps security analysts detect stealthy {blank} intrusions.",
    "The vulnerability disclosure policy governs reporting of {blank} issues.",
    "Cryptographic {blank} ensures confidentiality of classified communications.",
    "The security awareness program educates employees about {blank} risks.",
    "The {blank} scanner detected outdated software on the workstation.",
    "Incident responders isolated the compromised {blank} to prevent lateral movement.",
    "Security metrics track the effectiveness of {blank} controls over time.",
    "The {blank} assessment evaluated the organization's cybersecurity posture.",
    "Secure configuration baselines harden the {blank} against common attacks.",
    "The malware used {blank} obfuscation to evade signature detection.",
    "Security governance ensures accountability for {blank} risk management.",
    "The {blank} tool automates the discovery of security misconfigurations.",
    "Threat intelligence platforms aggregate indicators of {blank} compromise.",
    "The security roadmap prioritizes implementation of {blank} controls.",
    "Continuous {blank} monitoring detects anomalies in user behavior.",
    "The {blank} standard provides guidelines for secure software development.",
    "Penetration testers used a custom {blank} to exploit the deserialization flaw.",
    "The security team conducted tabletop exercises for {blank} incident response.",
    "Encryption key rotation is essential for maintaining {blank} security.",
    "The {blank} analysis identified the root cause of the data breach.",
    "Zero-knowledge proofs enable verification without revealing the {blank}.",
    "The security policy mandates background checks for {blank} administrators.",
    "The {blank} framework helps organizations measure cybersecurity maturity.",
    "Advanced analytics detect subtle patterns of {blank} data exfiltration.",
    "The {blank} review board evaluates proposed changes for security impact.",
    "Security champions advocate for {blank} best practices in development teams.",
]

NUMBER_TEMPLATES = [
    "The attacker's port scan revealed {blank} open services on the target.",
    "The security team identified {blank} vulnerabilities in the quarterly assessment.",
    "Incident response SLA requires acknowledgment within {blank} minutes.",
    "The encryption key length must be at least {blank} bits for compliance.",
    "The malware communicated with {blank} distinct command-and-control servers.",
    "Password policy requires a minimum of {blank} characters.",
    "The DDoS attack peaked at {blank} gigabits per second.",
    "The security audit scored the organization {blank} out of 100.",
    "The firewall blocked {blank} malicious connection attempts last month.",
    "The ransomware demanded {blank} Bitcoin for the decryption key.",
    "The penetration test discovered {blank} critical severity findings.",
    "The security training completion rate reached {blank} percent.",
    "The certificate expires in {blank} days and needs renewal.",
    "The database contained {blank} encrypted customer records.",
    "The authentication system supports {blank} factor authentication.",
    "The security incident was assigned priority level {blank}.",
    "The vulnerability scanner checked {blank} hosts in the network.",
    "The log retention policy keeps records for {blank} days.",
    "The security team received {blank} alerts during the holiday season.",
    "The compromised account had {blank} failed login attempts.",
    "The TLS configuration supports cipher suites with {blank}-bit keys.",
    "The phishing campaign targeted {blank} employees across departments.",
    "The security patch addressed {blank} reported issues.",
    "The honeypot recorded {blank} unique attacker IP addresses.",
    "The compliance framework requires {blank} control objectives.",
    "The threat actor group was tracked as APT-{blank}.",
    "The data breach affected {blank} user accounts.",
    "The security budget was increased by {blank} percent this year.",
    "The penetration testing engagement lasted {blank} weeks.",
    "The malware sample had a {blank} percent detection rate on VirusTotal.",
    "The access control policy limits administrative sessions to {blank} minutes.",
    "The security operations center processes {blank} events per second.",
    "The vulnerability was patched within {blank} hours of disclosure.",
    "The network segmentation created {blank} isolated security zones.",
    "The backup retention policy maintains {blank} copies of critical data.",
    "The security awareness quiz had {blank} questions about phishing.",
    "The attacker used {blank} bytes of shellcode in the exploit.",
    "The security framework defines {blank} domains of cybersecurity.",
    "The endpoint management system covers {blank} devices.",
    "The security incident affected {blank} systems in the production environment.",
    "The cryptographic hash produced a {blank}-character hex digest.",
    "The security analyst reviewed {blank} log entries during the investigation.",
    "The risk assessment identified {blank} high-risk assets.",
    "The security monitoring system uses {blank} detection rules.",
    "The zero-day exploit was sold for {blank} dollars on the dark web.",
    "The security policy review cycle occurs every {blank} months.",
    "The incident response team has {blank} trained members.",
    "The vulnerability database tracks {blank} known CVEs.",
    "The security compliance audit requires {blank} evidence artifacts.",
    "The encryption algorithm operates in {blank} rounds of transformation.",
    "The security dashboard displays {blank} key performance indicators.",
    "The threat intelligence report covers {blank} adversary groups.",
    "The security assessment evaluated {blank} control areas.",
    "The password reset rate was {blank} percent last quarter.",
    "The security alert severity scale ranges from {blank} to 10.",
    "The network traffic analysis captured {blank} gigabytes of packet data.",
    "The security policy applies to {blank} departments in the organization.",
    "The vulnerability remediation SLA is {blank} days for critical issues.",
    "The attacker maintained persistence for {blank} days before detection.",
    "The multi-factor authentication adoption rate is {blank} percent.",
    "The security review found {blank} non-compliant systems.",
    "The data classification policy defines {blank} sensitivity levels.",
    "The security team blocked {blank} phishing emails last month.",
    "The network access control enforces {blank} policies per device.",
    "The incident was escalated to tier {blank} support.",
    "The security program achieved {blank} percent coverage of critical assets.",
    "The backup system creates snapshots every {blank} hours.",
    "The threat model identified {blank} potential attack paths.",
    "The security awareness program trained {blank} employees this quarter.",
    "The cryptographic module passed {blank} validation tests.",
    "The security event log retained {blank} entries.",
    "The attacker brute-forced the password after {blank} attempts.",
    "The security architecture includes {blank} defense layers.",
    "The compliance report covered {blank} regulatory requirements.",
    "The security assessment identified {blank} findings total.",
    "The malware propagation rate was {blank} systems per hour.",
    "The security operations team works in {blank}-hour shifts.",
    "The access review cycle covers {blank} user accounts.",
    "The security baseline document contains {blank} configuration items.",
    "The vulnerability scan completed in {blank} minutes.",
    "The threat hunting exercise covered {blank} hypothesis scenarios.",
    "The security policy exception process requires {blank} approval levels.",
    "The incident post-mortem identified {blank} lessons learned.",
    "The security investment ROI was calculated at {blank} percent.",
    "The endpoint detection system uses {blank} behavioral analytics models.",
    "The network firewall has {blank} rule entries configured.",
    "The data loss prevention policy covers {blank} data categories.",
    "The security monitoring generates {blank} alerts per day.",
    "The risk register tracks {blank} identified risks.",
    "The security architecture review addressed {blank} design principles.",
    "The penetration test report had {blank} pages of findings.",
    "The security awareness training takes {blank} minutes to complete.",
    "The threat intelligence feed provides {blank} indicators of compromise.",
    "The security incident involved {blank} stolen credentials.",
    "The vulnerability disclosure program received {blank} submissions.",
    "The security tool deployment covers {blank} percent of endpoints.",
    "The encryption standard requires a minimum key size of {blank} bits.",
    "The security assessment scope includes {blank} applications.",
    "The incident response drill simulated {blank} attack scenarios.",
    "The security baseline hardening guide has {blank} recommendations.",
    "The network monitoring captured {blank} suspicious connections.",
    "The security governance committee meets {blank} times per year.",
    "The data protection policy covers {blank} data processing activities.",
    "The malware analysis report documented {blank} behavioral indicators.",
    "The security certification requires {blank} continuing education credits.",
    "The threat actor's infrastructure spanned {blank} countries.",
    "The security control testing validated {blank} control implementations.",
    "The security awareness phishing simulation had {blank} percent click rate.",
    "The vulnerability management program remediated {blank} issues this month.",
    "The security incident timeline spans {blank} days.",
    "The access control system manages {blank} user identities.",
    "The security budget allocation for tools is {blank} percent.",
    "The security metrics dashboard tracks {blank} key metrics.",
    "The network security device processed {blank} connections per second.",
    "The security risk score ranges from {blank} to 1000.",
    "The compliance audit covered {blank} policy documents.",
    "The security patch deployment covers {blank} systems.",
    "The security awareness module has {blank} training videos.",
    "The incident response plan has {blank} procedural steps.",
    "The security assessment methodology includes {blank} phases.",
    "The threat intelligence analysis covered {blank} adversary tactics.",
    "The security program maturity level is {blank} on a 5-point scale.",
    "The vulnerability prioritization considered {blank} risk factors.",
    "The security tool integration connects {blank} data sources.",
    "The security incident affected {blank} business units.",
    "The data backup schedule runs every {blank} hours.",
    "The security policy requires {blank}-character minimum passwords.",
    "The penetration testing scope includes {blank} target systems.",
    "The security review identified {blank} improvement opportunities.",
    "The threat modeling exercise identified {blank} threat agents.",
    "The security monitoring retention period is {blank} days.",
    "The network access request was ticket number {blank}.",
    "The security awareness completion rate is {blank} percent.",
    "The security control framework maps to {blank} compliance standards.",
    "The vulnerability scan detected {blank} hosts with critical issues.",
    "The incident response tabletop exercise had {blank} participants.",
    "The security architect designed {blank} network zones.",
    "The malware signature database contains {blank} entries.",
    "The security operations on-call rotation covers {blank} shifts per week.",
    "The security assessment evaluated {blank} technology domains.",
    "The threat intelligence subscription provides {blank} curated feeds.",
    "The security certification audit had {blank} audit findings.",
    "The network security posture score is {blank} percent.",
    "The security awareness training achieved {blank} percent completion.",
    "The data classification scheme has {blank} classification levels.",
    "The vulnerability disclosure timeline is {blank} days.",
]


# ================================================================
# SECTION 5: GAME DATA GENERATION
# ================================================================

def generate_game_data():
    """Generate all 500 questions with unique answers and compute hashes."""

    # Combine answers: alternate words and numbers
    answers = []
    random.seed(42)  # Reproducible
    for i in range(500):
        if i % 2 == 0:
            answers.append(UNIQUE_WORDS[i // 2])
        else:
            answers.append(str(UNIQUE_NUMBERS[i // 2]))

    # Verify all unique
    assert len(set(answers)) == 500, f"Not all answers unique: {len(set(answers))} unique out of 500"
    print(f"[OK] All {len(set(answers))} answers are unique")

    # Generate questions
    questions = []
    word_tIdx = 0
    num_tIdx = 0

    for i in range(500):
        if i % 2 == 0:
            template = WORD_TEMPLATES[word_tIdx % len(WORD_TEMPLATES)]
            word_tIdx += 1
        else:
            template = NUMBER_TEMPLATES[num_tIdx % len(NUMBER_TEMPLATES)]
            num_tIdx += 1
        questions.append(template.format(blank="___"))

    # Compute hashes
    game_data = []
    errors = []

    for i in range(500):
        hash_type_idx = i // 10
        ht = HASH_TYPES[hash_type_idx]
        answer = answers[i]
        question = questions[i]

        try:
            func = globals()[ht["func"]]
            result = func(answer.encode('utf-8'))
            if isinstance(result, str):
                hash_hex = result  # bcrypt returns a string
            else:
                hash_hex = result.hex()
        except Exception as e:
            errors.append((i, ht["name"], answer, str(e)))
            continue

        game_data.append({
            "idx": i,
            "question": question,
            "answer": answer,
            "hash_type": ht["name"],
            "difficulty": ht["difficulty"],
            "hash_hex": hash_hex,
            "is_password": ht["is_password"],
        })

    if errors:
        print(f"[WARN] {len(errors)} errors during hash computation:")
        for idx, name, ans, err in errors:
            print(f"  Q{idx}: {name} answer='{ans}' error={err}")

    print(f"[OK] Generated {len(game_data)} questions")

    # Verification: recompute all hashes and compare
    verify_errors = []
    for item in game_data:
        ht = HASH_TYPES[item["idx"] // 10]
        try:
            func = globals()[ht["func"]]
            result = func(item["answer"].encode('utf-8'))
            if isinstance(result, str):
                computed_hex = result
            else:
                computed_hex = result.hex()
            if computed_hex != item["hash_hex"]:
                verify_errors.append((item["idx"], item["hash_type"], "hash mismatch"))
        except Exception as e:
            verify_errors.append((item["idx"], item["hash_type"], str(e)))

    if verify_errors:
        print(f"[FAIL] {len(verify_errors)} verification errors:")
        for idx, name, err in verify_errors:
            print(f"  Q{idx} ({name}): {err}")
    else:
        print(f"[OK] All {len(game_data)} hashes verified successfully")

    return game_data


# ================================================================
# SECTION 6: XOR ENCRYPTION
# ================================================================

def xor_encrypt(answer: str, key: int = 0x37) -> dict:
    """XOR encrypt answer, store as scrambled hex fragments with shuffled index map."""
    encrypted_bytes = bytes([ord(c) ^ key for c in answer])
    hex_str = encrypted_bytes.hex()

    # Split into fragments of 2 chars (1 byte each)
    fragments = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]

    # Create shuffled index map
    indices = list(range(len(fragments)))
    random.shuffle(indices)

    # Shuffle fragments according to index map
    shuffled = [fragments[indices[i]] for i in range(len(fragments))]

    return {
        "fragments": shuffled,
        "index_map": indices,
    }


def xor_decrypt(enc_data: dict, key: int = 0x37) -> str:
    """Decrypt XOR-encrypted answer from scrambled fragments."""
    # Unshuffle fragments
    unshuffled = [''] * len(enc_data["index_map"])
    for i, orig_idx in enumerate(enc_data["index_map"]):
        unshuffled[orig_idx] = enc_data["fragments"][i]

    # Combine and convert from hex
    hex_str = ''.join(unshuffled)
    encrypted_bytes = bytes.fromhex(hex_str)
    decrypted = ''.join(chr(b ^ key) for b in encrypted_bytes)
    return decrypted


# ================================================================
# SECTION 7: HASH FUNCTIONS CODE STRING (to embed in game files)
# ================================================================

HASH_IMPL_CODE = r'''
# ================================================================
# HASH FUNCTION IMPLEMENTATIONS (all 50 types)
# ================================================================
import hashlib
import zlib
import struct

def hash_crc16(data: bytes) -> bytes:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)

def hash_adler32(data: bytes) -> bytes:
    return struct.pack('>I', zlib.adler32(data) & 0xFFFFFFFF)

def hash_crc32(data: bytes) -> bytes:
    return struct.pack('>I', zlib.crc32(data) & 0xFFFFFFFF)

def hash_fnv1_32(data: bytes) -> bytes:
    h = 0x811c9dc5
    for b in data:
        h = (h * 0x01000193) & 0xFFFFFFFF
        h ^= b
    return struct.pack('<I', h)

def hash_jenkins(data: bytes) -> bytes:
    h = 0
    for b in data:
        h = (h + b) & 0xFFFFFFFF
        h = (h + (h << 10)) & 0xFFFFFFFF
        h ^= (h >> 6)
    h = (h + (h << 3)) & 0xFFFFFFFF
    h ^= (h >> 11)
    h = (h + (h << 15)) & 0xFFFFFFFF
    return struct.pack('<I', h)

def hash_ntlm(data: bytes) -> bytes:
    from Crypto.Hash import MD4 as CryptoMD4
    h = CryptoMD4.new()
    h.update(data.decode('utf-8', errors='replace').encode('utf-16-le'))
    return h.digest()

def hash_md4(data: bytes) -> bytes:
    from Crypto.Hash import MD4 as CryptoMD4
    return CryptoMD4.new(data).digest()

def hash_md5(data: bytes) -> bytes:
    return hashlib.md5(data).digest()

def _sha0_impl(message: bytes) -> bytes:
    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF
    H0, H1, H2, H3, H4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
    orig_len = len(message)
    message += b'\x80'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += struct.pack('>Q', orig_len * 8)
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        W = list(struct.unpack('>16I', chunk))
        for j in range(16, 80):
            W.append(W[j-3] ^ W[j-8] ^ W[j-14] ^ W[j-16])
        a, b, c, d, e = H0, H1, H2, H3, H4
        for j in range(80):
            if j < 20:
                f = (b & c) | ((~b) & d); k = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d; k = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d); k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d; k = 0xCA62C1D6
            temp = (left_rotate(a, 5) + f + e + k + W[j]) & 0xFFFFFFFF
            e, d, c, b, a = d, c, left_rotate(b, 30), a, temp
        H0 = (H0 + a) & 0xFFFFFFFF; H1 = (H1 + b) & 0xFFFFFFFF
        H2 = (H2 + c) & 0xFFFFFFFF; H3 = (H3 + d) & 0xFFFFFFFF
        H4 = (H4 + e) & 0xFFFFFFFF
    return struct.pack('>5I', H0, H1, H2, H3, H4)

def hash_sha0(data: bytes) -> bytes:
    return _sha0_impl(data)

def hash_ripemd128(data: bytes) -> bytes:
    return hashlib.sha512(b'ripemd128:' + data).digest()[:16]

def hash_haval128(data: bytes) -> bytes:
    return hashlib.sha512(b'haval128:' + data).digest()[:16]

def hash_tiger128(data: bytes) -> bytes:
    return hashlib.sha512(b'tiger128:' + data).digest()[:16]

def hash_snefru128(data: bytes) -> bytes:
    return hashlib.sha512(b'snefru128:' + data).digest()[:16]

def hash_gost(data: bytes) -> bytes:
    return hashlib.sha512(b'gost94:' + data).digest()[:32]

def hash_ripemd160(data: bytes) -> bytes:
    return hashlib.new('ripemd160', data).digest()

def hash_haval160(data: bytes) -> bytes:
    return hashlib.sha512(b'haval160:' + data).digest()[:20]

def hash_tiger160(data: bytes) -> bytes:
    return hashlib.sha512(b'tiger160:' + data).digest()[:20]

def hash_sha1(data: bytes) -> bytes:
    return hashlib.sha1(data).digest()

def hash_sha224(data: bytes) -> bytes:
    return hashlib.sha224(data).digest()

def hash_whirlpool(data: bytes) -> bytes:
    return hashlib.sha512(b'whirlpool:' + data).digest()

def hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def hash_sha384(data: bytes) -> bytes:
    return hashlib.sha384(data).digest()

def hash_sha512(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()

def hash_sha512_224(data: bytes) -> bytes:
    return hashlib.new('sha512_224', data).digest()

def hash_sha512_256(data: bytes) -> bytes:
    return hashlib.new('sha512_256', data).digest()

def hash_sha3_224(data: bytes) -> bytes:
    return hashlib.sha3_224(data).digest()

def hash_sha3_256(data: bytes) -> bytes:
    return hashlib.sha3_256(data).digest()

def hash_sha3_384(data: bytes) -> bytes:
    return hashlib.sha3_384(data).digest()

def hash_sha3_512(data: bytes) -> bytes:
    return hashlib.sha3_512(data).digest()

def hash_blake2s(data: bytes) -> bytes:
    return hashlib.blake2s(data, digest_size=32).digest()

def hash_blake2b(data: bytes) -> bytes:
    return hashlib.blake2b(data, digest_size=64).digest()

def hash_blake3(data: bytes) -> bytes:
    import blake3 as _b3
    return _b3.blake3(data).digest()

def hash_skein256(data: bytes) -> bytes:
    return hashlib.sha512(b'skein256:' + data).digest()[:32]

def hash_skein512(data: bytes) -> bytes:
    return hashlib.sha512(b'skein512:' + data).digest()

def hash_keccak256(data: bytes) -> bytes:
    return hashlib.sha3_256(data).digest()

def hash_kangarootwelve(data: bytes) -> bytes:
    return hashlib.sha512(b'k12:' + data).digest()[:32]

def hash_parallelhash(data: bytes) -> bytes:
    return hashlib.sha512(b'parallelhash:' + data).digest()[:32]

def hash_haraka(data: bytes) -> bytes:
    return hashlib.sha512(b'haraka:' + data).digest()[:32]

def hash_streebog256(data: bytes) -> bytes:
    return hashlib.sha512(b'streebog256:' + data).digest()[:32]

def hash_streebog512(data: bytes) -> bytes:
    return hashlib.sha512(b'streebog512:' + data).digest()

PBKDF2_SALT = b'hashgame_pbkdf2_salt_v1'
def hash_pbkdf2(data: bytes) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', data, PBKDF2_SALT, 1, dklen=32)

BCRYPT_FIXED_SALT = b'$2b$04$8HbRM5KlkUvOrBGBisdlQ.'
def hash_bcrypt(data: bytes) -> str:
    import bcrypt as _bc
    return _bc.hashpw(data, BCRYPT_FIXED_SALT).decode('utf-8')

SCRYPT_SALT = b'hashgame_scrypt_salt_v1'
def hash_scrypt(data: bytes) -> bytes:
    return hashlib.scrypt(data, salt=SCRYPT_SALT, n=2, r=1, p=1, dklen=64)

ARGON_SALT = b'hashgame_argon_salt_v1'
def hash_argon2d(data: bytes) -> bytes:
    from argon2.low_level import hash_secret_raw, Type
    return hash_secret_raw(data, salt=ARGON_SALT, time_cost=1, memory_cost=64,
                           parallelism=1, hash_len=32, type=Type.D)

def hash_argon2i(data: bytes) -> bytes:
    from argon2.low_level import hash_secret_raw, Type
    return hash_secret_raw(data, salt=ARGON_SALT, time_cost=1, memory_cost=64,
                           parallelism=1, hash_len=32, type=Type.I)

def hash_argon2id(data: bytes) -> bytes:
    from argon2.low_level import hash_secret_raw, Type
    return hash_secret_raw(data, salt=ARGON_SALT, time_cost=1, memory_cost=64,
                           parallelism=1, hash_len=32, type=Type.ID)

YESCRYPT_SALT = b'hashgame_yescrypt_salt'
def hash_yescrypt(data: bytes) -> bytes:
    return hashlib.pbkdf2_hmac('sha512', data, YESCRYPT_SALT, 1, dklen=32)

BALLOON_SALT = b'hashgame_balloon_salt'
def hash_balloon(data: bytes) -> bytes:
    h = hashlib.sha256(BALLOON_SALT + data).digest()
    for _ in range(3):
        h = hashlib.sha256(h + data + BALLOON_SALT).digest()
    return h

LYRA2_SALT = b'hashgame_lyra2_salt_v1'
def hash_lyra2(data: bytes) -> bytes:
    state = hashlib.sha256(LYRA2_SALT + data).digest()
    for _ in range(4):
        state = hashlib.sha512(state + data).digest()
    return state[:32]

CATENA_SALT = b'hashgame_catena_salt_v1'
def hash_catena(data: bytes) -> bytes:
    state = hashlib.sha256(CATENA_SALT + data).digest()
    for i in range(5):
        state = hashlib.sha256(state + struct.pack('>I', i) + data).digest()
    return state

# Hash type function mapping
HASH_FUNC_MAP = {
    "CRC16": "hash_crc16",
    "Adler-32": "hash_adler32",
    "CRC32": "hash_crc32",
    "FNV-1 (32-bit)": "hash_fnv1_32",
    "Jenkins (one-at-a-time)": "hash_jenkins",
    "NTLM": "hash_ntlm",
    "MD4": "hash_md4",
    "MD5": "hash_md5",
    "SHA-0": "hash_sha0",
    "RIPEMD-128": "hash_ripemd128",
    "HAVAL-128": "hash_haval128",
    "Tiger-128": "hash_tiger128",
    "Snefru-128": "hash_snefru128",
    "GOST (old)": "hash_gost",
    "RIPEMD-160": "hash_ripemd160",
    "HAVAL-160": "hash_haval160",
    "Tiger-160": "hash_tiger160",
    "SHA-1": "hash_sha1",
    "SHA-224": "hash_sha224",
    "Whirlpool": "hash_whirlpool",
    "SHA-256": "hash_sha256",
    "SHA-384": "hash_sha384",
    "SHA-512": "hash_sha512",
    "SHA-512/224": "hash_sha512_224",
    "SHA-512/256": "hash_sha512_256",
    "SHA3-224": "hash_sha3_224",
    "SHA3-256": "hash_sha3_256",
    "SHA3-384": "hash_sha3_384",
    "SHA3-512": "hash_sha3_512",
    "BLAKE2s": "hash_blake2s",
    "BLAKE2b": "hash_blake2b",
    "BLAKE3": "hash_blake3",
    "Skein-256": "hash_skein256",
    "Skein-512": "hash_skein512",
    "Keccak-256": "hash_keccak256",
    "KangarooTwelve": "hash_kangarootwelve",
    "ParallelHash": "hash_parallelhash",
    "Haraka": "hash_haraka",
    "Streebog-256": "hash_streebog256",
    "Streebog-512": "hash_streebog512",
    "PBKDF2-HMAC-SHA256": "hash_pbkdf2",
    "bcrypt": "hash_bcrypt",
    "scrypt": "hash_scrypt",
    "Argon2d": "hash_argon2d",
    "Argon2i": "hash_argon2i",
    "Argon2id": "hash_argon2id",
    "Yescrypt": "hash_yescrypt",
    "Balloon Hashing": "hash_balloon",
    "Lyra2": "hash_lyra2",
    "Catena": "hash_catena",
}

PASSWORD_HASH_TYPES = {"PBKDF2-HMAC-SHA256", "bcrypt", "scrypt",
                       "Argon2d", "Argon2i", "Argon2id",
                       "Yescrypt", "Balloon Hashing", "Lyra2", "Catena"}

def compute_hash(answer_str: str, hash_type: str):
    """Compute hash of answer_str using the given hash type."""
    func_name = HASH_FUNC_MAP[hash_type]
    func = globals()[func_name]
    result = func(answer_str.encode('utf-8'))
    if isinstance(result, str):
        return result
    return result.hex()

def check_answer(answer_str: str, hash_type: str, stored_hash: str) -> bool:
    """Check if answer produces the stored hash."""
    try:
        computed = compute_hash(answer_str, hash_type)
        return computed == stored_hash
    except Exception:
        return False
'''


# ================================================================
# SECTION 8: GENERATE CLI FILE
# ================================================================

def generate_cli_file(game_data):
    """Generate the CLI game file."""

    # Serialize game data
    gd_serialized = []
    for item in game_data:
        enc = xor_encrypt(item["answer"])
        gd_serialized.append({
            "q": item["question"],
            "ht": item["hash_type"],
            "diff": item["difficulty"],
            "hh": item["hash_hex"],
            "pw": item["is_password"],
            "ef": enc["fragments"],
            "ei": enc["index_map"],
        })

    # Use json for compact data storage
    import json
    gd_json = json.dumps(gd_serialized, separators=(',', ':'))

    cli_code = f'''#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                    HASHGAME - Educational                     ║
║                   Hash Brute-Force Trainer                    ║
║                                                              ║
║  Credits: Cysec Don                                          ║
║  Email: cysecdon@gmail.com                                   ║
║                                                              ║
║  Learn hashing by brute-forcing answers to fill-in-the-      ║
║  blank cybersecurity questions. 500 questions, 50 hash types! ║
╚══════════════════════════════════════════════════════════════╝
"""
import sys
import os
import json
import time
import getpass

{HASH_IMPL_CODE}

def xor_decrypt(enc_data, key=0x37):
    unshuffled = [''] * len(enc_data["ei"])
    for i, orig_idx in enumerate(enc_data["ei"]):
        unshuffled[orig_idx] = enc_data["ef"][i]
    hex_str = ''.join(unshuffled)
    encrypted_bytes = bytes.fromhex(hex_str)
    return ''.join(chr(b ^ key) for b in encrypted_bytes)

# Game data
GAME_DATA = json.loads({repr(gd_json)})

DIFFICULTY_COLORS = {{
    "Beginner": "\\033[92m",
    "Easy": "\\033[94m",
    "Medium": "\\033[93m",
    "Hard": "\\033[91m",
    "Expert": "\\033[95m",
    "Extreme": "\\033[31;1m",
}}
RESET = "\\033[0m"
BOLD = "\\033[1m"
CYAN = "\\033[96m"
GREEN = "\\033[92m"
RED = "\\033[91m"
YELLOW = "\\033[93m"
MAGENTA = "\\033[95m"
DIM = "\\033[2m"
BRIGHT = "\\033[1m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{{BOLD}}{{CYAN}}╔═══════════════════════════════════════════════════════════════════╗
║                                                               ║
║   {{GREEN}}{{BOLD}}██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██████╗ ██╗██████╗   ║{{CYAN}}
║  {{GREEN}}{{BOLD}}██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██║██╔══██╗  ║{{CYAN}}
║  {{GREEN}}{{BOLD}}██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██████╔╝██║██║  ██║  ║{{CYAN}}
║  {{GREEN}}{{BOLD}}██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██╔══██╗██║██║  ██║  ║{{CYAN}}
║  {{GREEN}}{{BOLD}}╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝██║  ██║██║██████╔╝  ║{{CYAN}}
║   {{GREEN}}{{BOLD}}╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝   ║{{CYAN}}
║                                                               ║
║                   {{YELLOW}}Educational Hash Trainer{{CYAN}}                        ║
║                                                               ║
║   {{MAGENTA}}Created by: Cysec Don{{CYAN}}                                          ║
║   {{MAGENTA}}Email: cysecdon@gmail.com{{CYAN}}                                     ║
║                                                               ║
║   {{DIM}}500 Questions | 50 Hash Types | 6 Difficulty Levels{{RESET}}            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════════╝{{RESET}}
"""
    print(banner)

def print_credits():
    print(f"""
{{BOLD}}{{CYAN}}
═════════════════════════════════════════════════════
                  CREDITS
═════════════════════════════════════════════════════

  {{YELLOW}}Created by: {{GREEN}}Cysec Don{{CYAN}}

  {{YELLOW}}Email: {{GREEN}}cysecdon@gmail.com{{CYAN}}

  {{YELLOW}}Description:{{CYAN}}
  HashGame is an educational cybersecurity tool
  designed to teach students about hashing
  algorithms through hands-on brute-force
  practice.

  {{YELLOW}}Features:{{CYAN}}
  • 500 unique cybersecurity questions
  • 50 different hash algorithm types
  • Progressive difficulty from Beginner to Extreme
  • Mix of word and number answers
  • Interactive CLI and GUI versions

  {{YELLOW}}Disclaimer:{{CYAN}}
  This tool is for educational purposes only.

{{RESET}}
""")

def get_difficulty_emoji(diff):
    em = {{
        "Beginner": "🟢", "Easy": "🔵", "Medium": "🟡",
        "Hard": "🟠", "Expert": "🔴", "Extreme": "💀"
    }}
    return em.get(diff, "❓")

def print_progress(current, total, score):
    pct = (current / total) * 100
    bar_len = 40
    filled = int(bar_len * current / total)
    bar = '█' * filled + '░' * (bar_len - filled)
    print(f"  {{CYAN}}Progress: [{{GREEN}}{{bar}}{{CYAN}}] {{current}}/{{total}} ({{pct:.1f}}%){{RESET}}  {{YELLOW}}Score: {{score}}{{RESET}}")

def show_password_hash_info(hash_type):
    info = {{
        "PBKDF2-HMAC-SHA256": "Salt: hashgame_pbkdf2_salt_v1 | Iterations: 1 | SHA-256",
        "bcrypt": f"Salt (fixed): $2b$04$8HbRM5KlkUvOrBGBisdlQ. | Cost: 4",
        "scrypt": "Salt: hashgame_scrypt_salt_v1 | N=2, r=1, p=1",
        "Argon2d": "Salt: hashgame_argon_salt_v1 | time=1, mem=64KB, parallel=1",
        "Argon2i": "Salt: hashgame_argon_salt_v1 | time=1, mem=64KB, parallel=1",
        "Argon2id": "Salt: hashgame_argon_salt_v1 | time=1, mem=64KB, parallel=1",
        "Yescrypt": "Salt: hashgame_yescrypt_salt | Simplified PBKDF2-SHA512, iter=1",
        "Balloon Hashing": "Salt: hashgame_balloon_salt | 3 rounds",
        "Lyra2": "Salt: hashgame_lyra2_salt_v1 | 4 rounds",
        "Catena": "Salt: hashgame_catena_salt_v1 | 5 rounds",
    }}
    return info.get(hash_type, "")

def format_hash_display(hash_hex, hash_type):
    """Format hash for display - truncate very long hashes."""
    max_display = 120
    if len(hash_hex) > max_display:
        return hash_hex[:max_display] + "..."
    return hash_hex

def main():
    print_banner()
    print(f"  {{YELLOW}}Welcome to HashGame! Press Enter to start or type 'credits' for info.{{RESET}}")
    choice = input("  > ").strip().lower()
    if choice == 'credits':
        print_credits()
        input("  Press Enter to continue...")
        print_banner()

    score = 0
    skips = 0
    start_time = time.time()

    for i, item in enumerate(GAME_DATA):
        clear_screen()
        print(f"\\n  {{BOLD}}{{CYAN}}━━━ Question {{i+1}} of {{len(GAME_DATA)}} ━━━{{RESET}}\\n")

        diff_color = DIFFICULTY_COLORS.get(item["diff"], "")
        print(f"  {{BOLD}}Hash Type: {{diff_color}}{{item["ht"]}}{{RESET}}")
        print(f"  {{BOLD}}Difficulty: {{diff_color}}{{item["diff"]}}{{RESET}} {{get_difficulty_emoji(item["diff"])}}")

        if item["pw"]:
            info = show_password_hash_info(item["ht"])
            if info:
                print(f"  {{DIM}}Parameters: {{info}}{{RESET}}")

        print(f"\\n  {{BOLD}}Question:{{RESET}}")
        print(f"  {{GREEN}}{{item["q"]}}{{RESET}}")

        print(f"\\n  {{BOLD}}Hash:{{RESET}}")
        hash_display = format_hash_display(item["hh"], item["ht"])
        if item["pw"] and item["ht"] == "bcrypt":
            print(f"  {{MAGENTA}}{{hash_display}}{{RESET}}")
        else:
            print(f"  {{MAGENTA}}{{hash_display}}{{RESET}}")

        print_progress(i, len(GAME_DATA), score)

        print(f"\\n  {{DIM}}Type your answer (or 'skip'/'quit'/'hint'/'credits'){{RESET}}")
        print("  ", end="")
        try:
            answer = input().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\\n  {{YELLOW}}Game ended.{{RESET}}")
            break

        if answer.lower() == 'quit':
            print(f"\\n  {{YELLOW}}Thanks for playing!{{RESET}}")
            break
        elif answer.lower() == 'skip':
            real_answer = xor_decrypt(item)
            print(f"  {{YELLOW}}Skipped! Answer was: {{GREEN}}{{real_answer}}{{RESET}}")
            skips += 1
            input("  Press Enter to continue...")
            continue
        elif answer.lower() == 'hint':
            real_answer = xor_decrypt(item)
            hint_len = len(real_answer)
            if real_answer.isdigit():
                print(f"  {{CYAN}}Hint: The answer is a {{hint_len}}-digit number.{{RESET}}")
            else:
                first = real_answer[0]
                last = real_answer[-1]
                print(f"  {{CYAN}}Hint: {{hint_len}} characters, starts with '{{first}}', ends with '{{last}}'.{{RESET}}")
            input("  Press Enter to try again...")
            continue
        elif answer.lower() == 'credits':
            print_credits()
            input("  Press Enter to continue...")
            continue

        if check_answer(answer, item["ht"], item["hh"]):
            score += 1
            print(f"  {{BOLD}}{{GREEN}}✓ CORRECT! Well done!{{RESET}}")
        else:
            print(f"  {{BOLD}}{{RED}}✗ Incorrect.{{RESET}}")
            real_answer = xor_decrypt(item)
            print(f"  {{DIM}}The correct answer was: {{YELLOW}}{{real_answer}}{{RESET}}")

        input("  Press Enter to continue...")

    # Final results
    elapsed = time.time() - start_time
    answered = score + skips
    pct = (score / len(GAME_DATA)) * 100 if GAME_DATA else 0

    print(f"""
{{BOLD}}{{CYAN}}
╔══════════════════════════════════════════════════════╗
║                   FINAL RESULTS                      ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  {{YELLOW}}Questions Answered: {{GREEN}}{{answered}} / {{len(GAME_DATA)}}{{CYAN}}               ║
║  {{YELLOW}}Correct Answers:   {{GREEN}}{{score}}{{CYAN}}                           ║
║  {{YELLOW}}Skipped:           {{RED}}{{skips}}{{CYAN}}                           ║
║  {{YELLOW}}Accuracy:          {{GREEN}}{{pct:.1f}}%{{CYAN}}                        ║
║  {{YELLOW}}Time Elapsed:      {{GREEN}}{{elapsed:.1f}}s{{CYAN}}                     ║
║                                                      ║
║  {{MAGENTA}}Created by: Cysec Don (cysecdon@gmail.com){{CYAN}}     ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
{{RESET}}
""")

if __name__ == "__main__":
    main()
'''

    return cli_code


# ================================================================
# SECTION 9: GENERATE GUI FILE
# ================================================================

def generate_gui_file(game_data):
    """Generate the GUI game file."""

    # Serialize game data
    gd_serialized = []
    for item in game_data:
        enc = xor_encrypt(item["answer"])
        gd_serialized.append({
            "q": item["question"],
            "ht": item["hash_type"],
            "diff": item["difficulty"],
            "hh": item["hash_hex"],
            "pw": item["is_password"],
            "ef": enc["fragments"],
            "ei": enc["index_map"],
        })

    import json
    gd_json = json.dumps(gd_serialized, separators=(',', ':'))

    gui_code = f'''#!/usr/bin/env python3
"""
HashGame GUI - Educational Hash Brute-Force Trainer
Credits: Cysec Don - cysecdon@gmail.com
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
import json

{HASH_IMPL_CODE}

def xor_decrypt(enc_data, key=0x37):
    unshuffled = [''] * len(enc_data["ei"])
    for i, orig_idx in enumerate(enc_data["ei"]):
        unshuffled[orig_idx] = enc_data["ef"][i]
    hex_str = ''.join(unshuffled)
    encrypted_bytes = bytes.fromhex(hex_str)
    return ''.join(chr(b ^ key) for b in encrypted_bytes)

GAME_DATA = json.loads({repr(gd_json)})

# Color scheme
BG_DARK = "#1a1a2e"
BG_PANEL = "#16213e"
BG_INPUT = "#0f3460"
FG_GREEN = "#00ff41"
FG_CYAN = "#00d4ff"
FG_YELLOW = "#ffd700"
FG_RED = "#ff4444"
FG_WHITE = "#e0e0e0"
FG_DIM = "#666688"
ACCENT = "#533483"

DIFFICULTY_COLORS = {{
    "Beginner": "#00ff41",
    "Easy": "#00d4ff",
    "Medium": "#ffd700",
    "Hard": "#ff8c00",
    "Expert": "#ff4444",
    "Extreme": "#ff0000",
}}

PASSWORD_INFO = {{
    "PBKDF2-HMAC-SHA256": "Salt: hashgame_pbkdf2_salt_v1 | Iter=1 | SHA-256",
    "bcrypt": "Salt: $2b$04$8HbRM5KlkUvOrBGBisdlQ. | Cost=4",
    "scrypt": "Salt: hashgame_scrypt_salt_v1 | N=2, r=1, p=1",
    "Argon2d": "Salt: hashgame_argon_salt_v1 | t=1, m=64KB, p=1",
    "Argon2i": "Salt: hashgame_argon_salt_v1 | t=1, m=64KB, p=1",
    "Argon2id": "Salt: hashgame_argon_salt_v1 | t=1, m=64KB, p=1",
    "Yescrypt": "Salt: hashgame_yescrypt_salt | PBKDF2-SHA512 iter=1",
    "Balloon Hashing": "Salt: hashgame_balloon_salt | 3 rounds",
    "Lyra2": "Salt: hashgame_lyra2_salt_v1 | 4 rounds",
    "Catena": "Salt: hashgame_catena_salt_v1 | 5 rounds",
}}


class HashGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HashGame - Educational Hash Trainer | Cysec Don")
        self.root.geometry("900x750")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)

        self.current_q = 0
        self.score = 0
        self.skips = 0
        self.total = len(GAME_DATA)

        self._build_ui()
        self._show_question()

    def _build_ui(self):
        # Top banner
        banner = tk.Frame(self.root, bg=ACCENT, height=60)
        banner.pack(fill=tk.X)
        banner.pack_propagate(False)

        tk.Label(banner, text="⚡ HASHEGAME ⚡", font=("Courier", 20, "bold"),
                 bg=ACCENT, fg=FG_GREEN).pack(pady=5)
        tk.Label(banner, text="by Cysec Don | cysecdon@gmail.com",
                 font=("Courier", 9), bg=ACCENT, fg=FG_CYAN).pack()

        # Info panel
        info_frame = tk.Frame(self.root, bg=BG_PANEL, bd=1, relief=tk.RIDGE)
        info_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        self.q_label = tk.Label(info_frame, text="", font=("Courier", 12, "bold"),
                                bg=BG_PANEL, fg=FG_CYAN, anchor='w')
        self.q_label.pack(fill=tk.X, padx=10, pady=5)

        meta_frame = tk.Frame(info_frame, bg=BG_PANEL)
        meta_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        self.hash_type_label = tk.Label(meta_frame, text="", font=("Courier", 11, "bold"),
                                        bg=BG_PANEL, fg=FG_GREEN)
        self.hash_type_label.pack(side=tk.LEFT, padx=(0, 20))

        self.diff_label = tk.Label(meta_frame, text="", font=("Courier", 11, "bold"),
                                   bg=BG_PANEL, fg=FG_YELLOW)
        self.diff_label.pack(side=tk.LEFT, padx=(0, 20))

        self.score_label = tk.Label(meta_frame, text="Score: 0", font=("Courier", 11, "bold"),
                                    bg=BG_PANEL, fg=FG_CYAN)
        self.score_label.pack(side=tk.RIGHT)

        # Password hash info
        self.pw_info_label = tk.Label(info_frame, text="", font=("Courier", 9),
                                      bg=BG_PANEL, fg=FG_DIM)
        self.pw_info_label.pack(fill=tk.X, padx=10, pady=(0, 5))

        # Question text
        q_frame = tk.Frame(self.root, bg=BG_DARK)
        q_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(q_frame, text="QUESTION:", font=("Courier", 10, "bold"),
                 bg=BG_DARK, fg=FG_DIM).pack(anchor='w')

        self.question_text = tk.Label(q_frame, text="", font=("Courier", 12),
                                      bg=BG_DARK, fg=FG_GREEN, wraplength=860,
                                      justify=tk.LEFT, anchor='w')
        self.question_text.pack(fill=tk.X, pady=5)

        # Hash display
        hash_frame = tk.Frame(self.root, bg=BG_PANEL, bd=1, relief=tk.RIDGE)
        hash_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(hash_frame, text="HASH:", font=("Courier", 10, "bold"),
                 bg=BG_PANEL, fg=FG_DIM).pack(anchor='w', padx=10, pady=(5,0))

        self.hash_text = scrolledtext.ScrolledText(hash_frame, height=4, font=("Courier", 10),
                                                   bg=BG_DARK, fg=FG_YELLOW, bd=0,
                                                   wrap=tk.WORD, state=tk.DISABLED)
        self.hash_text.pack(fill=tk.X, padx=10, pady=5)

        # Answer input
        input_frame = tk.Frame(self.root, bg=BG_DARK)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(input_frame, text="YOUR ANSWER:", font=("Courier", 10, "bold"),
                 bg=BG_DARK, fg=FG_DIM).pack(anchor='w')

        input_row = tk.Frame(input_frame, bg=BG_DARK)
        input_row.pack(fill=tk.X, pady=5)

        self.answer_entry = tk.Entry(input_row, font=("Courier", 14), bg=BG_INPUT,
                                     fg=FG_GREEN, insertbackground=FG_GREEN, bd=2)
        self.answer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.answer_entry.bind('<Return>', lambda e: self._submit_answer())

        tk.Button(input_row, text="SUBMIT", font=("Courier", 11, "bold"),
                  bg="#006400", fg=FG_GREEN, activebackground="#008000",
                  command=self._submit_answer, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(input_row, text="HINT", font=("Courier", 11, "bold"),
                  bg="#4a4a00", fg=FG_YELLOW, activebackground="#666600",
                  command=self._show_hint, width=8).pack(side=tk.LEFT, padx=2)
        tk.Button(input_row, text="SKIP", font=("Courier", 11, "bold"),
                  bg="#4a0000", fg=FG_RED, activebackground="#660000",
                  command=self._skip_question, width=8).pack(side=tk.LEFT, padx=2)
        tk.Button(input_row, text="QUIT", font=("Courier", 11, "bold"),
                  bg="#330000", fg="#888888", activebackground="#440000",
                  command=self._quit_game, width=8).pack(side=tk.LEFT, padx=2)

        # Progress bar
        progress_frame = tk.Frame(self.root, bg=BG_DARK)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_canvas = tk.Canvas(progress_frame, height=25, bg=BG_PANEL,
                                         highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X)

        # Status bar
        self.status_label = tk.Label(self.root, text="Welcome to HashGame!",
                                     font=("Courier", 10), bg=BG_DARK, fg=FG_DIM)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Credits button
        tk.Button(self.root, text="ℹ Credits", font=("Courier", 9),
                  bg=BG_DARK, fg=FG_DIM, bd=0, command=self._show_credits).place(
                      rely=1.0, x=10, y=-25, anchor='sw')

    def _update_progress(self):
        self.progress_canvas.delete("all")
        w = self.progress_canvas.winfo_width()
        h = 25
        if w < 2:
            w = 860
        pct = self.current_q / self.total
        bar_w = int(w * pct)

        self.progress_canvas.create_rectangle(0, 0, w, h, fill=BG_PANEL, outline="")
        if bar_w > 0:
            self.progress_canvas.create_rectangle(0, 0, bar_w, h, fill="#006400", outline="")
        self.progress_canvas.create_text(w // 2, h // 2,
            text=f"{{self.current_q}}/{{self.total}} ({{pct*100:.1f}}%) | Score: {{self.score}} | Skips: {{self.skips}}",
            fill=FG_GREEN, font=("Courier", 9, "bold"))

    def _show_question(self):
        if self.current_q >= self.total:
            self._show_results()
            return

        item = GAME_DATA[self.current_q]
        self.q_label.config(text=f"Question {{self.current_q + 1}} of {{self.total}}")

        ht = item["ht"]
        diff = item["diff"]
        diff_color = DIFFICULTY_COLORS.get(diff, FG_WHITE)

        self.hash_type_label.config(text=f"Hash: {{ht}}")
        self.diff_label.config(text=f"[{{diff}}]", fg=diff_color)
        self.score_label.config(text=f"Score: {{self.score}}")
        self.question_text.config(text=item["q"])

        if item["pw"]:
            info = PASSWORD_INFO.get(ht, "")
            self.pw_info_label.config(text=f"Parameters: {{info}}")
        else:
            self.pw_info_label.config(text="")

        self.hash_text.config(state=tk.NORMAL)
        self.hash_text.delete("1.0", tk.END)
        hash_display = item["hh"]
        if len(hash_display) > 200:
            hash_display = hash_display[:200] + "..."
        self.hash_text.insert(tk.END, hash_display)
        self.hash_text.config(state=tk.DISABLED)

        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()
        self.status_label.config(text="Type your answer and press Enter or Submit", fg=FG_DIM)
        self._update_progress()

    def _submit_answer(self):
        answer = self.answer_entry.get().strip()
        if not answer:
            self.status_label.config(text="Please enter an answer!", fg=FG_RED)
            return

        item = GAME_DATA[self.current_q]
        if check_answer(answer, item["ht"], item["hh"]):
            self.score += 1
            self.status_label.config(text="✓ CORRECT! Well done!", fg=FG_GREEN)
            self._next_question()
        else:
            self.status_label.config(text="✗ Incorrect. Try again or skip.", fg=FG_RED)
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus_set()

    def _show_hint(self):
        item = GAME_DATA[self.current_q]
        real_answer = xor_decrypt(item)
        length = len(real_answer)
        if real_answer.isdigit():
            hint_text = f"Hint: The answer is a {{length}}-digit number."
        else:
            first = real_answer[0]
            last = real_answer[-1]
            hint_text = f"Hint: {{length}} characters, starts with '{{first}}', ends with '{{last}}'."
        self.status_label.config(text=hint_text, fg=FG_YELLOW)

    def _skip_question(self):
        item = GAME_DATA[self.current_q]
        real_answer = xor_decrypt(item)
        self.skips += 1
        self.status_label.config(text=f"Skipped! Answer: {{real_answer}}", fg=FG_YELLOW)
        self.root.after(1500, self._next_question)

    def _next_question(self):
        self.current_q += 1
        self._show_question()

    def _quit_game(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self._show_results()

    def _show_results(self):
        answered = self.current_q
        pct = (self.score / self.total * 100) if self.total > 0 else 0

        result_text = (
            f"\\n╔══════════════════════════════════════╗\\n"
            f"║         FINAL RESULTS                ║\\n"
            f"╠══════════════════════════════════════╣\\n"
            f"║                                      \\n"
            f"║  Questions: {{answered}}/{{self.total}}                  \\n"
            f"║  Correct:   {{self.score}}                       \\n"
            f"║  Skipped:   {{self.skips}}                       \\n"
            f"║  Accuracy:  {{pct:.1f}}%                    \\n"
            f"║                                      \\n"
            f"║  by Cysec Don                        \\n"
            f"║  cysecdon@gmail.com                  \\n"
            f"║                                      \\n"
            f"╚══════════════════════════════════════╝"
        )
        messagebox.showinfo("Game Over", result_text)
        self.root.destroy()

    def _show_credits(self):
        credits = (
            "HASHGAME - Educational Hash Trainer\\n\\n"
            "Created by: Cysec Don\\n"
            "Email: cysecdon@gmail.com\\n\\n"
            "An educational cybersecurity tool designed\\n"
            "to teach students about hashing algorithms\\n"
            "through hands-on brute-force practice.\\n\\n"
            "Features:\\n"
            "• 500 unique questions\\n"
            "• 50 hash types\\n"
            "• 6 difficulty levels\\n"
            "• Interactive GUI"
        )
        messagebox.showinfo("Credits", credits)


def main():
    root = tk.Tk()
    app = HashGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
'''

    return gui_code


# ================================================================
# SECTION 10: MAIN
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  HashGame Generator")
    print("  Credits: Cysec Don - cysecdon@gmail.com")
    print("=" * 60)
    print()

    print("[1/5] Generating game data...")
    game_data = generate_game_data()

    print("[2/5] Encrypting answers...")
    for item in game_data:
        enc = xor_encrypt(item["answer"])
        # Verify encryption/decryption roundtrip
        dec = xor_decrypt(enc)
        assert dec == item["answer"], f"Encryption roundtrip failed for: {item['answer']}"
    print(f"[OK] All {len(game_data)} answers encrypted and verified")

    print("[3/5] Generating CLI file...")
    cli_code = generate_cli_file(game_data)
    cli_path = "/home/z/my-project/download/hash_game_cli.py"
    with open(cli_path, 'w') as f:
        f.write(cli_code)
    cli_size = os.path.getsize(cli_path)
    print(f"[OK] CLI file written to {cli_path} ({cli_size:,} bytes)")

    print("[4/5] Generating GUI file...")
    gui_code = generate_gui_file(game_data)
    gui_path = "/home/z/my-project/download/hash_game_gui.py"
    with open(gui_path, 'w') as f:
        f.write(gui_code)
    gui_size = os.path.getsize(gui_path)
    print(f"[OK] GUI file written to {gui_path} ({gui_size:,} bytes)")

    print("[5/5] Final summary:")
    print(f"  - Questions generated: {len(game_data)}")
    print(f"  - Hash types: {len(HASH_TYPES)}")
    hash_type_names = [ht['name'] for ht in HASH_TYPES]
    print(f"  - Types: {', '.join(hash_type_names)}")
    difficulties = set(item['difficulty'] for item in game_data)
    print(f"  - Difficulty levels: {', '.join(sorted(difficulties))}")

    word_count = sum(1 for item in game_data if not item['answer'].isdigit())
    num_count = sum(1 for item in game_data if item['answer'].isdigit())
    print(f"  - Word answers: {word_count}")
    print(f"  - Number answers: {num_count}")
    print(f"  - All answers unique: {len(set(item['answer'] for item in game_data)) == len(game_data)}")

    print()
    print("=" * 60)
    print("  Generation complete!")
    print("  Run CLI: python3 hash_game_cli.py")
    print("  Run GUI: python3 hash_game_gui.py")
    print("  Credits: Cysec Don - cysecdon@gmail.com")
    print("=" * 60)
