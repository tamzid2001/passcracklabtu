#!/usr/bin/env python3
import argparse
import time
import os
import hashlib

def parse_arguments():
    parser = argparse.ArgumentParser(description='MD5 Password Cracking Script for Apache $apr1$ hashes')
    parser.add_argument('hashfile', help='Path to the hashed password file')
    parser.add_argument('wordlist', help='Path to the wordlist file')
    return parser.parse_args()

def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def load_hashes(hashfile):
    hashes = {}
    try:
        with open(hashfile, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                username, hash_part = line.split(':', 1)
                hash_part = hash_part.strip()
                hashes[username] = hash_part
        return hashes
    except FileNotFoundError:
        print(f"ERROR: Hash file '{hashfile}' not found.")
        exit(1)

def to64(value, length):
    # Converts an integer to a base64-like string with the specified length
    chars = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    result = ''
    while length > 0:
        result += chars[value & 0x3f]
        value >>= 6
        length -= 1
    return result

def apr1_crypt(password, salt):
    # Apache's MD5-based password algorithm implementation
    magic = '$apr1$'
    if salt.startswith(magic):
        salt = salt[len(magic):]
    salt = salt.split('$')[0]
    max_length = 8
    salt = salt[:max_length]

    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    magic_bytes = magic.encode('utf-8')

    # Initial MD5 digest
    md5_initial = hashlib.md5()
    md5_initial.update(password_bytes + magic_bytes + salt_bytes)

    # Intermediate MD5 digest
    md5_intermediate = hashlib.md5()
    md5_intermediate.update(password_bytes + salt_bytes + password_bytes)

    intermediate_result = md5_intermediate.digest()

    # Loop to handle password length
    password_length = len(password)
    for i in range(password_length, 0, -16):
        md5_initial.update(intermediate_result[:min(16, i)])

    # Append null bytes based on password bits
    i = password_length
    while i:
        if i & 1:
            md5_initial.update(b'\x00')
        else:
            md5_initial.update(password_bytes[:1])
        i >>= 1

    final_result = md5_initial.digest()

    # 1000 rounds of MD5
    for i in range(1000):
        md5_loop = hashlib.md5()
        if i % 2:
            md5_loop.update(password_bytes)
        else:
            md5_loop.update(final_result)
        if i % 3:
            md5_loop.update(salt_bytes)
        if i % 7:
            md5_loop.update(password_bytes)
        if i % 2:
            md5_loop.update(final_result)
        else:
            md5_loop.update(password_bytes)
        final_result = md5_loop.digest()

    # Reorder the bytes for final hash
    reordered = b''
    # Corrected indices based on Apache's implementation
    indices = [
        (0, 6, 12),
        (1, 7, 13),
        (2, 8, 14),
        (3, 9, 15),
        (4, 10, 5),
        (11,)
    ]

    for idx in indices[:-1]:
        a, b, c = idx
        l = (final_result[a] << 16) | (final_result[b] << 8) | final_result[c]
        reordered += to64(l, 4).encode('utf-8')

    # Handle the last index separately
    l = final_result[indices[-1][0]]
    reordered += to64(l, 2).encode('utf-8')

    return f'{magic}{salt}${reordered.decode("utf-8")}'

def crack_md5(hashfile, wordlist):
    hashes = load_hashes(hashfile)
    cracked = {}
    total_hashes = len(hashes)
    start_time = time.time()
    total_attempts = 0

    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as wl:
            for password in wl:
                password = password.strip()
                total_attempts += 1

                for user, stored_hash in hashes.items():
                    if user in cracked:
                        continue

                    # Get salt from stored_hash
                    if stored_hash.startswith('$apr1$'):
                        salt = stored_hash.split('$')[2]
                        generated_hash = apr1_crypt(password, salt)
                        if generated_hash == stored_hash:
                            cracked[user] = password
                            print(f"[+] Cracked: {user} => {password}")
                    else:
                        continue  # Skip if not an Apache MD5 hash

                if len(cracked) == total_hashes:
                    break

        end_time = time.time()
        print("\n=== Cracking Completed ===")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Total attempts: {total_attempts}")
        print(f"Passwords Cracked: {len(cracked)}/{total_hashes}")

    except FileNotFoundError:
        print(f"ERROR: Wordlist file '{wordlist}' not found.")
        exit(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        exit(1)

def main():
    clear_terminal()
    args = parse_arguments()
    crack_md5(args.hashfile, args.wordlist)

if __name__ == "__main__":
    main()
