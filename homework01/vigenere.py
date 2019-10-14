def encrypt_vigenere(plaintext: str, keyword: str) -> str:
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

    ciphertext = " "
    keyword = keyword.lower()
    code_a = ord('a')
    code_A = ord('A')
    if code_a > code_A:
        m = code_a
    else:
        m = code_A

    while len(plaintext) > len(keyword):
        keyword += keyword
    for i, j in enumerate(plaintext):
        if 'a' <= j <= 'z':
            key = (ord(keyword[i % len(keyword)]) - m) % 26
            mid = (ord(j) + key - code_a) % 26 + code_a
            ciphertext += chr(mid)
        elif 'A' <= j <= 'Z':
            key = (ord(keyword[i % len(keyword)]) - m) % 26
            mid = (ord(j) + key - code_A) % 26 + code_A
            ciphertext += chr(mid)
        else:
            ciphertext += j

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
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

    plaintext = " "
    keyword = keyword.lower()
    code_a = ord('a')
    code_A = ord('A')
    if code_a > code_A:
        m = code_a
    else:
        m = code_A

    while len(ciphertext) > len(keyword):
        keyword += keyword
    ss = len(ciphertext) // len(keyword)
    for i, j in enumerate(ciphertext):
        if 'a' <= j <= 'z':
            key = (ord(keyword[i % len(keyword)]) - m) % 26
            mid = (ord(j) - key - code_a) % 26 + code_a
            plaintext += chr(mid)
        elif 'A' <= j <= 'Z':
            key = (ord(keyword[i % len(keyword)]) - m) % 26
            mid = (ord(j) - key - code_A) % 26 + code_A
            plaintext += chr(mid)
        else:
            plaintext += j

    return plaintext
