class RD:
    def __init__(self):
        self.Te0 = [0] * 256
        self.Te1 = [0] * 256
        self.Te2 = [0] * 256
        self.Te3 = [0] * 256
        self.Te4 = [0] * 256
        self.Td0 = [0] * 256
        self.Td1 = [0] * 256
        self.Td2 = [0] * 256
        self.Td3 = [0] * 256
        self.Td4 = [0] * 256
        self.rcon = [16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 452984832, 905969664]

        alog = [0] * 512
        log = [0] * 256
        v10 = [0] * 256
        v11 = [0] * 256
        v5 = 1
        for v9 in range(0, 256):
            alog[v9] = v5
            alog[v9 + 255] = v5;
            log[v5] = v9
            xor_value = 0
            if ( v5 & 128 ) != 0:
                xor_value = 27
            v5 = (v5 ^ v5 << 1 ^ xor_value) & 255
            # v5 = (v5 ^ v5 << 1 ^ ((v5 & 128) != 0) ? 27 : 0) & 255

        log[1] = 0
        for v9 in range(0, 256):
            v3 = 0
            if v9 != 0 :
                v3 = alog[ 255 - log[v9] ]
            v3 ^= v3 << 1 ^ v3 << 2 ^ v3 << 3 ^ v3 << 4
            v3 = 99 ^ (v3 ^ v3 >> 8)
            v10[v9] = v3 & 255
            v11[v3 & 255] = v9

        v7 = [[2, 1, 1, 3], [3, 2, 1, 1], [1, 3, 2, 1], [1, 1, 3, 2], [1, 1, 1, 1]]
        v6 = [[14, 9, 13, 11], [11, 14, 9, 13], [13, 11, 14, 9], [9, 13, 11, 14], [1, 1, 1, 1]]

        for v1 in range( 0, 256 ):
            v2 = v10[v1]
            self.Te0[v1] = self.ab(v2, v7[0], alog, log)
            self.Te1[v1] = self.ab(v2, v7[1], alog, log)
            self.Te2[v1] = self.ab(v2, v7[2], alog, log)
            self.Te3[v1] = self.ab(v2, v7[3], alog, log)
            self.Te4[v1] = self.ab(v2, v7[4], alog, log)
            v2 = v11[v1]
            self.Td0[v1] = self.ab(v2, v6[0], alog, log)
            self.Td1[v1] = self.ab(v2, v6[1], alog, log)
            self.Td2[v1] = self.ab(v2, v6[2], alog, log)
            self.Td3[v1] = self.ab(v2, v6[3], alog, log)
            self.Td4[v1] = self.ab(v2, v6[4], alog, log)


    def ab(self, a, b, alog, log):
        if a == 0:
            return 0
        a = log[ a & 255 ]
        v5 = [0] * 4
        if b[0] != 0:
            v5[0] = (alog[(a + log[b[0] & 255]) % 255] & 255)
        if b[1] != 0:
            v5[1] = (alog[(a + log[b[1] & 255]) % 255] & 255)
        if b[2] != 0:
            v5[2] = (alog[(a + log[b[2] & 255]) % 255] & 255)
        if b[3] != 0:
            v5[3] = (alog[(a + log[b[3] & 255]) % 255] & 255)

        v3 = ''
        v2 = 0
        while (v2 < 4):
            v1 = hex( int( v5[v2] ) )[2:]  #.toString(16)
            if len(v1) == 1:
                v3 += '0' + v1
            else:
                v3 += v1
            v2 += 1
        return int( v3, 16 )

    def byte2hex(self, byte):
        #print byte
        #print hex(byte)[2:].upper()
        h = hex(int(byte))[2:].upper()
        if len(h) == 1:
            h = '0' + h
        return h
