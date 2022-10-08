from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv("keys.env")
token = str(os.getenv("RPC_KEY"))


def get_web3():
    # Create a Web3 object
    w3 = Web3(Web3.HTTPProvider(token))
    return w3

def get_balance(address):
    w3 = get_web3()
    # Get balance
    balance = w3.eth.getBalance(address)
    
    # convert balance to ether
    ether = w3.fromWei(balance, 'ether')
    return str(ether) + "eth"

def getUsdcBalance(address):
    """Get the USDC balance of an address"""
    w3 = get_web3()
    # Get balance
    balance = w3.eth.getBalance(address)
    
    # convert balance to ether
    ether = w3.fromWei(balance, 'ether')
    return ether


def test_connection():
    w3 = get_web3()
    # Check if connected to Ethereum
    if w3.isConnected():
        print("Connected to Ethereum")
    else:
        print("Not connected to Ethereum")

if __name__ == "__main__":
    print(get_balance("0xD93Bcd514471730a7B5C3052dA61e8EE4D7415B0"))