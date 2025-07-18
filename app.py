import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de la API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Preguntas definidas previamente
PREDEFINED_QUESTIONS = {
    "¿Cuál es la capital de Francia?": "París",
    "¿Quién escribió 'Cien años de soledad'?": "Gabriel García Márquez",
    "¿Cuál es el propósito de la inteligencia artificial?": "Crear sistemas capaces de imitar la inteligencia humana para automatizar tareas y tomar decisiones."
}

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()

    # Respuesta automática según preguntas definidas
    if question in PREDEFINED_QUESTIONS:
        answer = PREDEFINED_QUESTIONS[question]
    else:
        # Si la pregunta no está definida, se utiliza API de OpenAI para respuesta dinámica.
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=question,
                max_tokens=150,
                temperature=0.5,
            )
            answer = response.choices[0].text.strip()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"question": question, "answer": answer})


if __name__ == "__main__":
    app.run(debug=True)

