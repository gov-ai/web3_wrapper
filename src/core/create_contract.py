import os
import json
from web3 import Web3
from dotenv import load_dotenv
from core.abi_and_bytecode import get_abi_and_bytecode


load_dotenv()

RPC_URL = os.getenv("GANACHE_RPC_URL")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def create_contract(compiled_sol_path, contract_name, chain_id, my_address):

    # Get ABI and bytecode
    abi, bytecode = get_abi_and_bytecode(compiled_sol_path=compiled_sol_path, contract_name=contract_name)

    # Create the contract in Python
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Get the latest transaction. `nonce` is txn counter
    nonce = w3.eth.getTransactionCount(my_address)

    # Submit the transaction that deploys the contract
    transaction = contract.constructor(my_address).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )

    return transaction

def sign_transaction(txn, private_key):
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    return signed_txn