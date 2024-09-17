import os
import time

from dotenv import load_dotenv
import pywaves as pw
import requests

class WavesConnection:

    def __init__(self):
        load_dotenv()
        self.seed = os.getenv("seed")
        self.node = os.getenv("node")
        self.contractAddress = os.getenv("contractAddress")
        self.network = os.getenv("network")
        self.chainId = 87
        self.assetId = os.getenv("assetId")

        if self.network == "testnet":
            self.chainId = 84

        pw.setNode(self.node, self.network)
        self.myAddress = pw.Address(seed=self.seed)

    def getPaymentForTaskType(self, taskType):
        price = requests.get(self.node + '/addresses/data/' + self.contractAddress + '/price_' + taskType).json()["value"]

        return price

    def waitForSolution(self, taskId):
        try:
            solution = requests.get(self.node + '/addresses/data/' + self.contractAddress + "/" + taskId).json()["value"]

            return solution
        except:
            time.sleep(3)

            return self.waitForSolution(taskId)


    def solveTask(self, task, taskType):
        try:
            necessaryPaymentAmount = self.getPaymentForTaskType(taskType)
            args = [
                {"type": "string", "value": task},
                {"type": "string", "value": taskType}
            ]
            payment = [
                {"assetId": self.assetId, "amount": necessaryPaymentAmount}
            ]
            tx = self.myAddress.invokeScript(self.contractAddress, "registerTask", args, payment)

            taskId = tx["id"] + '_' + tx["senderPublicKey"] + '_result_' + taskType

            return self.waitForSolution(taskId)
        except Exception as err:
            print(err)