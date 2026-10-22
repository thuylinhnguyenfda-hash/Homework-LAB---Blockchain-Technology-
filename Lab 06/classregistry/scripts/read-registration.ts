import { network } from "hardhat";

const { ethers } = await network.connect("trustkeys");

const addr = process.env.REGISTRY;
if (!addr) throw new Error("Thiếu REGISTRY");

const registry = await ethers.getContractAt("ClassRegistry", addr);

const count = await registry.memberCount();
console.log("Số thành viên hiện tại:", count.toString());
for (let i = 0n; i < count; i++) {
  const who = await registry.memberAt(i);
  console.log(`#${i}`, who, "-", await registry.nameOf(who));
}

const events = await registry.queryFilter(registry.filters.Registered());
console.log("\nLịch sử đăng ký (event log):");
for (const e of events) {
  console.log("block", e.blockNumber, e.args.who, "-", e.args.name);
}