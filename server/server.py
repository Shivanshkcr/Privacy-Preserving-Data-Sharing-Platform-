import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

aes_key = b'6a2c8b46d187f8e2cb6af26edc79ae5d'

def encrypt_message(aes_key, plaintext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padding_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + (chr(padding_length) * padding_length).encode()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext

def broadcast_message(message, clients):
    for client in clients:
        try:
            client.sendall(message)
        except:
            clients.remove(client)

def handle_client(client_socket, clients):
    while True:
        try:
            pass
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    server_ip = '0.0.0.0'
    server_port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{server_port}...")

    clients = []

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}")
            clients.append(client_socket)

            threading.Thread(target=handle_client, args=(client_socket, clients)).start()

            plaintext_message = input("Enter message to send to all clients: ")
            encrypted_message = encrypt_message(aes_key, plaintext_message.encode())
            broadcast_message(encrypted_message, clients)
            print("Encrypted message broadcasted to all clients.")
            print(encrypted_message)
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
