import { network } from "hardhat";

const { ethers } = await network.connect("trustkeys");

const addr = process.env.REGISTRY;
const name = process.env.NAME;
if (!addr || !name) throw new Error("Thiếu REGISTRY hoặc NAME");

const [me] = await ethers.getSigners();
const registry = await ethers.getContractAt("ClassRegistry", addr);

const tx = await registry.register(name);
console.log("Register tx hash:", tx.hash);
await tx.wait();

console.log("Tên đã lưu on-chain:", await registry.nameOf(me.address));
console.log("Tổng thành viên:", (await registry.memberCount()).toString());