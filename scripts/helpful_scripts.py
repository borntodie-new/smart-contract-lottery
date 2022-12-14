from os import link
from brownie import (
    accounts,
    config,
    network,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface
)

FORKED_LOCAL_ENVIRONMENTS = ("mainnet-fork-dev", "mainnet-fork")
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ("development", "ganache-local")


def get_account(index=None, id=None):
    # 1. accounts[0]
    # 2. accounts.add("private_key")
    # 3. accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    'link_token': LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses form the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deploeyed
            version of this contract.
            MockV3Aggregator[-1]

    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:  # Local
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:  # online
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimal=DECIMALS, initial=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimal, initial, {"from": account})
    link_token = LinkToken.deploy({'from': account})
    VRFCoordinatorMock.deploy(link_token, {'from': account})
    print("Deployed!")

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000): # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {'from': account, 'gasLimit': 20000})
    # link_token_contract = interface.LinktokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {'from': account})
    tx.wait(1)
    print("Fund contract")
    return tx
