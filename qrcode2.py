# Importing library
import qrcode
 
# Data to be encoded
data = 'https://linktr.ee/edwin_uzoefuna'
 
# Encoding data using make() function
img = qrcode.make(data)
 
# Saving as an image file
img.save('MyQRCode2.png')
