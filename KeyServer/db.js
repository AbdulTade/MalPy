const mongoose = require('mongoose');
const dburl = 'mongodb://localhost:27017/MalDev';
const { hash }= require('./Utils');

mongoose.connect(dburl,{useNewUrlParser : true, useUnifiedTopology  : true , useCreateIndex : true});
const db = mongoose.connection;
db.on('error',console.error.bind(console,'connection: error'));
db.once('open',() => {
    console.log('Database connected successfully');
});

const UserSchema = new mongoose.Schema({
    email : {
        type : String,
        required : true,
        unique : true
    },
    passcode : {
        type: String,
        required : true
    },
    credentials : {
    }
});

UserSchema.pre('save',(err,user) => {
    if(err) console.error(err);
    user.passcode = hash(user.passcode);
});

const User = mongoose.model('User',UserSchema);

module.exports = {
    User
}

