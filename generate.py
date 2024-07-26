from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Schlüssel generiert und in 'secret.key' gespeichert.")

generate_key()
print("nur einmal machen")