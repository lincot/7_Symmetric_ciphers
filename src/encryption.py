from math import ceil
from collections import Counter
from random import randint


def encrypt_caesar(k, m):
    return ''.join(map(lambda x: chr((ord(x) ^ k) % 0x110000), m))


def hack_caesar(m):
    k = ord(Counter(m).most_common()[0][0]) ^ ord(' ')
    return encrypt_caesar(k, m)


def encrypt_vigenere(k, m):
    return ''.join(map(lambda ix: chr((ord(ix[1]) ^ ord(k[ix[0] % len(k)]))
                                      % 0x110000),
                       enumerate(m)))


def encrypt_otp(k, m):
    assert len(k) >= len(m)
    return encrypt_vigenere(k, m)


def encrypt_cbc(k, m):
    results = []
    results.append(encrypt_otp(k, m[:len(k)]))
    for i in range(1, ceil(len(m) / len(k))):
        t = encrypt_otp(results[-1], m[i * len(k):(i + 1) * len(k)])
        results.append(encrypt_otp(k, t))
    return ''.join(results)


def decrypt_cbc(k, m):
    results = []
    for i in range(ceil(len(m) / len(k)) - 1, 0, -1):
        t = encrypt_otp(k, m[i * len(k):(i + 1) * len(k)])
        results.append(encrypt_otp(m[(i - 1) * len(k):i * len(k)], t))
    return encrypt_otp(k, m[:len(k)]) + ''.join(reversed(results))


if __name__ == '__main__':
    assert encrypt_caesar(2, 'Hello!') == 'Jgnnm#'
    assert encrypt_caesar(2, 'Jgnnm#') == 'Hello!'

    TEXT = 'Съешь же ещё этих мягких французских булок да выпей чаю.'

    assert hack_caesar(encrypt_caesar(randint(0, 1_000_000_000), TEXT)) == TEXT

    assert encrypt_vigenere('\x02\x03', 'Hello!') == 'Jfnom"'
    assert encrypt_vigenere('\x02\x03', 'Jfnom"') == 'Hello!'

    assert encrypt_otp(
        '\U000e0b3b\U000b94e1\U00019853\U000e6e88\U000c6063\U000b8893',
        'Hello!') \
        == '\U000e0b73\U000b9484\U0001983f\U000e6ee4\U000c600c\U000b88b2'
    assert encrypt_otp(
        '\U000e0b3b\U000b94e1\U00019853\U000e6e88\U000c6063\U000b8893',
        '\U000e0b73\U000b9484\U0001983f\U000e6ee4\U000c600c\U000b88b2') \
        == 'Hello!'

    assert encrypt_cbc('\x02\x03', 'Hello!') == 'Jf$\tI+'
    assert decrypt_cbc('\x02\x03', 'Jf$\tI+') == 'Hello!'
