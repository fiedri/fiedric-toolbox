const fs = require('fs');
const puppeteer = require('puppeteer');

(async () => {
    const mensaje = `¡Hola! Te invito a seguir Phiexlab, mi canal de programación 💻🔥`;
    const numeros = fs.readFileSync('numeros.txt', 'utf8')
        .split('\n')
        .map(numero => numero.replace(/[\s\-]/g, '').trim())
        .filter(numero => /^\d+$/.test(numero) && numero.length > 0);
        
    const navegador = await puppeteer.launch({
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
        defaultViewport: null,
    });
    const pagina = await navegador.newPage();
    await pagina.goto('https://web.whatsapp.com/');
    console.log('Escanea el código QR con tu teléfono y espera a que se cargue el chat...');
    await pagina.waitForSelector('#pane-side', { timeout: 0 });

    for (const numero of numeros) {
        await pagina.goto(`https://web.whatsapp.com/send?phone=${numero.replace('+', '')}`);
        // Espera a que el chat esté listo o detecta si el número no tiene WhatsApp
        await pagina.waitForSelector('div[contenteditable="true"][aria-label="Type a message"]', { timeout: 0 });
        await pagina.type('div[contenteditable="true"][aria-label="Type a message"]', mensaje);
        await pagina.click('span[data-icon="send"]');
        console.log(`Mensaje enviado a ${numero}`);
        await new Promise(resolve => setTimeout(resolve, 4000));
    }
    await navegador.close();
})();