import { network } from "hardhat";

const { ethers } = await network.connect("trustkeys");

const addr = process.env.REGISTRY;
if (!addr) throw new Error("Thiếu REGISTRY");

const code = await ethers.provider.getCode(addr);
console.log("Địa chỉ:", addr);
console.log(code === "0x" ? "KHÔNG có contract ở địa chỉ này" : "Có contract (code length " + code.length + ")");