# BrutalFlask

## ⚠️ Disclaimer
This is for **educational and ethical use only**. DO NOT use it on systems you do not have explicit permission to access.

## 📖 Introduction
In this lab, I explored how password brute-forcing works by building a self-contained, localhost-safe Flask web application designed for penetration testing exercises. I also examined defenses against password brute-forcing, such as automatic soft account lockouts after a certain number of failed attempts and progressive login delays.

## 🔑🔤🛠️ Key Components and Technologies
- Python
- Flask

## 🚀 How to Run
```bash
pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt

python3 app.py
```

ℹ️To access the web application go to [http://localhost:8088/](http://localhost:8088/).

Then launch the attack script:
```
python3 attack.py \
  --target-url <target-url> \
  --usernames-file <usernames-file> \
  --passwords-file <passwords-file> \
  --valid-login-regex <regex-for-valid-login> \
  --continue-if-found <true/false> \
  --delay <seconds>
```
For this lab exercise, replace \<target-url\> with ```"http://localhost:8088/"``` and use the following regex for \<regex-for-valid-login\>:```"Welcome [^.!]|^((?!Invalid|account locked).)*$"```

Example command:
```
python3 attack.py \
  --target-url "http://localhost:8088/" \
  --usernames-file "usernames.txt" \
  --passwords-file "passwords.txt" \
  --valid-login-regex "Welcome [^.!]|^((?!Invalid|account locked).)*$" \
  --continue-if-found false \
  --delay 0.5
```
## 📸Screenshots
![BrutalFlask](https://github.com/kvang138/BrutalFlask/blob/main/Screenshots/BrutalFlask.png)

## 💡Conclusion
To prevent your account from being compromised by always use at least the industry-standard length and complexity for passwords, enable multi-factor authentication (MFA), and change your password immediately if you suspect a compromise. For example, use at least four unrelated passphrases combined (such as Dragon-Magnet-Bifrost-Bridge-2028!) instead of something like p@ssW0rd2026!. Avoid passwords that appear in data breaches and common passwords. Check whether your credentials have been exposed using a trusted service such as Have I Been Pwned. Organizations and websites should implement strong protections, including:

- Rate limiting (e.g., a maximum number of login attempts within a specific time window)
- Services like Cloudflare to detect and block suspected malicious bot activity in real time
- CAPTCHA challenges to stop automated login attempts

On the backend, never store passwords in plaintext. Instead, use modern, secure hashing algorithms such as Argon2 or bcrypt with unique salts per password. This greatly increases the computational cost and length of time of the offline brute-force attacks.

