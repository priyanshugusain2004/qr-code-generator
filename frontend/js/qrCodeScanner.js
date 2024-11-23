function startScanner() {
    const scanner = new Html5QrcodeScanner(
        "scanner-container", 
        { fps: 10, qrbox: 250 }, 
        true 
    );

    scanner.render(onScanSuccess, onScanError);
}

async function onScanSuccess(decodedText, decodedResult) {
    document.getElementById("scannedText").textContent = `Scanning QR Code: ${decodedText}`;

    try {
        const response = await fetch(`http://localhost:3000/data/${decodedText}`);
        const data = await response.json();

        if (response.ok) {
            document.getElementById("scannedText").textContent = `Scanned Text: ${data.text}`;
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to retrieve data.');
    }
}

function onScanError(errorMessage) {
    console.log(`Scan error: ${errorMessage}`);
}
