const express = require('express');
const bodyParser = require('body-parser');
const QRCode = require('qrcode');

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));

// Set view engine and views directory
app.set('view engine', 'ejs');
app.set('views', './views');

// Routes
app.get('/', (req, res) => {
    res.render('index', { qrCodeUrl: null, message: null, qrType: null, error: null });
});

// Generate QR code for sending text
app.post('/generate', async (req, res) => {
    const text = req.body.text;

    if (!text) {
        return res.render('index', {
            qrCodeUrl: null,
            message: null,
            qrType: null,
            error: 'Please provide text to generate a QR code',
        });
    }

    try {
        const qrCodeUrl = await QRCode.toDataURL(text);
        res.render('index', { qrCodeUrl, message: text, qrType: 'send-text', error: null });
    } catch (err) {
        console.error(err);
        res.render('index', { qrCodeUrl: null, message: null, qrType: null, error: 'Failed to generate QR code' });
    }
});

// Generate QR code to receive text submission
app.post('/generate-receive-qr', async (req, res) => {
    try {
        const receiveUrl = `${req.protocol}://${req.get('host')}/receive`;
        const qrCodeUrl = await QRCode.toDataURL(receiveUrl);

        res.render('index', { qrCodeUrl, message: null, qrType: 'receive-text', error: null });
    } catch (err) {
        console.error(err);
        res.render('index', { qrCodeUrl: null, message: null, qrType: null, error: 'Failed to generate QR code' });
    }
});

// Form to receive text submission
app.get('/receive', (req, res) => {
    res.render('receive', { message: null });
});

// Handle text submission from scanned device
app.post('/receive', (req, res) => {
    const message = req.body.message;

    if (!message) {
        return res.render('receive', { message: 'Please enter a valid message!' });
    }

    res.render('receive', { message: `Received message: ${message}` });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
