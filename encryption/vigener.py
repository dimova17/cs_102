def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE

    abc = 'abcdefghijklmnopqrstuvwxyz'
    ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keyword *= len(plaintext) // len(keyword) + 1
    key = []
    for k in keyword:
        x = abc.find(k)
        if x == -1:
            x = ABC.find(k)
        key.append(x)
    ciphertext = ''
    z = 0
    for l in plaintext:
        if plaintext.islower():
            num = ord(l) - ord('a')
            num = (num + key[z]) % 26 + ord('a')
            l = chr(num)
            l.lower()
            z += 1
            ciphertext += l
        if plaintext.isupper():
            num = ord(l) - ord('A')
            num = (num + key[z]) % 26 + ord('A')
            l = chr(num)
            l.upper()
            z += 1
            ciphertext += l

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    abc = 'abcdefghijklmnopqrstuvwxyz'
    ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keyword *= len(ciphertext) // len(keyword) + 1
    key = []
    for k in keyword:
        x = abc.find(k)
        if x == -1:
            x = ABC.find(k)
        key.append(x)
    plaintext = ''
    z = 0
    for l in ciphertext:
        if ciphertext.islower():
            num = ord(l) - ord('a')
            num = (num - key[z]) % 26 + ord('a')
            l = chr(num)
            l.lower()
            z += 1
            plaintext += l
        if ciphertext.isupper():
            num = ord(l) - ord('A')
            num = (num - key[z]) % 26 + ord('A')
            l = chr(num)
            l.upper()
            z += 1
            plaintext += l
    return plaintext
