# Dylan Bloemendaal     9485961
# Hugo van Hattem       1957074

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

        return Vector(vector_sum)

    def __mul__(self, other):
        return


class Matrix:
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

        return Matrix(matrix_sum)

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

            return Matrix(matrix_product)

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
                return Vector(vector_output)


# ################################FUNCTIONS####################################

# TODO: Write functions that can encode, decode, and possibly correct messages
#       using the parity bit and the Hamming(7,4) code.

def CreateHamming(message):
    """Turns a string of four bits (e.g. '1011') into a Hamming(7,4) code
        using matrix multiplication"""
    x = Vector([int(bit) for bit in message])
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

# TODO: Write a function that randomly converts a given number of bits to test
#       your code.

# #################################MAIN########################################

# TODO: Your code should be able to translate a given message, provided as a string,
#       into binary format and be able to encode it, correct it if necessary and decode
#       it again.

# TODO: Extend your code to handle more complex Hamming codes.

# TODO: Implement the functions also based on bitwise operations and compare
# the speed with the matrix implementation.


x = Matrix([[1,0,0,0], [0,1,0,0]])*Vector([1,0,1,1])
y = Vector([1,0,1,0,0,1])+Vector([0,0,1,1,1,1])+Vector([1,0,1,0,0,1])

inputs = "1001"
y = GenerateHamming(inputs)
print(y, type(y))
