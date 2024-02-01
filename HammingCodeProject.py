# Dylan Bloemendaal     9485961
# Hugo van Hattem       1957074

import random as rn


# ###############################CLASSES#####################################


class Vector:
    """This class is designed for binary operations.
        Vector operations are only defined on Vectors with binary elements.
        The following operations are defined on this class:
        - Vector addition,
        - Vector and Matrix multiplication.
        The input for this class should be a list of integers.
        All operations will return a list instead of a Vector or Matrix object"""

    def __init__(self, lst):
        self.lst = lst

    def __str__(self):
        return str(self.lst)

    def __add__(self, other):
        """Vector addition is defined here."""
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
    """This class is designed for binary operations.
        Matrix operations are only defined on Matrices with binary elements.
        The following operations are defined on this class:
        - Matrix addition,
        - Matrix multiplication
        - Matrix and Vector multiplication.
        The input for this class should be a nested list of lists, where each list represents a row of the Matrix.
        All operations will return a list instead of a Vector or Matrix object"""

    def __init__(self, lst):
        self.lst = lst

    def __str__(self):
        return str(self.lst)

    def __add__(self, other):
        """Matrix addition is defined here"""
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
        """Matrix multiplication and Matrix and Vector multiplication are defined here"""
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
    """Takes a string and turns it into a binary string
        where each character is represented by 8 bits"""
    ListInt = []
    BinaryMessage = ""

    for char in Message:
        ListInt.append(ord(char))

    for integer in ListInt:
        BinaryMessage += str("{0:08b}".format(integer))

    return BinaryMessage


def EncodeNibble(nibble):
    """Encodes a string of four bits into a Hamming(7,4) code
        using matrix multiplication. The output will be a list."""
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
    return HammingCode


def EncodeBitwise(bitstring, length):
    """Encodes a string of any amount of bits into a Hamming code of given length.
        The output will be a list."""
    # Place bitstring in a Hamming code with all parity bits = 0
    y = 0
    z = 0
    paritybits = []
    HammingCode = [0 for i in range(length)]
    for indx in range(length):

        # Check if the selected position will be a parity bit
        if indx == 2**z - 1:
            paritybits.append(indx)
            z += 1
            continue

        # Place the next bit if the position should be a message bit
        elif y < len(bitstring):
            HammingCode[indx] = int(bitstring[y])
            y += 1

    # Change the parity bits using bitwise operations
    for paritybit in paritybits:
        parity = 0

        # Calculate the parity for the current parity check
        for indx in range(len(HammingCode)):

            if (indx + 1) % (2 * paritybit + 2) >= (paritybit + 1):
                parity += HammingCode[indx]

        # Change parity bit based on parity
        HammingCode[paritybit] = parity % 2

    return HammingCode


def EncodeMessage(message, length=0):
    """Given a binary message and length n, will split the message into chunks,
        which it encodes into Hamming(n,k) codes using bitwise operations.
        If the message cannot be evenly split, it will add extra zeros to the last Hamming code.
        If the length parameter is left empty, Matrix multiplication will be used instead.
        The return value will be a list of Hamming codes and the amount of zeros that were added."""
    matrixmethod = False

    if length in (1, 2, 3):
        raise ValueError("Length of Hammingcode must be greater than 3")

    elif length == 0:
        length += 7
        matrixmethod = True

    paritybits = len(bin(length)) - 2
    messagebits = length - paritybits

    # Split the message into a list of bitstrings
    bitstrings = []
    bitstring = ""
    counter = 1

    for bit in message:
        bitstring += bit

        if counter % messagebits == 0:
            bitstrings.append(bitstring)
            bitstring = ""
            counter = 0

        counter += 1

    # Any leftover bits are added into a last bitstring topped with extra zero's
    if len(bitstring) != 0:
        AddedZeros = 0

        while len(bitstring) < messagebits:
            bitstring += "0"
            AddedZeros += 1

        bitstrings.append(bitstring)

    else:
        AddedZeros = 0

    # Create a Hamming code for each bitstring.
    HammingCodes = []

    for bitstring in bitstrings:

        if matrixmethod:
            HammingCode = EncodeNibble(bitstring)
        else:
            HammingCode = EncodeBitwise(bitstring, length)

        HammingCodes.append(HammingCode)

    return HammingCodes, AddedZeros


def EncodeRandom(MessageLength=50, HammingCodeLength=7):
    """Generates a random nibble and encodes it into a Hamming(7,4) code."""

    RandomBits = [rn.randint(0, 1) for i in range(MessageLength)]
    RandomMessage = ""

    for bit in RandomBits:
        RandomMessage += str(bit)

    HammingCodes, AddedZeros = EncodeMessage(RandomMessage, HammingCodeLength)

    return RandomMessage, HammingCodes, AddedZeros


def Parity(HammingCodes):
    """Given a list of Hamming codes, will correct singular errors in
        each code using matrix multipication."""
    Corrected = []

    for Code in HammingCodes:
        # Calculate the position of the error using the parity-check matrix.
        Recieved = Vector(Code)
        sevenfourparity = Matrix([[0,0,0,1,1,1,1], [0,1,1,0,0,1,1],[1,0,1,0,1,0,1]])*Recieved
        sfparity = 4 * sevenfourparity[0] + 2 * sevenfourparity[1] + sevenfourparity[2]

        # Correct the error if needed
        if sfparity == 0:
            Corrected.append(Code)
        else:
            Code[sfparity-1] = (Code[sfparity-1] + 1) % 2
            Corrected.append(Code)

    return Corrected


def BitParity(HammingCodes):
    """Given a list of Hamming codes, will correct singular errors in
        each code using bitwise operations."""
    # Calculate how many parity bits are in the Hamming Codes
    z = 0
    paritybits = []

    for indx, bit in enumerate(HammingCodes[0]):

        if indx == 2**z - 1:
            paritybits.append(indx)
            z += 1

    length = len(paritybits)
    BitCorrected = []

    # Correct each of the Hamming codes
    for Codes in HammingCodes:
        Bits = []
        Counter = 1

        # Create a list of binary strings which represent the bit positions
        while Counter <= len(HammingCodes[0]):

            if Codes[Counter-1] == 1:
                bit = format(Counter, f"0{length}b")
                bits = [int(i) for i in bit]
                Bits.append(bits)

            Counter += 1

        # Calculate the position of the error
        errorposition = [0 for i in range(length)]

        for X in Bits:
            errorposition = Vector(errorposition) + Vector(X)

        finalbitstring = ""

        for bit in errorposition:
            finalbitstring += str(bit)

        finalbit = int(finalbitstring, 2)

        # Correct the error if needed
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

        # Ignore if bit is a parity bit
        if indx == 2**z - 1:
            z += 1
            continue
        else:
            bitstring += str(bit)

    return bitstring


def DecodeMessage(HammingCodes, addedzeros=0):
    """Decodes a list of HammingCodes into a binary string with extra added zeros removed."""
    message = ""

    for HammingCode in HammingCodes:
        bitstring = DecodeHamming(HammingCode)
        message += bitstring

    return message[::-1][addedzeros:][::-1]


def toString(BinMessage):
    """Converts a string of all Binary numbers to a String of text"""
    line = BinMessage
    Text = ""
    length = 8

    # Split the message into strings of length 8
    bitstrings = [line[i:i+length] for i in range(0, len(line), length)]

    for bitstring in bitstrings:
        value = int(bitstring, 2)
        Text += chr(value)

    return Text


# ###################################MAIN######################################


# Example code

message, HammingCodeLength = "Hello, World!", 15

print("\nMessage:")
print(message)

bits = toBinary(message)
print("\nMessage in binary:")
print(bits)

encoded, addedzeros = EncodeMessage(bits, HammingCodeLength)
print("\nEncoded message:")
print(encoded)


# Create an error in the message by flipping the bit at a chosen position
HammingCodeIndex = 0
BitIndex = 4
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
