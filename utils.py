local_host = "http://localhost:3000/call"
import json
import qrcode

def format_call_data(txn):
    """Format the call data for the transaction."""
    print("Formatting call data")
    try:
      to_address = txn['to']
      call_data = txn['data']
      return local_host + "?to=" + to_address + "&calldata=" + call_data
    except:
      return "Error: Invalid transaction."

def generate_qr_code(url):
    """Generate a QR code from the url."""
    print("Generating QR code")
    try:
      qr = qrcode.QRCode(
          version=1,
          error_correction=qrcode.constants.ERROR_CORRECT_L,
          box_size=10,
          border=4,
      )
      qr.add_data(url)
      qr.make(fit=True)
      img = qr.make_image(fill_color="black", back_color="white")
      # return img
      # save image to file
      img.save("qr.png")
      return "qr.png"
    except:
      return "Error: Invalid URL."