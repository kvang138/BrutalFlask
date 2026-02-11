from flask import Flask, request, redirect, url_for, session
from datetime import datetime
from threading import Timer
from collections import defaultdict

app = Flask(__name__)

# Simulated users database for simplicity
USERS_DB = {
    "admin" : "sD77LSKzJsxc94Jx88",
    "root" : "fCbd8a4k7Vf3RSNjZ8",
    "alice" : "Y8sR7Qs9a6gG9wG866",
    "bob" : "Z87uZP6ujNbrgh9AR7"
}

PORT = 8088
MAX_ATTEMPTS = 5
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "login_attempts.log"
SECONDS_UNTIL_UNLOCK = 360
SECRET_FILE = ".secret"

# Keep track of the logins
logins = defaultdict(dict)

# Read file
def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except:
        return ""

# Unlock the locked the specific account
def unlock_account(username, delay):
     logins[username]["attempts"] = 0
     logins[username]["isLocked"] = False

     log(LOG_FILE, f"[{datetime.now().strftime(TIMESTAMP_FORMAT)}] User {username} unlocked after {delay} seconds.\n")
     print(f"[{datetime.now().strftime(TIMESTAMP_FORMAT)}] User {username} unlocked after {delay} seconds.\n")

# Wait the failed login to logs
def log(log_file, data):
    with open(log_file, 'a') as log:
        log.write(data)

@app.route('/login', methods = ["GET", "POST"])
def login():
    # Handle the POST request
    if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')

            if username == "":
                 return "<strong>ℹ️ Please enter a username.</strong>"
            
            if password == "":
                 return "<strong>ℹ️ Please enter a password.</strong>"
            
            # If not a valid user on the system.
            if username not in USERS_DB:
                log(LOG_FILE, f"[{datetime.now().strftime(TIMESTAMP_FORMAT)}] Log in failed for {username}:{password} from {request.remote_addr} with {request.user_agent}.\n")

                return "❌ Invalid username or password."
            
            # Add the valid user to the login dictionary for tracking states
            if username not in logins:
                 logins[username] = {}

            # Show the user that the account is locked.
            if logins[username].get("isLocked", False) == True:
                return "🚫Account locked due to too many failed attempts. Please try again later."

            # If the password is invalid.
            if username in USERS_DB and USERS_DB[username] != password:
                logins[username]["attempts"] = logins[username].get("attempts", 0) + 1

                 # Lock the account after x attempts
                if logins[username].get("attempts", 0) >= MAX_ATTEMPTS:
                    if logins[username].get("isLocked", False) == False:
                        logins[username]["isLocked"] = True

                         # Unlock the locked the specific account after x seconds
                        Timer(SECONDS_UNTIL_UNLOCK, unlock_account, args=[username, SECONDS_UNTIL_UNLOCK]).start()
                    
                        return "🚫Account locked due to too many failed attempts."
                else:
                    log(LOG_FILE, f"[{datetime.now().strftime(TIMESTAMP_FORMAT)}] Log in failed for {username}:{password} from {request.remote_addr} with {request.user_agent}.\n")

                    return "❌ Invalid username or password."

            # The provided login credentials are valid.    
            logins[username]["attempts"] = 0
            session["username"] = username
            session.permanent = False

            # Log the log in.
            log(LOG_FILE, f"[{datetime.now().strftime(TIMESTAMP_FORMAT)}] User {username} logged in successfully from {request.remote_addr} with {request.user_agent}.\n")

            # Redirect the user to the home page.
            return redirect(url_for("home"))
    
    # The GET request
    return """
        <form method="POST">
            Username: <input type="text" name="username"/><br/>
            Password: <input type="text" name="password"/><br/>
            <input type="submit" value="Log in"/>
        </form>
        """

# Log the user out of the system
@app.route("/logout", methods = ["GET"])
def log_out():
    username = session.get("username")

    if username is None:
          return redirect(url_for("home"))
     
    try:
        logins.pop(username)
    except:
        None

    session.pop("username", None)

    return redirect(url_for("home"))

# The home page
@app.route('/', methods = ["GET"])
def home():
    # redirect to login if haven't logged in
    username = session.get("username")

    if username is None:
            return redirect(url_for("login"))
    
    # If the user has already logged into the system.
    return f"""
        <h1><strong>Welcome {username}!</strong></h1>
        <br/>
        <a href="/logout">Log out</a>
        """

if __name__ == "__main__":
    # Read the secret from the secret file and set the secret to use for the session objects
    secrect_key = read_file(SECRET_FILE).strip()

    # Do not start the server if the secret file is empty
    if secrect_key == "":
         print(f"[{datetime.now().strftime(TIMESTAMP_FORMAT)}]ℹ️ Invalid .secret file.")
         exit(1)
    else:
         app.secret_key = secrect_key
    
    # start the Flask server
    print(f"Starting web application on port {PORT}.")

    app.run(port=PORT)








