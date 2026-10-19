from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

w3 = Web3(Web3.HTTPProvider("https://l1testnet.trustkeys.network"))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

h = "0x348e7c0036227faf30d9885acdf6fa1e1c9af99bd1b4abc81bf1bca094ae0d3b"
rcpt = w3.eth.get_transaction_receipt(h)
tx   = w3.eth.get_transaction(h)
blk  = w3.eth.get_block(rcpt["blockNumber"])

base_fee  = blk["baseFeePerGas"]
gas_used  = rcpt["gasUsed"]
eff_price = rcpt["effectiveGasPrice"]

paid   = gas_used * eff_price
burned = gas_used * base_fee
tip    = gas_used * (eff_price - base_fee)

print("type              =", tx["type"])   # mong đợi 2
print("gasUsed           =", gas_used)     # mong đợi 21000
print("baseFee           =", base_fee, "wei")
print("effectiveGasPrice =", eff_price, "wei")
print("maxFeePerGas      =", tx.get("maxFeePerGas"))
print("maxPriorityFee    =", tx.get("maxPriorityFeePerGas"))
print(paid, "=", burned, "+", tip, "?", paid == burned + tip)