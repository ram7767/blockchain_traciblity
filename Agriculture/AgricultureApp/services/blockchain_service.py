"""
Blockchain Service — Handles all Web3/Ethereum interactions.
Provides a clean interface for saving and reading data from the blockchain.
Falls back gracefully if the blockchain is unavailable.
"""

import json
import os
import logging

logger = logging.getLogger(__name__)

# Blockchain availability flag
BLOCKCHAIN_AVAILABLE = False

try:
    from web3 import Web3, HTTPProvider
    WEB3_INSTALLED = True
except ImportError:
    WEB3_INSTALLED = False
    logger.warning("web3 not installed — blockchain features disabled")


class BlockchainService:
    """Singleton-style service for blockchain interactions."""

    _instance = None
    _web3 = None
    _contract = None

    BLOCKCHAIN_URL = 'http://127.0.0.1:9545'
    CONTRACT_ADDRESS = '0xd374Cb05bd6187D6cF905D7bBD85f2b704fBDD29'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._web3 is None:
            self._connect()

    def _connect(self):
        """Establish Web3 connection and load contract."""
        global BLOCKCHAIN_AVAILABLE

        if not WEB3_INSTALLED:
            BLOCKCHAIN_AVAILABLE = False
            return

        try:
            self._web3 = Web3(HTTPProvider(self.BLOCKCHAIN_URL))
            if not self._web3.isConnected():
                logger.warning("Cannot connect to blockchain at %s", self.BLOCKCHAIN_URL)
                BLOCKCHAIN_AVAILABLE = False
                return

            self._web3.eth.defaultAccount = self._web3.eth.accounts[0]

            # Load contract ABI
            contract_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                'Agricultural.json'
            )
            if os.path.exists(contract_path):
                with open(contract_path) as f:
                    contract_json = json.load(f)
                    contract_abi = contract_json['abi']
                self._contract = self._web3.eth.contract(
                    address=self.CONTRACT_ADDRESS, abi=contract_abi
                )
                BLOCKCHAIN_AVAILABLE = True
                logger.info("Blockchain connected successfully")
            else:
                logger.warning("Contract JSON not found at %s", contract_path)
                BLOCKCHAIN_AVAILABLE = False

        except Exception as e:
            logger.warning("Blockchain connection failed: %s", str(e))
            BLOCKCHAIN_AVAILABLE = False

    @property
    def is_available(self):
        return BLOCKCHAIN_AVAILABLE and self._contract is not None

    def reconnect(self):
        """Try to reconnect to blockchain."""
        self._web3 = None
        self._contract = None
        self._connect()

    # --- User Operations ---

    def get_users(self):
        """Read all users from blockchain."""
        if not self.is_available:
            return ""
        try:
            return self._contract.functions.getUser().call()
        except Exception as e:
            logger.error("Failed to read users: %s", str(e))
            return ""

    def save_user(self, data):
        """Save user data to blockchain."""
        if not self.is_available:
            return None
        try:
            current = self.get_users()
            msg = self._contract.functions.addUser(current + data).transact()
            return self._web3.eth.waitForTransactionReceipt(msg)
        except Exception as e:
            logger.error("Failed to save user: %s", str(e))
            return None

    # --- Product Operations ---

    def get_products(self):
        """Read all products from blockchain."""
        if not self.is_available:
            return ""
        try:
            return self._contract.functions.getTracingData().call()
        except Exception as e:
            logger.error("Failed to read products: %s", str(e))
            return ""

    def save_product(self, data):
        """Save product data to blockchain."""
        if not self.is_available:
            return None
        try:
            current = self.get_products()
            msg = self._contract.functions.setTracingData(current + data).transact()
            return self._web3.eth.waitForTransactionReceipt(msg)
        except Exception as e:
            logger.error("Failed to save product: %s", str(e))
            return None

    def update_products(self, data):
        """Overwrite all product data on blockchain."""
        if not self.is_available:
            return None
        try:
            msg = self._contract.functions.setTracingData(data).transact()
            return self._web3.eth.waitForTransactionReceipt(msg)
        except Exception as e:
            logger.error("Failed to update products: %s", str(e))
            return None

    # --- Purchase Operations ---

    def get_purchases(self):
        """Read all purchases from blockchain."""
        if not self.is_available:
            return ""
        try:
            return self._contract.functions.getPurchase().call()
        except Exception as e:
            logger.error("Failed to read purchases: %s", str(e))
            return ""

    def save_purchase(self, data):
        """Save purchase data to blockchain."""
        if not self.is_available:
            return None
        try:
            current = self.get_purchases()
            msg = self._contract.functions.setPurchase(current + data).transact()
            return self._web3.eth.waitForTransactionReceipt(msg)
        except Exception as e:
            logger.error("Failed to save purchase: %s", str(e))
            return None


# Module-level singleton
blockchain = BlockchainService()
