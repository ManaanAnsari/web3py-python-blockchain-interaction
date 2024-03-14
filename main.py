from configparser import ConfigParser
from hexbytes import HexBytes
from web3.middleware import geth_poa_middleware
config = ConfigParser()
config.read('config.ini')

account = config.get('Account_Details', 'account')
print(account)

http_rpc_url = config.get('Connection_Details', 'http_rpc_url')

from web3 import Web3, EthereumTesterProvider

w3 = Web3(Web3.HTTPProvider(http_rpc_url))

# whats this?


w3.middleware_onion.inject(geth_poa_middleware, layer=0)

w3.eth.block_number

w3.eth.get_balance(account)

w3.from_wei(w3.eth.get_balance(account), 'ether')
w3.eth.get_transaction_count(account)


# transfger ether

# acc2 = config.get('Account_Details', 'account2')
def send_eth(recipient):
    nonce = w3.eth.get_transaction_count(account)
    tx = {
        'nonce': nonce,
        'to': recipient,
        'value': w3.to_wei(0.01, 'ether'),
        'gas': 21_000,
        'gasPrice': w3.eth.gas_price,
    }

    signed_tx = w3.eth.account.sign_transaction(tx, config.get('Account_Details', 'private_key'))
    trx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(w3.eth.get_transaction_receipt(trx_hash))
    print(w3.eth.get_transaction(trx_hash))


recipient = '0x70997970C51812dc3A010C7d01b50e0d17dc79C8'
send_eth(recipient)

