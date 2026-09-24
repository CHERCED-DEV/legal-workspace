// Cliente minimo de DevTools para Edge sin ventana: valida las paginas como las usara
// quien declara (doble clic, file://), sin instalar nada. Node 20: --experimental-websocket.
//
//   node --experimental-websocket cdp.mjs <guion.json> [CLAVE=valor ...]
//
// Cada {{CLAVE}} del guion se sustituye por su valor (rutas, URLs file:///...).
// Pasos: {"tam":[w,h]} {"ir":url} {"js":codigo} {"ver":codigo} {"esperar":ms}
//        {"hasta":codigo,"max":ms,"nombre":...} espera a que el codigo devuelva true
//        {"tecla":"Enter"|" "} {"sobre":expresion-elemento} (mueve el raton encima)
//        {"descargas":"C:/ruta"} (a nivel de NAVEGADOR: la orden a nivel de pagina se ignora)
//        {"inyectar":archivo,"variable":nombre} {"volcar":codigo,"a":carpeta} {"foto":png}
// Los dialogos (alert/confirm) se aceptan solos y se imprimen.
//
// Lecciones que ya costaron (no quitar):
//  - Se abre SIEMPRE una pestaña propia: la primera de la lista puede ser un dialogo del
//    navegador (edge://sync-confirmation-dialog, 360x505) y todo lo medido sale falso.
//  - La sesion del navegador que fija la carpeta de descargas se deja abierta hasta el
//    final: cerrarla anula la orden y la descarga no aparece en ninguna parte.
//  - Arrancar Edge con perfil TEMPORAL (--user-data-dir) y --no-first-run --disable-sync:
//    lo que se prueba no debe quedar en el navegador de nadie.
import fs from "node:fs";
import path from "node:path";

let texto = fs.readFileSync(process.argv[2], "utf8");
for (const par of process.argv.slice(3)) { const i = par.indexOf("="); texto = texto.split("{{" + par.slice(0, i) + "}}").join(par.slice(i + 1)); }
const faltan = texto.match(/\{\{[A-Z_0-9]+\}\}/g);
if (faltan) throw new Error("faltan valores para: " + [...new Set(faltan)].join(", "));
const guion = JSON.parse(texto);
const PUERTO = process.env.CDP_PUERTO || "9333";
const SALIDA = guion.salida;
fs.mkdirSync(SALIDA, { recursive: true });
// Siempre una pestaña propia y nueva: no se toma la primera de la lista, que puede ser
// un dialogo del propio navegador (paso con edge://sync-confirmation-dialog, 360x505).
const pagina = await (await fetch("http://127.0.0.1:" + PUERTO + "/json/new?about:blank", { method: "PUT" })).json();
if (!pagina.webSocketDebuggerUrl || !/^about:blank/.test(pagina.url || "about:blank")) throw new Error("no se pudo abrir una pestaña propia");
console.log("pestaña propia:", pagina.id);
const ws = new WebSocket(pagina.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener("open", r, { once: true }));
let id = 0;
const pendientes = new Map();
ws.addEventListener("message", ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pendientes.has(m.id)) { pendientes.get(m.id)(m); pendientes.delete(m.id); return; }
  if (m.method === "Page.javascriptDialogOpening") {
    console.log("DIALOGO (" + m.params.type + "): " + m.params.message.replace(/\s+/g, " ").slice(0, 300));
    enviar("Page.handleJavaScriptDialog", { accept: true, promptText: guion.respuesta_prompt || "" });
  }
});
const enviar = (method, params = {}) => new Promise(r => { id += 1; pendientes.set(id, r); ws.send(JSON.stringify({ id, method, params })); });
const dormir = ms => new Promise(r => setTimeout(r, ms));
const evaluar = async (codigo) => {
  const r = await enviar("Runtime.evaluate", { expression: codigo, awaitPromise: true, returnByValue: true, userGesture: true });
  if (r.result && r.result.exceptionDetails) return { error: (r.result.exceptionDetails.exception || {}).description || JSON.stringify(r.result.exceptionDetails).slice(0, 300) };
  return { valor: r.result && r.result.result ? r.result.result.value : undefined };
};

await enviar("Page.enable");
await enviar("Runtime.enable");
for (const paso of guion.pasos) {
  if (paso.tam) {
    await enviar("Emulation.setDeviceMetricsOverride", { width: paso.tam[0], height: paso.tam[1], deviceScaleFactor: 1, mobile: false });
  } else if (paso.descargas) {
    fs.mkdirSync(paso.descargas, { recursive: true });
    const v = await (await fetch("http://127.0.0.1:" + PUERTO + "/json/version")).json();
    const wb = new WebSocket(v.webSocketDebuggerUrl);
    await new Promise(r => wb.addEventListener("open", r, { once: true }));
    const r = await new Promise(res => { wb.addEventListener("message", ev => res(JSON.parse(ev.data)), { once: true });
      wb.send(JSON.stringify({ id: 1, method: "Browser.setDownloadBehavior", params: { behavior: "allow", downloadPath: paso.descargas.replace(/\//g, "\\"), eventsEnabled: true } })); });
    console.log("descargas del navegador ->", paso.descargas, r.error ? "ERROR " + JSON.stringify(r.error) : "ok");
    globalThis.__wb = wb;
  } else if (paso.ir) {
    await enviar("Page.navigate", { url: paso.ir });
    await dormir(paso.espera || 3000);
  } else if (paso.js || paso.ver) {
    const r = await evaluar(paso.js || paso.ver);
    if (r.error) console.log("ERROR JS:", r.error.slice(0, 400));
    else if (paso.ver) console.log(typeof r.valor === "string" ? r.valor : JSON.stringify(r.valor));
    await dormir(paso.espera || 400);
  } else if (paso.hasta) {
    const fin = Date.now() + (paso.max || 20000);
    let ok = false;
    while (Date.now() < fin) { const r = await evaluar(paso.hasta); if (r.valor === true) { ok = true; break; } await dormir(250); }
    console.log((ok ? "OK hasta: " : "TIEMPO AGOTADO: ") + (paso.nombre || paso.hasta.slice(0, 80)));
  } else if (paso.tecla) {
    const k = paso.tecla;
    const code = k === " " ? "Space" : k;
    await enviar("Input.dispatchKeyEvent", { type: "keyDown", key: k, code, text: k.length === 1 ? k : undefined, windowsVirtualKeyCode: k === "Enter" ? 13 : (k === " " ? 32 : 0) });
    await enviar("Input.dispatchKeyEvent", { type: "keyUp", key: k, code, windowsVirtualKeyCode: k === "Enter" ? 13 : (k === " " ? 32 : 0) });
    await dormir(paso.espera || 400);
  } else if (paso.sobre) {
    const r = await evaluar("(()=>{const e=" + paso.sobre + ";const b=e.getBoundingClientRect();return [b.left+Math.min(40,b.width/2),b.top+Math.min(20,b.height/2)]})()");
    if (r.error) { console.log("ERROR sobre:", r.error.slice(0, 200)); continue; }
    await enviar("Input.dispatchMouseEvent", { type: "mouseMoved", x: r.valor[0], y: r.valor[1] });
    await dormir(paso.espera || 500);
  } else if (paso.inyectar) {
    const texto = fs.readFileSync(paso.inyectar, "utf8");
    const r = await evaluar("window[" + JSON.stringify(paso.variable) + "]=" + JSON.stringify(texto) + ";true");
    console.log("inyectado", path.basename(paso.inyectar), "en", paso.variable, r.error ? "ERROR " + r.error : "ok");
  } else if (paso.volcar) {
    const r = await evaluar(paso.volcar);
    if (r.error) { console.log("ERROR volcar:", r.error.slice(0, 300)); continue; }
    fs.mkdirSync(paso.a, { recursive: true });
    for (const [n, t] of Object.entries(r.valor || {})) { fs.writeFileSync(path.join(paso.a, n), t, "utf8"); console.log("volcado", n, t.length, "bytes"); }
  } else if (paso.esperar) {
    await dormir(paso.esperar);
  } else if (paso.foto) {
    const r = await enviar("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(path.join(SALIDA, paso.foto), Buffer.from(r.result.data, "base64"));
    console.log("foto", paso.foto);
  }
}
ws.close();
if (globalThis.__wb) globalThis.__wb.close();
await fetch("http://127.0.0.1:" + PUERTO + "/json/close/" + pagina.id).catch(() => {});
