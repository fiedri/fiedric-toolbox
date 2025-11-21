# WhatsAppJS

Este proyecto es un script automatizado en Node.js que utiliza [Puppeteer](https://pptr.dev/) para enviar mensajes de WhatsApp de forma masiva a una lista de números telefónicos.

## ¿Qué hace este script?

El script abre WhatsApp Web en un navegador automatizado, espera a que escanees el código QR con tu teléfono y luego envía un mensaje personalizado a cada número listado en el archivo `src/numeros.txt`.

## Requisitos

- [Node.js](https://nodejs.org/) instalado en tu sistema.
- Tener instalado Google Chrome o Chromium (Puppeteer lo descarga automáticamente si no lo tienes).
- Una cuenta activa de WhatsApp en tu teléfono.

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias ejecutando:

   ```sh
   npm install puppetter

## Uso

1. **Edita el archivo de números:**  
   Abre `src/numeros.txt` y coloca un número de teléfono por línea, en formato internacional (por ejemplo: 584121234567).

2. **Edita el mensaje:**  
   Puedes cambiar el mensaje que se enviará editando la variable `mensaje` en `src/main.js`.

3. **Ejecuta el script:**

   ```sh
   node src/main.js


4. **Escanea el código QR:**  
   Cuando el script abra el navegador, escanea el código QR con tu teléfono desde WhatsApp para iniciar sesión.

5. **Envío automático:**  
   El script enviará el mensaje a cada número de la lista y mostrará en consola el progreso.

## Notas importantes

- No cierres el navegador hasta que el script termine de enviar todos los mensajes.
- WhatsApp puede bloquear temporalmente tu cuenta si detecta actividad sospechosa. Usa este script bajo tu propio riesgo y con responsabilidad.
- El script no verifica si el número tiene WhatsApp, simplemente intenta enviar el mensaje.

## Riesgos y advertencias sobre el uso del script

Es importante que sepas que WhatsApp **puede bloquear temporal o permanentemente** tu cuenta si detecta actividad que considera sospechosa o abusiva, como el envío masivo automatizado de mensajes no autorizados.

### ¿Por qué puede ocurrir un bloqueo?

- Enviar muchos mensajes iguales a múltiples contactos en poco tiempo puede ser interpretado como spam.
- Si varios usuarios reportan o bloquean tu número tras recibir mensajes no solicitados.

### Consejos para reducir riesgos

- Usa el script con moderación y evita enviar una cantidad de mensajes que pueda ser considerada como spam.
- Personaliza los mensajes para que no parezcan spam.
- Evita reenviar mensajes a los mismos números repetidamente.

**Usa esta herramienta bajo tu propio riesgo y con responsabilidad.**
