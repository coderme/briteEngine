#! /usr/bin/env python3

from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcZF3wA1tEMY_EhUs08QwdmH1NWsdKpm5S5BNT-riATk-kLbxvwp-O90TcC3XmzOKjdSvUG_s9f9kY2hLw2yf0sm8LpYirxxwePu-tWM4G8R0JZlT7D4x65aYkGy-zDC_X5oMpq8l7rxRy53mN3Xgoa40X74ExIrS2j-U1E4Qr1IucU88='


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
