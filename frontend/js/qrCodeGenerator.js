async function generateQRCode() {
    const text = document.getElementById('inputText').value.trim();

    if (text === "") {
        alert('Please enter some text to generate QR code.');
        return;
    }

    try {
        const response = await fetch('http://localhost:3000/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (response.ok) {
            const qrCodeContainer = document.getElementById('qrCode');
            qrCodeContainer.innerHTML = `<img src="${data.qrCodeUrl}" alt="QR Code">`;
            console.log('QR code generated successfully!');
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate QR code.');
    }
}
