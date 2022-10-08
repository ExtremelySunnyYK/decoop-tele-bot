local_host = "http://localhost:3000/call"
import json
# import pprint

def format_call_data(txn):
    """Format the call data for the transaction."""
    print("Formatting call data")
    try:
      to_address = txn['to']
      call_data = txn['data']
      return local_host + "?to=" + to_address + "&calldata=" + call_data
    except:
      return "Error: Invalid transaction."