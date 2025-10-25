from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def encrypt(message, key1, key2):
    msg = []
    for i, char in enumerate(message):
        ascii_val = ord(char)
        ascii_val += key1 if i % 2 == 0 else key2
        msg.append(chr(ascii_val))
    return ''.join(msg)

def decrypt(message, key1, key2):
    d_msg = []
    for i, char in enumerate(message):
        ascii_val = ord(char)
        ascii_val -= key1 if i % 2 == 0 else key2
        d_msg.append(chr(ascii_val))
    return ''.join(d_msg)

@socketio.on('send_message')
def handle_message(data):
    name = data['name']
    email = data['email']
    message = data['message']
    key1, key2 = 4, 5
    encrypted_message = encrypt(message, key1, key2)
    decrypted_message = decrypt(encrypted_message, key1, key2)
    print(f"Received message from {name} ({email}): {message}")
    print(f"Encrypted: {encrypted_message}")
    print(f"Decrypted: {decrypted_message}")

    emit('new_message', {
        'name': name,
        'email': email,
        'encrypted_message': encrypted_message,
        'decrypted_message': decrypted_message
    }, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
