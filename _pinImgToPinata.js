const process = require("process");
const fs = require('fs');
const pinataSDK = require('@pinata/sdk');
const PINATA_API_KEY = 'a3e45709eba1fe13a614';
const PINATA_SECRET_API_KEY = 'bcbae387c4a66237a5492e22101c13493fe37f75d1ccf3bd780e4f22dda9b189';
const pinata = pinataSDK(PINATA_API_KEY, PINATA_SECRET_API_KEY);

var imgPath = process.argv[2]
const readableStreamForFile = fs.createReadStream(imgPath);
const options = {};

pinata.pinFileToIPFS(readableStreamForFile, options).then((result) => {
    console.log(result["IpfsHash"])
}).catch((err) => {
    console.log(err)
});