// Carpeta simulada en memoria con la misma forma que la API de acceso a archivos
// (getDirectoryHandle, getFileHandle, entries, getFile, createWritable, permisos).
// Instrumento de validacion: registra cada escritura para poder volcarla.
(function () {
  function carpeta(nombre) {
    const hijos = new Map();
    return {
      kind: "directory", name: nombre, _hijos: hijos,
      async getDirectoryHandle(n, o = {}) {
        if (!hijos.has(n)) { if (!o.create) throw new DOMException("no existe " + n, "NotFoundError"); hijos.set(n, carpeta(n)); }
        const h = hijos.get(n); if (h.kind !== "directory") throw new DOMException(n, "TypeMismatchError"); return h;
      },
      async getFileHandle(n, o = {}) {
        if (!hijos.has(n)) { if (!o.create) throw new DOMException("no existe " + n, "NotFoundError"); hijos.set(n, archivo(n)); }
        const h = hijos.get(n); if (h.kind !== "file") throw new DOMException(n, "TypeMismatchError"); return h;
      },
      async removeEntry(n) { hijos.delete(n); },
      async *entries() { for (const e of hijos) yield e; },
      async queryPermission() { return "granted"; },
      async requestPermission() { return "granted"; },
      async isSameEntry(o) { return o === this; },
    };
  }
  function archivo(nombre) {
    let datos = "", t = Date.now();
    return {
      kind: "file", name: nombre,
      async getFile() { return { name: nombre, lastModified: t, size: datos.length, text: async () => datos }; },
      async createWritable() { let b = ""; return { write: async (x) => { b += typeof x === "string" ? x : (x && x.data !== undefined ? x.data : String(x)); }, close: async () => { datos = b; t = Date.now(); window.__escrituras = (window.__escrituras || 0) + 1; } }; },
      async queryPermission() { return "granted"; }, async requestPermission() { return "granted"; },
    };
  }
  window.__carpeta = carpeta;
  // Serializar y reconstruir: {nombre: {…}} para carpetas, texto para archivos.
  window.__serializar = async function (d) {
    const o = {};
    for (const [n, h] of d._hijos) o[n] = h.kind === "directory" ? await window.__serializar(h) : await (await h.getFile()).text();
    return o;
  };
  window.__reconstruir = async function (nombre, o) {
    const d = carpeta(nombre);
    for (const [n, v] of Object.entries(o)) {
      if (typeof v === "string") { const f = await d.getFileHandle(n, { create: true }); const w = await f.createWritable(); await w.write(v); await w.close(); }
      else d._hijos.set(n, await window.__reconstruir(n, v));
    }
    return d;
  };
})();
true;
