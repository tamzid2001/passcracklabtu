#!/usr/bin/env python3
import argparse
import time
import os
import crypt  # Import the crypt module for password hashing

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
                hash_part = hash_part.strip()
                hashes[username] = hash_part
        return hashes
    except FileNotFoundError:
        print(f"ERROR: Hash file '{hashfile}' not found.")
        exit(1)

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

                    # Use crypt.crypt to hash the password with the salt from stored_hash
                    if crypt.crypt(password, stored_hash) == stored_hash:
                        cracked[user] = password
                        print(f"[+] Cracked: {user} => {password}")

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
