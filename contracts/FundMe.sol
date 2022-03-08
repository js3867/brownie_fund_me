// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;
// pragma solidity ^0.6.6;

// this import is equivalent to pasting all of the code in from that specific page/repo
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] funders;
    // ******* NEW TO LESSON 6 *******
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        // add instruction for where to pull price feed from instead of hard coding the address below
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    // 1 Wei = 1e-9 Gwei = 1e-18 Ether <check this>
    function fund() public payable {
        // set a minimum vale to be Funded
        uint256 minUSD = 5 * 10**18;
        require(
            getConversionRate(msg.value) > minUSD,
            "spend more, don't be so tight!"
        );

        // add funders to mapping
        addressToAmountFunded[msg.sender] += msg.value;

        // add funding address to list
        // so each ETH address that Funds this contract is added to the list
        // for easy access to see who has contributed
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        // AggregatorV3Interface priceFeed = AggregatorV3Interface( <<< NO LONGER REQUIRED IN L6
        //     0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        // );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        // we can still return a 5 item tuple without providing 'unused values'
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10_000_000_000);
    }

    // 1 gwei = 1000000000 wei (1e9)
    // 1 gwei = 0.000000001 eth (1e-9)
    //
    // 1. pass in amount of eth
    // 2. func pulls 1ETH price
    // 3. multiplies together
    // 4. converts eth>wei 10**18
    // == 0.5 * 2750usd * 10**18
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / (10**18); // solidity words in wei integers, so must convert ETH to WEI
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }

    // the modifier code shall run..
    // ..running the calling function upon "_;"
    modifier onlyOwner() {
        // _; << calling function runs here
        require(msg.sender == owner);
        _; // << calling function runs here
    }

    // address(this) = this smart contract
    // .balance = the value held in the contract at that time
    function withdraw() public payable onlyOwner {
        // only allow contract owner to withdraw (via modifier)
        // ..as in the address who deployed the contract ONLY
        payable(msg.sender).transfer(address(this).balance); // "transfer thisContract balance to he who clicks Withdraw IF he is the contract deployer/owner"

        // following withdrawal, loop thru list of funders..
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            // ..set funder address in order to..
            address funder = funders[funderIndex];
            // ..reset mapping 'AmountFunded' for this address
            addressToAmountFunded[funder] = 0;
        }
        // then funders array will be initialized to 0
        // ..thereby remove all now-irrelevant addresses
        funders = new address[](0);
    }
}
