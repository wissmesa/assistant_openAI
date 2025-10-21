"""
Script para probar el endpoint /chat/continue con conversaciones contextuales.
"""
import requests
import json

# Configuración
PRODUCTION_URL = "https://assistantopenai-production.up.railway.app"
ASSISTANT_ID = "asst_hcYW49TgFL4OtyAFNLGrlnDm"

print("="*70)
print("🧪 PRUEBA DE CONVERSACIÓN CONTEXTUAL")
print("="*70)

# Paso 1: Crear nueva conversación con /chat
print("\n📤 Paso 1: Iniciando conversación (POST /chat)")
print("Mensaje: 'you have a 3/2'")

response1 = requests.post(
    f"{PRODUCTION_URL}/chat",
    json={
        "message": "you have a 3/2",
        "assistant_id": ASSISTANT_ID
    },
    timeout=90
)

if response1.status_code == 200:
    data1 = response1.json()
    print(f"\n✅ Respuesta exitosa:")
    print(f"💬 {data1['response'][:100]}...")
    print(f"🆔 Thread ID: {data1['thread_id']}")
    
    thread_id = data1['thread_id']
    
    # Paso 2: Continuar conversación con /chat/continue
    print("\n" + "="*70)
    print("\n📤 Paso 2: Continuando conversación (POST /chat/continue)")
    print("Mensaje: 'What is the price of that home?'")
    print(f"Thread ID: {thread_id}")
    
    response2 = requests.post(
        f"{PRODUCTION_URL}/chat/continue",
        json={
            "message": "What is the price of that home?",
            "assistant_id": ASSISTANT_ID,
            "thread_id": thread_id
        },
        timeout=90
    )
    
    if response2.status_code == 200:
        data2 = response2.json()
        print(f"\n✅ Respuesta exitosa:")
        print(f"💬 {data2['response']}")
        print(f"🆔 Thread ID: {data2['thread_id']}")
        
        # Paso 3: Otra pregunta en el mismo contexto
        print("\n" + "="*70)
        print("\n📤 Paso 3: Tercera pregunta en mismo contexto (POST /chat/continue)")
        print("Mensaje: 'Can I schedule a showing?'")
        print(f"Thread ID: {thread_id}")
        
        response3 = requests.post(
            f"{PRODUCTION_URL}/chat/continue",
            json={
                "message": "Can I schedule a showing?",
                "assistant_id": ASSISTANT_ID,
                "thread_id": thread_id
            },
            timeout=90
        )
        
        if response3.status_code == 200:
            data3 = response3.json()
            print(f"\n✅ Respuesta exitosa:")
            print(f"💬 {data3['response']}")
            print(f"🆔 Thread ID: {data3['thread_id']}")
        else:
            print(f"\n❌ Error {response3.status_code}: {response3.text}")
    else:
        print(f"\n❌ Error {response2.status_code}: {response2.text}")
else:
    print(f"\n❌ Error {response1.status_code}: {response1.text}")

print("\n" + "="*70)
print("✅ PRUEBA COMPLETADA")
print("="*70)
print("\n📊 Resumen:")
print("✅ /chat - Crea nuevo thread")
print("✅ /chat/continue - Continúa conversación con thread_id")
print(f"\n🌍 API: {PRODUCTION_URL}")




