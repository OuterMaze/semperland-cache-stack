CURRENCY_DEFINITION_PLUGIN_CONTRACT_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_metaverse",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_earningsReceiver",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "_wmaticImage",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_wmaticIcon16x16",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_wmaticIcon32x32",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_wmaticIcon64x64",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_beatImage",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_beatIcon16x16",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_beatIcon32x32",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_beatIcon64x64",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "_timeout",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "updatedBy",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newReceiver",
                "type": "address"
            }
        ],
        "name": "BrandCurrencyDefinitionEarningsReceiverUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "brandId",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "definedBy",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "paidPrice",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "description",
                "type": "string"
            }
        ],
        "name": "CurrencyDefined",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "updatedBy",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newCost",
                "type": "uint256"
            }
        ],
        "name": "CurrencyDefinitionCostUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "updatedBy",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "CurrencyMetadataUpdated",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "BEATType",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "WMATICType",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "brandCurrencyDefinitionEarningsReceiver",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "currencyDefinitionCost",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "initialize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "initialized",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "metaverse",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "interfaceId",
                "type": "bytes4"
            }
        ],
        "name": "supportsInterface",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "timeout",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            }
        ],
        "name": "uri",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [],
        "name": "title",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            }
        ],
        "name": "currencyExists",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "newCost",
                "type": "uint256"
            }
        ],
        "name": "setCurrencyDefinitionCost",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_newReceiver",
                "type": "address"
            }
        ],
        "name": "setBrandCurrencyDefinitionEarningsReceiver",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_definedBy",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_description",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_image",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_icon16x16",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_icon32x32",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_icon64x64",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_color",
                "type": "string"
            }
        ],
        "name": "defineSystemCurrency",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "_delegation",
                "type": "bytes"
            },
            {
                "internalType": "address",
                "name": "_brandId",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_description",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_image",
                "type": "string"
            }
        ],
        "name": "defineBrandCurrency",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
        "payable": True
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "_delegation",
                "type": "bytes"
            },
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_image",
                "type": "string"
            }
        ],
        "name": "setCurrencyImage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "_delegation",
                "type": "bytes"
            },
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_color",
                "type": "string"
            }
        ],
        "name": "setCurrencyColor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "_delegation",
                "type": "bytes"
            },
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_icon16x16",
                "type": "string"
            }
        ],
        "name": "setCurrencyIcon16x16",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "_delegation",
                "type": "bytes"
            },
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_icon32x32",
                "type": "string"
            }
        ],
        "name": "setCurrencyIcon32x32",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "_delegation",
                "type": "bytes"
            },
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_icon64x64",
                "type": "string"
            }
        ],
        "name": "setCurrencyIcon64x64",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_plugIn",
                "type": "address"
            }
        ],
        "name": "setMintingPlugin",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "_data",
                "type": "bytes"
            }
        ],
        "name": "mintCurrency",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
