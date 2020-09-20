require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');

const { Client } = require('pg');
const pg = new Client({connectionString: process.env.DATABASE_URL});

pg.connect().catch((error) => {
  console.log('Error connecting to database', error)
})

const app = express();
const port = process.env.PORT || 4000;

app.use(bodyParser.json());

app.post('/canvasbot', (req, res) => {
  console.log(req.body);
  let args = req.body.payload.cmd;
  let returnData = '';

  const { spawn } = require('child_process');
  const pyProg = spawn('python', ['canvas.py', args]);

  function pyScript(token) {
    return new Promise(function (fulfill) {
      pyProg.stdout.on('data', function (data) {
        returnData = data.toString();
        fulfill(returnData);
      });
    }).then(() => {
      sendChat(token, returnData);
    });
  }

  if (req.headers.authorization === process.env.zoom_verification_token) {
    res.status(200);
    res.send();
    pg.query('SELECT * FROM chatbot_token', (error, results) => {
      if (error) {
        console.log('Error getting chatbot_token from database.', error);
      } else {
        if (results.rows[0].expires_on > (new Date().getTime() / 1000)) {
          pyScript(results.rows[0].token);
        } else {
          getChatbotToken();
        }
      }
    });
  } else {
    res.status(401);
    res.send('Unauthorized request to Canvas Chatbot for Zoom.');
  }

  function getChatbotToken () {
    request({
      url: `https://zoom.us/oauth/token?grant_type=client_credentials`,
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(process.env.zoom_client_id + ':' + process.env.zoom_client_secret).toString('base64')
      }
    }, (error, httpResponse, body) => {
      if (error) {
        console.log('Error getting chatbot_token from Zoom.', error);
      } else {
        body = JSON.parse(body);

        pg.query(`UPDATE chatbot_token SET token = '${body.access_token}', expires_on = ${(new Date().getTime() / 1000) + body.expires_in}`, (error, results) => {
          if (error) {
            console.log('Error setting chatbot_token in database.', error);
          } else {
            pyScript(body.access_token);
          }
        });
        
      }
    })
  }

  function sendChat (chatbotToken, data) {
    request({
      url: 'https://api.zoom.us/v2/im/chat/messages',
      method: 'POST',
      json: true,
      body: {
        'robot_jid': process.env.zoom_bot_jid,
        'to_jid': req.body.payload.toJid,
        'account_id': req.body.payload.accountId,
        'content': {
          'head': {
            'text': 'Canvas'
          },
          'body': [{
            'type': 'message',
            'text': data,
          }]
        }
      },
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + chatbotToken
      }
    }, (error, httpResponse, body) => {
      if (error) {
        console.log('Error sending chat.', error);
      } else {
        console.log(body);
      }
    });
  }
});

app.listen(port, () => console.log(`Canvas Chatbot for Zoom listening on port ${port}!`));

/*************************************/
/* Won't need these until deployment */
app.get('/', (req, res) => {
  res.send('Welcome to the Canvas Chatbot for Zoom!');
});

app.get('/authorize', (req, res) => {
  res.redirect('https://zoom.us/launch/chat?jid=robot_' + process.env.zoom_bot_jid);
});

app.get('/support', (req, res) => {
  res.send('Contact forvirenra@gmail.com');
});

app.get('/privacy', (req, res) => {
  res.send('The Canvas Chatbot for Zoom does not store any user data.');
});

app.get('/terms', (req, res) => {
  res.send('By installing the Canvas Chatbot for Zoom, you are accept and agree to these terms...');
});

app.get('/documentation', (req, res) => {
  res.send('');
});

app.get('/zoomverify/verifyzoom.html', (req, res) => {
  res.send(process.env.zoom_verification_code);
});

app.post('/deauthorize', (req, res) => {
  if (req.headers.authorization === process.env.zoom_verification_token) {
    res.status(200);
    res.send();
    request({
      url: 'https://api.zoom.us/oauth/data/compliance',
      method: 'POST',
      json: true,
      body: {
        'client_id': req.body.payload.client_id,
        'user_id': req.body.payload.user_id,
        'account_id': req.body.payload.account_id,
        'deauthorization_event_received': req.body.payload,
        'compliance_completed': true
      },
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + Buffer.from(process.env.zoom_client_id + ':' + process.env.zoom_client_secret).toString('base64'),
        'cache-control': 'no-cache'
      }
    }, (error, httpResponse, body) => {
      if (error) {
        console.log(error);
      } else {
        console.log(body);
      }
    });
  } else {
    res.status(401);
    res.send('Unauthorized request to Canvas Chatbot for Zoom.');
  }
});

