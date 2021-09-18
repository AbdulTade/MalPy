let password = "";
const crypto = require('crypto');
const process = require('process');
const os = require('os');

var bcolors = {
    OK: "\\33[92m",
    WARNING: "\\33[93m",
    FAIL: "\\33[91m",
    RESET: "\\33[0m"
}

function hash(string="") {
    let buff = Buffer.from(string);
    let salt = crypto.randomBytes(parseInt(16 + Math.random()*100));
    let hashString = "";
    let algorithm = crypto.createHash('sha512');
    hash = algorithm.update(string+salt).digest('hex');
    return hashString;
}

function generateToken(num=0)
{
    let date = new Date();
    let buffdate = Buffer.from(date.toString());
    let buff = crypto.randomBytes(num);
    let algorithm = crypto.createHash('sha512');
    let hash = algorithm.update(buff+buffdate).digest('base64');
    return hash;
}

function  ServerHealthInfo(interval=0)
{
    const usageInfo  = {
        memory : 0,
        cpu    : 0
    }
    const cpu = process.cpuUsage();
    const mem = process.memoryUsage();
    setInterval(() => {
        usageInfo.memory = process.cpuUsage(cpu);
        usageInfo.cpu    =  process.memoryUsage(mem);
        console.log(usageInfo);
    },interval);
}

function formatColor(string = "", type = "OK") {
    let start = "";
    if (type === "OK") start = bcolors.OK;
    if (type === "WARNING") start = bcolors.WARNING;
    if (type === "FAIL") start = bcolors.FAIL;

    return start + string + bcolors.RESET;
}


module.exports = {
    generateToken,
    ServerHealthInfo,
    hash
}