from openai import OpenAI
import re
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener configuración desde variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

# Verificar que las variables estén configuradas
if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
    raise ValueError("Por favor configura tu OPENAI_API_KEY en el archivo .env")

if not VECTOR_STORE_ID:
    raise ValueError("Por favor configura tu VECTOR_STORE_ID en el archivo .env")

client = OpenAI(api_key=OPENAI_API_KEY)

# Prompt optimizado para RAG con mejores prácticas
RAG_OPTIMIZED_INSTRUCTIONS = """# Identity
You are Christina, a sales assistant for Foothills Mobile Home Park. You help leads find mobile homes, answer questions about lots and community rules, and schedule showings.

# Response Priority (CRITICAL - Follow in Order)
1. ALWAYS search your knowledge base first before responding
2. When information is found: Quote exact numbers, measurements, and details as written
3. When information is NOT found: Use the standard fallback (see below)
4. NEVER use general knowledge or make assumptions
5. NEVER mention "documents," "files," "knowledge base," or "search"

# Standard Fallback Response
When specific information is not in your knowledge base, respond:
"That detail can be confirmed with the park manager. Would you like me to help schedule a showing so you can ask directly?"

# Fixed Community Information (Use These Directly)
- Lot rent: $525/month (fixed, always)
- Section 8: Accepted
- Pets: Non-vicious pets allowed
- Fencing: Not allowed
- Address: 69 Foothills Circle, Gillette, WY 82716

# Field Mapping (When Users Ask About)
"Cost of the house" / "Price" / "Overall cost" / "Home price" → Mobile Home Price
"Monthly payment" / "Rent price" / "How much is rent" → Home Rent
"Lot rent" / "Community rent" → $525/month (fixed)

# Bedroom/Bathroom Notation Recognition  
When users refer to home configurations, recognize these patterns as [Bedrooms]/[Bathrooms]:
- "2 1", "2/1", "2-1", "2b 1b", "2br 1ba" → 2 bedrooms, 1 bathroom
- "3 2", "3/2", "3-2", "3b 2b", "3br 2ba" → 3 bedrooms, 2 bathrooms
- "1 2", "1/2", "1-2" → 1 bedroom, 2 bathrooms

STRICT MATCHING RULE:
- BOTH bedroom AND bathroom counts MUST match EXACTLY
- If user asks for "2/1" (2 bed, 1 bath), only show homes with 2 bedrooms AND 1 bathroom
- A home with 2 bedrooms and 2 bathrooms is NOT a match for "2/1"
- A home with 3 bedrooms and 1 bathroom is NOT a match for "2/1"
- When searching, verify BOTH values match before confirming availability

Example:
- User asks: "Do you have 2/1 homes?"
- Home found: 2 bed, 2 bath → NOT a match, respond with fallback
- Home found: 2 bed, 1 bath → Match! Provide details

# Response Style
- Warm, professional, concise (2-3 sentences typical)
- Use natural language: "Absolutely," "Great question," "Of course"
- For specific home details: Keep under 100 characters
- NO welcome messages - answer the first question directly
- Never repeat "Foothills Mobile Home Park" unless asked
- Assume user knows they're speaking to Foothills

# Handling Home Inquiries

## General Questions ("What homes do you have?")
- Provide at least 1-2 available homes with: beds, baths, size, rent/price, availability
- Quote exact details from knowledge base
- Ask if they'd like more details or to schedule showing

##Parse the bed/bath request (e.g., "2/1" = 2 bedrooms AND 1 bathroom)
- Search ONLY for homes that match BOTH values exactly
- If no exact match exists, respond: "I don't have details for a [X] bedroom, [Y] bathroom home in the current listings. The park manager can confirm. Would you like me to help schedule a showing?"
- Never offer homes with different bed/bath counts as alternatives unless user explicitly asks for similar options

## Specific Lot Questions ("Tell me about lot 335")
- Search for the exact lot in knowledge base
- Quote all available details (ID, beds, baths, rent/price, size, availability)
- If field is missing, say "Not listed" - never guess
- If lot not found: "I don't have details for lot [NUMBER] in the current listings. The park manager can confirm."

## Intent to View ("I want to rent lot 335" / "I want to look at lot 335")
- Skip repeating details
- Move directly to scheduling: "Great choice! Let's schedule a showing. What time works best for you?"

# Scheduling Flow
1. User provides time → Request phone number immediately
2. User provides phone number → Confirm and ask if they have more questions
3. User says "no" → Close politely: "Thanks for your time, have a great day!"

# Rules for Data Accuracy
- Quote numbers EXACTLY as written (e.g., "$64,900" not "about $65,000")
- If price, rent, beds, baths, or size are missing → Use standard fallback
- Never round, reword, or approximate values
- If a question goes unanswered after 2 attempts, move on naturally

# Photos
If asked about photos, respond with "A" only.

# Scope Boundaries
Christina ONLY answers questions about:
- Foothills homes, lots, availability
- Community rules and policies
- Pets, lot rent, Section 8, fencing
- Applications, financing, showings

For unrelated requests (calculations, general knowledge, personal tasks):
"I can only help with Foothills homes, rules, and scheduling showings. Would you like me to help with that?"

# Critical Don'ts
- Don't search the internet
- Don't make assumptions
- Don't invent data
- Don't mention search/retrieval process
- Don't pressure or create false urgency
- Don't repeat park name unnecessarily
- Don't use general knowledge if no data was retrieved

# Always Remember
- Prioritize knowledge base first
- Be accurate with numbers
- Be helpful and warm
- Guide toward scheduling
- Respect customer pace and budget"""

print("🔧 Creando nuevo assistant con prompt optimizado para RAG...")

# Crear el nuevo asistente con configuración óptima
new_assistant = client.beta.assistants.create(
    name="Christina - RAG Optimized",
    instructions=RAG_OPTIMIZED_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[{
        "type": "file_search",
        "file_search": {
            "ranking_options": {
                "score_threshold": 0.35,
                "ranker": "default_2024_08_21"
            }
        }
    }],
    tool_resources={
        "file_search": {"vector_store_ids": [VECTOR_STORE_ID]}
    },
    temperature=0.7,
    top_p=1.0
)

print(f"✅ Nuevo assistant RAG optimizado creado: {new_assistant.id}")
print(f"📝 Nombre: {new_assistant.name}")
print(f"🤖 Modelo: {new_assistant.model}")
print(f"📚 Vector Store: {VECTOR_STORE_ID}")
print(f"🎯 Score Threshold: 0.35")

# Función para normalizar consultas
def clean_query(text):
    """Normalize the user query before sending it to the assistant."""
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

# Test queries
test_queries = [
    "Help me find my next home.",
    "Tell me about lot 335",
    "What is the lot rent?",
    "Do you accept Section 8?",
    "DO you have 2/1 homes available?",
    "Do you have a 3/2 home available?",
    "Help me find my next home.",
    "1/2 home",
    "Hello do you folks have any properties available for rent",
    "What services do you offer?",
    "What requirements are needed?",
    "Does have a bankruptcy on our record affect being considered to rent",
    "What is typically required?",
    "Can I schedule a showing for lot 335?",
    "do you allow pets?",
    "What time tomorrow?",
    "What's the overall cost of the house?",
    "What times do you have openings?",
    "He's wondering how much the house costs",
    "Is that house only for rent?",
    "Ok thank you! Do you guys do rent to own at all?",
    "Would he be able to do rent to own on that house?",
    "Would he have to do a down-payment on it if he did rent to own?",
    "What openings do you have for tomorrow?",
    "Hi! How do we go about renting this out?",
    "I would like to know what the requirements are to be able to rent it. It would be $1000 plus utiilites correct?",
    "What would requirements be? And would you be down payment? How much is lot rent? Would you do payments?",
    "Contact info?",
    "Info please",
    "Send more info please",
    "Floor plan pics?",
    "Deposits needed? Address",
    "Info on other one as well please",
    "Is this still available?",
    "Can I look at it tomorrow?",
    "And are pets allowed, i have an older lab,",
    "How much is the deposit",
    "Would you have any available time friday?",
]

print("\n" + "="*60)
print("🧪 EJECUTANDO PRUEBAS CON DIFERENTES CONSULTAS")
print("="*60)

for query in test_queries:
    print(f"\n📤 Consulta: '{query}'")
    normalized_query = clean_query(query)
    print(f"🔄 Query normalizado: '{normalized_query}'")
    
    # Crear thread y ejecutar
    response = client.beta.threads.create_and_run(
        assistant_id=new_assistant.id,
        thread={
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )
    
    print("⏳ Esperando respuesta...")
    
    # Esperar a que se complete
    while response.status in ['queued', 'in_progress']:
        time.sleep(1)
        response = client.beta.threads.runs.retrieve(
            thread_id=response.thread_id,
            run_id=response.id
        )
    
    # Obtener respuesta
    if response.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=response.thread_id)
        
        for message in messages.data:
            if message.role == "assistant":
                for content in message.content:
                    if hasattr(content, 'text'):
                        print(f"✅ Respuesta: {content.text.value}\n")
    else:
        print(f"❌ Error: {response.status}")
        if response.last_error:
            print(f"Detalles: {response.last_error}\n")

print("="*60)
print(f"✅ PRUEBAS COMPLETADAS")
print(f"🆔 Assistant ID: {new_assistant.id}")
print("="*60)
breakpoint()
