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

    def bulk_write(self, trans):
        self.collection.bulk_write(
            list(map(lambda tran: UpdateOne(
                {"hash": tran["hash"]}, {"$set": tran}, True), trans))
        )

    def bulk_write_logs(self, logs):

        def format_write(log):
            logs_dict = {}
            logs_dict[str(log["logIndex"])] = log
            return UpdateOne(
                {"hash": log["transactionHash"]},
                {"$set": { "logs": logs_dict } },
                True
            )

        self.collection.bulk_write(
            list(map(lambda log: format_write(log), logs))
        )
