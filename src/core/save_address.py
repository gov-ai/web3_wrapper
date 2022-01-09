def save_address(contract_address, contract_name):
    with open(f'contract/{contract_name}.address', 'a') as fp:
        fp.write(f"{contract_address}\n")

def fetch_addresses(contract_name):
    with open(f'contract/{contract_name}.address', 'r') as fp:
        addresses = fp.read()
    addresses = addresses.split("\n")
    addresses = [i for i in addresses if i!='']
    return addresses
