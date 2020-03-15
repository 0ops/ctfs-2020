const express = require("express")
const fs = require("fs")
const vm = require("vm")
const watchdog = require("./watchdog");

global.flag = fs.readFileSync("flag").toString()
const source = fs.readFileSync(__filename).toString()
const help = "There is no help on the way."

const app = express()
const port = 3000

app.use(express.json())
app.use('/', express.static('public'))

app.post('/repl', (req, res) => {
    let sandbox = vm.createContext({par: (v => `(${v})`), source, help})
    let validInput = /^[a-zA-Z0-9 ${}`]+$/g
    
    let command = req.body['cmd']
    
    console.log(`${req.ip}> ${command}`)

    let response;

    try {
        if(validInput.test(command))
        {    
            let watch = watchdog.schedule()
            try {
                response = vm.runInContext(command, sandbox, {
                    timeout: 300,
                    displayErrors: false
                });
            } finally {
                watchdog.stop(watch)
            }
        } else
            throw new Error("Invalid input.")
    } catch(ex)
    {
        response = ex.toString()
    }

    console.log(`${req.ip}< ${response}`)
    res.send(JSON.stringify({"response": response}))
})

console.log(`Listening on :${port}...`)
app.listen(port, '0.0.0.0')
