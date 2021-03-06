const express = require("express");
const {spawn} = require("child_process");

const app = express();
app.set("view engine", "ejs");

app.use(express.json());
app.use(express.urlencoded({extended: true}));

app.use(express.static("public"));

var initial;

app.get("/", (req, res) => {
  initial = true;
  res.render("index", {result: " SUBMIT TEXT TO GET RESULT!", initial});
});

app.post("/", (req, res) => {
  res.redirect(`/result?text=${req.body.text}`);
});

app.get("/result", (req, res) => {
  var dataToSend;
  var arrayString;
  initial = false;
  const python = spawn("python", ["./All_senti.py", req.query.text]);

  python.stdout.on("data", (data) => {
    console.log("Pipe data from python script ...");
    dataToSend = data.toString();
    arrayString = dataToSend.split("\r\n" + "\r\n");
  });

  python.stderr.on("data", (error) => {
    console.log(`error: ${error}`);
  });
  python.on("close", (code) => {
    console.log(`child process close all stdio with code ${code}`);
    res.render("index", {result: arrayString, initial});
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});
