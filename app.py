from flask import Flask, request, jsonify, send_file
import subprocess
import os
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Pasta onde estarão os modelos de voz
MODELS_DIR = "/app/models"  # esse caminho será ajustado para o Docker

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text")
    voice = data.get("voice", "pt_BR-edresson-low")

    if not text:
        return jsonify({"error": "Texto não fornecido"}), 400

    # Cria diretório de saída, se não existir
    os.makedirs("output", exist_ok=True)

    output_filename = f"{uuid.uuid4()}.wav"
    output_path = os.path.join("output", output_filename)

    model_path = os.path.join(MODELS_DIR, voice, f"{voice}.onnx")
    config_path = os.path.join(MODELS_DIR, voice, f"{voice}.onnx.json")

    try:
        subprocess.run([
            "./piper", 
            "--model", model_path,
            "--config", config_path,
            "--output_file", output_path,
            "--text", text
        ], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Erro ao gerar áudio: {str(e)}"}), 500

    return send_file(output_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

