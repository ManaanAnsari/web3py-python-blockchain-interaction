from configparser import ConfigParser
from hexbytes import HexBytes
from web3.middleware import geth_poa_middleware
import json


erc20_abi = json.load(open('out/ERC20.sol/MyToken.json', 'r'))
erc20_abi = erc20_abi['abi']
simple_storage_abi = json.load(open('out/SimpleStorage.sol/SimpleStorage.json', 'r'))
simple_storage_abi = simple_storage_abi['abi']


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


def transfer_erc20(recipient, token_address, amount):
    token_contract = w3.eth.contract(abi=erc20_abi, address=token_address)
    nonce = w3.eth.get_transaction_count(account)
    tx = token_contract.functions.transfer(recipient, amount).build_transaction({
        'nonce': nonce,
        'gas': 60_000,
        'gasPrice': w3.eth.gas_price,
    })
    print(tx)
    signed_tx = w3.eth.account.sign_transaction(tx, config.get('Account_Details', 'private_key'))
    trx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(w3.eth.get_transaction_receipt(trx_hash))
    print(w3.eth.get_transaction(trx_hash))
    
def get_erc20_balance(token_address, account):
    token_contract = w3.eth.contract(abi=erc20_abi, address=token_address)
    return token_contract.functions.balanceOf(account).call()
 

recipient = '0x70997970C51812dc3A010C7d01b50e0d17dc79C8'
send_eth(recipient)
w3.eth.get_balance(recipient)

transfer_erc20(recipient, '0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9', 1000)

get_erc20_balance('0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9', recipient)

def interact_simpleStorage(contract_address):
    simple_storage_contract = w3.eth.contract(abi=simple_storage_abi, address=contract_address)
    simple_storage_contract.functions.storedData().call()

    trx = simple_storage_contract.functions.set(100).build_transaction({
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 100_000,
        'gasPrice': w3.eth.gas_price,
    })

    signed_trx = w3.eth.account.sign_transaction(trx, config.get('Account_Details', 'private_key'))

    trx_hash = w3.eth.send_raw_transaction(signed_trx.rawTransaction)
    receipt = w3.eth.get_transaction_receipt(trx_hash)
    print(receipt)

interact_simpleStorage('0xA51c1fc2f0D1a1b8494Ed1FE312d7C3a78Ed91C0')





