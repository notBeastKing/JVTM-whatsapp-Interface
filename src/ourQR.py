import qrcode
from PIL import Image
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def generate_qr_code(context):

    for key in context.keys():
        unique_code = key
    for val in context.values():
        info = val
    
    data = f"Info: {info}\nUnique Code: {unique_code}"

    encrypted_data = data

    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(encrypted_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    template_path = 'qrtemp/templa.jpg'
    template_img = Image.open(template_path)

    x = (template_img.width - img.width)//2
    y = (template_img.height - img.height)//2
    template_img.paste(img,(x,y))

    temp,name = unique_code.split('+')
    filepath = f"qr_codes/{name}.jpeg"

    template_img.save(filepath)
    print("Encrypted QR code generated successfully.")
    return filepath,name

