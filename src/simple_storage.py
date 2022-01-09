import os
from web3 import Web3
from dotenv import load_dotenv

from core.abi_and_bytecode import get_abi_and_bytecode
from core.save_address import fetch_addresses


load_dotenv()


RPC_URL = os.getenv("GANACHE_RPC_URL")
MY_ADDRESS = os.getenv("GANACHE_ACCOUNT_ADDRESS")
PRIVATE_KEY = os.getenv("GANACHE_PRIVATE_KEY")
CHAIN_ID = int(os.getenv("GANACHE_CHAIN_ID")) # network-id for single peer

w3 = Web3(Web3.HTTPProvider(RPC_URL))
print('GAS:', w3.eth.gas_price)

def main():
    # define contract name
    CONTRACT_NAME = 'SimpleStorage' # os.getenv("CONTRACT_NAME")
    COMPILED_SOL_PATH = f'compiled/{CONTRACT_NAME}Compiled.json'

    # contract metadata
    abi, bytecode = get_abi_and_bytecode(COMPILED_SOL_PATH, CONTRACT_NAME)
    addresses = fetch_addresses(CONTRACT_NAME)
    address = addresses[-1] # latest address

    # fetch contract
    contract = w3.eth.contract(address=address, abi=abi)
    
    # call contract function requiring no transaction
    existing_value = getattr(contract.functions, 'retrieve')().call()
    print("existing_value:", existing_value)

    # call contract function requiring transaction
    params = {
        'chainId': CHAIN_ID, 
        'gasPrice': w3.eth.gas_price, 
        'from': MY_ADDRESS,
        'nonce': w3.eth.getTransactionCount(MY_ADDRESS)
    }

    txn = getattr(contract.functions, 'store')(existing_value+100).buildTransaction(params) # create txn
    txn_signed = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY) # sign txn
    txn_hash = w3.eth.send_raw_transaction(txn_signed.rawTransaction) # send txn
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash) # wait for receipt

    # call contract function requiring no transaction
    stored_value = getattr(contract.functions, 'retrieve')().call()
    print("stored_value:", stored_value)

if __name__=='__main__':
    main()