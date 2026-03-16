const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT = 8080;
const DATA_FILE = path.join(__dirname, 'love_history.jsonl');

const server = http.createServer((req, res) => {
    if (req.method === 'GET') {
        // הגשת קבצים סטטיים
        let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
        const extname = path.extname(filePath);
        let contentType = 'text/html';

        switch (extname) {
            case '.js': contentType = 'text/javascript'; break;
            case '.css': contentType = 'text/css'; break;
            case '.json': contentType = 'application/json'; break;
            case '.png': contentType = 'image/png'; break;
            case '.jpg': contentType = 'image/jpg'; break;
        }

        fs.readFile(filePath, (error, content) => {
            if (error) {
                if (error.code === 'ENOENT') {
                    res.writeHead(404);
                    res.end('File not found');
                } else {
                    res.writeHead(500);
                    res.end('Server error: ' + error.code);
                }
            } else {
                res.writeHead(200, { 'Content-Type': contentType });
                res.end(content, 'utf-8');
            }
        });
    } else if (req.method === 'POST' && req.url === '/submit-love') {
        // קבלת נתוני אהבה
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                console.log('Received love data:', data);

                // שמירה לקובץ
                fs.appendFileSync(DATA_FILE, JSON.stringify(data) + '\n');

                // שליחת הודעה לברק בטלגרם דרך OpenClaw CLI
                const msg = `❤️ *עדכון מה-Love Meter!* ❤️\n\n*הציון:* ${data.score}/10\n*הודעה:* ${data.message || '(אין הודעה)'}`;
                
                // שימוש ב-openclaw message send
                // הנחה: target הוא telegram:923217579
                const command = `openclaw message send --target "telegram:923217579" --message "${msg.replace(/"/g, '\\"')}"`;
                
                exec(command, (err, stdout, stderr) => {
                    if (err) console.error('Error sending message:', err);
                    else console.log('Message sent to Barak!');
                });

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'success' }));
            } catch (e) {
                res.writeHead(400);
                res.end('Invalid JSON');
            }
        });
    }
});

server.listen(PORT, '0.0.0.0', () => {
    console.log(`Love Meter server running at http://localhost:${PORT}/`);
    console.log(`To access from other devices, use the server's IP address.`);
});
