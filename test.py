
from ast import literal_eval
from web3 import Web3



value = Web3.fromWei(literal_eval("0x00000000000000000000000000000000000000000000010f0cf064dd59200000"), 'ether')
print(value)