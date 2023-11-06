BRAND_REGISTRY_CONTRACT_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_metaverse",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_brandEarningsReceiver",
                "type": "address"
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
                "name": "brandId",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "permission",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "set",
                "type": "bool"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "name": "BrandPermissionChanged",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "registeredBy",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "brandId",
                "type": "address"
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
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "price",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "mintedBy",
                "type": "address"
            }
        ],
        "name": "BrandRegistered",
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
        "name": "BrandRegistrationCostUpdated",
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
                "internalType": "address",
                "name": "newReceiver",
                "type": "address"
            }
        ],
        "name": "BrandRegistrationEarningsReceiverUpdated",
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
                "internalType": "address",
                "name": "brand",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "committed",
                "type": "bool"
            }
        ],
        "name": "BrandSocialCommitmentUpdated",
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
                "internalType": "address",
                "name": "brandId",
                "type": "address"
            }
        ],
        "name": "BrandUpdated",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "brandEarningsReceiver",
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
        "name": "brandRegistrationCost",
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
                "name": "_newCost",
                "type": "uint256"
            }
        ],
        "name": "setBrandRegistrationCost",
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
        "name": "setBrandRegistrationEarningsReceiver",
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
            }
        ],
        "name": "registerBrand",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
        "payable": True
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
                "name": "_committed",
                "type": "bool"
            }
        ],
        "name": "updateBrandSocialCommitment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_brandId",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_newOwner",
                "type": "address"
            }
        ],
        "name": "onBrandOwnerChanged",
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
                "name": "_image",
                "type": "string"
            }
        ],
        "name": "updateBrandImage",
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
                "name": "_challengeUrl",
                "type": "string"
            }
        ],
        "name": "updateBrandChallengeUrl",
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
                "name": "_icon",
                "type": "string"
            }
        ],
        "name": "updateBrandIcon16x16Url",
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
                "name": "_icon",
                "type": "string"
            }
        ],
        "name": "updateBrandIcon32x32Url",
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
                "name": "_icon",
                "type": "string"
            }
        ],
        "name": "updateBrandIcon64x64Url",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_brandId",
                "type": "address"
            }
        ],
        "name": "brandMetadataURI",
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
                "internalType": "address",
                "name": "_brandId",
                "type": "address"
            }
        ],
        "name": "brandExists",
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
        "inputs": [
            {
                "internalType": "address",
                "name": "_brandId",
                "type": "address"
            },
            {
                "internalType": "bytes32",
                "name": "_permission",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
            }
        ],
        "name": "isBrandAllowed",
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
            }
        ],
        "name": "isCommitted",
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
                "internalType": "bytes32",
                "name": "_permission",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "_user",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "_allowed",
                "type": "bool"
            }
        ],
        "name": "brandSetPermission",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
