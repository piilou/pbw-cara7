import pandas as pd
import os
from dotenv import load_dotenv
import json
import subprocess
import re

from util.tokens import mint_token
from util.account import get_account

VIN_FILE_PATH = "VIN.csv"

df = pd.read_csv(VIN_FILE_PATH)

vin_numbers = df["VIN"].tolist()
print(f"VIN Numbers: {vin_numbers}")

# Get account info from seed and connect it
load_dotenv()
XRP_WALLET_SEED = os.getenv("XRP_WALLET_SEED")
print(f"Wallet Seed: {XRP_WALLET_SEED}")
wallet = get_account(XRP_WALLET_SEED)
print(f"Wallet address: {wallet.classic_address}")

def store_smart_contract_in_evm(data):
    # Define the command to be executed
    command = "cd ../evm-interaction && npx truffle migrate --network xrpl"

    # Execute the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the command to complete
    stdout, stderr = process.communicate()

    # Check if the command was executed successfully
    if process.returncode == 0:
        print("Command executed successfully")
        # print(stdout.decode())  # Print the standard output
    else:
        print("Error executing command")
        print(stderr.decode())  # Print the standard error
    # Use regular expression to find the contract address
    match = re.search(r'> contract address:\s+(0x[a-fA-F0-9]+)', stdout.decode())

    # Extract and print the contract address if found
    if match:
        contract_address = match.group(1)
        print("Contract Address:", contract_address)
    else:
        print("Contract address not found.")
    return contract_address

# Create smart contract for each VIN number and store them (EVM)
for vin in vin_numbers:
    print(f"Creating smart contract for VIN: {vin}")

    # Create a dictionary with VIN and smart contract address
    data = {"VIN": vin, "SmartContractAddress": smart_contract_address}

    # TODO Store SmartContract in EVM

    smart_contract_address = store_smart_contract_in_evm(data)

    # Create a JSON file named after the VIN number and store the data
    file_name = f"db/{vin}.json"
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
    results = mint_token(
        XRP_WALLET_SEED,
        smart_contract_address,
        0x0009,  # lsfBurnable + lsfTransferable, see https://xrpl.org/docs/references/protocol/data-types/nftoken/
        0x13A, # Transfer fee
        0, # Taxon
    )