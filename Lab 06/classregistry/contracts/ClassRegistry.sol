// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract ClassRegistry {
    // ---------- Errors ----------
    error EmptyName();
    error AlreadyRegistered(address who);
    error NotOwner();
    error NotRegistered(address who);

    // ---------- Events ----------
    event Registered(address indexed who, string name);
    event Deregistered(address indexed who);

    // ---------- State ----------
    address public immutable owner;
    mapping(address => string) private _names;      // address => tên
    mapping(address => uint256) private _indexOf;   // address => vị trí trong mảng + 1 (0 = chưa đăng ký)
    address[] private _members;                     // để duyệt danh sách

    // ---------- Modifier ----------
    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    // ---------- Write ----------
    function register(string calldata name) external {
        if (bytes(name).length == 0) revert EmptyName();
        if (_indexOf[msg.sender] != 0) revert AlreadyRegistered(msg.sender);

        _names[msg.sender] = name;
        _members.push(msg.sender);
        _indexOf[msg.sender] = _members.length; // index + 1

        emit Registered(msg.sender, name);
    }

    function deregister(address who) external onlyOwner {
        uint256 idxPlusOne = _indexOf[who];
        if (idxPlusOne == 0) revert NotRegistered(who);

        // swap-and-pop: đưa phần tử cuối vào chỗ trống rồi pop
        uint256 idx = idxPlusOne - 1;
        uint256 lastIdx = _members.length - 1;
        if (idx != lastIdx) {
            address last = _members[lastIdx];
            _members[idx] = last;
            _indexOf[last] = idx + 1;
        }
        _members.pop();

        delete _indexOf[who];
        delete _names[who];

        emit Deregistered(who);
    }

    // ---------- Read ----------
    function memberCount() external view returns (uint256) {
        return _members.length;
    }

    function memberAt(uint256 i) external view returns (address) {
        return _members[i];
    }

    function nameOf(address who) external view returns (string memory) {
        return _names[who];
    }

    function isRegistered(address who) external view returns (bool) {
        return _indexOf[who] != 0;
    }
}