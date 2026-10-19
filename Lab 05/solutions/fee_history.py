from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

w3 = Web3(Web3.HTTPProvider("https://l1testnet.trustkeys.network"))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

print("Connected:", w3.is_connected(), "| chainId =", w3.eth.chain_id,
      "| head =", w3.eth.block_number)

# eth_getBlockByNumber
blk = w3.eth.get_block("latest")
print("gasLimit =", blk["gasLimit"], "| gasUsed =", blk["gasUsed"])
print("baseFeePerGas =", blk["baseFeePerGas"], "wei")

# eth_getBalance (thay bằng địa chỉ MetaMask của bạn)
addr = "0xA3adDeD89109E99BCdcA1365A2303eE56D23A533"
bal = w3.eth.get_balance(Web3.to_checksum_address(addr))
print("balance =", bal, "wei =", Web3.from_wei(bal, "ether"), "coin")

# eth_feeHistory
fh = w3.eth.fee_history(20, "latest", [10, 50, 90])
ratios = fh["gasUsedRatio"]
for i, base in enumerate(fh["baseFeePerGas"][:-1]):
    print(fh["oldestBlock"] + i, base, f"{ratios[i]*100:.2f}%")
print("next block projected baseFee =", fh["baseFeePerGas"][-1], "wei")

avg = sum(ratios) / len(ratios)
print(f"avg gasUsedRatio = {avg*100:.2f}% ->",
      "chain is BUSY" if avg > 0.5 else "chain is quiet")