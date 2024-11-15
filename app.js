const express = require('express');
const bodyParser = require('body-parser');
const QRCode = require('qrcode');

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static('public'));

// Set view engine and views directory
app.set('view engine', 'ejs');
app.set('views', './views'); // This explicitly tells Express to look in the "views" folder

// Routes
app.get('/', (req, res) => {
    res.render('index', { qrCodeUrl: null, error: null });
});

app.post('/generate', async (req, res) => {
    const text = req.body.text;

    if (!text) {
        return res.render('index', { qrCodeUrl: null, error: 'Please provide text to generate QR code' });
    }

    try {
        const qrCodeUrl = await QRCode.toDataURL(text);
        res.render('index', { qrCodeUrl, error: null });
    } catch (err) {
        console.error(err);
        res.render('index', { qrCodeUrl: null, error: 'Failed to generate QR code' });
    }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
