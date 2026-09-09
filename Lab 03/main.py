import hashlib, time

def mine(data: bytes, k: int) -> tuple[int, float]:
    target = "0"*k
    nonce, t0 = 0, time.time()
    while True:
        h = hashlib.sha256(data + str(nonce).encode()).hexdigest()
        if h.startswith(target):
            return nonce, time.time() - t0
        nonce += 1

for k in range(1,7):
    nonce, dt = mine(b"block#1|txroot=abc|", k)
    print(f"k={k} nonce={nonce:>9} time={dt:.3f}s")

