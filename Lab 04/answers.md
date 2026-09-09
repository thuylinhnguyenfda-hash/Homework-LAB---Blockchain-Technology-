# Lab 04 — Answers / Trả lời

Block: **#840,000** — `0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5`
bits = `0x17034219`

---

## Q1

**EN:** The target `mantissa * 256^(exponent-3)` for bits `0x17034219` works out to:

```
0000000000000000000342190000000000000000000000000000000000000000... (padded to 64 hex chars)
```

It has **~19 leading zero hex digits** (about 76 leading zero bits). Since the expected number of
hashes to find a header below a target `T` is roughly `2^256 / T`, plugging in the numbers gives
`log2(target) ≈ 177.7`, so one valid header represents roughly **2^78** double-SHA-256 hash
attempts (~3 × 10^23 hashes) — this matches the real difficulty of block 840,000.

**VI:** Target của bits `0x17034219` có khoảng **19 chữ số hex 0** dẫn đầu (~76 bit 0). Số lần băm
kỳ vọng để tìm một header hợp lệ xấp xỉ `2^256 / target`, tính ra một header hợp lệ tương đương
khoảng **2^78** lần băm dSHA256 — con số này khớp với độ khó thật của block 840,000.

---

## Q2

**EN:** SHA-256 (and dSHA256) is a **one-way / preimage-resistant** cryptographic hash function.
Computing the hash of a given input is cheap — one pass through the compression function, done in
microseconds (2 evaluations to verify the header). But there is no algebraic shortcut to go
*backwards*: to find an input whose hash lands below the target, the only known strategy is
**brute-force trial and error** — try a nonce, hash, check, repeat. That asymmetry (cheap to
verify, expensive to search) is exactly what lets a single laptop verify in milliseconds what took
the entire network of ASICs ~10 minutes at ~10^20 H/s to find.

**VI:** SHA-256 là hàm băm mật mã **một chiều (preimage-resistant)**. Băm một input cho trước rất
rẻ (chỉ vài micro-giây, 2 lần băm để kiểm header). Nhưng không có cách nào đi ngược từ "hash mong
muốn" về input — cách duy nhất là **thử ngẫu nhiên (brute-force)**: đổi nonce, băm, kiểm tra, lặp
lại. Chính sự bất đối xứng "kiểm rẻ — tìm đắt" này khiến máy laptop verify trong mili-giây điều mà
cả mạng ASIC mất ~10 phút ở ~10^20 H/s mới tìm ra.

---

## Q3

**EN:** Block 840,000 was mined on **2024-04-19/20**, the exact day of Bitcoin's **4th halving**
*and* the launch of the **Runes** protocol. Many users wanted their transaction to be the first
ever recorded in the historic halving block (collectible/bragging-rights value), and Runes minters
were racing to be first in the new protocol — both effects flooded the mempool with users
aggressively outbidding each other for the very limited block space (~1–4 million weight units).
This produced an extreme, temporary spike to ~3,600,000 sat/vB for a 187 vB transaction
(~6.73 BTC in fees). **Lesson:** transaction fees are not fixed — they are set by a real-time
**auction for scarce block space**; fee rate reflects momentary demand, not any inherent cost of
the transaction itself.

**VI:** Block 840,000 được đào đúng ngày **halving lần 4** và cũng là ngày ra mắt giao thức
**Runes** (19/20-4-2024). Rất nhiều người muốn giao dịch của mình nằm trong block halving lịch sử
đầu tiên, cộng với người dùng Runes đua nhau mint đầu tiên — cả hai hiệu ứng khiến mempool bị dồn
ứ, người dùng đấu giá nhau kịch liệt để giành chỗ trong không gian block có hạn. Kết quả là mức phí
tăng vọt tạm thời lên ~3.600.000 sat/vB cho một giao dịch 187 vB (~6,73 BTC phí). **Bài học:** phí
giao dịch không cố định — nó hình thành từ **đấu giá không gian block khan hiếm** theo thời gian
thực, phản ánh nhu cầu tức thời chứ không phải chi phí nội tại của giao dịch.

---

## Q4

**EN:** `4,075,061,499 sat − 312,500,000 sat = 3,762,561,499 sat`. This difference is the **sum of
all transaction fees** paid by every non-coinbase transaction in the block. Miners collect
`block subsidy + total fees` in the coinbase transaction, and because of the Runes-launch/halving-day
fee spike (Q3), the fee total for this particular block was unusually large relative to the
subsidy itself.

**VI:** `4.075.061.499 sat − 312.500.000 sat = 3.762.561.499 sat`. Phần chênh lệch chính là **tổng
phí của toàn bộ giao dịch** trong block (không tính coinbase). Miner nhận `subsidy + tổng phí` vào
coinbase, và do đợt tăng phí đột biến ngày halving/Runes launch (xem Q3), tổng phí của block này
lớn bất thường so với subsidy.

---

## Q5

**EN:** A recomputed Merkle root matching the header's `merkle_root` field proves the **integrity
and completeness of the block's exact transaction list**: because dSHA256 exhibits the
**avalanche effect** (any single-bit change to any transaction, or any change in the number/order
of transactions, cascades unpredictably through every parent hash up the tree), it is
computationally infeasible to alter, add, remove, or reorder even one transaction and still
produce the same 32-byte root. So a match is proof — accepted the same way a full node accepts it
— that the transaction list is exactly the one the miner committed to when the block was mined,
without needing to re-examine every transaction pairwise.

**VI:** Merkle root tính lại khớp với `merkle_root` trong header chứng minh **tính toàn vẹn và đầy
đủ** của đúng danh sách giao dịch trong block: vì dSHA256 có **hiệu ứng lan truyền (avalanche
effect)** — chỉ cần đổi 1 bit trong bất kỳ giao dịch nào, hoặc đổi số lượng/thứ tự giao dịch, kết
quả sẽ lan truyền không thể đoán trước lên mọi hash cha trong cây — nên gần như bất khả thi để sửa,
thêm, bớt, hay đổi thứ tự dù chỉ một giao dịch mà vẫn ra cùng root 32 byte. Vậy khớp root chính là
bằng chứng — đúng như cách một full node xác nhận — rằng danh sách giao dịch chính xác là danh
sách miner đã cam kết khi đào block, mà không cần kiểm tra thủ công từng cặp giao dịch.