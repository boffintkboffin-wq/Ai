from flask import Flask, render_template, request, send_file
import requests
import io

app = Flask(__name__)

# API gratuita de Hugging Face para Stable Diffusion XL
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": "Bearer TU_TOKEN_DE_HUGGINGFACE"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generar", methods=["POST"])
def generar():
    data = request.json
    prompt = data.get("prompt", "")
    
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.content, 200, {"Content-Type": "image/png"}
    else:
        return {"error": "No se pudo generar la imagen, checa tu token o espera un momento."}, 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
