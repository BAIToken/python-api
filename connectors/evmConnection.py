import os
import time

from dotenv import load_dotenv
from ethtoken.abi import EIP20_ABI
from web3 import Web3

class EvmConnection:

    abi = [
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "previousAdmin",
                    "type": "address"
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "newAdmin",
                    "type": "address"
                }
            ],
            "name": "AdminChanged",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "beacon",
                    "type": "address"
                }
            ],
            "name": "BeaconUpgraded",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "uint8",
                    "name": "version",
                    "type": "uint8"
                }
            ],
            "name": "Initialized",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "previousOwner",
                    "type": "address"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address"
                }
            ],
            "name": "OwnershipTransferred",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "string",
                    "name": "taskId",
                    "type": "string"
                },
                {
                    "indexed": False,
                    "internalType": "string",
                    "name": "response",
                    "type": "string"
                }
            ],
            "name": "TaskCommitted",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "string",
                    "name": "taskId",
                    "type": "string"
                },
                {
                    "indexed": False,
                    "internalType": "string",
                    "name": "description",
                    "type": "string"
                }
            ],
            "name": "TaskRegistered",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "implementation",
                    "type": "address"
                }
            ],
            "name": "Upgraded",
            "type": "event"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "addr",
                    "type": "address"
                }
            ],
            "name": "addressToString",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "pure",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "aiToken",
            "outputs": [
                {
                    "internalType": "contract IERC20",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "name": "checkedOutTasksByAgentAndType",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "taskId",
                    "type": "string"
                }
            ],
            "name": "checkoutTask",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "taskId",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "response",
                    "type": "string"
                }
            ],
            "name": "commitTask",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "agent",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "taskType",
                    "type": "string"
                }
            ],
            "name": "getCheckedOutTaskByAgentAndType",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "taskId",
                    "type": "string"
                }
            ],
            "name": "getDescriptionForTaskId",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getLastCounter",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "taskType",
                    "type": "string"
                }
            ],
            "name": "getOpenTasksByType",
            "outputs": [
                {
                    "internalType": "string[]",
                    "name": "",
                    "type": "string[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "taskType",
                    "type": "string"
                }
            ],
            "name": "getPriceForType",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "taskId",
                    "type": "string"
                }
            ],
            "name": "getResultForTaskId",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "aiTokenAddress",
                    "type": "address"
                }
            ],
            "name": "initialize",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "name": "openTasksByType",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "name": "prices",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "proxiableUUID",
            "outputs": [
                {
                    "internalType": "bytes32",
                    "name": "",
                    "type": "bytes32"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "description",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "taskType",
                    "type": "string"
                }
            ],
            "name": "registerTask",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "description",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "taskType",
                    "type": "string"
                }
            ],
            "name": "registerTaskCallback",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "renounceOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "taskType",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "price",
                    "type": "uint256"
                }
            ],
            "name": "setPriceForType",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "name": "tasks",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "description",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "typeId",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "status",
                    "type": "string"
                },
                {
                    "internalType": "string",
                    "name": "result",
                    "type": "string"
                },
                {
                    "internalType": "address",
                    "name": "initializer",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "checkedOutBy",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "registerHeight",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "registerTimestamp",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "checkoutHeight",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "checkoutTimestamp",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "commitHeight",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "commitTimestamp",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "name": "tasksWithCallback",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "string",
                            "name": "description",
                            "type": "string"
                        },
                        {
                            "internalType": "string",
                            "name": "typeId",
                            "type": "string"
                        },
                        {
                            "internalType": "string",
                            "name": "status",
                            "type": "string"
                        },
                        {
                            "internalType": "string",
                            "name": "result",
                            "type": "string"
                        },
                        {
                            "internalType": "address",
                            "name": "initializer",
                            "type": "address"
                        },
                        {
                            "internalType": "address",
                            "name": "checkedOutBy",
                            "type": "address"
                        },
                        {
                            "internalType": "uint256",
                            "name": "registerHeight",
                            "type": "uint256"
                        },
                        {
                            "internalType": "uint256",
                            "name": "registerTimestamp",
                            "type": "uint256"
                        },
                        {
                            "internalType": "uint256",
                            "name": "checkoutHeight",
                            "type": "uint256"
                        },
                        {
                            "internalType": "uint256",
                            "name": "checkoutTimestamp",
                            "type": "uint256"
                        },
                        {
                            "internalType": "uint256",
                            "name": "commitHeight",
                            "type": "uint256"
                        },
                        {
                            "internalType": "uint256",
                            "name": "commitTimestamp",
                            "type": "uint256"
                        }
                    ],
                    "internalType": "struct Task",
                    "name": "task",
                    "type": "tuple"
                },
                {
                    "internalType": "address",
                    "name": "callbackAddress",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address"
                }
            ],
            "name": "transferOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "newImplementation",
                    "type": "address"
                }
            ],
            "name": "upgradeTo",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "newImplementation",
                    "type": "address"
                },
                {
                    "internalType": "bytes",
                    "name": "data",
                    "type": "bytes"
                }
            ],
            "name": "upgradeToAndCall",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function"
        }
    ]

    def __init__(self):
        load_dotenv()
        self.privateKey = os.getenv("privateKey")
        self.node = os.getenv("endpoint")
        self.contractAddress = os.getenv("contractAddress")
        self.chainId = int(os.getenv("chainId"))
        self.w3 = Web3(Web3.HTTPProvider(self.node))
        self.tokenId = os.getenv("tokenId")
        self.contract = self.w3.eth.contract(address = self.contractAddress, abi =self.abi)
        self.myAddress = self.getAddressFromPrivateKey(self.privateKey)

    def getAddressFromPrivateKey(self, privateKeyHex):
        privateKeyBytes = bytes.fromhex(privateKeyHex) if isinstance(privateKeyHex, str) else privateKeyHex
        publicKey = self.w3.eth.account.privateKeyToAccount(privateKeyBytes).address

        return publicKey

    def getPaymentForTaskType(self, taskType):
        price = self.contract.functions.getPriceForType(taskType).call()

        return price

    def waitForSolution(self, taskId):
        solution = self.contract.functions.getResultForTaskId(taskId).call()

        if len(solution) > 0:
            return solution
        else:
            time.sleep(3)
            return self.waitForSolution(taskId)

    def solveTask(self, task, taskType):
        counter = self.contract.functions.getLastCounter().call()
        price = self.getPaymentForTaskType(taskType)
        tokenContract = self.w3.eth.contract(address=self.tokenId, abi=EIP20_ABI)
        nonce = self.w3.eth.getTransactionCount(self.myAddress)
        gasPrice = self.w3.eth.gasPrice
        estimatedGasApprove = tokenContract.functions.approve(self.contractAddress, price).estimateGas({'from': self.myAddress})
        approveTx = tokenContract.functions.approve(self.contractAddress, price).buildTransaction({
            'chainId': self.chainId,
            'gas': estimatedGasApprove,
            'gasPrice': gasPrice,
            'nonce': nonce
        })
        signedApproveTx = self.w3.eth.account.signTransaction(approveTx, private_key=self.privateKey)
        id = self.w3.eth.sendRawTransaction(signedApproveTx.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(id.hex())
        nonce += 1
        gasPrice = self.w3.eth.gasPrice
        estimatedGas = self.contract.functions.registerTask(task, taskType).estimateGas({'from': self.myAddress})
        tx = self.contract.functions.registerTask(task, taskType).buildTransaction({
            'chainId': self.chainId,
            'gas': estimatedGas,
            'gasPrice': gasPrice,
            'nonce': nonce
        })
        signed_tx = self.w3.eth.account.signTransaction(tx, private_key=self.privateKey)
        txId = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(txId, timeout=120)
        taskId = self.myAddress.lower() + '_' + str(counter + 1)

        return self.waitForSolution(taskId)

