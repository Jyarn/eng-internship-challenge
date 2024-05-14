"""
Module that decrypts a text encrypted with a playfair cipher.
"""
import sys


def create_playfair_matrix(key):
    """
    Generates the matrix needed to decrypt encrypted text.
    """
    matrix = [
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None]
    ]

    counter = 0
    for i in key:
        if i not in key[0:counter]:
            matrix[counter // 5][counter % 5] = i
            counter += 1

    for i in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if counter == 25:
            break
        if i not in key:
            matrix[counter // 5][counter % 5] = i
            counter += 1
    return matrix


def find_in_matrix(c, matrix):
    """
    Helper function that finds a charcter c in matrix and returns
    a tuple of the form (y, x) where matrix[y][x] == c
    """

    if c == 'J':
        return find_in_matrix('I', matrix)

    for i in range(0, 25):
        if matrix[i // 5][i % 5] == c:
            return (i // 5, i % 5)
    return (5, 5)   # search failed


def decrypt(msg, matrix):
    """
    Decrypts a piece of text given an encrypted msg, msg and a matrix
    """

    decrypted_msg = ""
    for i in range(0, len(msg), 2):
        (a_y, a_x) = find_in_matrix(msg[i], matrix)
        (b_y, b_x) = find_in_matrix(msg[i+1], matrix)

        if a_y == 5 or a_x == 5:
            print(f"error: unable to find '{msg[i]}' in matrix")
            sys.exit(1)
        elif b_y == 5 or b_x == 5:
            print(f"error: unable to find '{msg[i+1]}' in matrix")
            sys.exit(1)

        if a_x == b_x:      # same column
            decrypted_msg += matrix[a_y-1][a_x]
            decrypted_msg += matrix[b_y-1][b_x]
        elif a_y == b_y:    # same row
            decrypted_msg += matrix[a_y][a_x-1]
            decrypted_msg += matrix[b_y][b_x-1]
        else:
            decrypted_msg += matrix[a_y][b_x]
            decrypted_msg += matrix[b_y][a_x]
    return decrypted_msg


if __name__ == "__main__":
    key_matrix = create_playfair_matrix("SUPERSPY")
    message = decrypt("IKEWENENXLNQLPZSLERUMRHEERYBOFNEINCHCV", key_matrix)
    for k in message:   # filter string and remove any 'X's
        if k != 'X':
            print(k, end='')
    print()
