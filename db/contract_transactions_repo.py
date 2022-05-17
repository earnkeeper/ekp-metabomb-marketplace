from ekp_sdk.db import MgClient
from pymongo import DESCENDING, UpdateOne


class ContractTransactionsRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['contract_transactions']
        self.collection.create_index("hash", unique=True)
        self.collection.create_index([("blockNumber", DESCENDING)])
        self.collection.create_index([("timeStamp", DESCENDING)])
        self.collection.create_index("source_contract_address")

    def get_latest(self, contract_address):
        return list(
            self.collection.find(
                {"source_contract_address": contract_address}
            )
            .sort("blockNumber", -1).limit(1)
        )

    def find_since_block_number(self, block_number):
        return list(
            self.collection
            .find({"blockNumber": {"$gte": block_number}})
            .sort("blockNumber")
        )

    def bulk_write(self, trans):
        self.collection.bulk_write(
            list(map(lambda tran: UpdateOne(
                {"hash": tran["hash"]}, {"$set": tran}, True), trans))
        )

    def bulk_write_logs(self, logs):

        def format_write(log):
            log_index = log["logIndex"]
            return UpdateOne(
                {"hash": log["transactionHash"]},
                {"$set": {f"logs.{log_index}": log}},
                True
            )

        self.collection.bulk_write(
            list(map(lambda log: format_write(log), logs))
        )
