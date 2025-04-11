from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>App1 - Animated Frontend</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            body {
                margin: 0;
                padding: 0;
                height: 100vh;
                background: linear-gradient(135deg, #667eea, #764ba2);
                overflow: hidden;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            /* Blobs */
            .blob {
                position: absolute;
                border-radius: 50%;
                opacity: 0.4;
                filter: blur(80px);
                animation: float 10s infinite ease-in-out;
            }

            .blob1 {
                width: 300px;
                height: 300px;
                background: #ff9a9e;
                top: -50px;
                left: -50px;
                animation-delay: 0s;
            }

            .blob2 {
                width: 400px;
                height: 400px;
                background: #fad0c4;
                bottom: -100px;
                right: -100px;
                animation-delay: 2s;
            }

            .container {
                position: relative;
                z-index: 1;
                color: white;
                background-color: rgba(255, 255, 255, 0.1);
                margin: 100px auto;
                max-width: 500px;
                padding: 50px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                animation: slideIn 1.2s ease;
            }

            h1 {
                font-size: 3em;
                margin-bottom: 10px;
                animation: fadeIn 1.5s ease;
            }

            p {
                font-size: 1.2em;
                color: #f0f0f0;
                margin-bottom: 30px;
                animation: fadeIn 2s ease;
            }

            input[type="text"] {
                padding: 12px 20px;
                width: 80%;
                max-width: 300px;
                border-radius: 8px;
                border: none;
                margin-bottom: 20px;
                font-size: 1em;
                animation: pulse 2s infinite alternate;
            }

            button {
                padding: 12px 25px;
                font-size: 1em;
                border: none;
                border-radius: 8px;
                background-color: #ffffff;
                color: #764ba2;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                animation: bounce 2s infinite;
            }

            button:hover {
                background-color: #f4f4f4;
                transform: scale(1.05);
            }

            .icons {
                margin-top: 30px;
                font-size: 1.8em;
            }

            .icons i {
                margin: 0 12px;
                transition: transform 0.3s, color 0.3s;
            }

            .icons i:hover {
                color: #ffd700;
                transform: rotate(10deg) scale(1.2);
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes slideIn {
                from { opacity: 0; transform: translateY(-30px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes pulse {
                from { box-shadow: 0 0 0px rgba(255,255,255,0.2); }
                to { box-shadow: 0 0 20px rgba(255,255,255,0.4); }
            }

            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }

            @keyframes float {
                0% { transform: translateY(0) translateX(0); }
                50% { transform: translateY(-30px) translateX(20px); }
                100% { transform: translateY(0) translateX(0); }
            }
        </style>
    </head>
    <body>
        <div class="blob blob1"></div>
        <div class="blob blob2"></div>
        <div class="container">
            <h1><i class="fas fa-rocket"></i> Hello from App1!</h1>
            <p>Welcome to your vibrant, animated Flask frontend 🎨</p>
            <input type="text" placeholder="Type something fun...">
            <br><br>
            <button><i class="fas fa-magic"></i> Click Me</button>
            <div class="icons">
                <i class="fab fa-python" title="Python"></i>
                <i class="fab fa-github" title="GitHub"></i>
                <i class="fas fa-code" title="Code"></i>
                <i class="fas fa-heart" title="Love for Devs"></i>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(port=5001, debug=True)

