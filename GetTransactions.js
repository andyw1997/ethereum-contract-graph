var Web3 = require('web3');
var config = require('./config.json');
var fs = require("fs");
module.exports.dump = function (dexAddress) {
    yieldDexDump()
}

function yieldDexDump() {
    console.log("RUNNING")
    if (typeof web3 !== 'undefined') {
        web3 = new Web3(web3.currentProvider);
    } else {
        // set the provider you want from Web3.providers
        web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
    }

    // look at last 1000 blocks
    endBlockNumber = web3.eth.blockNumber;
    console.log("endBlockNumber = " + endBlockNumber);
    startBlockNumber = endBlockNumber - 1000;
    console.log("startBlockNumber = " + startBlockNumber);

    let output_buffer = []; // Written to disk at end 
    for (let i = startBlockNumber; i <= endBlockNumber; i++) {
        let block = web3.eth.getBlock(i, true);
        if (block != null && block.transactions != null) {
            block.transactions.forEach( function(e) {
                output_buffer.append((e.from, e.to));
            })
        }
    }
    fs.writeFile("data/transactions.json",JSON.stringify(output_buffer));
}