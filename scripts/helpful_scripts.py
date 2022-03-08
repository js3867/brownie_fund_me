from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 18
STARTING_PRICE = 2000  # rather than hard code any numbers, use ALL_CAPS variable for 'should never change', as Rock said


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
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account}
        )
        # 18, 20... required due to contructor parameters in MockV3~.sol
    print("Mocks Deployed!")
