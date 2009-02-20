#!/usr/bin/python

from rd import RD

cp_strings = ['c402fb2f70c89a0df112c5e38583f9202a96c6de3fa1aa3da6849bb317a983b3',
              'e1a28374f5562768c061f22394a556a75860f132432415d67768e0c112c31495',
              'd3802c10649503a60619b709d1278efef84c1856dfd4097541d55c6740442d8b',
              'Copyright (c) 2007, 2008 Hulu, LLC.  All Rights Reserved.']

R = RD()

def hulu_decrypt(p):
    global cp_strings

    for v1 in range(0, len(cp_strings) - 1):
        v2 = dec1(p, cp_strings[v1])
        if (dec2(v2)):
            return v2

    
def dec1(v1, ke):
    # split value
    v3 = v1.split("~")
    v1 = AK()

    sdk( v3[1], 256, v1 )

    # use part 1 of split for something
    v2 = [ e( v3[0][0:32], v1 ), e( v3[0][32:], v1 ) ]
    v1 = AK()
    sdk( ke[0:64], 256, v1 )
    v2 = [ e( v2[0], v1 ), e( v2[1], v1 ) ]
    return "".join( [ h2s( v2[0] ), h2s( v2[1] ) ] )


def dec2(s):
    v3 = 0
    while v3 < len(s):
        v1 = ord( s[v3] )
        v2 = ( ord('a') <= v1 ) and ( v1 <= ord('z') )
        v2 = v2 or ( ord('A') <= v1 ) and ( v1 <= ord('Z') )
        v2 = v2 or ( ord('0') <= v1 ) and ( v1 <= ord('9') )
        v2 = v2 or ( ord('-') == v1 ) or ( ord('_') == v1 ) or ( ord(' ') == v1 )
        if not v2:
            return False
        v3 += 1
    return True

def AK():
    return { 'rounds': 12, 'rd_key': [0]*256 }

def sek(userkey, bits, key):
    v3 = 0
    v4 = 0
    v1 = 0
    rcon = [16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 452984832, 905969664]
    if ( not userkey or not key ):
        return -1

    if ( bits != 128 and bits != 192 and bits != 256 ):
        return -2

    if ( bits == 128 ):
        key['rounds'] = 10
    else:
        if (bits == 192):
            key['rounds'] = 12
        else:
            key['rounds'] = 14

    key['rd_key'][0] = int( '0x' + userkey[0:8],   16)
    key['rd_key'][1] = int( '0x' + userkey[8:16],  16)
    key['rd_key'][2] = int( '0x' + userkey[16:24], 16)
    key['rd_key'][3] = int( '0x' + userkey[24:32], 16)
    if (bits == 128):
        while True:
            v3 = key['rd_key'][3 + v1]
            key['rd_key'][4 + v1] = key['rd_key'][v1] ^ R.Te4[v3 >> 16 & 255] & 4278190080 ^ R.Te4[v3 >> 8 & 255] & 16711680 ^ R.Te4[v3 & 255] & 65280 ^ R.Te4[v3 >> 24 & 255] & 255 ^ R.rcon[v4]
            key['rd_key'][5 + v1] = key['rd_key'][1 + v1] ^ key['rd_key'][4 + v1]
            key['rd_key'][6 + v1] = key['rd_key'][2 + v1] ^ key['rd_key'][5 + v1]
            key['rd_key'][7 + v1] = key['rd_key'][3 + v1] ^ key['rd_key'][6 + v1]
            v4 += 1
            if (v4 == 10):
                return 0
            v1 += 4

    key['rd_key'][4] = int('0x' + userkey[32:40], 16)
    key['rd_key'][5] = int('0x' + userkey[40:48], 16)
    if (bits == 192):
        while True:
            v3 = key['rd_key'][5 + v1]
            key['rd_key'][6 + v1] = key['rd_key'][v1] ^ R.Te4[v3 >> 16 & 255] & 4278190080 ^ R.Te4[v3 >> 8 & 255] & 16711680 ^ R.Te4[v3 & 255] & 65280 ^ R.Te4[v3 >> 24 & 255] & 255 ^ R.rcon[v4]
            key['rd_key'][7 + v1] = key['rd_key'][1 + v1] ^ key['rd_key'][6 + v1]
            key['rd_key'][8 + v1] = key['rd_key'][2 + v1] ^ key['rd_key'][7 + v1]
            key['rd_key'][9 + v1] = key['rd_key'][3 + v1] ^ key['rd_key'][8 + v1]
            v4 += 1
            if (v4 == 8):
                return 0
            key['rd_key'][10 + v1] = key['rd_key'][4 + v1] ^ key['rd_key'][9 + v1]
            key['rd_key'][11 + v1] = key['rd_key'][5 + v1] ^ key['rd_key'][10 + v1]
            v1 += 6

    key['rd_key'][6] = int('0x' + userkey[48: 56], 16)
    key['rd_key'][7] = int('0x' + userkey[56: 64], 16)
    if (bits == 256):
        while True:
            v3 = key['rd_key'][7 + v1]
            key['rd_key'][8 + v1] = key['rd_key'][v1] ^ R.Te4[v3 >> 16 & 255] & 4278190080 ^ R.Te4[v3 >> 8 & 255] & 16711680 ^ R.Te4[v3 & 255] & 65280 ^ R.Te4[v3 >> 24 & 255] & 255 ^ R.rcon[v4]
            key['rd_key'][9 + v1] = key['rd_key'][1 + v1] ^ key['rd_key'][8 + v1]
            key['rd_key'][10 + v1] = key['rd_key'][2 + v1] ^ key['rd_key'][9 + v1]
            key['rd_key'][11 + v1] = key['rd_key'][3 + v1] ^ key['rd_key'][10 + v1]
            v4 += 1
            if (v4 == 7):
                return 0

            v3 = key['rd_key'][11 + v1]
            key['rd_key'][12 + v1] = key['rd_key'][4 + v1] ^ R.Te4[v3 >> 24 & 255] & 4278190080 ^ R.Te4[v3 >> 16 & 255] & 16711680 ^ R.Te4[v3 >> 8 & 255] & 65280 ^ R.Te4[v3 & 255] & 255
            key['rd_key'][13 + v1] = key['rd_key'][5 + v1] ^ key['rd_key'][12 + v1]
            key['rd_key'][14 + v1] = key['rd_key'][6 + v1] ^ key['rd_key'][13 + v1]
            key['rd_key'][15 + v1] = key['rd_key'][7 + v1] ^ key['rd_key'][14 + v1]
            v1 += 8

    return 0


def sdk(userkey, bits, key):
    v5 = 0
    v3 = 0
    v4 = 0
    v2 = 0
    v6 = sek(userkey, bits, key)

    if (v6 < 0):
        return undefined

    v3 = 0
    v4 = 4 * key['rounds']
    while (v3 < v4):
        v5 = key['rd_key'][v3]
        key['rd_key'][v3] = key['rd_key'][v4]
        key['rd_key'][v4] = v5
        v5 = key['rd_key'][v3 + 1]
        key['rd_key'][v3 + 1] = key['rd_key'][v4 + 1]
        key['rd_key'][v4 + 1] = v5
        v5 = key['rd_key'][v3 + 2]
        key['rd_key'][v3 + 2] = key['rd_key'][v4 + 2]
        key['rd_key'][v4 + 2] = v5
        v5 = key['rd_key'][v3 + 3]
        key['rd_key'][v3 + 3] = key['rd_key'][v4 + 3]
        key['rd_key'][v4 + 3] = v5
        v3 += 4
        v4 -= 4

    v3 = 1
    while (v3 < key['rounds']):
        v2 += 4
        key['rd_key'][v2] = R.Td0[R.Te4[key['rd_key'][v2] >> 24 & 255] & 255] ^ R.Td1[R.Te4[key['rd_key'][v2] >> 16 & 255] & 255] ^ R.Td2[R.Te4[key['rd_key'][v2] >> 8 & 255] & 255] ^ R.Td3[R.Te4[key['rd_key'][v2] & 255] & 255]
        key['rd_key'][1 + v2] = R.Td0[R.Te4[key['rd_key'][1 + v2] >> 24 & 255] & 255] ^ R.Td1[R.Te4[key['rd_key'][1 + v2] >> 16 & 255] & 255] ^ R.Td2[R.Te4[key['rd_key'][1 + v2] >> 8 & 255] & 255] ^ R.Td3[R.Te4[key['rd_key'][1 + v2] & 255] & 255]
        key['rd_key'][2 + v2] = R.Td0[R.Te4[key['rd_key'][2 + v2] >> 24 & 255] & 255] ^ R.Td1[R.Te4[key['rd_key'][2 + v2] >> 16 & 255] & 255] ^ R.Td2[R.Te4[key['rd_key'][2 + v2] >> 8 & 255] & 255] ^ R.Td3[R.Te4[key['rd_key'][2 + v2] & 255] & 255]
        key['rd_key'][3 + v2] = R.Td0[R.Te4[key['rd_key'][3 + v2] >> 24 & 255] & 255] ^ R.Td1[R.Te4[key['rd_key'][3 + v2] >> 16 & 255] & 255] ^ R.Td2[R.Te4[key['rd_key'][3 + v2] >> 8 & 255] & 255] ^ R.Td3[R.Te4[key['rd_key'][3 + v2] & 255] & 255]
        v3 += 1

    return 0



def e(bin, key):
    if ( not bin or not key ):
        return 0

    v5 = int('0x' + bin[0:   8], 16) ^ key['rd_key'][0]
    v4 = int('0x' + bin[8:  16], 16) ^ key['rd_key'][1]
    v3 = int('0x' + bin[16: 24], 16) ^ key['rd_key'][2]
    v2 = int('0x' + bin[24: 32], 16) ^ key['rd_key'][3]

    v9 = R.Td0[v5 >> 24 & 255] ^ R.Td1[v2 >> 16 & 255] ^ R.Td2[v3 >> 8 & 255] ^ R.Td3[v4 & 255] ^ key['rd_key'][4]
    v8 = R.Td0[v4 >> 24 & 255] ^ R.Td1[v5 >> 16 & 255] ^ R.Td2[v2 >> 8 & 255] ^ R.Td3[v3 & 255] ^ key['rd_key'][5]
    v7 = R.Td0[v3 >> 24 & 255] ^ R.Td1[v4 >> 16 & 255] ^ R.Td2[v5 >> 8 & 255] ^ R.Td3[v2 & 255] ^ key['rd_key'][6]
    v6 = R.Td0[v2 >> 24 & 255] ^ R.Td1[v3 >> 16 & 255] ^ R.Td2[v4 >> 8 & 255] ^ R.Td3[v5 & 255] ^ key['rd_key'][7]
    v5 = R.Td0[v9 >> 24 & 255] ^ R.Td1[v6 >> 16 & 255] ^ R.Td2[v7 >> 8 & 255] ^ R.Td3[v8 & 255] ^ key['rd_key'][8]
    v4 = R.Td0[v8 >> 24 & 255] ^ R.Td1[v9 >> 16 & 255] ^ R.Td2[v6 >> 8 & 255] ^ R.Td3[v7 & 255] ^ key['rd_key'][9]
    v3 = R.Td0[v7 >> 24 & 255] ^ R.Td1[v8 >> 16 & 255] ^ R.Td2[v9 >> 8 & 255] ^ R.Td3[v6 & 255] ^ key['rd_key'][10]
    v2 = R.Td0[v6 >> 24 & 255] ^ R.Td1[v7 >> 16 & 255] ^ R.Td2[v8 >> 8 & 255] ^ R.Td3[v9 & 255] ^ key['rd_key'][11]
    v9 = R.Td0[v5 >> 24 & 255] ^ R.Td1[v2 >> 16 & 255] ^ R.Td2[v3 >> 8 & 255] ^ R.Td3[v4 & 255] ^ key['rd_key'][12]
    v8 = R.Td0[v4 >> 24 & 255] ^ R.Td1[v5 >> 16 & 255] ^ R.Td2[v2 >> 8 & 255] ^ R.Td3[v3 & 255] ^ key['rd_key'][13]
    v7 = R.Td0[v3 >> 24 & 255] ^ R.Td1[v4 >> 16 & 255] ^ R.Td2[v5 >> 8 & 255] ^ R.Td3[v2 & 255] ^ key['rd_key'][14]
    v6 = R.Td0[v2 >> 24 & 255] ^ R.Td1[v3 >> 16 & 255] ^ R.Td2[v4 >> 8 & 255] ^ R.Td3[v5 & 255] ^ key['rd_key'][15]
    v5 = R.Td0[v9 >> 24 & 255] ^ R.Td1[v6 >> 16 & 255] ^ R.Td2[v7 >> 8 & 255] ^ R.Td3[v8 & 255] ^ key['rd_key'][16]
    v4 = R.Td0[v8 >> 24 & 255] ^ R.Td1[v9 >> 16 & 255] ^ R.Td2[v6 >> 8 & 255] ^ R.Td3[v7 & 255] ^ key['rd_key'][17]
    v3 = R.Td0[v7 >> 24 & 255] ^ R.Td1[v8 >> 16 & 255] ^ R.Td2[v9 >> 8 & 255] ^ R.Td3[v6 & 255] ^ key['rd_key'][18]
    v2 = R.Td0[v6 >> 24 & 255] ^ R.Td1[v7 >> 16 & 255] ^ R.Td2[v8 >> 8 & 255] ^ R.Td3[v9 & 255] ^ key['rd_key'][19]
    v9 = R.Td0[v5 >> 24 & 255] ^ R.Td1[v2 >> 16 & 255] ^ R.Td2[v3 >> 8 & 255] ^ R.Td3[v4 & 255] ^ key['rd_key'][20]
    v8 = R.Td0[v4 >> 24 & 255] ^ R.Td1[v5 >> 16 & 255] ^ R.Td2[v2 >> 8 & 255] ^ R.Td3[v3 & 255] ^ key['rd_key'][21]
    v7 = R.Td0[v3 >> 24 & 255] ^ R.Td1[v4 >> 16 & 255] ^ R.Td2[v5 >> 8 & 255] ^ R.Td3[v2 & 255] ^ key['rd_key'][22]
    v6 = R.Td0[v2 >> 24 & 255] ^ R.Td1[v3 >> 16 & 255] ^ R.Td2[v4 >> 8 & 255] ^ R.Td3[v5 & 255] ^ key['rd_key'][23]
    v5 = R.Td0[v9 >> 24 & 255] ^ R.Td1[v6 >> 16 & 255] ^ R.Td2[v7 >> 8 & 255] ^ R.Td3[v8 & 255] ^ key['rd_key'][24]
    v4 = R.Td0[v8 >> 24 & 255] ^ R.Td1[v9 >> 16 & 255] ^ R.Td2[v6 >> 8 & 255] ^ R.Td3[v7 & 255] ^ key['rd_key'][25]
    v3 = R.Td0[v7 >> 24 & 255] ^ R.Td1[v8 >> 16 & 255] ^ R.Td2[v9 >> 8 & 255] ^ R.Td3[v6 & 255] ^ key['rd_key'][26]
    v2 = R.Td0[v6 >> 24 & 255] ^ R.Td1[v7 >> 16 & 255] ^ R.Td2[v8 >> 8 & 255] ^ R.Td3[v9 & 255] ^ key['rd_key'][27]
    v9 = R.Td0[v5 >> 24 & 255] ^ R.Td1[v2 >> 16 & 255] ^ R.Td2[v3 >> 8 & 255] ^ R.Td3[v4 & 255] ^ key['rd_key'][28]
    v8 = R.Td0[v4 >> 24 & 255] ^ R.Td1[v5 >> 16 & 255] ^ R.Td2[v2 >> 8 & 255] ^ R.Td3[v3 & 255] ^ key['rd_key'][29]
    v7 = R.Td0[v3 >> 24 & 255] ^ R.Td1[v4 >> 16 & 255] ^ R.Td2[v5 >> 8 & 255] ^ R.Td3[v2 & 255] ^ key['rd_key'][30]
    v6 = R.Td0[v2 >> 24 & 255] ^ R.Td1[v3 >> 16 & 255] ^ R.Td2[v4 >> 8 & 255] ^ R.Td3[v5 & 255] ^ key['rd_key'][31]
    v5 = R.Td0[v9 >> 24 & 255] ^ R.Td1[v6 >> 16 & 255] ^ R.Td2[v7 >> 8 & 255] ^ R.Td3[v8 & 255] ^ key['rd_key'][32]
    v4 = R.Td0[v8 >> 24 & 255] ^ R.Td1[v9 >> 16 & 255] ^ R.Td2[v6 >> 8 & 255] ^ R.Td3[v7 & 255] ^ key['rd_key'][33]
    v3 = R.Td0[v7 >> 24 & 255] ^ R.Td1[v8 >> 16 & 255] ^ R.Td2[v9 >> 8 & 255] ^ R.Td3[v6 & 255] ^ key['rd_key'][34]
    v2 = R.Td0[v6 >> 24 & 255] ^ R.Td1[v7 >> 16 & 255] ^ R.Td2[v8 >> 8 & 255] ^ R.Td3[v9 & 255] ^ key['rd_key'][35]
    v9 = R.Td0[v5 >> 24 & 255] ^ R.Td1[v2 >> 16 & 255] ^ R.Td2[v3 >> 8 & 255] ^ R.Td3[v4 & 255] ^ key['rd_key'][36]
    v8 = R.Td0[v4 >> 24 & 255] ^ R.Td1[v5 >> 16 & 255] ^ R.Td2[v2 >> 8 & 255] ^ R.Td3[v3 & 255] ^ key['rd_key'][37]
    v7 = R.Td0[v3 >> 24 & 255] ^ R.Td1[v4 >> 16 & 255] ^ R.Td2[v5 >> 8 & 255] ^ R.Td3[v2 & 255] ^ key['rd_key'][38]
    v6 = R.Td0[v2 >> 24 & 255] ^ R.Td1[v3 >> 16 & 255] ^ R.Td2[v4 >> 8 & 255] ^ R.Td3[v5 & 255] ^ key['rd_key'][39]
    if (key['rounds'] > 10) :
        v5 = R.Td0[v9 >> 24 & 255] ^ R.Td1[v6 >> 16 & 255] ^ R.Td2[v7 >> 8 & 255] ^ R.Td3[v8 & 255] ^ key['rd_key'][40]
        v4 = R.Td0[v8 >> 24 & 255] ^ R.Td1[v9 >> 16 & 255] ^ R.Td2[v6 >> 8 & 255] ^ R.Td3[v7 & 255] ^ key['rd_key'][41]
        v3 = R.Td0[v7 >> 24 & 255] ^ R.Td1[v8 >> 16 & 255] ^ R.Td2[v9 >> 8 & 255] ^ R.Td3[v6 & 255] ^ key['rd_key'][42]
        v2 = R.Td0[v6 >> 24 & 255] ^ R.Td1[v7 >> 16 & 255] ^ R.Td2[v8 >> 8 & 255] ^ R.Td3[v9 & 255] ^ key['rd_key'][43]
        v9 = R.Td0[v5 >> 24 & 255] ^ R.Td1[v2 >> 16 & 255] ^ R.Td2[v3 >> 8 & 255] ^ R.Td3[v4 & 255] ^ key['rd_key'][44]
        v8 = R.Td0[v4 >> 24 & 255] ^ R.Td1[v5 >> 16 & 255] ^ R.Td2[v2 >> 8 & 255] ^ R.Td3[v3 & 255] ^ key['rd_key'][45]
        v7 = R.Td0[v3 >> 24 & 255] ^ R.Td1[v4 >> 16 & 255] ^ R.Td2[v5 >> 8 & 255] ^ R.Td3[v2 & 255] ^ key['rd_key'][46]
        v6 = R.Td0[v2 >> 24 & 255] ^ R.Td1[v3 >> 16 & 255] ^ R.Td2[v4 >> 8 & 255] ^ R.Td3[v5 & 255] ^ key['rd_key'][47]
        if (key['rounds'] > 12):
            v5 = R.Td0[v9 >> 24 & 255] ^ R.Td1[v6 >> 16 & 255] ^ R.Td2[v7 >> 8 & 255] ^ R.Td3[v8 & 255] ^ key['rd_key'][48]
            v4 = R.Td0[v8 >> 24 & 255] ^ R.Td1[v9 >> 16 & 255] ^ R.Td2[v6 >> 8 & 255] ^ R.Td3[v7 & 255] ^ key['rd_key'][49]
            v3 = R.Td0[v7 >> 24 & 255] ^ R.Td1[v8 >> 16 & 255] ^ R.Td2[v9 >> 8 & 255] ^ R.Td3[v6 & 255] ^ key['rd_key'][50]
            v2 = R.Td0[v6 >> 24 & 255] ^ R.Td1[v7 >> 16 & 255] ^ R.Td2[v8 >> 8 & 255] ^ R.Td3[v9 & 255] ^ key['rd_key'][51]
            v9 = R.Td0[v5 >> 24 & 255] ^ R.Td1[v2 >> 16 & 255] ^ R.Td2[v3 >> 8 & 255] ^ R.Td3[v4 & 255] ^ key['rd_key'][52]
            v8 = R.Td0[v4 >> 24 & 255] ^ R.Td1[v5 >> 16 & 255] ^ R.Td2[v2 >> 8 & 255] ^ R.Td3[v3 & 255] ^ key['rd_key'][53]
            v7 = R.Td0[v3 >> 24 & 255] ^ R.Td1[v4 >> 16 & 255] ^ R.Td2[v5 >> 8 & 255] ^ R.Td3[v2 & 255] ^ key['rd_key'][54]
            v6 = R.Td0[v2 >> 24 & 255] ^ R.Td1[v3 >> 16 & 255] ^ R.Td2[v4 >> 8 & 255] ^ R.Td3[v5 & 255] ^ key['rd_key'][55]

    v11 = key['rounds'] << 2
    v5 = R.Td4[v9 >> 24 & 255] & 4278190080 ^ R.Td4[v6 >> 16 & 255] & 16711680 ^ R.Td4[v7 >> 8 & 255] & 65280 ^ R.Td4[v8 & 255] & 255 ^ key['rd_key'][v11]
    v10 = R.byte2hex(v5 >> 24 & 255)
    v10 += R.byte2hex(v5 >> 16 & 255)
    v10 += R.byte2hex(v5 >> 8 & 255)
    v10 += R.byte2hex(v5 & 255)
    v4 = R.Td4[v8 >> 24 & 255] & 4278190080 ^ R.Td4[v9 >> 16 & 255] & 16711680 ^ R.Td4[v6 >> 8 & 255] & 65280 ^ R.Td4[v7 & 255] & 255 ^ key['rd_key'][v11 + 1]
    v10 += R.byte2hex(v4 >> 24 & 255)
    v10 += R.byte2hex(v4 >> 16 & 255)
    v10 += R.byte2hex(v4 >> 8 & 255)
    v10 += R.byte2hex(v4 & 255)
    v3 = R.Td4[v7 >> 24 & 255] & 4278190080 ^ R.Td4[v8 >> 16 & 255] & 16711680 ^ R.Td4[v9 >> 8 & 255] & 65280 ^ R.Td4[v6 & 255] & 255 ^ key['rd_key'][v11 + 2]
    v10 += R.byte2hex(v3 >> 24 & 255)
    v10 += R.byte2hex(v3 >> 16 & 255)
    v10 += R.byte2hex(v3 >> 8 & 255)
    v10 += R.byte2hex(v3 & 255)
    v2 = R.Td4[v6 >> 24 & 255] & 4278190080 ^ R.Td4[v7 >> 16 & 255] & 16711680 ^ R.Td4[v8 >> 8 & 255] & 65280 ^ R.Td4[v9 & 255] & 255 ^ key['rd_key'][v11 + 3]
    v10 += R.byte2hex(v2 >> 24 & 255)
    v10 += R.byte2hex(v2 >> 16 & 255)
    v10 += R.byte2hex(v2 >> 8 & 255)
    v10 += R.byte2hex(v2 & 255)
    return v10

def h2s( h ):
    if ( len(h) % 2 ) == 1:
        raise Exception("h2s called with odd length 'h': "+h)
    s = ''
    for v1 in range(0, len(h), 2):
        s += chr( int( h[v1:v1+2], 16 ) )
    return s

if __name__=="__main__":
    pid = "46fc4f0d4a15515e0a1090a2ece4918a04a70c31feb2c6f7d8d19b73a7f8717e~767ab4bb7950c065112579e2dfde374d60d22bb71ab013b86f9d853c45edf32d"
    # wanted = "2QpCmO87j4IL84l6feso4r6yU5EwVM8b"
    print hulu_decrypt( pid )
