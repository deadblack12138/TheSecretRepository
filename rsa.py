from base64 import b64encode
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

public_key = """-----BEGIN PUBLIC KEY-----
                    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCoZG+2JfvUXe2P19IJfjH+iLmp
                    VSBX7ErSKnN2rx40EekJ4HEmQpa+vZ76PkHa+5b8L5eTHmT4gFVSukaqwoDjVAVR
                    TufRBzy0ghfFUMfOZ8WluH42luJlEtbv9/dMqixikUrd3H7llf79QIb3gRhIIZT8
                    TcpN6LUbX8noVcBKuwIDAQAB
                    -----END PUBLIC KEY-----
                 """


def encrpt(password, public_key=public_key):
    """
    学号加密
    :param password:
    :param public_key:
    :return:
    """
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()