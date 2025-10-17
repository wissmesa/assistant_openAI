# 🚀 Deployment en Railway

Guía rápida para publicar tu API en Railway (gratis y fácil).

## 📋 Prerequisitos

1. Cuenta en [GitHub](https://github.com)
2. Cuenta en [Railway](https://railway.app) (usa tu cuenta de GitHub para login)
3. Tu `OPENAI_API_KEY` y `VECTOR_STORE_ID`

## 🚂 Pasos para Deployment

### Paso 1: Subir el Código a GitHub

1. **Inicializa Git** (si no lo has hecho):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Assistant API"
   ```

2. **Crea un repositorio en GitHub**:
   - Ve a https://github.com/new
   - Nombre del repo: `assistant-api` (o el que prefieras)
   - Puede ser **privado** o público
   - NO agregues README, .gitignore ni license (ya los tienes)
   - Click en "Create repository"

3. **Sube tu código**:
   ```bash
   git remote add origin https://github.com/TU-USUARIO/assistant-api.git
   git branch -M main
   git push -u origin main
   ```

### Paso 2: Configurar Railway

1. **Ve a [Railway.app](https://railway.app)**
   - Click en "Login" y usa tu cuenta de GitHub

2. **Crear nuevo proyecto**:
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Autoriza Railway a acceder a tu GitHub (si es primera vez)
   - Selecciona el repositorio `assistant-api` que creaste

3. **Railway detectará automáticamente**:
   - ✅ Python
   - ✅ `requirements.txt`
   - ✅ `Procfile`
   - ✅ Comenzará a instalar dependencias y desplegar

4. **Agregar Variables de Entorno**:
   - En tu proyecto de Railway, ve a la pestaña "Variables"
   - Click en "New Variable" y agrega:
   
   ```
   OPENAI_API_KEY = tu_clave_de_openai_aqui
   VECTOR_STORE_ID = tu_vector_store_id_aqui
   ```

5. **Generar un Dominio Público**:
   - Ve a la pestaña "Settings"
   - En la sección "Domains", click en "Generate Domain"
   - Railway te dará una URL como: `https://assistant-api-production-xxxx.up.railway.app`

### Paso 3: ¡Listo! Probar tu API

Tu API ya está en línea. Pruébala:

```bash
# Verificar salud
curl https://tu-dominio.up.railway.app/health

# Enviar un mensaje
curl -X POST https://tu-dominio.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "you have a 3/2",
    "assistant_id": "tu_assistant_id_aqui"
  }'
```

## 🔄 Actualizar tu API

Cada vez que hagas cambios y los subas a GitHub, Railway automáticamente:
1. Detecta los cambios
2. Re-deploya tu aplicación
3. La nueva versión queda disponible en minutos

```bash
# Hacer cambios en tu código
# Luego:
git add .
git commit -m "Descripción de cambios"
git push
```

Railway hará el resto automáticamente. 🎉

## 💰 Plan Gratuito de Railway

Railway ofrece:
- ✅ $5 USD de crédito gratis cada mes
- ✅ ~500 horas de servicio activo
- ✅ Sin necesidad de tarjeta de crédito
- ✅ Deployments ilimitados
- ✅ Sin tiempo de "sleep" (siempre activo)

**Nota**: Si necesitas más, puedes agregar $5 USD/mes.

## 📊 Monitoreo

En el dashboard de Railway puedes ver:
- 📈 Uso de recursos (CPU, RAM)
- 📝 Logs en tiempo real
- 💵 Consumo de créditos
- 🔄 Historial de deployments

## 🐛 Ver Logs

Para ver los logs de tu aplicación:
1. En Railway, click en tu servicio
2. Ve a la pestaña "Deployments"
3. Click en "View Logs"

O desde tu código, los `print()` aparecerán en los logs de Railway.

## ⚙️ Variables de Entorno Adicionales (Opcional)

Si necesitas agregar más variables:
- En Railway → "Variables" → "New Variable"

Ejemplos:
```
ENVIRONMENT = production
MAX_TIMEOUT = 90
API_KEY = tu_api_key_secreta (para autenticación)
```

## 🔒 Seguridad Recomendada

Para producción, considera agregar autenticación:

```python
# En app.py
API_KEY = os.getenv('API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    # Verificar API Key
    auth_header = request.headers.get('Authorization')
    if auth_header != f'Bearer {API_KEY}':
        return jsonify({"error": "Unauthorized"}), 401
    
    # ... resto del código
```

Luego agrega `API_KEY` en las variables de Railway.

## ✅ Checklist de Deployment

- [ ] Código subido a GitHub
- [ ] Proyecto creado en Railway
- [ ] Variables de entorno configuradas (`OPENAI_API_KEY`, `VECTOR_STORE_ID`)
- [ ] Dominio generado en Railway
- [ ] Endpoint `/health` responde 200 OK
- [ ] Endpoint `/chat` funciona correctamente
- [ ] URL de producción guardada y documentada

## 📞 Usar tu API en Producción

Una vez desplegado, usa tu URL de Railway en tus aplicaciones:

```python
import requests

API_URL = "https://tu-dominio.up.railway.app"

response = requests.post(
    f"{API_URL}/chat",
    json={
        "message": "you have a 3/2",
        "assistant_id": "asst_xxxxx"
    }
)

print(response.json()['response'])
```

## 🆘 Solución de Problemas

### Mi servicio no inicia
- Verifica los logs en Railway
- Asegúrate de que `Procfile` exista
- Verifica que `requirements.txt` tenga todas las dependencias

### Error de API Key
- Ve a Variables y confirma que `OPENAI_API_KEY` esté correcta
- No debe tener espacios al inicio o final
- Después de agregar/cambiar variables, Railway re-deploya automáticamente

### El servicio se quedó sin créditos
- Railway te da $5/mes gratis
- Puedes agregar $5 más si es necesario
- Verifica el uso en el dashboard

## 🎉 ¡Listo!

Tu API está en la nube, siempre disponible y lista para usarse desde cualquier lugar. 🌍

**URL de tu API**: https://tu-dominio.up.railway.app

