import os
import getpass
import json
import cryptography
from cryptography.fernet import Fernet
import pyperclip

def main():
    key = load_key()
    
    if verify_password():
        print("Verifizierung erfolgreich!")
    
        while True:
            choice = main_menu()
    
            match choice:
                
                case "1":
                    print("Lege ein neues Konto an!")
                    konto = query_name()
                    password = query_password()
                    
                    data = json.dumps({"benutzername": konto, "passwort": password})
                    encrypted_data = encrypt_data(data, key)
                    save_encrypted_data(encrypted_data)
                    print("Daten wurden sicher gespeichert.")
                    
                case "2":
                    encrypted_data = load_encrypted_data()
                    if encrypted_data:
                        data = decrypt_data(encrypted_data, key)
                        if data:
                            credentials = json.loads(data)
                            print(f"Gespeicherte Daten: Benutzername: {credentials['benutzername']}")
                            if input("Möchten Sie das Passwort in die Zwischenablage kopieren? (ja/nein): ").lower() == "ja":
                                pyperclip.copy(credentials['passwort'])
                                print("Passwort wurde in die Zwischenablage kopiert. Sie können es jetzt mit STRG+V einfügen.")
                            else:
                                print("Passwort wurde nicht in die Zwischenablage kopiert.")
                    
                case "3":
                    print("Gebe ein bestehendes Konto an: ")
                    konto = query_name()
                    print("Gebe ein NEUES Passwort an: ")
                    new_password = query_password()

                    encrypted_data = load_encrypted_data()
                    data = decrypt_data(encrypted_data, key)
                    credentials = json.loads(data)
                    if credentials['benutzername'] == konto:
                        credentials['passwort'] = new_password
                        new_encrypted_data = encrypt_data(json.dumps(credentials), key)
                        save_encrypted_data(new_encrypted_data)
                        print("Passwort wurde erfolgreich geändert.")
                    else:
                        print("Benutzername nicht gefunden.")                    
                case "4":
                    print("Beenden")
                    break
                
                case _:
                    print("Ungültige Wahl. Bitte erneut versuchen.")


def main_menu():
    print("Wählen Sie eine Option:")
    print("1. Neue Daten speichern")
    print("2. Gespeicherte Daten abrufen")
    print("3. Passwort ändern")
    print("4. Beenden")

    choice = input("Ihre Wahl: ")
    return choice

def query_name():
    name = input("Der Name deines Kontos: ")
    return name

def query_password():
    print(f"Passwort wird aus Sicherheitsgründen nicht ersichtlich sein")
    password = getpass.getpass("Passwort: ")
    return password

def control_password():
    pass

# Funktion zum Laden des Schlüssels aus einer Datei
def load_key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        print("Fehler: Der Schlüssel wurde nicht gefunden. Bitte generieren Sie einen Schlüssel.")
        return None

# Funktion zum Verschlüsseln der Daten
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Funktion zum Entschlüsseln der Daten
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data
    except cryptography.fernet.InvalidToken:
        print("Fehler: Ungültiges Token. Die Daten konnten nicht entschlüsselt werden.")
        return None

# Funktion zur Speicherung der verschlüsselten Daten in einer Datei
def save_encrypted_data(encrypted_data):
    with open("data.enc", "wb") as data_file:
        data_file.write(encrypted_data)
    print("Daten wurden gespeichert.")
        
# Funktion zum Laden der verschlüsselten Daten aus einer Datei
def load_encrypted_data():
    try:
        with open("data.enc", "rb") as data_file:
            return data_file.read()
    except FileNotFoundError:
        print("Fehler: Die Daten-Datei 'data.enc' wurde nicht gefunden.")
        return None

def verify_password():
    hauptpasswort = getpass.getpass("Hauptpasswort: ")
    main_password = os.getenv("schokolade")

    if hauptpasswort == main_password:
        return True
    else:
        return False    


if __name__ == "__main__":
    main()