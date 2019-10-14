def encrypt_caesar(plaintext: str) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    for i in plaintext:
        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            if ('a' <= i <= 'w') or ('A' <= i <= 'W'):
                l = chr(ord(i) + 3)
            else:
                l = chr(ord(i) - 23)
        else:
            i += l
        plaintext = plaintext.replace(i, l)

    return plaintext


def decrypt_caesar(ciphertext: str) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    for i in ciphertext:
        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            if ('d' <= i <= 'z') or ('D' <= i <= 'Z'):
                l = chr(ord(i) - 3)
            else:
                l = chr(ord(i) + 23)
        else:
            i += l
        ciphertext = ciphertext.replace(i, l)
    return ciphertext
