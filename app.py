from flask import Flask, request, jsonify
from openai import OpenAI
import re
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verificar que la API key esté configurada
if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
    raise ValueError("Por favor configura tu OPENAI_API_KEY en el archivo .env")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

# Función para normalizar consultas
def clean_query(text):
    """Normalize the user query before sending it to the assistant."""
    return re.sub(r'[^\w\s]', '', text.lower()).strip()


@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint para procesar mensajes del usuario con el asistente de OpenAI.
    
    Parámetros esperados (JSON):
    - message: String con el mensaje del usuario
    - assistant_id: String con el ID del asistente
    
    Retorna:
    - response: String con la respuesta del asistente
    - normalized_query: String con el query normalizado
    - status: String con el estado de la ejecución
    """
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No se proporcionaron datos en el request"
            }), 400
        
        user_message = data.get('message')
        assistant_id = data.get('assistant_id')
        
        # Validar parámetros requeridos
        if not user_message:
            return jsonify({
                "error": "El parámetro 'message' es requerido"
            }), 400
        
        if not assistant_id:
            return jsonify({
                "error": "El parámetro 'assistant_id' es requerido"
            }), 400
        
        # Normalizar el mensaje del usuario
        normalized_query = clean_query(user_message)
        
        # Crear thread y ejecutar el asistente
        run = client.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }
        )
        
        # Esperar a que se complete la ejecución
        max_wait_time = 60  # Máximo 60 segundos de espera
        start_time = time.time()
        
        while run.status in ['queued', 'in_progress']:
            # Verificar timeout
            if time.time() - start_time > max_wait_time:
                return jsonify({
                    "error": "Timeout: El asistente tardó demasiado en responder",
                    "status": run.status
                }), 408
            
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=run.thread_id,
                run_id=run.id
            )
        
        # Verificar si se completó exitosamente
        if run.status == 'completed':
            # Obtener los mensajes del thread
            messages = client.beta.threads.messages.list(thread_id=run.thread_id)
            
            # Buscar la respuesta del asistente
            assistant_response = None
            for message in messages.data:
                if message.role == "assistant":
                    for content in message.content:
                        if hasattr(content, 'text'):
                            assistant_response = content.text.value
                            break
                    if assistant_response:
                        break
            
            if assistant_response:
                return jsonify({
                    "response": assistant_response,
                    "normalized_query": normalized_query,
                    "status": "success",
                    "thread_id": run.thread_id
                }), 200
            else:
                return jsonify({
                    "error": "No se pudo obtener la respuesta del asistente",
                    "status": "error"
                }), 500
        
        else:
            # La ejecución falló
            error_message = "Error desconocido"
            if run.last_error:
                error_message = f"{run.last_error.code}: {run.last_error.message}"
            
            return jsonify({
                "error": f"La ejecución falló con estado: {run.status}",
                "details": error_message,
                "status": "error"
            }), 500
    
    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e),
            "status": "error"
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar que el servidor esté funcionando."""
    return jsonify({
        "status": "healthy",
        "message": "API endpoint está funcionando correctamente"
    }), 200


if __name__ == '__main__':
    # Obtener puerto desde variable de entorno o usar 5000 por defecto
    port = int(os.getenv('PORT', 5000))
    
    print("🚀 Iniciando API endpoint...")
    print(f"📡 Servidor corriendo en http://0.0.0.0:{port}")
    print("\nEndpoints disponibles:")
    print("  POST /chat - Procesar mensajes del usuario")
    print("  GET  /health - Verificar estado del servidor")
    print("\nEjemplo de uso:")
    print(f"""
    curl -X POST http://localhost:{port}/chat \\
      -H "Content-Type: application/json" \\
      -d '{{
        "message": "Do you have any 3/2 homes available?",
        "assistant_id": "asst_xxxxxxxxxxxxx"
      }}'
    """)
    
    # En producción, no usar debug=True
    is_production = os.getenv('ENVIRONMENT', 'development') == 'production'
    app.run(debug=not is_production, host='0.0.0.0', port=port)

