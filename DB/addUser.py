from DB.ORM import *
import re
from security import TOTP, password

def add_user():
    Session = sessionmaker(bind=engine)
    session = Session()

    name = input("Username: ")
    if not re.match("^[a-zA-Z0-9_]{3,30}$", name):
        exit("Invalid username format")

    passwd = input("Password: ")

    CanEditAirportsList = input("Comma separated values of ICAOs this user can edit: ")
    for icao in CanEditAirportsList.split(","):
        if not re.match("^[A-Z]{4}$", icao):
            exit("Invalid ICAO code:", icao)

    CanCreate = input("Can create airports? (y/N)") in ["y", "Y"]
    CanDelete = input("Can delete airports? (y/N)") in ["y", "Y"]
    
    TwoFactorKey = None
    if input("Generate TOTP? (y/N)") in ["y", "Y"]:
        TwoFactorKey = TOTP.gen2fa(name)
        token = input("Type TOTP token: ")
        while not TOTP.check2fa(TwoFactorKey, token):
            token = input("Type TOTP token: ")

    password_hash = password.hash_password(passwd)
    session.add(User(Name=name, 
                    PasswordHash=password_hash,
                    CanEditAirportsList=CanEditAirportsList,
                    CanCreate=CanCreate,
                    CanDelete=CanDelete,
                    TwoFactorKey=TwoFactorKey))

    session.commit()
