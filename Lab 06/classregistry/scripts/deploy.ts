import { network } from "hardhat";

const { ethers } = await network.connect("trustkeys");

const [deployer] = await ethers.getSigners();
console.log("Deployer:", deployer.address);

const registry = await ethers.deployContract("ClassRegistry");
await registry.waitForDeployment();

console.log("ClassRegistry deployed to:", await registry.getAddress());
console.log("Deploy tx hash:", registry.deploymentTransaction()?.hash);