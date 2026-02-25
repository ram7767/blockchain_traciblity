pragma solidity >= 0.8.11 <= 0.8.11;

contract Agricultural {
    string public users;
    string public products;
    string public purchase;
       
    //add user details to Blockchain memory	
    function addUser(string memory us) public {
       users = us;	
    }
   //get user details
    function getUser() public view returns (string memory) {
        return users;
    }
    //add product tracing details to Blockchain memory
    function setTracingData(string memory p) public {
       products = p;	
    }

    function getTracingData() public view returns (string memory) {
        return products;
    }

    //add purchase tracing details to Blockchain memory
    function setPurchase(string memory pu) public {
       purchase = pu;	
    }

    function getPurchase() public view returns (string memory) {
        return purchase;
    }

    constructor() public {
        users = "";
	products="";
	purchase="";
    }
}