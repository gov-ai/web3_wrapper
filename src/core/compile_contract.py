import json
from solcx import compile_standard, install_solc

def compile(input_sol_path, output_json_path, version):
    contract_name = input_sol_path.split("/")[-1]
    print('contract_name:', contract_name)

    with open(input_sol_path, "r") as file:
        simple_storage_file = file.read()

    print(f"Installing solc {version}...")
    install_solc(version)

    # Solidity source code
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {f"{contract_name}": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version=version,
    )

    with open(output_json_path, "w") as file:
        json.dump(compiled_sol, file)
        print(f'Compiled contract at: {output_json_path}')


if __name__ == '__main__':
    compile(input_sol_path='contract/SimpleStorage.sol',
            output_json_path='compiled/SimpleStorageCompiled.json')