from solcx import compile_source, install_solc

from data.config import SOLC_VERSION


def get_abi_and_bytecode_from_contract(
        contract_path: str,
        solc_version: str = SOLC_VERSION
) -> tuple[list, str]:
    install_solc(solc_version)

    with open(contract_path) as f:
        contract_text = f.read()

    compiled_solidity = compile_source(
        source=contract_text,
        output_values=['abi', 'bin'],
        solc_version=solc_version
    )

    contract_id, contract_interface = compiled_solidity.popitem()
    abi, bytecode = contract_interface['abi'], contract_interface['bin']
    return abi, bytecode
