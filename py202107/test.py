import hashlib


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


a = input()
b = input()


def setkey(setaccount, setIDcard):
    return str(md5(setaccount) + md5(setIDcard))


print(setkey(a, b))
