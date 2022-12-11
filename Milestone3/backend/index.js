
const express = require('express');
const app = express();

const axios = require("axios");

const bodyParser = require('body-parser');
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }));
  
app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

const server = app.listen(8000, function () {
    let host = server.address().address
    let port = server.address().port
})

app.post('/', async (req, res) => {
    const url = req.body.url;
    const solr_response = await axios.get(url); // send request to solr
    res.send(solr_response.data); // send solr response to frontend
})  