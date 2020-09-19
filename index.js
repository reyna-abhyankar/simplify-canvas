require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const { send } = require('process');

const app = express();
const port = process.env.PORT || 4000;

app.use(bodyParser.json());

/* Probably don't need these */
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
// ************************* //

app.post('/canvasbot', (req, res) => {
  console.log(req.body);
  let args = req.body.payload.cmd;
  let returnData = 'ye';

  const { spawn } = require('child_process');
  const pyProg = spawn('python', ['canvas.py', args]);

  function pythonScript(body) {
    pyProg.stdout.on('data', function(data) {
        returnData = data.toString();
        console.log(returnData);
    });
  }

  getChatbotToken();

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
        const pyPromise = new Promise(pythonScript(body)).then(sendChat(body.access_token));
        //pythonScript(body).then(sendChat(body.access_token));
      }
    })
  }

  function sendChat (chatbotToken) {
    console.log(returnData);
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
            'text': returnData,
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

app.get('/course', (req, res) => {
  const { spawn } = require('child_process');
  const pyProg = spawn('python', ['canvas.py']);

  pyProg.stdout.on('data', function(data) {
      console.log(data.toString());
      res.write(data);
      res.end('end');
  });
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

app.listen(port, () => console.log(`Canvas Chatbot for Zoom listening on port ${port}!`));
















function getPhoto (chatbotToken) {
  request(`https://api.unsplash.com/photos/random?query=${req.body.payload.cmd}&orientation=landscape&client_id=${process.env.unsplash_access_key}`, (error, body) => {
    if (error) {
      console.log('Error getting photo from Unsplash.', error)
      var errors = [
          {
            'type': 'section',
            'sidebar_color': '#D72638',
            'sections': [{
              'type': 'message',
              'text': 'Error getting photo from Unsplash.'
            }]
          }
        ]
        sendChat(errors, chatbotToken)
    } else {
      body = JSON.parse(body.body)
      if (body.errors) {
        var errors = [
          {
            'type': 'section',
            'sidebar_color': '#D72638',
            'sections': body.errors.map((error) => {
              return { 'type': 'message', 'text': error }
            })
          }
        ]
        sendChat(errors, chatbotToken)
      } else {
        var photo = [
          {
            'type': 'section',
            'sidebar_color': body.color,
            'sections': [
              {
                'type': 'attachments',
                'img_url': body.urls.regular,
                'resource_url': body.links.html,
                'information': {
                  'title': {
                    'text': 'Photo by ' + body.user.name
                  },
                  'description': {
                    'text': 'Click to view on Unsplash'
                  }
                }
              }
            ]
          }
        ]
        sendChat(photo, chatbotToken)
      }
    }
  })
}