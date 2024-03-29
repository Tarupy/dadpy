import requests
import string
import random
import argparse
import sys

def getRandomString(length):
    pool = string.ascii_lowercase + string.digits
    return "".join(random.choice(pool) for i in range(length))

def getRandomText(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def getCustomEmail(email_file):
    with open(email_file, "r") as file:
        emails = file.read().splitlines()
    if len(emails) == 0:
        sys.exit("Email file is empty.")
    return random.choice(emails)

def generate(email_file):
    nick = getRandomText(8)
    passw = "parkshit01"
    email = getCustomEmail(email_file)

    headers = {
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US",
        "App-Platform": "Android",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "spclient.wg.spotify.com",
        "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
        "Spotify-App-Version": "8.6.72",
        "X-Client-Id": getRandomString(32)
    }

    payload = {
        "creation_point": "client_mobile",
        "gender": "male" if random.randint(0, 1) else "female",
        "birth_year": random.randint(1990, 2000),
        "displayname": nick,
        "iagree": "true",
        "birth_month": random.randint(1, 11),
        "password_repeat": passw,
        "password": passw,
        "key": "142b583129b2df829de3656f9eb484e6",
        "platform": "Android-ARM",
        "email": email,
        "birth_day": random.randint(1, 20)
    }

    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload)

    if r.status_code == 200:
        if r.json()['status'] == 1:
            return (True, nick + ":" + r.json()["username"] + ":" + email + ":" + passw)
        else:
            return (False, "Could not create the account, some errors occurred")
    else:
        return (False, "Could not load the page. Response code: " + str(r.status_code))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help="how many accounts to generate, default is 1",
                        type=lambda x: (int(x) > 0) and int(x) or sys.exit("Invalid number: minimum amount is 1"))
    parser.add_argument("-o", "--output", help="output file, default prints to the console")
    parser.add_argument("-e", "--email-file", help="file containing the list of emails", required=True)  # Make the email-file option required
    args = parser.parse_args()

    N = args.number if args.number else 1
    file = open(args.output, "a") if args.output else sys.stdout

    print("Generating accounts in the following format:", file=sys.stdout)
    print("NICKNAME:USERNAME:EMAIL:PASSWORD\n", file=sys.stdout)

    # Read existing accounts from the output file, if provided
    existing_accounts = set()
    if args.output:
        with open(args.output, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 2:
                    existing_accounts.add(parts[1])

    generated_accounts = 0
    while generated_accounts < N:
        result = generate(args.email_file)
        if result[0]:
            _, username, _, _ = result[1].split(":")
            if username not in existing_accounts:
                print(result[1], file=file)
                if file is not sys.stdout:
                    print(result[1], file=sys.stdout)
                generated_accounts += 1
        else:
            print(str(generated_accounts + 1) + "/" + str(N) + ": " + result[1], file=sys.stdout)

    if file is not sys.stdout:
        file.close()
