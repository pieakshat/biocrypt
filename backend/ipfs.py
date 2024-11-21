import requests
from rsa_keygen import * 

def add_file_to_ipfs(file, public_pem):
    
    files = {'file': (file.filename, file)}
    print(public_pem)
    
    response = requests.post('http://127.0.0.1:5001/api/v0/add', files=files)
    
    if response.status_code != 200:
        raise Exception(f"Failed to add file to IPFS. Status code: {response.status_code}, Response: {response.text}")
    
    res_json = response.json()
    print(f"File added to IPFS with hash: {res_json['Hash']}")
    cid = res_json['Hash']

    print("sending cid for encryption")
    encrypted_cid = encrypt_message(public_pem, cid)
    print("got encrypted cid")
    return encrypted_cid


def get_file_from_ipfs(encrypted_cid, output_path, private_pem): 
    print("starting decryption process")
    print(encrypted_cid)
    print(private_pem)
    cid = decrypt_message(private_pem, encrypted_cid)
    print("cid after decryption", cid)
    try: 
        response = requests.post(f'http://127.0.0.1:5001/api/v0/cat?arg={cid}')
        if response.status_code == 200: 
            with open (output_path, 'wb') as output_file: 
                output_file.write(response.content) 
                print("file retrived from IPFS") 
                return output_path
        else: 
            print(f"Error fetching file: {response.status_code} - {response.text}")
    except Exception as e: 
        print(f"error downloading the file: {str(e)}")




