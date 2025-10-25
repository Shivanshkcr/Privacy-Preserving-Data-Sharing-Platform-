import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

aes_key = b'6a2c8b46d187f8e2cb6af26edc79ae5d'

def decrypt_message(aes_key, encrypted_message):
    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    padding_length = padded_plaintext[-1]
    plaintext = padded_plaintext[:-padding_length]
    return plaintext.decode()

def start_client():
    server_ip = '127.0.0.1'
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    try:
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print("Decrypted message from server:", decrypted_message)
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
