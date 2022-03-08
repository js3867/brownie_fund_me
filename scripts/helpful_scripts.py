from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8  # github has this as 8, youtube has 18..?
STARTING_PRICE = 2000_00000000  # this is to match 2000 + 8dps
# rather than hard code any numbers, use ALL_CAPS variable for 'should never change', as Rock said


def get_account():
    # if network.show_active() == "development":
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed!")
    # 18, 20... required due to contructor parameters in MockV3~.sol
