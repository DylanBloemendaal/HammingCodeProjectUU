# HammingCodeProjectUU
### Overview:
This Python script implements a Hamming code generator and corrector. The Hamming Codes are created using either Matrix Multiplication or Bit-Wise operation.

### Features:
- Code Converter: Convert text to data bits or data bits to text. <br />
- Code Generation: Create Hamming codes by adding parity bits to the original data bits. <br />
- Error Detection: Identify errors in received Hamming codes using calculated parity bits. <br />
- Error Correction: Correct single-bit errors in Hamming codes.

## Usage:
### How to Install:
Make sure python is installed and open the .py file using any python editor.

### How to Use:
We have created 2 classes and 10 functions to be used.

#### Classes:
_Vector class:_ <br />
To use this class, input a list representing the vector, Vector operations that have been defined are: <br />
- Vector addition <br />
- Matrix and Vector multiplication

_Matrix class:_ <br />
To use this class, input a netsed list of lists where each list represents a row of the Matrix, Matrix operations that have been defined are: 
- Matrix addition,
- Matrix multiplication,
- Matrix and Vector multiplication

#### Functions:
Below are examples of how to use the functions we have made: <br />

_toBinary("Hi")_ <br />
returns "0100100001101001"

_EncodeNibble_("1001") <br />
returns [0, 0, 1, 1, 0, 0, 1]

_EncodeBitwise_("10001100100", 15) <br />
returns [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]

_EncodeMessage_("1011000", 7) <br />
returns [[0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0]], 1

_EncodeRandom_(5, 7) <br />
returns "01101", [[1, 1, 0, 0, 1, 1, 0], [1, 1, 1, 0, 0, 0, 0]], 3

_Parity_([[1, 1, 1, 0, 0, 1, 1], [0, 0, 1, 0, 0, 0, 0]]) <br />
returns [[0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0]]

_BitParity_([[1, 1, 1, 0, 0, 1, 1], [0, 0, 1, 0, 0, 0, 0]]) <br />
returns [[0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0]]

_DecodeHamming_([1, 0, 1, 1, 0, 1, 0]) <br />
returns "1010"

_DecodeMessage_([[0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0]], 1) <br />
returns "1011000"

_toString_("0100100001101001") <br />
returns "Hi"

We have also provided some example code in the .py file.

### Credits:
Dylan Bloemendaal (9485961) <br />
Hugo van Hattem (1957074)
