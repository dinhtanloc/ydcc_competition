import streamlit as st
from Crypto.Cipher import AES
import os
from werkzeug.utils import secure_filename
import base64


st.markdown("# Local Encryption")
st.markdown("AES is considered one of the most widely used encryption standards and is extensively employed in various applications and security systems.")
st.sidebar.markdown("# Local Encryption")

class Encryptor:
    def __init__(self, key):
        self.key = key

    # Encryption method
    def encrypt_file(self, filename):
        cipher = AES.new(self.key, AES.MODE_EAX)
        with open(filename, 'rb') as f:
            data = f.read()
        ciphertext, tag = cipher.encrypt_and_digest(data)
        with open(filename + '.enc', 'wb') as f:
            [f.write(x) for x in (cipher.nonce, tag, ciphertext)]

    # Decryption method
    def decrypt_file(self, filename):
        with open(filename, 'rb') as f:
            nonce = f.read(12) 
            ciphertext = f.read()
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        data = cipher.decrypt(ciphertext)
        with open(filename[:-4], 'wb') as f:
            f.write(data)

key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)

clear = lambda: os.system('cls')

# Streamlit app
def main():
    st.title('File Encryption Tool')

    st.sidebar.header('Options')
    choice = st.sidebar.radio('Choose an option:', ['Encrypt', 'Decrypt'])

    if choice == 'Encrypt':
        file_to_encrypt = st.file_uploader('Upload a file to encrypt')
        if file_to_encrypt is not None:
            if st.button('Encrypt File'):
                encrypted_filename = secure_filename(file_to_encrypt.name) + '.enc'
                with open(encrypted_filename, 'wb') as f:
                    f.write(file_to_encrypt.getvalue())
                enc.encrypt_file(encrypted_filename)
                st.success('File encrypted successfully!')

                # Add download button for encrypted file
                with open(encrypted_filename, 'rb') as f:
                    encrypted_file_data = f.read()
                    encrypted_file_b64 = base64.b64encode(encrypted_file_data).decode('utf-8')
                href = f'<a href="data:file/encrypted;base64,{encrypted_file_b64}" download="{encrypted_filename}">Download encrypted file</a>'
                st.markdown(href, unsafe_allow_html=True)

    elif choice == 'Decrypt':
        file_to_decrypt = st.file_uploader('Upload a file to decrypt')
        if file_to_decrypt is not None:
            if st.button('Decrypt File'):
                decrypted_filename = secure_filename(file_to_decrypt.name)[:-4]  # Removing '.enc' extension
                with open(decrypted_filename, 'wb') as f:
                    f.write(file_to_decrypt.getvalue())
                enc.decrypt_file(decrypted_filename)
                st.success('File decrypted successfully!')

                # Add download button for decrypted file
                with open(decrypted_filename, 'rb') as f:
                    decrypted_file_data = f.read()
                    decrypted_file_b64 = base64.b64encode(decrypted_file_data).decode('utf-8')
                href = f'<a href="data:file/decrypted;base64,{decrypted_file_b64}" download="{decrypted_filename}">Download decrypted file</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
