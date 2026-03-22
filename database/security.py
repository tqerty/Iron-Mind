import hashlib 

def secure(data):
    return hashlib.md5(data.encode()).hexdigest()
