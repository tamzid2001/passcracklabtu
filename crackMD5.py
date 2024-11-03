#!/usr/bin/env python3
import argparse
import hashlib
import time
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='MD5 Password Cracking Script')
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
                # Assuming the hash is a standard MD5 hex digest
                if len(hash_part) == 32 and all(c in '0123456789abcdefABCDEF' for c in hash_part):
                    hashes[username] = hash_part.lower()
        return hashes
    except FileNotFoundError:
        print(f"ERROR: Hash file '{hashfile}' not found.")
        exit(1)

def crack_md5(hashfile, wordlist):
    hashes = load_hashes(hashfile)
    cracked = {}
    total_hashes = len(hashes)
    start_time = time.time()

    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as wl:
            for line_number, password in enumerate(wl, 1):
                password = password.strip()
                md5_digest = hashlib.md5(password.encode('utf-8')).hexdigest()

                for user, stored_hash in hashes.items():
                    if user not in cracked and md5_digest == stored_hash:
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
    crack_md5(args.hashfile, args.wordlist)

if __name__ == "__main__":
    main()
