const express = require('express');
const bodyParser = require('body-parser');
const QRCode = require('qrcode');
const fs = require('fs');

const app = express();
const port = 3000;

// In-memory data store (this can be replaced with a database)
let dataStore = {};

// Middleware
app.use(bodyParser.json());
app.use(express.static('frontend'));

// Endpoint to receive text and generate QR code
app.post('/generate', (req, res) => {
    const { text } = req.body;

    if (!text) {
        return res.status(400).json({ message: 'Text is required to generate QR code.' });
    }

    // Generate QR code
    QRCode.toDataURL(text, (err, url) => {
        if (err) {
            return res.status(500).json({ message: 'Error generating QR code.' });
        }

        // Store QR code URL in dataStore
        const id = Date.now().toString();  // Unique ID for the generated data
        dataStore[id] = { text, qrCodeUrl: url };

        // Respond with the QR code URL and ID
        res.status(200).json({ id, qrCodeUrl: url });
    });
});

// Endpoint to retrieve data by ID (for QR code scanner)
app.get('/data/:id', (req, res) => {
    const id = req.params.id;
    const data = dataStore[id];

    if (!data) {
        return res.status(404).json({ message: 'Data not found.' });
    }

    res.status(200).json({ text: data.text });
});

// Start server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
