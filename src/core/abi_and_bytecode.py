import json

def get_abi_and_bytecode(compiled_sol_path, contract_name):
    with open(compiled_sol_path, "rb") as file:
        compiled_sol = json.load(file)
    abi = json.loads(compiled_sol["contracts"][f"{contract_name}.sol"][f"{contract_name}"]["metadata"])["output"]["abi"]
    bytecode = compiled_sol["contracts"][f"{contract_name}.sol"][f"{contract_name}"]["evm"]["bytecode"]["object"]
    return abi, bytecode
