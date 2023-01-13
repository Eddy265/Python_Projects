# Importing library
import qrcode

# Data to be encoded
data = 'https://linktr.ee/edwin_uzoefuna'

# Creating the QR code object
qr = qrcode.QRCode(version=1, box_size=10, border=5)

# Adding data to the QR code object
qr.add_data(data)
qr.make(fit=True)

# Creating an image from the QR code object
img = qr.make_image(fill_color="black", back_color="white")

# Saving the image as a PNG file in the specified path
img.save("C:/Users/euzoe/OneDrive/Desktop/DATA_ANALYSIS/MY_PROJECTS/Python/Python_Projects")
