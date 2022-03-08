# when verifying and publishing contracts on Etherscan, etherscan is unable to read import @chainlink stuff
# as such, we can copy them into here, '__init__.py' in a process known as 'flatten'ing
#
# import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
#
### HOWEVER...
#
# much better way is to use an etherscan login API to automatically do it
# see: https://etherscan.io/myapikey
