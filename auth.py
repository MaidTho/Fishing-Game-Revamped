import os
import bcrypt 

class Auth:
    def __init__(self, user_file='users.txt'):
        self.user_file = user_file

    def register(self, username, password):
        if self.user_exists(username):
            print("Username already exists. Please choose another.")
            return False

        hashed_password = self.hash_password(password)
        with open(self.user_file, 'a') as file:
            file.write(f"{username}:{hashed_password.decode()}\n")
        print("Registration successful!")
        return True

    def login(self, username, password):
        if not self.user_exists(username):
            print("Username does not exist.")
            return False
        
        with open(self.user_file, 'r') as file:
            for line in file:
                user, hashed_pwd = line.strip().split(':')
                if user == username and self.check_password(password.encode(), hashed_pwd.encode()):
                    print("Login successful!")
                    return True
        
        print("Incorrect password.")
        return False

    def user_exists(self, username):
        if not os.path.exists(self.user_file):
            return False

        with open(self.user_file, 'r') as file:
            for line in file:
                user, _ = line.strip().split(':')
                if user == username:
                    return True
        return False

    def hash_password(self, password):
        # Hash the password with bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password, hashed_password):
        # Check if the provided password matches the hashed password
        return bcrypt.checkpw(password, hashed_password)
