# 如果想使用加密则取消注释

# import binascii
# from math import e
# from pyDes import des, CBC, PAD_PKCS5

# key = 'sustcits'
# iv = "sustcits"

# def des_encrypt(s):
#     k = des(key, CBC, iv, padmode=PAD_PKCS5)
#     en = k.encrypt(s, padmode=PAD_PKCS5)
#     return binascii.b2a_hex(en).decode()


# def des_decrypt(s):
#     k = des(key, CBC, iv, padmode=PAD_PKCS5)
#     de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
#     return de.decode()


def des_encrypt(s):
    return s


def des_decrypt(s):
    return s
