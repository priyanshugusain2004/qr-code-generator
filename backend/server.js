const express = require('express');
const path = require('path');
const app = express();

// Serve static files from the 'frontend' directory
app.use(express.static(path.join(__dirname, 'frontend')));

// Serve the index.html file for the root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

// Example route for the scanner page
app.get('/scanner', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'scanner.html'));
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
