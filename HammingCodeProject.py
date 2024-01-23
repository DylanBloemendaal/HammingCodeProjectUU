# Dylan Bloemendaal     9485961
# Hugo van Hattem       1957074

import random as rn
import time
import math

# ###############################CLASSES#####################################

# TODO: Create classes to perform calculations with matrices and vectors whose
#       elements are 0 or 1. Your classes should support at least addition and
#       matrix multiplication.


class Vector:
    """Working: V + V"""

    def __init__(self, lst):
        self.lst = lst

    def __str__(self):
        return str(self.lst)

    def __add__(self, other):

        if len(self.lst) != len(other.lst):
            raise TypeError("Cannot add vectors of different sizes")

        vector_sum = []
        for bit1, bit2 in zip(self.lst, other.lst):
            if bit1 + bit2 == 1:
                vector_sum.append(1)
            else:
                vector_sum.append(0)

        return vector_sum

    def __mul__(self, other):
        return


class Matrix:
    """Matrix multiplication and addition return as a list"""
    """Working: M + M, M * M, M * V"""

    def __init__(self, lst):
        self.lst = lst

    def __str__(self):
        return str(self.lst)

    def __add__(self, other):

        if len(self.lst) != len(other.lst) or len(self.lst[0]) != len(other.lst[0]):
            raise TypeError("Matrix dimensions do not support addition")

        matrix_sum = []

        for row1, row2 in zip(self.lst, other.lst):
            matrix_sum_row = []

            for element1, element2 in zip(row1, row2):
                matrix_sum_row.append(element1 + element2)

            matrix_sum.append(matrix_sum_row)

        return matrix_sum

    def __mul__(self, other):

        if len(self.lst[0]) != len(other.lst):
            raise TypeError("Matrix/Vector dimensions do not support multiplication")

        # Multiplying two matrices
        if isinstance(other, Matrix):
            matrix_product = []

            for row_indx in range(len(self.lst)):
                matrix_product_row = []

                for column_indx in range(len(other.lst[0])):
                    element = 0

                    for indx in range(len(other.lst)):
                        element += self.lst[row_indx][indx] * other.lst[indx][column_indx]

                    matrix_product_row.append(element % 2)

                matrix_product.append(matrix_product_row)

            return matrix_product

        # Multiplying a matrix with a vector
        else:
            vector_output = []

            for row_indx in range(len(self.lst)):
                element = 0

                for indx in range(len(other.lst)):
                    element += self.lst[row_indx][indx] * other.lst[indx]

                vector_output.append(element % 2)

            # If output is a 1x1-matrix then return the value
            if len(vector_output) == 1:
                return vector_output[0]
            else:
                return vector_output


# ################################FUNCTIONS####################################

# TODO: Write functions that can encode, decode, and possibly correct messages
#       using the parity bit and the Hamming(7,4) code.

def EncodeNibble(nibble):
    """Turns a string of four bits (e.g. '1011') into a Hamming(7,4) code
        using matrix multiplication"""

    x = Vector([int(bit) for bit in nibble])
    # Generator matrix
    G = Matrix([[1, 1, 0, 1],
                [1, 0, 1, 1],
                [1, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])

    HammingCode = G*x
    # Return HammingCode in the form of a list
    return HammingCode


def toBinary(Message):
    """Converts a string into Binary to use in the HammingCode"""
    ListInt=[]
    BinaryMessage = ""
    for char in Message:
        ListInt.append(ord(char))
    for integer in ListInt:
        BinaryMessage = BinaryMessage + str("{0:07b}".format(integer))

    return BinaryMessage


def EncodeMessage(message):
    """Splits the message into nibbles of size 4 and encodes them into Hamming(7,4) codes.
        The input should be in binary format in the form of a string (e.g. '011000111000').
        If the message is not divisible by 4, then 0 to 3 zeros will be added to the message"""

    # Split the message into a list of nibbles
    nibbles = []
    nibble = []
    counter = 1
    for bit in message:
        nibble.append(int(bit))
        if counter % 4 == 0:
            nibbles.append(nibble)
            nibble = []
            counter = 0
        counter += 1

    # Any leftover bits are added into a last nibble topped with extra zero's
    if len(nibble) != 0:
        AddedZeros = 0
        while len(nibble) < 4:
            nibble.append(0)
            AddedZeros += 1
        nibbles.append(nibble)
    else:
        AddedZeros = 0

    # Create a Hamming(7,4) code for each nibble.
    HammingCodes = []
    for nibble in nibbles:
        HammingCode = EncodeNibble(nibble)
        HammingCodes.append(HammingCode)

    # Return list of HammingCodes in the form of a list
    # Return the amount of zeros added to make the message divisible by 4
    return HammingCodes, AddedZeros


# TODO: Write a function that randomly converts a given number of bits to test
#       your code.


def EncodeRandom():
    """Generates a random nibble and encodes it into a Hamming(7,4) code."""

    RandomBits = [rn.randint(0, 1) for i in range(rn.randint(10, 100))]
    RandomMessage = ""

    for bit in RandomBits:
        RandomMessage += str(bit)

    HammingCodes, AddedZeros = EncodeMessage(RandomMessage)

    return RandomMessage, HammingCodes, AddedZeros


def Parity(HammingCode):
    """Checks if there aren't any mistakes in the nibble using matrix multiplication."""

    for Codes in HammingCode:
        Recieved = Vector(Codes)
        sevenfourparity = Matrix([[0,0,0,1,1,1,1], [0,1,1,0,0,1,1],[1,0,1,0,1,0,1]])*Recieved
        sfparity = 4 * sevenfourparity[0] + 2 * sevenfourparity[1] + sevenfourparity[2]
        Corrected = []

        if sfparity == 0:
            Corrected.append(Codes)
        else:
            Codes[sfparity-1] = (Codes[sfparity-1] + 1) % 2
            Corrected.append(Codes)

        return Corrected


def BitParity(HammingCode):
    """Checks if there are any mistakes in the nibble using bitwise operations."""

    BitCorrected = []
    for Codes in HammingCode:
        Bits = []
        Counter = 1

        while Counter < 8:

            if Codes[Counter-1] == 1:
                bit = "{0:03b}".format(Counter)
                bits = [int(i) for i in bit]
                Bits.append(bits)
            Counter += 1

        error = [0, 0, 0]

        for X in Bits:
            error = Vector(error) + Vector(X)

        finalbit = 4 * error[0] + 2*error[1] + error[2]

        if finalbit == 0:
            BitCorrected.append(Codes)
        else:
            Codes[finalbit-1] = (Codes[finalbit-1] + 1) % 2
            BitCorrected.append(Codes)

    return BitCorrected


def DecodeHamming(HammingCode):
    """Decodes a Hamming(7,4) code into a nibble."""

    nibble = ""
    for indx, bit in enumerate(HammingCode):
        if indx + 1 in (3, 5, 6, 7):
            nibble += str(bit)

    return nibble


def DecodeMessage(Corrected, addedzeros=0):
    """Decodes a list of HammingCodes into a message."""

    message = ""
    for HammingCode in Corrected:
        nibble = DecodeHamming(HammingCode)
        message += nibble

    # Return the message with the extra zeros removed
    return message[::-1][addedzeros:][::-1]


def toString(BinMessage):
    """Converts a string of all Binary numbers to a String of text"""
    line = BinMessage
    Text = ""
    n = 7
    Thingy = [line[i:i+n] for i in range(0, len(line), n)]
    for i in Thingy:
        j = int(i, 2)
        Text += chr(j)
    return Text


# #################################MAIN########################################

# TODO: Your code should be able to translate a given message, provided as a string,
#       into binary format and be able to encode it, correct it if necessary and decode
#       it again.

# TODO: Extend your code to handle more complex Hamming codes.

# TODO: Implement the functions also based on bitwise operations and compare
# the speed with the matrix implementation.

"""
x = "111111111111111110001010000101010101101010110101011111111111111110010"
x, codes, z = EncodeRandom()
print(codes)
print()
corrected = BitParity(codes)
print(corrected)
print(corrected == codes)
print()
"""

message = "Hello World!"
print("\nMessage:")
print(message)

bits = toBinary(message)
print("\nMessage in binary:")
print(bits)

encoded, addedzeros = EncodeMessage(bits)
print("\nEncoded:")
print(encoded)

decoded = DecodeMessage(encoded, addedzeros)
print("\nDecoded:")
print(decoded)

result = toString(decoded)
print("\nResulting message:")
print(result)

correct = bits == decoded
print("\nCorrect:")
print(correct)




