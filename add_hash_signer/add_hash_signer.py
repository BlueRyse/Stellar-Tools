from stellar_sdk import Keypair, Network, Server, TransactionBuilder, SignerKey
import hashlib

class add_hash_signer:
    def __init__(self, source_secr_seed, signer_string, fee = 100):
        self.fee = fee
        self.server = Server("https://horizon-testnet.stellar.org")
        self.source = Keypair.from_secret(source_secr_seed)
        self.source_account = self.server.load_account(account_id=self.source.public_key)
        self.sha256 = hashlib.sha256(signer_string.encode('utf-8')).hexdigest()
        self.__create_transaction()

    def __create_transaction(self):
        self.transaction = (
            TransactionBuilder(
                source_account = self.source_account,
                network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee = self.fee
            )
         .add_text_memo("Added signer")
         .append_hashx_signer(
          sha256_hash = self.sha256,
          weight = 1
          )
         .set_timeout(30)  # Make this transaction valid for the next 30 seconds only
         .build()
        )
        self.__execute_transaction()

    def __execute_transaction(self):
        self.transaction.sign(self.source)
        self.response = self.server.submit_transaction(self.transaction)
