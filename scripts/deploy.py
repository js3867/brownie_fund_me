from brownie import FundMe, config, network
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like Rinkeby, use the associated address "0x8A7..."
    # brownie can pass this address from the .sol compiler _priceFeed to our XYZ.deploy function

    # however, if we're not on persistent network, deploy mocks
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        

    fund_me = FundMe.deploy(
        "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e",
        {"from": account},
        publish_source=True,
    )  # "publish source code = Yes"
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
