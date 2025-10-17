"""
Script de ejemplo para probar el endpoint de API del asistente.
"""
import requests
import json

# Configuración
API_URL = "http://localhost:5000/chat"
ASSISTANT_ID = "asst_xxxxxxxxxxxxx"  # Reemplaza con tu assistant_id real

# Ejemplos de mensajes para probar
test_messages = [
    "Hi",
    "you have a 3/2",
    "i want to know what homes you have with 3/2",
    "Tell me about lot 335",
    "What is the lot rent?",
    "Do you accept Section 8?",
    "Contact info?",
    "Info please",
    "What services do you offer?"
]


def test_endpoint(message, assistant_id):
    """
    Prueba el endpoint con un mensaje específico.
    """
    print(f"\n{'='*60}")
    print(f"📤 Enviando mensaje: '{message}'")
    print(f"{'='*60}")
    
    # Preparar el payload
    payload = {
        "message": message,
        "assistant_id": assistant_id
    }
    
    try:
        # Hacer la petición POST
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=65  # Timeout mayor al del servidor
        )
        
        # Verificar el código de respuesta
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Respuesta exitosa:")
            print(f"🔄 Query normalizado: '{data.get('normalized_query', 'N/A')}'")
            print(f"💬 Respuesta del asistente:")
            print(f"   {data.get('response', 'N/A')}")
            print(f"🆔 Thread ID: {data.get('thread_id', 'N/A')}")
        else:
            print(f"\n❌ Error {response.status_code}:")
            print(f"   {response.json()}")
    
    except requests.exceptions.Timeout:
        print("\n⏰ Timeout: El servidor tardó demasiado en responder")
    except requests.exceptions.ConnectionError:
        print("\n🔌 Error de conexión: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo (python app.py)")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")


def test_health():
    """
    Prueba el endpoint de salud.
    """
    print("\n🏥 Verificando estado del servidor...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('message', 'Servidor funcionando')}")
            return True
        else:
            print(f"❌ Error {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ No se pudo conectar al servidor: {str(e)}")
        print("   Asegúrate de ejecutar: python app.py")
        return False


if __name__ == "__main__":
    print("🧪 PRUEBA DEL API ENDPOINT")
    print("="*60)
    
    # Verificar que el servidor esté corriendo
    if not test_health():
        print("\n⚠️  Inicia el servidor primero con: python api_endpoint.py")
        exit(1)
    
    # Actualizar el assistant_id si es necesario
    if ASSISTANT_ID == "asst_xxxxxxxxxxxxx":
        print("\n⚠️  IMPORTANTE: Actualiza el ASSISTANT_ID en este archivo")
        print("   Usa el ID del asistente que creaste con create_rag_optimized_assistant.py")
        exit(1)
    
    # Probar cada mensaje
    for message in test_messages:
        test_endpoint(message, ASSISTANT_ID)
        input("\n⏸️  Presiona Enter para continuar con el siguiente mensaje...")
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60)

