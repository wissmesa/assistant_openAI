"""
Script para probar el endpoint de producción en Railway.
"""
import requests
import json

# Configuración
PRODUCTION_URL = "https://assistantopenai-production.up.railway.app"
ASSISTANT_ID = "asst_hcYW49TgFL4OtyAFNLGrlnDm"  # ⚠️ REEMPLAZA CON TU ASSISTANT_ID REAL

def test_health():
    """Prueba el endpoint de health."""
    print("\n🏥 Probando endpoint /health...")
    try:
        response = requests.get(f"{PRODUCTION_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"✅ Health check exitoso: {response.json()}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_chat(message):
    """Prueba el endpoint /chat."""
    print(f"\n💬 Enviando mensaje: '{message}'")
    
    payload = {
        "message": message,
        "assistant_id": ASSISTANT_ID
    }
    
    try:
        response = requests.post(
            f"{PRODUCTION_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=90  # El asistente puede tardar
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Respuesta exitosa:")
            print(f"📝 Query normalizado: {data.get('normalized_query')}")
            print(f"💬 Respuesta del asistente:")
            print(f"   {data.get('response')}")
            print(f"🆔 Thread ID: {data.get('thread_id')}")
        else:
            print(f"\n❌ Error {response.status_code}:")
            print(response.text)
    
    except requests.exceptions.Timeout:
        print("\n⏰ Timeout: El servidor tardó demasiado (más de 90 segundos)")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    print("="*70)
    print("🧪 PRUEBA DEL ENDPOINT EN PRODUCCIÓN (RAILWAY)")
    print("="*70)
    
    # Verificar que el assistant_id esté configurado
    if ASSISTANT_ID == "asst_xxxxxxxxxxxxx":
        print("\n⚠️  IMPORTANTE: Actualiza el ASSISTANT_ID en este archivo")
        print("   Línea 9: ASSISTANT_ID = 'tu_assistant_id_real'")
        exit(1)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ El servidor no está respondiendo correctamente")
        exit(1)
    
    print("\n" + "="*70)
    
    # Test 2: Chat endpoint
    test_messages = [
        "Hi",
        "you have a 3/2",
        "What is the lot rent?",
        "Contact info?"
    ]
    
    for msg in test_messages:
        test_chat(msg)
        print("\n" + "-"*70)
        input("⏸️  Presiona Enter para continuar...")
    
    print("\n" + "="*70)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*70)
    print(f"\n🌍 Tu API está funcionando en: {PRODUCTION_URL}")

