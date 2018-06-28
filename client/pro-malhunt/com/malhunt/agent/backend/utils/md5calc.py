import hashlib


def md5(path):
    try:
        path = path.strip()
        with open(path, 'rb') as file:
            H = hashlib.md5()
            H.update(file.read())
            md5hash = H.hexdigest()
    except IOError:
        #print "Couldn't get contents for file: {}, insufficient access privileges!".format(path)
        md5hash = None
    return md5hash


# with open("C:\\Users\ganesh.vernekar\Documents\python_progs\wfile.txt") as f:
#     md5(f.readlines())
