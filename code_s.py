def enc(key, msg):
    for e in key:
        tmp = round(e, msg)
        res = round(e, tmp)
    return res


def enc_cbc(bloc, key, v):
    tab = []
    res = []
    chr_r = []
    index = 0
    for x in bloc:
        tab.append(int(bin(ord(x)), 2))
    tab[0] = tab[0] ^ v
    nib1 = tab[0] >> 4
    nib2 = tab[0] & 0x0F
    res.append(bin(enc(key, nib1) << 4 ^ enc(key, nib2)))
    for x in tab:
        if index != 0:
            tab[index] = tab[index] ^ int(res[index - 1], 2)
            nib1 = tab[index] >> 4
            nib2 = tab[index] & 0x0F
            res.append(bin(enc(key, nib1) << 4 ^ enc(key, nib2)))
        index += 1
    for x in res:
        chr_r.append(chr(int(x, 2)))
    return chr_r
