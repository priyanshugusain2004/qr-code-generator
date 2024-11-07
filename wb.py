import qrcode
import socket
from flask import Flask, render_template_string, send_file

app = Flask(__name__)

# HTML template with JavaScript for a whiteboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Whiteboard</title>
    <style>
        body, html { margin: 0; padding: 0; overflow: hidden; display: flex; align-items: center; justify-content: center; height: 100vh; }
        canvas { border: 1px solid black; touch-action: none; }
        #buttons { position: fixed; top: 10px; display: flex; gap: 10px; }
    </style>
</head>
<body>
    <div id="buttons">
        <button onclick="chooseColor()">Choose Color</button>
        <button onclick="toggleEraser()">Toggle Eraser</button>
        <button onclick="clearCanvas()">Clear All</button>
    </div>
    <canvas id="whiteboard"></canvas>
    <script>
        const canvas = document.getElementById('whiteboard');
        const ctx = canvas.getContext('2d');
        let drawing = false;
        let isEraser = false;
        let color = 'black';

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Update canvas size on window resize
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });

        function startPosition(e) {
            drawing = true;
            draw(e);
        }

        function endPosition() {
            drawing = false;
            ctx.beginPath();
        }

        function draw(e) {
            if (!drawing) return;
            ctx.lineWidth = 5;
            ctx.lineCap = 'round';
            ctx.strokeStyle = isEraser ? 'white' : color;

            ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
        }

        function clearCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        function chooseColor() {
            color = prompt("Enter a color name or hex code:", color) || color;
            isEraser = false; // Turn off eraser after choosing a color
        }

        function toggleEraser() {
            isEraser = !isEraser;
        }

        // Touch and Mouse events
        canvas.addEventListener('mousedown', startPosition);
        canvas.addEventListener('mouseup', endPosition);
        canvas.addEventListener('mousemove', draw);

        canvas.addEventListener('touchstart', (e) => startPosition(e.touches[0]));
        canvas.addEventListener('touchend', endPosition);
        canvas.addEventListener('touchmove', (e) => draw(e.touches[0]));
    </script>
</body>
</html>
"""

@app.route('/')
def whiteboard():
    return render_template_string(HTML_TEMPLATE)

def generate_qr_code(url):
    """Generate a QR code for the given URL."""
    qr = qrcode.make(url)
    qr.save("whiteboard_qr.png")

def get_local_ip():
    """Get the local IP address of the current machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external server
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    # Set up the server IP and port
    ip_address = get_local_ip()
    port = 5000
    url = f"http://{ip_address}:{port}"

    # Generate and save the QR code
    generate_qr_code(url)
    print(f"QR code generated! Scan the QR code (whiteboard_qr.png) to access the whiteboard on your mobile device.")
    print(f"Or access the whiteboard directly at: {url}")

    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=True)
