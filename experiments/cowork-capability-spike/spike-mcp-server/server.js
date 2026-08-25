#!/usr/bin/env node
/*
 * ============================================================================
 *  NON-PRODUCTION SPIKE — instrumento de medida, NO componente del producto
 * ============================================================================
 *
 *  Servidor MCP local mínimo para el Cowork Capability Spike (bloque 3, B-04).
 *
 *  Su ÚNICO propósito es responder la pregunta decisiva del perímetro:
 *  ¿puede un servidor MCP local alcanzar rutas que NO están adjuntadas a la
 *  sesión de Cowork, mientras las file tools del host no pueden?
 *
 *  PROHIBIDO: importar este archivo desde src/. No es código de producción,
 *  no tiene manejo de errores serio, no valida rutas y lee cualquier fichero
 *  que el proceso pueda abrir — eso es precisamente lo que queremos medir.
 *
 *  Sin dependencias: JSON-RPC 2.0 sobre stdio, escrito a mano para que se
 *  pueda ejecutar con Node sin instalar nada.
 * ============================================================================
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Registro de todo lo que ocurre, para poder pegarlo en el informe después.
// ---------------------------------------------------------------------------
const LOG_PATH = path.join(__dirname, 'spike-log.txt');

function log(event, detail) {
  const line = `${new Date().toISOString()}  ${event}  ${JSON.stringify(detail)}\n`;
  try { fs.appendFileSync(LOG_PATH, line); } catch (_) { /* el log nunca rompe la prueba */ }
}

// ---------------------------------------------------------------------------
// Las tres tools del spike.
// ---------------------------------------------------------------------------
const TOOLS = [
  {
    name: 'spike_read_path',
    description:
      'SPIKE: lee los primeros 200 bytes de una ruta absoluta del sistema de archivos. ' +
      'Instrumento de medida del perímetro; no es una capacidad de producto.',
    inputSchema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Ruta absoluta del fichero a leer.' },
      },
      required: ['path'],
    },
  },
  {
    name: 'spike_write_path',
    description:
      'SPIKE: añade una línea al final de un fichero en una ruta absoluta. ' +
      'Instrumento de medida del perímetro; no es una capacidad de producto.',
    inputSchema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Ruta absoluta del fichero a modificar.' },
        text: { type: 'string', description: 'Texto a añadir.' },
      },
      required: ['path', 'text'],
    },
  },
  {
    name: 'spike_whoami',
    description:
      'SPIKE: informa del contexto en que corre el servidor MCP (cwd, usuario, plataforma). ' +
      'Sirve para saber DÓNDE se está ejecutando el proceso.',
    inputSchema: { type: 'object', properties: {} },
  },
];

// ---------------------------------------------------------------------------
// Ejecución de cada tool. Devuelve SIEMPRE un resultado legible: si falla,
// el error literal es el dato que interesa registrar.
// ---------------------------------------------------------------------------
function runTool(name, args) {
  args = args || {};

  if (name === 'spike_read_path') {
    try {
      const fd = fs.openSync(args.path, 'r');
      const buf = Buffer.alloc(200);
      const n = fs.readSync(fd, buf, 0, 200, 0);
      fs.closeSync(fd);
      const text = buf.slice(0, n).toString('utf8');
      log('READ_OK', { path: args.path, bytes: n });
      return { ok: true, text: `LECTURA CORRECTA (${n} bytes):\n${text}` };
    } catch (err) {
      log('READ_FAIL', { path: args.path, code: err.code, message: err.message });
      return {
        ok: false,
        text:
          `LECTURA FALLIDA\n` +
          `ruta:    ${args.path}\n` +
          `código:  ${err.code}\n` +
          `mensaje: ${err.message}\n` +
          `\n[IMPORTANTE para el informe: este error viene del SERVIDOR MCP (del propio ` +
          `sistema de archivos). Si Cowork hubiera bloqueado la llamada antes de llegar aquí, ` +
          `no verías este texto en absoluto.]`,
      };
    }
  }

  if (name === 'spike_write_path') {
    try {
      fs.appendFileSync(args.path, `\n[SPIKE-MCP-WRITE ${new Date().toISOString()}] ${args.text}\n`);
      log('WRITE_OK', { path: args.path });
      return { ok: true, text: `ESCRITURA CORRECTA en ${args.path}` };
    } catch (err) {
      log('WRITE_FAIL', { path: args.path, code: err.code, message: err.message });
      return {
        ok: false,
        text:
          `ESCRITURA FALLIDA\n` +
          `ruta:    ${args.path}\n` +
          `código:  ${err.code}\n` +
          `mensaje: ${err.message}\n` +
          `\n[Este error viene del SERVIDOR MCP, no de Cowork.]`,
      };
    }
  }

  if (name === 'spike_whoami') {
    const info = {
      cwd: process.cwd(),
      platform: process.platform,
      nodeVersion: process.version,
      pid: process.pid,
      user: process.env.USERNAME || process.env.USER || '(desconocido)',
      execPath: process.execPath,
      serverDir: __dirname,
    };
    log('WHOAMI', info);
    return { ok: true, text: JSON.stringify(info, null, 2) };
  }

  return { ok: false, text: `Tool desconocida: ${name}` };
}

// ---------------------------------------------------------------------------
// Transporte JSON-RPC 2.0 sobre stdio, con framing por Content-Length.
// ---------------------------------------------------------------------------
function send(msg) {
  const body = Buffer.from(JSON.stringify(msg), 'utf8');
  process.stdout.write(`Content-Length: ${body.length}\r\n\r\n`);
  process.stdout.write(body);
}

function handle(msg) {
  const { id, method, params } = msg;

  if (method === 'initialize') {
    log('INITIALIZE', { params });
    // Se devuelve la misma versión que pide el cliente: es un spike, no un
    // servidor que deba negociar nada.
    const requested = (params && params.protocolVersion) || '2025-06-18';
    return send({
      jsonrpc: '2.0',
      id,
      result: {
        protocolVersion: requested,
        capabilities: { tools: {} },
        serverInfo: { name: 'legal-os-capability-spike', version: '0.0.1-NON-PRODUCTION' },
      },
    });
  }

  if (method === 'notifications/initialized' || method === 'initialized') {
    return; // notificación: sin respuesta
  }

  if (method === 'tools/list') {
    log('TOOLS_LIST', {});
    return send({ jsonrpc: '2.0', id, result: { tools: TOOLS } });
  }

  if (method === 'tools/call') {
    const name = params && params.name;
    const args = (params && params.arguments) || {};
    log('TOOLS_CALL', { name, args });
    const r = runTool(name, args);
    return send({
      jsonrpc: '2.0',
      id,
      result: { content: [{ type: 'text', text: r.text }], isError: !r.ok },
    });
  }

  if (id !== undefined) {
    return send({
      jsonrpc: '2.0',
      id,
      error: { code: -32601, message: `Método no implementado en el spike: ${method}` },
    });
  }
}

// --- lector de stdin con framing ---
let buffer = Buffer.alloc(0);

process.stdin.on('data', (chunk) => {
  buffer = Buffer.concat([buffer, chunk]);

  for (;;) {
    const sep = buffer.indexOf('\r\n\r\n');
    if (sep === -1) return;

    const header = buffer.slice(0, sep).toString('utf8');
    const match = /Content-Length:\s*(\d+)/i.exec(header);
    if (!match) { buffer = buffer.slice(sep + 4); continue; }

    const len = parseInt(match[1], 10);
    const start = sep + 4;
    if (buffer.length < start + len) return; // mensaje incompleto

    const body = buffer.slice(start, start + len).toString('utf8');
    buffer = buffer.slice(start + len);

    try {
      handle(JSON.parse(body));
    } catch (err) {
      log('PARSE_ERROR', { message: err.message });
    }
  }
});

log('SERVER_START', { argv: process.argv, cwd: process.cwd() });
