import os
import re

# Example dictionaries
carrier_names_and_codes = {
    "maersk": "MAEU",
    "msc": "MSCU",
    "cma": "CMAU",
    "hapag": "HLCU",
}

contract_numbers = {
    "12345": "Contract A",
    "67890": "Contract B",
    "CNTR001": "Contract C",
}


def check_for_company(file_name_root: str, carrier_dict: dict) -> str | None:
    """
    Check if any substring in the file name corresponds to a key in carrier_dict.
    Returns the value if found, else None.
    """
    file_name_lower = file_name_root.lower()
    for key, value in carrier_dict.items():
        if key.lower() in file_name_lower:
            return value
    return None


def check_for_contract(file_name_root: str, contract_dict: dict) -> str | None:
    """
    Split file name into tokens and check if any match a known contract number.
    Returns the value if found, else None.
    """
    tokens = re.split(r'[\s\-_]+', file_name_root)  # split on space, dash, underscore
    for token in tokens:
        if token in contract_dict:
            return contract_dict[token]
    return None


def parse_file_name(file_path: str,
                    carrier_dict: dict = carrier_names_and_codes,
                    contract_dict: dict = contract_numbers) -> str | None:
    """
    Parse file path:
    1) Extract file name root
    2) Check for company
    3) If not found, check for contract number
    Returns the first match found, else None.
    """
    # Step 1: Extract file name root (without extension)
    file_name = os.path.basename(file_path)
    file_name_root, _ = os.path.splitext(file_name)

    # Step 2: Check for company
    company = check_for_company(file_name_root, carrier_dict)
    if company:
        return company

    # Step 3: Check for contract
    contract = check_for_contract(file_name_root, contract_dict)
    if contract:
        return contract

    # Nothing found
    return None


# Example usage
if __name__ == "__main__":
    print(parse_file_name("/docs/contracts/maersk_agreement_2025.pdf"))  # → MAEU
    print(parse_file_name("msc_shipping_CNTR001.xlsx"))  # → MSCU (company match wins first)
    print(parse_file_name("contract-12345.txt"))  # → Contract A
    print(parse_file_name("random_file.pdf"))  # → None
