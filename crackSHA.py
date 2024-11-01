#!/usr/bin/env python3
import argparse
import hashlib
import base64
import time
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='SHA1 Password Cracking Script')
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
                if hash_part.startswith('{SHA}'):
                    hash_b64 = hash_part[5:]
                    hashes[username] = hash_b64
        return hashes
    except FileNotFoundError:
        print(f"ERROR: Hash file '{hashfile}' not found.")
        exit(1)

def crack_sha1(hashfile, wordlist):
    hashes = load_hashes(hashfile)
    cracked = {}
    total_hashes = len(hashes)
    start_time = time.time()

    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as wl:
            for line_number, password in enumerate(wl, 1):
                password = password.strip()
                sha1_digest = hashlib.sha1(password.encode('utf-8')).digest()
                sha1_b64 = base64.b64encode(sha1_digest).decode('utf-8')

                for user, stored_hash in hashes.items():
                    if user not in cracked and sha1_b64 == stored_hash:
                        cracked[user] = password
                        print(f"[+] Cracked: {user} => {password}")

                if len(cracked) == total_hashes:
                    break

        end_time = time.time()
        print("\n=== Cracking Completed ===")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Total attempts: {line_number}")
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
    crack_sha1(args.hashfile, args.wordlist)

if __name__ == "__main__":
    main()
