#!/usr/bin/env python3
"""Lab 3.2 — Merkle tree (starter).

Hoàn thành 3 TODO rồi chạy:  python3 merkle_starter.py
Mọi dòng CHECK phải in OK.   All CHECK lines must print OK.

Quy ước (theo Bitcoin) / Convention (Bitcoin rule):
 - Lá = sha256(dữ liệu giao dịch).            Leaf = sha256(tx bytes).
 - Cha = sha256(trái + phải) trên byte digest. Parent = sha256(left + right) over raw digests.
 - Tầng lẻ: nhân đôi phần tử cuối.             Odd level: duplicate the last element.
"""
import hashlib

def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def merkle_root(leaves: list[bytes]) -> bytes:
    """TODO 1: dựng cây từ dưới lên, trả về băm gốc.
    Build bottom-up, return the root digest."""
    if not leaves:
        return b""
    
    current_level = leaves
    
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            # Nhân đôi nút cuối nếu tầng có số lượng lẻ
            if i + 1 == len(current_level):
                right = current_level[i]
            else:
                right = current_level[i + 1]
                
            # Băm dữ liệu bytes của 2 node (cộng chuỗi bytes)
            next_level.append(H(left + right))
            
        current_level = next_level
        
    return current_level[0]

def merkle_proof(leaves: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    """TODO 2: trả về [(sibling_digest, sibling_is_left), ...] từ lá lên gốc.
    Return the sibling path from leaf `index` up to the root."""
    proof = []
    current_level = leaves
    curr_index = index
    
    while len(current_level) > 1:
        if curr_index % 2 == 0:
            # Nút hiện tại bên trái -> Nút anh em bên phải
            if curr_index + 1 == len(current_level):
                sibling_hash = current_level[curr_index]
            else:
                sibling_hash = current_level[curr_index + 1]
            proof.append((sibling_hash, False)) # False = không phải bên trái (bên phải)
        else:
            # Nút hiện tại bên phải -> Nút anh em bên trái
            sibling_hash = current_level[curr_index - 1]
            proof.append((sibling_hash, True)) # True = bên trái
            
        # Tính lại tầng tiếp theo để leo lên gốc
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i] if i + 1 == len(current_level) else current_level[i + 1]
            next_level.append(H(left + right))
            
        current_level = next_level
        curr_index = curr_index // 2 # Index của node cha ở tầng tiếp theo
        
    return proof

def verify_proof(leaf_hash: bytes, proof: list[tuple[bytes, bool]], root: bytes) -> bool:
    """TODO 3: tính ngược lên gốc rồi so sánh. Recompute upward and compare."""
    computed_hash = leaf_hash
    
    for sibling_hash, is_left in proof:
        if is_left:
            # Sibling bên trái -> cộng sibling + node hiện tại
            computed_hash = H(sibling_hash + computed_hash)
        else:
            # Sibling bên phải -> cộng node hiện tại + sibling
            computed_hash = H(computed_hash + sibling_hash)
            
    return computed_hash == root

# ------------------------------------------------------------------ checks
if __name__ == "__main__":
    txs = [f"tx{i}: A->B {i} coin".encode() for i in range(8)]
    leaves = [H(t) for t in txs]
    root = merkle_root(leaves)
    
    print("root:", root.hex())
    
    # CHECK 1: proof đúng cho mọi lá / valid proof for every leaf
    ok = all(verify_proof(leaves[i], merkle_proof(leaves, i), root) for i in range(8))
    print("CHECK 1 (all 8 proofs valid):", "OK" if ok else "FAIL")
    
    # CHECK 2: proof có đúng log2(8)=3 phần tử / proof has exactly 3 elements
    print("CHECK 2 (proof length == 3):", "OK" if len(merkle_proof(leaves, 4)) == 3 else "FAIL")
    
    # CHECK 3: lá bị sửa phải trượt / a tampered leaf must fail
    fake = H(b"tx4: A->B 999999 coin")
    print("CHECK 3 (tampered leaf fails):",
          "OK" if not verify_proof(fake, merkle_proof(leaves, 4), root) else "FAIL")
          
    # CHECK 4: số lá lẻ (7) vẫn chạy / odd leaf count (7) still works
    l7 = leaves[:7]
    r7 = merkle_root(l7)
    print("CHECK 4 (odd count works):",
          "OK" if all(verify_proof(l7[i], merkle_proof(l7, i), r7) for i in range(7)) else "FAIL")