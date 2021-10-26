from stellar_sdk import Keypair, Network, Server, TransactionBuilder

class account_merge:

    def __init__(self, source_secr_seed, destination, fee = 100):
        self.fee = fee
        self.destination = destination
        self.server = Server("https://horizon.stellar.org/")
        self.source = Keypair.from_secret(source_secr_seed)
        self.source_account = self.server.load_account(account_id=self.source.public_key)
        self.__create_transaction()

    def __create_transaction(self):
        self.transaction = (
            TransactionBuilder(
                source_account = self.source_account,
                network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE,
                base_fee = self.fee
            )
            .append_account_merge_op(
                destination=self.destination
            )
            .build()
        )
        self.__execute_transaction()

    def __execute_transaction(self):
        self.transaction.sign(self.source)
        self.response = self.server.submit_transaction(self.transaction)
