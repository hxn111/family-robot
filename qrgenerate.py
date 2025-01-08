import qrcode

# Dictionary mapping QR code data to sound files
qr_data_to_sound = {
    "qrcode_1": "./1.wav",
    "qrcode_2": "./2.wav",
}

# Generate and save QR codes
for data, sound_file in qr_data_to_sound.items():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(f"{data}.png")
