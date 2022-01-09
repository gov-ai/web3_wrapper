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


def add_fund(contract, value):
    # call contract function requiring transaction
    params = {
        'chainId': CHAIN_ID, 
        'gasPrice': w3.eth.gas_price, 
        'from': MY_ADDRESS,
        'nonce': w3.eth.getTransactionCount(MY_ADDRESS),
        'value': value, # 99764461280000000000=99eth
    }

    txn = getattr(contract.functions, 'fund')().buildTransaction(params) # create txn
    txn_signed = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY) # sign txn
    txn_hash = w3.eth.send_raw_transaction(txn_signed.rawTransaction) # send txn
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash) # wait for receipt
    return txn_receipt


def withdraw_funds(contract):
    # call contract function requiring transaction
    params = {
        'chainId': CHAIN_ID, 
        'gasPrice': w3.eth.gas_price, 
        'from': MY_ADDRESS,
        'nonce': w3.eth.getTransactionCount(MY_ADDRESS),
    }

    txn = getattr(contract.functions, 'withdraw')().buildTransaction(params) # create txn
    txn_signed = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY) # sign txn
    txn_hash = w3.eth.send_raw_transaction(txn_signed.rawTransaction) # send txn
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash) # wait for receipt
    return txn_receipt


def main(action):
    # define contract name
    CONTRACT_NAME = 'FundMe' # os.getenv("CONTRACT_NAME")
    COMPILED_SOL_PATH = f'compiled/{CONTRACT_NAME}Compiled.json'

    # contract metadata
    abi, bytecode = get_abi_and_bytecode(COMPILED_SOL_PATH, CONTRACT_NAME)
    addresses = fetch_addresses(CONTRACT_NAME)
    address = addresses[-1] # latest address

    # fetch contract
    contract = w3.eth.contract(address=address, abi=abi)
    
    # call contract function requiring no transaction
    fee = getattr(contract.functions, 'getEntranceFee')().call()
    print("entrance_fee:", fee) # 17857142857142857142

    eth_amt = 100
    rate = getattr(contract.functions, 'getConversionRate')(eth_amt).call()
    print("conversion_rate:", rate)

    if action=='fund':
        #### add fund
        txn_receipt = add_fund(contract, fee+1)

    if action=='withdraw':
        #### withdraw funds
        txn_receipt = withdraw_funds(contract)



if __name__=='__main__':
    import sys
    action = sys.argv[1]
    assert action in ['fund', 'withdraw'], "action not supported" 
    main(action)