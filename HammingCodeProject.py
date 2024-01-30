# Dylan Bloemendaal     9485961
# Hugo van Hattem       1957074

import random as rn
import time
import math

# ###############################CLASSES#####################################


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


def toBinary(Message):
    """Converts a string into Binary to use in the HammingCode"""
    ListInt = []
    BinaryMessage = ""
    for char in Message:
        ListInt.append(ord(char))
    for integer in ListInt:
        BinaryMessage = BinaryMessage + str("{0:08b}".format(integer))

    return BinaryMessage


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


def EncodeBitwise(bitstring, length):

    # Place bitstring in an empty Hamming Code
    y = 0
    z = 0
    paritybits = []
    HammingCode = [0 for i in range(length)]
    for indx in range(length):
        if indx == 2**z - 1:
            paritybits.append(indx)
            z += 1
            continue
        else:
            HammingCode[indx] = int(bitstring[y])
            y += 1

    # Change the parity bits using bitwise operations
    for paritybit in paritybits:
        parity = 0
        for indx in range(len(HammingCode)):
            if (indx + 1) % (2 * paritybit + 2) >= (paritybit + 1):
                parity += HammingCode[indx]
        HammingCode[paritybit] = parity % 2

    return HammingCode


def EncodeMessage(message, length=0):
    """Splits the message into nibbles of size 4 and encodes them into Hamming(7,4) codes.
        The input should be in binary format in the form of a string (e.g. '011000111000').
        If the message is not divisible by 4, then 0 to 3 zeros will be added to the message"""

    matrix = False
    if length in (1, 2):
        raise ValueError("Length of Hammingcode must be greater than 3")
    elif length == 0:
        length += 7
        matrix = True

    paritybits = len(bin(length)) - 2
    messagebits = length - paritybits

    # Split the message into a list of nibbles
    nibbles = []
    nibble = []
    counter = 1
    for bit in message:
        nibble.append(int(bit))
        if counter % messagebits == 0:
            nibbles.append(nibble)
            nibble = []
            counter = 0
        counter += 1

    # Any leftover bits are added into a last nibble topped with extra zero's
    if len(nibble) != 0:
        AddedZeros = 0
        while len(nibble) < messagebits:
            nibble.append(0)
            AddedZeros += 1
        nibbles.append(nibble)
    else:
        AddedZeros = 0

    # Create a Hamming code for each nibble.
    HammingCodes = []
    for nibble in nibbles:
        if matrix:
            HammingCode = EncodeNibble(nibble)
        else:
            HammingCode = EncodeBitwise(nibble, length)

        HammingCodes.append(HammingCode)

    # Return list of HammingCodes in the form of a list
    # Return the amount of zeros added to make the message divisible by 4
    return HammingCodes, AddedZeros


def EncodeRandom(length=50):
    """Generates a random nibble and encodes it into a Hamming(7,4) code."""

    RandomBits = [rn.randint(0, 1) for i in range(length)]
    RandomMessage = ""

    for bit in RandomBits:
        RandomMessage += str(bit)

    HammingCodes, AddedZeros = EncodeMessage(RandomMessage)

    return RandomMessage, HammingCodes, AddedZeros


def Parity(HammingCodes):
    """Checks if there are any mistakes in the nibble using matrix multiplication."""

    Corrected = []
    for Codes in HammingCodes:
        Recieved = Vector(Codes)
        sevenfourparity = Matrix([[0,0,0,1,1,1,1], [0,1,1,0,0,1,1],[1,0,1,0,1,0,1]])*Recieved
        sfparity = 4 * sevenfourparity[0] + 2 * sevenfourparity[1] + sevenfourparity[2]

        if sfparity == 0:
            Corrected.append(Codes)
        else:
            Codes[sfparity-1] = (Codes[sfparity-1] + 1) % 2
            Corrected.append(Codes)

    return Corrected


def BitParity(HammingCodes):
    """Checks if there are any mistakes in the nibble using bitwise operations."""

    # Calculate how many parity bits are in the Hamming Codes
    z = 0
    paritybits = []
    for indx, bit in enumerate(HammingCodes[0]):
        if indx == 2**z - 1:
            paritybits.append(indx)
            z += 1

    length = len(paritybits)

    BitCorrected = []
    for Codes in HammingCodes:
        Bits = []
        Counter = 1

        while Counter <= len(HammingCodes[0]):

            if Codes[Counter-1] == 1:
                bit = format(Counter, f"0{length}b")
                bits = [int(i) for i in bit]
                Bits.append(bits)

            Counter += 1

        error = [0 for i in range(length)]

        for X in Bits:
            error = Vector(error) + Vector(X)

        finalbitstring = ""
        for bit in error:
            finalbitstring += str(bit)

        finalbit = int(finalbitstring, 2)

        if finalbit == 0:
            BitCorrected.append(Codes)
        else:
            Codes[finalbit-1] = (Codes[finalbit-1] + 1) % 2
            BitCorrected.append(Codes)

    return BitCorrected


def DecodeHamming(HammingCode):
    """Decodes a Hamming code into a bitstring."""

    z = 0
    bitstring = ""
    for indx, bit in enumerate(HammingCode):
        if indx == 2**z - 1:
            z += 1
            continue
        else:
            bitstring += str(bit)

    return bitstring


def DecodeMessage(Corrected, addedzeros=0):
    """Decodes a list of HammingCodes into a message."""

    message = ""
    for HammingCode in Corrected:
        bitstring = DecodeHamming(HammingCode)
        message += bitstring

    # Return the message with the extra zeros removed
    return message[::-1][addedzeros:][::-1]


def toString(BinMessage):
    """Converts a string of all Binary numbers to a String of text"""

    line = BinMessage
    Text = ""
    n = 8
    Thingy = [line[i:i+n] for i in range(0, len(line), n)]
    for i in Thingy:
        j = int(i, 2)
        Text += chr(j)

    return Text


# ###################################MAIN######################################


# Example code

message = "Hello World!"

print("\nMessage:")
print(message)

bits = toBinary(message)
print("\nMessage in binary:")
print(bits)

encoded, addedzeros = EncodeMessage(bits, 15)
print("\nEncoded message:")
print(encoded)


# Create an error in the message by flipping the bit at a chosen position
HammingCodeIndex = 1
BitIndex = 13
# -----------------------------------------------------------------------------

encoded[HammingCodeIndex][BitIndex] -= 1
encoded[HammingCodeIndex][BitIndex] *= -1

print("\nEncoded message with error:")
print(encoded)

corrected = BitParity(encoded)
print("\nCorrected message:")
print(corrected)

decoded = DecodeMessage(corrected, addedzeros)
print("\nDecoded:")
print(decoded)

result = toString(decoded)
print("\nResulting message:")
print(result)

correct = message == result
print("\nCorrect:")
print(correct)
