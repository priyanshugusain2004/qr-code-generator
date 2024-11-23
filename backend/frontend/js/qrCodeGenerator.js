function generateQRCode() {
    const text = document.getElementById('text-input').value.trim(); // Remove leading/trailing whitespace

    const qrCodeContainer = document.getElementById('qr-code');
    if (text && text.length > 0) {
        qrCodeContainer.innerHTML = '';  // Clear previous QR code
        console.log('Data to encode:', text);  // Log the data being passed

        try {
            // Ensure the data is a string
            if (typeof text !== 'string') {
                throw new Error('Input data must be a string');
            }

            // Generate the QR code
            QRCode.toCanvas(qrCodeContainer, text, function (error) {
                if (error) {
                    console.error('QR code generation failed:', error);
                    qrCodeContainer.innerHTML = `Error: ${error.message}`;
                } else {
                    console.log('QR code generated!');
                }
            });
        } catch (error) {
            console.error('Unexpected error during QR code generation:', error);
            qrCodeContainer.innerHTML = 'Failed to generate QR code';
        }
    } else {
        qrCodeContainer.innerHTML = 'Please enter some text to generate the QR code.';
    }
}
