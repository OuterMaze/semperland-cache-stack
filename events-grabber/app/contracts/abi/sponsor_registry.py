SPONSOR_REGISTRY_CONTRACT_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_metaverse",
                "type": "address"
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
                "name": "_sponsor",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "_brandId",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "_sponsored",
                "type": "bool"
            }
        ],
        "name": "Sponsored",
        "type": "event"
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
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "sponsored",
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
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "sponsors",
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
                "internalType": "address",
                "name": "_brandId",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "_sponsored",
                "type": "bool"
            }
        ],
        "name": "sponsor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_sponsor",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "_enabled",
                "type": "bool"
            }
        ],
        "name": "setSponsor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "_interfaceId",
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
    }
]
