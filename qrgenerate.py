import qrcode

# Dictionary mapping QR code data to sound files
qr_data_to_sound = {
    "qrcode_1": "./finished1.wav",
    "qrcode_2": "./finished2.wav",
    "qrcode_3": "./finished3.wav",
    "qrcode_4": "./diary1.wav",
    "qrcode_5": "./diary2.wav",
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
