const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send('Bot Telegram actif!');
});

app.get('/ping', (req, res) => {
    res.send('pong');
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Serveur Express démarré sur le port ${port}`);
});
