const http = require('http');
const fs   = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.xml':  'text/xml',
  '.txt':  'text/plain',
};

http.createServer((req, res) => {
  let file = '.' + req.url.split('?')[0];
  if (file === './' || file === '.') file = './index.html';

  fs.readFile(file, (err, data) => {
    if (err) {
      // Fallback: always serve index.html
      fs.readFile('./index.html', (e2, d2) => {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(d2);
      });
    } else {
      const ext = path.extname(file);
      res.writeHead(200, { 'Content-Type': MIME[ext] || 'text/plain' });
      res.end(data);
    }
  });
}).listen(PORT, () => console.log('Clean Connect live auf Port ' + PORT));
