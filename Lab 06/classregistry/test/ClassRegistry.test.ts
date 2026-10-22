import { expect } from "chai";
import { network } from "hardhat";

const { ethers, networkHelpers } = await network.connect();

describe("ClassRegistry", function () {
  async function deployFixture() {
    const [owner, alice, bob, ...others] = await ethers.getSigners();
    const registry = await ethers.deployContract("ClassRegistry");
    return { registry, owner, alice, bob, others };
  }

  it("sets the deployer as owner", async function () {
    const { registry, owner } = await networkHelpers.loadFixture(deployFixture);
    expect(await registry.owner()).to.equal(owner.address);
  });

  it("register stores the name and emits Registered", async function () {
    const { registry, alice } = await networkHelpers.loadFixture(deployFixture);
    await expect(registry.connect(alice).register("Alice"))
      .to.emit(registry, "Registered")
      .withArgs(alice.address, "Alice");

    expect(await registry.nameOf(alice.address)).to.equal("Alice");
    expect(await registry.memberCount()).to.equal(1n);
    expect(await registry.memberAt(0)).to.equal(alice.address);
  });

  it("reverts on empty name", async function () {
    const { registry, alice } = await networkHelpers.loadFixture(deployFixture);
    await expect(registry.connect(alice).register(""))
      .to.be.revertedWithCustomError(registry, "EmptyName");
  });

  it("double register reverts with AlreadyRegistered", async function () {
    const { registry, alice } = await networkHelpers.loadFixture(deployFixture);
    await registry.connect(alice).register("Alice");
    await expect(registry.connect(alice).register("Alice 2"))
      .to.be.revertedWithCustomError(registry, "AlreadyRegistered")
      .withArgs(alice.address);
  });

  it("non-owner deregister reverts with NotOwner", async function () {
    const { registry, alice, bob } = await networkHelpers.loadFixture(deployFixture);
    await registry.connect(alice).register("Alice");
    await expect(registry.connect(bob).deregister(alice.address))
      .to.be.revertedWithCustomError(registry, "NotOwner");
  });

  it("owner deregister of unknown address reverts with NotRegistered", async function () {
    const { registry, owner, bob } = await networkHelpers.loadFixture(deployFixture);
    await expect(registry.connect(owner).deregister(bob.address))
      .to.be.revertedWithCustomError(registry, "NotRegistered")
      .withArgs(bob.address);
  });

  it("deregister uses swap-and-pop and keeps the array dense", async function () {
    const { registry, owner, alice, bob, others } =
      await networkHelpers.loadFixture(deployFixture);
    const carol = others[0];
    await registry.connect(alice).register("Alice");
    await registry.connect(bob).register("Bob");
    await registry.connect(carol).register("Carol");

    await registry.connect(owner).deregister(alice.address);

    expect(await registry.memberCount()).to.equal(2n);
    expect(await registry.memberAt(0)).to.equal(carol.address);
    expect(await registry.memberAt(1)).to.equal(bob.address);
    expect(await registry.isRegistered(alice.address)).to.equal(false);
    expect(await registry.nameOf(alice.address)).to.equal("");

    await registry.connect(owner).deregister(carol.address);
    expect(await registry.memberCount()).to.equal(1n);
    expect(await registry.memberAt(0)).to.equal(bob.address);
  });

  it("many signers with different names all round-trip", async function () {
    const { registry, owner, alice, bob, others } =
      await networkHelpers.loadFixture(deployFixture);
    const signers = [owner, alice, bob, ...others].slice(0, 10);

    for (let i = 0; i < signers.length; i++) {
      await registry.connect(signers[i]).register(`Student-${i}`);
    }

    expect(await registry.memberCount()).to.equal(BigInt(signers.length));
    for (let i = 0; i < signers.length; i++) {
      expect(await registry.nameOf(signers[i].address)).to.equal(`Student-${i}`);
      expect(await registry.memberAt(i)).to.equal(signers[i].address);
    }
  });
});