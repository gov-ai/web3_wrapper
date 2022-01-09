import json

from web3 import Web3

from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

from core.compile_contract import compile
from core.create_contract import  create_contract, sign_transaction
from core.deploy_contract import deploy_contract
from core.save_address import save_address


load_dotenv()

RPC_URL = os.getenv("GANACHE_RPC_URL")
MY_ADDRESS = os.getenv("GANACHE_ACCOUNT_ADDRESS")
PRIVATE_KEY = os.getenv("GANACHE_PRIVATE_KEY")
CHAIN_ID = int(os.getenv("GANACHE_CHAIN_ID")) # network-id for single peer

CONTRACT_VERSION = os.getenv("CONTRACT_VERSION")
CONTRACT_NAME = os.getenv("CONTRACT_NAME")
COMPILED_SOL_PATH = f'compiled/{CONTRACT_NAME}Compiled.json'

w3 = Web3(Web3.HTTPProvider(RPC_URL))


#### COMPILE
compile(input_sol_path=f'contract/{CONTRACT_NAME}.sol',
        output_json_path=f'compiled/{CONTRACT_NAME}Compiled.json',
        version=CONTRACT_VERSION)


#### DEPLOY 
txn = create_contract(compiled_sol_path=COMPILED_SOL_PATH,
                      contract_name=CONTRACT_NAME,
                      chain_id=CHAIN_ID, 
                      my_address=MY_ADDRESS)

txn_signed = sign_transaction(txn, private_key=PRIVATE_KEY)
txn_receipt = deploy_contract(txn_signed)


#### REMEMBER ADDRESS
save_address(txn_receipt.contractAddress, CONTRACT_NAME)