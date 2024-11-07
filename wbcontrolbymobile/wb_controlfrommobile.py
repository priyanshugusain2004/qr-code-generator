import qrcode
import socket
from flask import Flask, render_template_string
from flask_socketio import SocketIO

# Initialize Flask app and Flask-SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# HTML template for live whiteboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Web Whiteboard</title>
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
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.min.js"></script>
    <script>
        const socket = io();
        const canvas = document.getElementById('whiteboard');
        const ctx = canvas.getContext('2d');
        let drawing = false;
        let isEraser = false;
        let color = 'black';

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

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

            const x = e.clientX - canvas.offsetLeft;
            const y = e.clientY - canvas.offsetTop;

            ctx.lineWidth = 5;
            ctx.lineCap = 'round';
            ctx.strokeStyle = isEraser ? 'white' : color;
            ctx.lineTo(x, y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x, y);

            // Emit draw event to server
            socket.emit('draw', { x, y, color: ctx.strokeStyle, eraser: isEraser });
        }

        function clearCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            socket.emit('clear');
        }

        function chooseColor() {
            color = prompt("Enter a color name or hex code:", color) || color;
            isEraser = false;
        }

        function toggleEraser() {
            isEraser = !isEraser;
        }

        // Mouse and Touch events
        canvas.addEventListener('mousedown', startPosition);
        canvas.addEventListener('mouseup', endPosition);
        canvas.addEventListener('mousemove', draw);

        canvas.addEventListener('touchstart', (e) => startPosition(e.touches[0]));
        canvas.addEventListener('touchend', endPosition);
        canvas.addEventListener('touchmove', (e) => draw(e.touches[0]));

        socket.on('draw', (data) => {
            ctx.lineWidth = 5;
            ctx.lineCap = 'round';
            ctx.strokeStyle = data.eraser ? 'white' : data.color;
            ctx.lineTo(data.x, data.y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(data.x, data.y);
        });

        socket.on('clear', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def whiteboard():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('draw')
def handle_draw(data):
    # Broadcast drawing data to all connected clients except the sender
    socketio.emit('draw', data, broadcast=True, include_self=False)

@socketio.on('clear')
def handle_clear():
    # Broadcast clear event to all clients
    socketio.emit('clear', broadcast=True)

def generate_qr_code(url):
    """Generate a QR code for the given URL."""
    qr = qrcode.make(url)
    qr.save("whiteboard_qr.png")

def get_local_ip():
    """Get the local IP address of the current machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    # Get the local IP address of the server
    ip_address = get_local_ip()
    port = 5000
    url = f"http://{ip_address}:{port}"

    # Generate and save the QR code
    generate_qr_code(url)
    print(f"QR code generated! Scan the QR code (whiteboard_qr.png) to access the whiteboard on your mobile device.")
    print(f"Or access the whiteboard directly at: {url}")

    # Run the Flask app with SocketIO support
    socketio.run(app, host='0.0.0.0', port=port)
