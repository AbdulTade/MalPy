let password = "";
const crypto = require('crypto');
const process = require('process');
const os = require('os');

let token = "Token-to-check";
let isverified = false;

let mails = {};
mails.abdul  = "abdulhameedotade@gmail.com";
mails.abdul2 = "abdul.hameed@acity.edu.gh";

var bcolors = {
    OK      : "\033[92m",
    WARNING : "\033[93m",
    FAIL    : "\033[91m",
    RESET   : "\033[0m"
}



function formatColor(string="",type="OK")
{
    let start  = "";
    if(type === "OK")      start = bcolors.OK;
    if(type === "WARNING") start = bcolors.WARNING;
    if(type === "FAIL")    start = bcolors.FAIL;

    return start+string+bcolors.RESET;
}

function index(req,res)
{
    res.send("OK");
}

function verify(req,res)
{
    let params = req.params;
    isverified = (params.token === token) ? true : false;
    if(isverified) {
        password = "Your-password-here";
    }
}

function getKey(req,res)
{
    res.send(password);
    password = "";
    isverified = false;
}



function getScript(req,res)
{
    let filename = process.cwd().split('/')[process.cwd().split('/').length-1];
    if(isverified)
    {
        res.sendFile(`${process.cwd()}/Installer.py}`,(err) => {
            if(err){
                console.log(formatColor(`Could not open the file ${filename}: ${err}`,"FAIL"))
            }
            console.log(formatColor(`[*] Succcessfully sent the file ${filename}`,"OK"));
        })
    }
}

function generateToken(num=0)
{
    let date = new Date();
    let buffdate = Buffer.from(date.toString());
    let buff = crypto.randomBytes(num);
    let algorithm = crypto.createHash('sha512');
    let hash = algorithm.update(buff+buffdate).digest('hex');
    return hash;
}

function sendmail(sender="",recipients=[""],password="",subject="",message=""){
    let mail = require('mail').Mail({
        host       :  'smtp.gmail.com',
        username   :  sender,
        password   : password
    });

    mail.message({
        from    :    sender,
        to      :    recipients,
        subject :    subject
    }).body(message).send((err) => {
        if(err) throw err;
        console.log(formatColor('Sent!'));
    });
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

module.exports = {
    index,
    verify,
    getKey,
    getScript,
    formatColor,
    generateToken,
    sendmail,
    ServerHealthInfo
}