import os
from dotenv import load_dotenv
from web3 import Web3


load_dotenv()

RPC_URL = os.getenv("GANACHE_RPC_URL")
w3 = Web3(Web3.HTTPProvider(RPC_URL))


def deploy_contract(signed_txn):

    # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

    return tx_receipt

def fetch_contract(address, abi):
    return w3.eth.contract(address=address, abi=abi)
