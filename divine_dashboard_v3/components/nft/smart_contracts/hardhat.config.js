/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

// Default private key for development - DO NOT USE THIS IN PRODUCTION
const DEFAULT_PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";

module.exports = {
    solidity: {
        version: "0.8.20",
        settings: {
            optimizer: {
                enabled: true,
                runs: 200
            }
        }
    },
    networks: {
        hardhat: {
            chainId: 31337
        },
        localhost: {
            url: "http://127.0.0.1:8545",
            chainId: 31337
        },
        sepolia: {
            url: process.env.SEPOLIA_RPC_URL || "https://rpc.sepolia.org",
            accounts: [process.env.PRIVATE_KEY || DEFAULT_PRIVATE_KEY],
            chainId: 11155111
        },
        mumbai: {
            url: process.env.MUMBAI_RPC_URL || "https://rpc-mumbai.maticvigil.com",
            accounts: [process.env.PRIVATE_KEY || DEFAULT_PRIVATE_KEY],
            chainId: 80001
        }
    },
    etherscan: {
        apiKey: {
            sepolia: process.env.ETHERSCAN_API_KEY || "",
            polygonMumbai: process.env.POLYGONSCAN_API_KEY || ""
        }
    },
    gasReporter: {
        enabled: process.env.REPORT_GAS ? true : false,
        currency: "USD",
        coinmarketcap: process.env.COINMARKETCAP_API_KEY || "",
        token: "ETH",
        gasPriceApi: "https://api.etherscan.io/api?module=proxy&action=eth_gasPrice"
    },
    paths: {
        sources: "./contracts",
        tests: "./test",
        artifacts: "./artifacts",
        cache: "./cache"
    },
    mocha: {
        timeout: 40000
    }
}; 