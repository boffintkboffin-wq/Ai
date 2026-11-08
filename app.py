from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generar", methods=["POST"])
def generar():
    data = request.json
    prompt_base = data.get("prompt", "")
    estilo = data.get("estilo", "")
    
    if not prompt_base:
        return jsonify({"success": False, "error": "El prompt está vacío"}), 400
    
    # Combinamos el prompt con el estilo seleccionado
    prompt_completo = f"{prompt_base}, {estilo}" if estilo else prompt_base
    
    # URL directa de la API para retornar al frontend
    api_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt_completo)}?width=1024&height=1024&nologo=true"
    
    try:
        # Verificamos que la API responda bien
        response = requests.get(api_url)
        
        if response.status_code == 200:
            return jsonify({"success": True, "image_url": api_url})
        else:
            return jsonify({"success": False, "error": "No se pudo generar la imagen en el servicio."}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
