# Password Cracking Lab

Assignment 1
For this assignment, please submit a single pdf document that contains
your answers and screenshots. Be sure to include your name and student
id number in your document. Please submit your document with the
following file name:
Csci###_M0?_last name_ first letter of firstname.pdf
E.g.: If your name is John Adams then you should submit
csci330_M01_adams_j.pdf.
Your objective for this assignment to perform several access control tasks on
Linux machine. This will allow you to gain experience with virtualization, access
control mechanisms, and the GNU/Linux environment. Whenever you are
confused about how a command works, simply type "man command" to see
the manual page for that program or command.
For this lab you need to download Ubuntu Linux on your machine (i.e.,
Windows or Mac).
You can find online Installation resources.
Note: for Mac users, please follow instructions based on intel, M1 or M2 chip
on your machine.
https://www.youtube.com/watch?v=O19mv1pe76M
How To Install Ubuntu 22.10 On M1 or M2 Mac || RUN NEW
Ubuntu On ANY Mac W/ Apple Silicon Using UTM
Hint: Enable Apple Virtualization if your MacOS is operating on an M1 or M2 chip
Upon successful installation, you are all set for your assignment,
below!

Installing on Linux
If you want to install the basic Git tools on Linux via a binary installer, you can generally do so through the package management tool that comes with your distribution. If you’re on Fedora (or any closely-related RPM-based distribution, such as RHEL or CentOS), you can use dnf:

$ sudo dnf install git-all
If you’re on a Debian-based distribution, such as Ubuntu, try apt:

$ sudo apt install git-all

## **Overview**

Welcome to the **Password Cracking Lab**! The goal of this lab is to familiarize you with password files and some elementary password cracking schemes. Through hands-on exercises, you will learn about the security mechanisms in place for password management and understand the vulnerabilities associated with weak or common passwords.

## **Table of Contents**

1. [Getting Started](#getting-started)
2. [Task 1: Password Files](#task-1-password-files)
3. [Task 2: Dictionary Attacks](#task-2-dictionary-attacks)
4. [Task 3: Considering Execution Time](#task-3-considering-execution-time)
5. [Task 4: Personal Experimentation](#task-4-personal-experimentation)
6. [Submission](#submission)
7. [Appendix – Some Unix Commands](#appendix--some-unix-commands)
8. [Scripts](#scripts)
9. [Additional Notes](#additional-notes)

## **Getting Started**

### **A. Boot Your Linux System or VM**

1. **Launch Labtainer VM**:
   - If you haven't already, start your Labtainer VM. The pre-packaged Labtainer VM will open with a terminal window.

Ubuntu Instruction 

Install python via terminal: 
sudo apt update && sudo apt install python3

Download pass crack file:
git clone https://github.com/tamzid2001/passcracklabtu.git

Update your current file to be up to date:
git pull

Create a password file;
htpasswd -sc htpasswd-me alice

or for MD5:
htpasswd -mc htpasswd-me alice

You can add other entries by doing the following (slightly modified) command:
htpasswd -s htpasswd-me bob

## **Task 1: Password Files**

In this task, you will briefly examine how your Linux system manages and stores user passwords.

### **Steps:**

1. **View `/etc/passwd` File**:
   - Use the `more` command to view the `/etc/passwd` file:
     ```bash
     more /etc/passwd
     ```
   - **Observation**: This file lists all users with potential login access. Notice that password digests are not present here.

2. **View `/etc/shadow` File**:
   - Attempt to view the shadow password file:
     ```bash
     more /etc/shadow
     ```
   - **Expected Outcome**: You should receive an error message indicating insufficient permissions.

3. **Record Error Message**:
   - **Item #1**: Note the error message received when attempting to view `/etc/shadow`.

4. **Access `/etc/shadow` with Root Privileges**:
   - Use `sudo` to gain root privileges and view the shadow file:
     ```bash
     sudo more /etc/shadow
     ```
   - **Observation**: You will be prompted for your password. Upon successful authentication, you can view the contents of the shadow password file.

5. **Understand Shadow File Structure**:
   - Each line in `/etc/shadow` represents a user account, with fields separated by `:`:
     - **a.** Login name
     - **b.** Digest (hashed password)
     - **c.** Date of last password change
     - **d.** Minimum password age
     - **e.** Maximum password age
     - **f.** Password warning period
     - **g.** Password inactivity period
     - **h.** Account expiration date
     - **i.** Reserved

6. **Identify Hash Function and Salt**:
   - The digest field is further divided by `$`:
     ```
     $ID$salt$digest
     ```
   - **Interpretation**:
     - **ID**: Number corresponding to the hash function/algorithm.
     - **Salt**: Value used to salt the hash.
     - **Digest**: The actual hashed password.
   - **Tasks**:
     - **Item #3**: Determine and record the hash function used for your password.
     - **Item #4**: Record the salt value used.

7. **List Account Information**:
   - Execute the `chage` command to list account information:
     ```bash
     chage -l student
     ```
   - **Task**:
     - **Item #5**: Record the date when your password was chosen.

---

## **Task 2: Dictionary Attacks**

In this task, you will perform dictionary attacks to crack the contents of a password file.

### **Getting Started**
In this case, please create the respective password files using different cryptography flags. You can find it in this link here: https://httpd.apache.org/docs/trunk/programs/htpasswd.html
1. **View `htpasswd-sha1` File**:
   - Use the `cat` command:
     ```bash
     cat htpasswd-sha1
     ```
   - **Observation**: This file is in htpasswd format, used by Apache for password-based access control.

2. **Examine Digest Values**:
   - **Task**:
     - **Item #7**: Record the users that have selected the same password based on digest values.

### **Simple Dictionary Attack**

### **Common Password Dictionary Attack**

Use a larger wordlist to increase the chances of cracking more passwords.

1. **Execute `crackSHA.py` with `biglist.txt`**:
   ```bash
   ./crackSHA.py htpasswd-sha1 biglist.txt
   ```
2. **Tasks**:
   - **Item #9**: Record the username(s) and password(s) of the accounts cracked using `biglist.txt`.
   - **Item #10**: Record the number of words attempted, number of passwords cracked, and the time taken.

**Note**: Running in a VM and using an interpreted script may slow down the cracking process.

---

## **Task 3: Considering Execution Time**

Compare the execution time of various hash functions.

1. **Crack MD5-Hashed Passwords**:
   ```bash
   ./crackMD5.py htpasswd-md5 biglist.txt
   ```
   - **Task**:
     - **Item #12**: Record the number of words attempted, number of passwords cracked, and time taken.

2. **Speed Comparison Analysis**:
   - **Task**:
     - **Item #10**: Use recorded data to estimate the time required for a brute force attack on 15-character passwords using SHA1.

---

## **Task 4: Personal Experimentation**

Experiment with your own passwords to understand the cracking process.

### **Steps:**

1. **Create Your Own Password File**:
   - **Initial User (`alice`)**:
     ```bash
     htpasswd -sc htpasswd-me alice
     ```
     - You will be prompted to enter and confirm a password for `alice`.

   - **Add Additional Users (`bob`, etc.)**:
     ```bash
     htpasswd -s htpasswd-me bob
     ```
     - Enter and confirm the password when prompted.
     - Repeat to add more users as desired.

2. **Display `htpasswd-me` File**:
   ```bash
   cat htpasswd-me
   ```

3. **Perform Pre-Calculated Attack**:
   ```bash
   ./crackPre.py htpasswd-me ./output
   ```
4. **Task**:
   - **Item #20**: Record the results of your experiments without disclosing any actual passwords used.

5. **Complete Remaining Items**:
   - **Items #21 and #22**: Follow the worksheet instructions to complete these entries.

---

## **Submission**

After completing the lab:

1. **Stop the Lab**:
   ```bash
   stoplab pass-crack
   ```

2. **Ensure Report is Saved**:
   - If you edited the lab report or spreadsheet on a different system, copy those completed files into the displayed directory paths before stopping the lab.

3. **Provide Results**:
   - After stopping the lab, a path to the zipped lab results will be displayed. Provide this file to your instructor via the designated platform (e.g., Sakai).

---

## **Appendix – Some Unix Commands**

A quick reference to basic Unix commands used throughout the lab:

- **`cd`**: Change the current directory.
  ```bash
  cd destination
  ```
  - No "destination": Changes to the home directory.
  - `..`: Changes to the parent directory.

- **`cp`**: Copy a file.
  ```bash
  cp source destination
  ```

- **`clear`**: Erase all terminal output and place the shell prompt at the top.

- **`less`**: Display a text file one page at a time.
  ```bash
  less file
  ```
  - Navigate with space bar, Enter key, and quit with `q`.

- **`ls`**: List directory contents.
  ```bash
  ls [location or file]
  ```
  - No arguments: Lists current directory contents.

- **`man`**: Display the manual page for a command.
  ```bash
  man command
  ```

- **`more`**: Similar to `less`, display a file one page at a time.
  ```bash
  more file
  ```

- **`mv`**: Move or rename a file/directory.
  ```bash
  mv source destination
  ```

- **`pwd`**: Display the present working directory.
  ```bash
  pwd
  ```

---

## **Scripts**

### **1. `crackSHA.py`**

*Cracks SHA1-hashed passwords using a provided wordlist.*

```python
# [Include the `crackSHA.py` script provided earlier]
```

### **2. `crackMD5.py`**

*Cracks standard MD5-hashed passwords using a provided wordlist.*

```python
# [Include the updated `crackMD5.py` script provided above]
```

### **3. `crackPre.py`**

*Performs precomputed dictionary attacks using sorted hash files.*

```
sudo python3 ./crackPre.py htpasswd-me ./output
```

### **4. `precompute.py`** *(Optional but Recommended)* The output filde is already provided to you as the output directory.

*Precomputes and sorts SHA1 hashes from the wordlist into separate files based on the first two hex digits of each hash.*

```python
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
    parser = argparse.ArgumentParser(description='Precompute SHA1 Hashes')
    parser.add_argument('wordlist', help='Path to the wordlist file')
    parser.add_argument('precomp_dir', help='Directory to store precomputed hashes')
    args = parser.parse_args()

    precompute_hashes(args.wordlist, args.precomp_dir)

if __name__ == "__main__":
    main()
```

### **Usage Example**

```bash
python3 precompute.py biglist.txt calc
```

---

## **Additional Notes**

### **1. Python Environment**

- **Python Version**: Ensure all students use Python 3.x.
  
- **Virtual Environments**: It's recommended to use virtual environments to manage dependencies.
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Unix/Linux/macOS
  .\venv\Scripts\activate   # On Windows
  ```

### **2. Performance Considerations**

- **Large Wordlists**: Cracking large wordlists can be resource-intensive. Ensure that the Labtainer VM has adequate processing power and memory.
  
- **Optimizations**:
  - **Parallel Processing**: Implement multithreading or multiprocessing to speed up cracking.
  - **Efficient Data Structures**: Utilize sets or dictionaries for faster lookups if applicable.

### **3. Ethical and Security Considerations**

- **Ethical Use**: Emphasize that password cracking should only be performed in controlled, authorized environments for educational purposes.
  
- **Legal Implications**: Unauthorized access to systems is illegal and unethical.

### **4. Troubleshooting**

- **Permission Issues**: Ensure that scripts have execute permissions and that students are running commands with appropriate privileges.
  
- **File Paths**: Adapt file paths according to the operating system (use `./` for Unix-like systems and `.\\` for Windows if necessary).

- **Line Endings**: Be cautious of line ending differences between Windows (`CRLF`) and Unix-like systems (`LF`).

---

By following this guide and utilizing the provided scripts, your graduate-level class will gain a comprehensive understanding of password security, hashing mechanisms, and the practical aspects of password cracking. Ensure that all students are aware of the ethical considerations and use these tools responsibly within the confines of the lab environment.

If you have any further questions or require additional assistance, feel free to reach out!

---
