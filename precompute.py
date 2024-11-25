#!/usr/bin/env python3
import hashlib
import os

def precompute_hashes(wordlist, precomp_dir):
    if not os.path.exists(precomp_dir):
        os.makedirs(precomp_dir)

    with open(wordlist, 'r', encoding='utf-8', errors='ignore') as wl:
        for line_number, password in enumerate(wl, 1):
            password = password.strip()
            sha1_digest = hashlib.sha1(password.encode('utf-8')).digest()
            sha1_hex = sha1_digest.hex().upper()
            prefix = sha1_hex[:2]
            precomp_file = os.path.join(precomp_dir, f"{prefix}.txt")
            with open(precomp_file, 'a', encoding='utf-8') as pc:
                pc.write(password + '\n')

            if line_number % 100000 == 0:
                print(f"Processed {line_number} passwords.")

    print("Precomputation Completed.")

def main():
    wordlist = 'biglist.txt'  # Replace with your wordlist path
    precomp_dir = 'output'      # Replace with your desired precomputed directory
    precompute_hashes(wordlist, precomp_dir)

if __name__ == "__main__":
    main()
