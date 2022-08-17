# 0.025654576519905384
# 250000000000000000
from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_get_entrance_fee():
    # deploy account
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account}
    )
    result = lottery.getEntrenceFee()
    print(result)
    assert result > Web3.toWei(0.024, "ether")
    assert result < Web3.toWei(0.054, "ether")
# 54000000000000000
# 262497181686343335558411711

def main():
    test_get_entrance_fee()
