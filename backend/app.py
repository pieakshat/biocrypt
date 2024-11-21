from flask import Flask, jsonify, request, send_file
from rsa_keygen import generate_rsa_keypair, keys_to_pem, encrypt_message, decrypt_message
from ipfs import add_file_to_ipfs, get_file_from_ipfs
from werkzeug.utils import secure_filename
from getFingerprint import fingerprint_scan
import os 

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/generate_keys', methods=['POST'])
def generate_keys():
    user_input = request.json['user_input'] 
    fingerprint_scan()
    public_key, private_key, salt = generate_rsa_keypair(user_input)
    public_pem, private_pem = keys_to_pem(public_key, private_key)
    
    return jsonify({'public_key': public_pem, 'private_key': private_pem})


@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    public_pem = request.json['public_pem']
    message = request.json['message']
    encrypted_message = encrypt_message(public_pem, message)
    return jsonify({'encrypted_message': encrypted_message})


# Route to decrypt a message
@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    private_pem = request.json['private_pem']
    fingerprint_scan()
    ciphertext = bytes.fromhex(request.json['ciphertext'])  # Assuming ciphertext is hex encoded
    decrypted_message = decrypt_message(private_pem, ciphertext)
    
    return jsonify({'decrypted_message': decrypted_message})

@app.route('/api/uploadandEncrypt', methods=['POST'])
def upload_and_encrypt():
    try:
        print("starting the process...")
        public_pem = request.form['public_pem']
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Pass the file object and public key to the `add_file_to_ipfs` function
        encrypted_cid = add_file_to_ipfs(file, public_pem)
        
        return jsonify({'encrypted_cid': encrypted_cid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/decryptDownload', methods = ['POST'])
def decrypt_and_download(): 
    print("starting the processs")
    try: 
        private_pem = request.form['private_pem']
        ciphertext = request.form['ciphertext']
        print("getting the file")

        output_path = "/files" 
        file_path = get_file_from_ipfs(ciphertext, output_path, private_pem) 
        return send_file(
            file_path, 
            as_attachment=True, 
            download_name = "retrived_file",
            mimetype = "application/octet-stream"
        )
    except Exception as e: 
        return jsonify({'error': str(e)}), 500    
    # finally: 
    #     if os.path.exists(output_path):
    #         os.remove(output_path)

if __name__ == '__main__':
    app.run(port=5002, debug=True)
