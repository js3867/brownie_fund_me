from brownie import FundMe, config, accounts, network, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    # account = get_account() << needs to be altered by network
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like Rinkeby, use the associated address "0x8A7..."
    # brownie can pass this address from the .sol compiler _priceFeed to our XYZ.deploy function

    # however, if we're not on persistent network, deploy mocks:
    # IF deployment network is NOT development, take priceFeed from active_network
    #
    # when using Ganache-local, although for testing, is not 'development' so need to expand definition
    # we can add multiple 'development' chains -- see helpful_scripts/LOCAL_BL...
    # $brownie run scripts/deploy.py --network ganache-local
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = get_account()
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    # ELSE use our mock priceFeed regardless of what network it is using MockV3~.sol
    # i.e. running on development chain (Ganache)
    else:
        account = accounts[0]
        deploy_mocks()  # whole function moved to 'helpful_sctripts'
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
        # "publish source code = based on Verify; we only set up API for Rinkeby etherscan,
        # so only set as True for that' rest are False
    )

    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
