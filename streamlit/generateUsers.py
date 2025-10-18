
USERS = {
    "teste": "1234"
}

def validate_user(username, password):
    if username in USERS and USERS[username] == password:
        return True
    return False