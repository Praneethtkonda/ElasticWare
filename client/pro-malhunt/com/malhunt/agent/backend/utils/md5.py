import hashlib
def file_as_bytes(file):
    
    with open(file, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()
  
  
