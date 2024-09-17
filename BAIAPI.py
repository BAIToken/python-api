from dotenv import load_dotenv
import os

from connectors import wavesConnection
from connectors import evmConnection

class BAIAPI():
    def __init__(self):
        load_dotenv()
        self.type = os.getenv("type")

        if self.type == "Waves":
            self.blockChainConnection = wavesConnection.WavesConnection()
        elif self.type == "evm":
            self.blockChainConnection = evmConnection.EvmConnection()

    def solveTask(self, task, tasktype):
        try:
            return self.blockChainConnection.solveTask(task, tasktype)
        except Exception as err:
            print("Problem solving the task " + err)

