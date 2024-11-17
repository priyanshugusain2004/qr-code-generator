const express = require('express');
const bodyParser = require('body-parser');
const QRCode = require('qrcode');

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));

// Set view engine and views directory
app.set('view engine', 'ejs');
app.set('views', './views');

// Store received messages in an array (could be replaced with a DB)
let receivedMessages = [];

// Routes
app.get('/', (req, res) => {
    res.render('index', {
        qrCodeUrl: null,
        messages: receivedMessages,  // Display all received messages
        error: null,
    });
});

// Generate QR code that any device can scan to send data
app.post('/generate-receive-qr', async (req, res) => {
    try {
        const receiveUrl = `${req.protocol}://${req.get('host')}/receive`; // URL to send data
        const qrCodeUrl = await QRCode.toDataURL(receiveUrl); // Generate QR code

        res.render('index', { qrCodeUrl, messages: receivedMessages, error: null });
    } catch (err) {
        console.error(err);
        res.render('index', { qrCodeUrl: null, messages: receivedMessages, error: 'Failed to generate QR code' });
    }
});

// Receive data from QR code scan and store it
app.get('/receive', (req, res) => {
    const receivedData = req.query.data; // Get the data from the URL query

    if (receivedData) {
        receivedMessages.push(receivedData); // Store it in the array
    }

    res.redirect('/'); // Redirect back to the home page to show the data
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
