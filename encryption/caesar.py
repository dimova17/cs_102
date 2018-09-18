def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("")
    ''
    """
    abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ciphertext = ""
    for i in plaintext:
        if i in abc:
            num = ord(i) + 3

            if num >= ord('z'):
                num = num - 23
            elif num > ord('Z') and num < ord('a'):
                num = num - 23

            ciphertext += chr(num)
        else:
            ciphertext = plaintext
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE

    abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintext = ""

    for i in ciphertext :
        if i in abc:
            num = ord(i) - 3

            if num > ord('Z') and num < ord('a'):
                num += 26
            elif num < ord('A'):
                num += 26

            plaintext += chr(num)

        else:
            plaintext = ciphertext
    return plaintext
