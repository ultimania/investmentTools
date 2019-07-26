from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys,random,string

password_length = 20

def create_aes(password, iv):
    sha = SHA256.new()
    sha.update(password.encode())
    key = sha.digest()
    return AES.new(key, AES.MODE_CFB, iv)

def encrypt(data, pass_file_name):
    path = 'lib/password_' + pass_file_name
    # generate password
    password = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(password_length)])
    # encrypt
    iv = Random.new().read(AES.block_size)
    encrypt_data = iv + create_aes(password, iv).encrypt(data)
    # output password file
    with open(path, mode='w') as f:
        f.write(password)
    # output encrypt
    return encrypt_data

def decrypt(data, pass_file_name):
    path = 'lib/password_' + pass_file_name
    # read password
    with open(path) as f:
        password = f.read()
    # decrypt
    iv, cipher = data[:AES.block_size], data[AES.block_size:]
    decrypt_data = create_aes(password, iv).decrypt(cipher)
    # output encrypt
    return decrypt_data

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: invalid argument")
    elif sys.argv[1] == "enc":
        result = encrypt(sys.stdin.buffer.read(),sys.argv[2])
    elif sys.argv[1] == "dec":
        result = decrypt(sys.stdin.buffer.read(),sys.argv[2])
    else:
        print("Error: you need args enc or dec")

    sys.stdout.buffer.write(result)