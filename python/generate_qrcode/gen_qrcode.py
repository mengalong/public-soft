import qrcode
import sys


url = sys.argv[1]
img = qrcode.make(url)
img.save("./test.png")
