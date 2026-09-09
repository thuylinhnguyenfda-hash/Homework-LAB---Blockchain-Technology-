from eth_account import Account
from eth_account.messages import encode_defunct

# Tạo một tài khoản mới ngẫu nhiên (TUYỆT ĐỐI không dùng khóa này cho tiền thật)
acct = Account.create() 
print("address:", acct.address)

# Tạo thông điệp và mã hóa theo chuẩn Ethereum
msg = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 3")

# Ký thông điệp
sig = Account.sign_message(msg, acct.key)
print("r,s,v:", hex(sig.r), hex(sig.s), sig.v)

sig2 = Account.sign_message(msg, acct.key)
print("Chữ ký lần 2 (r,s,v):", hex(sig2.r), hex(sig2.s), sig2.v)

# Khôi phục địa chỉ chỉ từ chữ ký
who = Account.recover_message(msg, signature=sig.signature)
print("recovered:", who, "| match:", who == acct.address)

# Sửa 1 ký tự (Tamper 1 character) - Đổi "Buoi 3" thành "Buoi 4"
bad = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 4")
print("tampered ->", Account.recover_message(bad, signature=sig.signature))