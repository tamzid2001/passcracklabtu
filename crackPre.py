#!/usr/bin/env python3
import argparse
import hashlib
import base64
import time
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Precomputed SHA1 Password Cracking Script')
    parser.add_argument('hashfile', help='Path to the hashed password file')
    parser.add_argument('precomp_dir', help='Path to the precomputed hashes directory')
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
                    hash_bytes = base64.b64decode(hash_b64)
                    hash_hex = hash_bytes.hex().upper()
                    hashes[username] = hash_hex
        return hashes
    except FileNotFoundError:
        print(f"ERROR: Hash file '{hashfile}' not found.")
        exit(1)
    except base64.binascii.Error:
        print(f"ERROR: Invalid Base64 encoding in hash file '{hashfile}'.")
        exit(1)

def crack_precomputed(hashfile, precomp_dir):
    hashes = load_hashes(hashfile)
    cracked = {}
    total_hashes = len(hashes)
    start_time = time.time()

    try:
        for user, hash_hex in hashes.items():
            if user in cracked:
                continue
            prefix = hash_hex[:2]
            precomp_file = os.path.join(precomp_dir, f"{prefix}.txt")
            if not os.path.isfile(precomp_file):
                continue
            with open(precomp_file, 'r', encoding='utf-8', errors='ignore') as pc:
                for line_number, password in enumerate(pc, 1):
                    password = password.strip()
                    sha1_digest = hashlib.sha1(password.encode('utf-8')).digest()
                    sha1_hex = sha1_digest.hex().upper()
                    if sha1_hex == hash_hex:
                        cracked[user] = password
                        print(f"[+] Cracked: {user} => {password}")
                        break

        end_time = time.time()
        print("\n=== Precomputed Cracking Completed ===")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Passwords Cracked: {len(cracked)}/{total_hashes}")

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        exit(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        exit(1)

def main():
    clear_terminal()
    args = parse_arguments()
    crack_precomputed(args.hashfile, args.precomp_dir)

if __name__ == "__main__":
    main()
