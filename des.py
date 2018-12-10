import numpy as np

def create16Keys(key):
    '''
    key(string)
        - Binary string of 1's or 0's and 64 characters long
    Return(array[float])
        - Nested array of 16 48-bit keys in float representation
    '''
    keytab1 = [38, 28, 30, 34,  4, 21,  6,
               51, 13,  1, 55,  7, 17, 42,
               36, 26, 25, 58,  9, 41, 15,
               2, 49, 57, 43, 53, 19,  29,
               5, 10, 54, 44, 37, 47,  14,
               20, 59, 27, 45, 35, 60, 62,
               39, 50,  3, 46, 12, 18, 11,
               22, 23, 33, 63, 52, 31, 61]
    keytab2 = [ 7,  3, 45,  5, 22, 38, 
               40, 23, 19,  9, 31, 37,
               24, 21, 55, 30, 53, 46,
               39, 47,  6, 29, 18, 15,
               32, 28, 12, 49, 20,  0, 
                1,  4, 42, 44, 13, 16, 
               26, 17, 11, 43, 41, 35, 
               50, 10, 33, 14,  8, 51]
    lsTable = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    #Map 56 bits from the 64-bit key
    keyMapped = []
    [keyMapped.append(key[pos]) for pos in keytab1]
    
    #Split 56-bit key in half as 2 28-bit messages
    lkey = np.zeros((17, 28))
    rkey = np.zeros((17, 28))
    lkey[0] = keyMapped[:int(len(keyMapped)/2)]
    rkey[0] = keyMapped[int(len(keyMapped)/2):]
    
    #Left shift each half of the key 16 times, storing each iteration 
    for n in range(len(lsTable)):
        lkey[n+1] = np.append(lkey[n][lsTable[n]:], lkey[n][:lsTable[n]])
        rkey[n+1] = np.append(lkey[n][lsTable[n]:], lkey[n][:lsTable[n]])

    permutedKeys = np.zeros((16, 48))
    for n in range(1, len(lsTable)+1):
        #Concatenate both halves of the keys from each iteration
        concatKey = np.concatenate((lkey[n], rkey[n]))
        i = 0
        #Map 48 of the 56 bits per key from each iteration
        for pos in keytab2:
            permutedKeys[n-1][i] = concatKey[pos]
            i += 1
    return permutedKeys

tab1 = [58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7]
tab2 = [ 5,  4,  1, 19, 31,  2, 10, 20, 
        11, 17,  0, 30,  6, 29, 26, 28,
        12, 14, 27, 22, 13, 25, 18, 16,
         3, 23, 15, 21,  8, 24,  7,  9,
         9, 14, 20,  8, 18, 11, 21, 26,
        30,  1, 31,  0, 29,  7, 19, 16]
tab3 = [22,  4, 20, 19, 18,  3, 16,  2,
        31, 13, 26,  7, 21, 25, 11, 10, 
        23,  6,  5, 15, 17, 28,  9,  8,
         0, 12, 30, 14, 27, 29, 24,  1]
tab4 = [40,  8, 48, 16, 56, 24, 64, 32,
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25]
sboxes = [
    [ 2, 15,  8,  7, 13,  7,  5,  6, 13, 10,  4,  8, 11,  5,  1, 14, 
     12,  0,  0,  1,  5,  3, 12, 12,  9,  6, 14,  3,  0,  7,  7, 13,
      9, 10,  5,  9, 14,  4, 10,  2, 14,  0, 12,  8,  1, 11,  2,  4,
     15,  3,  6,  2,  8, 15, 11, 10,  4, 15,  9,  1,  6, 13,  3, 11],
    [ 8, 13, 10,  1,  5, 15,  4,  2,  3, 12,  9,  4, 10,  2,  8,  1, 
      3, 11, 12,  5,  9,  1, 13,  3,  0, 14,  7,  15, 0, 13,  5,  8, 
      1, 14, 15,  6, 11,  4, 13, 14,  4,  2,  7,  0,  5,  8,  9,  0, 
     14,  3, 12,  6,  7, 11, 11,  7, 10,  6, 15, 12,  9, 10,  2,  6],
    [ 1, 12,  15, 5,  2,  3, 12,  4, 12, 11, 14, 10,  4,  8,  8, 10, 
      2, 13,  0, 15, 13,  9,  8,  9, 11, 14, 12, 13,  0,  3,  4, 14, 
     10,  7,  3, 11,  2,  9,  6,  9,  0, 15,  4,  6,  6,  5, 13,  3, 
     11,  1,  2,  8,  7, 10,  5,  1,  7,  6,  7, 15, 14,  5,  0,  1],
    [ 6,  2, 11, 14,  9,  1,  8,  9, 12, 15, 10,  5,  3,  1,  6,  5,  
      0,  0,  5, 12,  6,  6, 11,  8,  8,  4,  0, 14,  2,  3, 15, 14,
      7, 10, 13, 10, 12,  9,  1,  2, 12,  2,  7, 15,  3, 11,  5, 10, 
      4,  7,  4, 13,  4,  0, 14, 11,  8, 13,  1,  7, 15,  3,  9, 13],
    [10,  3,  4,  4,  2,  7,  7,  2, 12,  0, 10, 14,  9, 13,  1, 15, 
      2,  9, 11, 13, 11, 15, 14,  5,  1,  9,  8,  1,  1, 13,  8, 13, 
      5,  7, 14,  2,  5, 10, 15,  6,  9,  6,  3, 11,  0, 12, 11, 14,
     15,  7,  8,  8,  4, 12,  4, 12,  6,  0,  5,  3,  3,  0, 10,  6],
    [15,  4,  4,  0,  1,  5, 14,  2, 11,  1, 11,  4, 10, 10,  9, 14, 
      5,  9,  6, 12, 12,  0,  4, 10,  3, 13,  2, 14,  9,  6,  8, 15,
      3,  7,  1, 14,  8, 13, 12,  3,  7,  6,  8, 15,  2,  2, 13, 11, 
      0, 10, 11,  5, 12,  7,  5, 15,  0, 13,  3,  6,  1,  7,  8,  9],
    [11, 12,  8,  9,  6, 11,  1,  4, 14,  0, 13,  7,  0,  9,  7, 15,
     14,  6,  7, 12,  2,  0, 15,  9,  9,  4,  3, 11,  3,  5, 13,  6,
      8,  7, 13, 15,  1, 10, 14,  0,  1,  2, 12,  2,  1,  8,  2,  4,
      6, 10,  5, 10, 15, 14, 12,  5, 11,  5,  4,  3,  8, 10,  3, 13],
    [ 3, 10, 14,  0, 15, 12,  1,  0, 14,  7, 11,  0,  8,  4, 13,  0, 
      9,  3,  4,  5,  7,  6, 15,  2,  7,  8, 12, 13,  2,  8,  8,  6,
     14, 13,  6,  9,  4,  7, 12, 15,  9,  3, 11, 10,  2, 12,  1,  1,
     10,  5,  9,  5, 11,  5, 13,  6,  3,  4,  2, 14, 10,  1, 11, 15]
]
    
def des(message, key, encryption = True):
    '''
    message(string):
        - Plaintext string for encryption
        - Hex string for decryption
    key(string):
        - 8 char string used for encrypting and decrypting message
    Return(string):
        - Returns Hex string for encryption
        - Returns plaintext string for decryption
    '''
    #Convert key from string to binary
    if len(key) != 8:
        print("Key is: ", len(key), " chars long. Expecting 8 chars.")
        return
    binKey = list(''.join(format(ord(digit), '08b') for digit in key))
    
    if encryption:
        #Pad messages that do not split into 64-bit blocks
        if (len(message)%8) != 0:
            message += (8-(len(message)%8)) * ' '
        #Convert message from string to binary
        binMsg = ''.join(format(ord(char), '08b') for char in message)
    else:
        #Convert message from hex to binary
        binMsg =  bin(int(message, 16))[2:]
        #Pad binary of hexMessage to 64-bit blocks
        if len(binMsg)%64 != 0:
            binMsg = (64-len(binMsg)%64)*'0' + binMsg
    
    messageReturn = []
    #Iterate through every 64 bits of input message
    for block in range(0, len(binMsg), 64):
        blockMessage = binMsg[block:block+64]
        #Remap 64-bit message based on generated table
        remappedMsg = []
        [remappedMsg.append(blockMessage[pos-1]) for pos in tab1]
        #Split 64-bit remapped message in half as 2 32-bit messages
        lmsg = remappedMsg[:int(len(remappedMsg)/2)]
        rmsg = remappedMsg[int(len(remappedMsg)/2):]
        #Iterate using the 16 keys and XOR logic to calculate
        #new left and right bit sequence, storing each iteration
        if encryption:
            xorKey = create16Keys(binKey)
        else:
            xorKey = create16Keys(binKey)[::-1]
        for n in range(16):
            #Expand 32-bit right message to 48-bit
            expandMsg = []
            [expandMsg.append(float(rmsg[pos-1])) for pos in tab2]
            #XOR 48-bit message with 48-bit key
            xormk = np.logical_xor(expandMsg, xorKey[n]).astype(int).tolist()
            
            #Remap 48-bit to 32-bit using Sboxes
            #Split 48-bit into 8 6-bits
            #Choose Sbox row using first and last bit of each 6-bit
            #Choose Sbox column using middle 4 bits of each 6-bit
            remappedr = ""
            for digit in range(0, len(xormk), 6):
                row = xormk[digit]*2 + xormk[digit+5]*1
                col = xormk[digit+1]*8 + xormk[digit+2]*4 + xormk[digit+3]*2 + xormk[digit+4]*1
                remappedr += '{0:04b}'.format(sboxes[int(digit/6)][row*15 + col])
            #Convert and remap string representation of 32-bits to float representation
            permutedr = []
            [permutedr.append(float(remappedr[pos-1])) for pos in tab3]
            floatlmsg = []
            [floatlmsg.append(float(char)) for char in lmsg]
            #XOR left and newly calculated and mapped right halves of the message bits
            newrmsg = np.logical_xor(floatlmsg, permutedr).astype(int).tolist()
            lmsg = rmsg
            rmsg = newrmsg
        concMsg = np.concatenate((rmsg, lmsg))
        finalPerm = []
        [finalPerm.append(concMsg[pos-1]) for pos in tab4]
        #Map final binary sequence, converting from array to string
        binFinalMsg = ''.join(format(str(int(char)), 's') for char in finalPerm)
        if encryption:
            #Convert to hex if encryption
            messageReturn.append((16-len(hex(int(binFinalMsg, 2))[2:]))*'0' + hex(int(binFinalMsg, 2))[2:])
        else:
            #Convert to string if decryption
            [messageReturn.append(chr(int(binFinalMsg[byte: byte+8], 2))) for byte in range(0, len(binFinalMsg), 8)]
    return ''.join(messageReturn)

encryption = input("Is this encryption? (y/n)\n")
if (encryption != 'y') and (encryption != 'n'):
    print("You chose: ", encryption ,",not (y) or (n)")
    return
if encryption == 'y':
    inputMessage = input("Enter input string message:\n")
    inputKey = input("Enter your 8 character encryption key:\n")
    encrypt = True
if encryption == 'n':
    inputMessage = input("Enter input hex message:\n")
    inputKey = input("Enter your 8 character decryption key:\n")
    encrypt = False
if len(inputKey) != 8:
    print("Your secret key is", len(inputKey), "characters long\nExpected 8 characters")

message = des(inputMessage, inputKey, encrypt)
if message != None:
    print("Message: ", message)
