# local_host = "http://localhost:3000/call"
local_host = "https://metamask.app.link/dapp/crypto-2022-hackathon.vercel.app/call"
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
    img = qrcode.make(url)
    # return img
    # save image to file
    img.save("./qr.png")
    return "./qr.png"
    

if __name__ == '__main__':
    # print("Testing utils.py")
    # print(format_call_data({"to": "0x123", "data": "0x456"}))
    print(generate_qr_code("https://google.com"))