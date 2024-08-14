// npm libraries
const fsP = require('fs').promises
const bodyParser = require('body-parser')

// express library setup
const express = require('express')
const app = express()
app.use(express.json())
app.use(bodyParser.urlencoded({ extended: true })) // support encoded bodies
app.use("/static", express.static('./static/'))

const PORT = process.env.PORT || 80


app.get('/', async (req, res) => {
    let data = await fsP.readFile('./summIT.html')

    const d = new Date();

    let canadaTime = d.toLocaleString("en-US", {
        timeZone: "America/New_York"
    });
    
    console.log(canadaTime + " -- " + req.ip)

    let logs = await fsP.readFile('./log.txt')
    logs += "\n" + canadaTime + " -- " + req.ip

    await fsP.writeFile('./log.txt', logs)
    res.writeHead(200, { 'Content-Type': 'text/html' }).end(data)
})




app.listen(PORT, (req, res) => console.log(`Port ${PORT} Opened`))