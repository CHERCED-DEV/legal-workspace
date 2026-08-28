// Conversor Markdown -> Word con tablas de verdad. ADR-014, pregunta abierta 2.
const {p,h,bullet,box,table,doc,Packer,HeadingLevel}=require('./lib.js');
const fs=require('fs');
const H1=HeadingLevel.HEADING_1,H2=HeadingLevel.HEADING_2,H3=HeadingLevel.HEADING_3;

function limpia(s){
  return s.replace(/\[([^\]]+)\]\([^)]*\)/g,'$1')   // enlaces -> solo texto
          .replace(/`([^`]+)`/g,'$1')                // codigo en linea
          .replace(/\s+$/,'');
}
function anchoCols(headers,rows){
  const n=headers.length; const w=new Array(n).fill(0);
  const todo=[headers,...rows];
  for(const r of todo) for(let i=0;i<n;i++) w[i]=Math.max(w[i], Math.min((r[i]||'').length, 90));
  return w.map(x=>Math.max(x,6));
}
function convierte(md){
  const lineas=md.split(/\r?\n/);
  const out=[]; let i=0; let titulo=null, subtitulo=null;
  while(i<lineas.length){
    let L=limpia(lineas[i]);
    if(/^#\s+/.test(L)&&titulo===null){ titulo=L.replace(/^#\s+/,''); i++;
      while(i<lineas.length && !lineas[i].trim()) i++;
      if(i<lineas.length && !/^[#>|-]/.test(lineas[i]) && lineas[i].trim()){ subtitulo=limpia(lineas[i]).replace(/\*\*/g,''); i++; }
      continue; }
    if(!L.trim()){ i++; continue; }
    if(/^---+$/.test(L.trim())){ i++; continue; }
    if(/^####\s+/.test(L)){ out.push(h(L.replace(/^####\s+/,''),H3)); i++; continue; }
    if(/^###\s+/.test(L)){ out.push(h(L.replace(/^###\s+/,''),H2)); i++; continue; }
    if(/^##\s+/.test(L)){ out.push(h(L.replace(/^##\s+/,''),H1)); i++; continue; }
    if(/^#\s+/.test(L)){ out.push(h(L.replace(/^#\s+/,''),H1)); i++; continue; }
    if(/^>\s?/.test(L)){                                  // cita destacada -> caja
      const buf=[];
      while(i<lineas.length && /^>\s?/.test(lineas[i])){ const t=limpia(lineas[i]).replace(/^>\s?/,''); if(t.trim())buf.push(t); i++; }
      out.push(box(buf.length?buf:[' '],"FFF2CC")); continue; }
    if(/^\s*\|/.test(L)){                                 // tabla
      const filas=[];
      while(i<lineas.length && /^\s*\|/.test(lineas[i])){ filas.push(limpia(lineas[i]).trim()); i++; }
      const celdas=filas.map(f=>f.replace(/^\|/,'').replace(/\|$/,'').split('|').map(c=>c.trim()));
      const cuerpo=celdas.filter(r=>!r.every(c=>/^:?-{2,}:?$/.test(c)||c===''));
      if(cuerpo.length>=1){
        const hd=cuerpo[0], rs=cuerpo.slice(1);
        const n=hd.length; const norm=rs.map(r=>{const c=r.slice(0,n); while(c.length<n)c.push(''); return c;});
        out.push(table(hd,norm,anchoCols(hd,norm)));
      } continue; }
    if(/^\*\*[HFVC]-\d+[^*]*\*\*\s*$/.test(L.trim())){    // ficha H-01 / F-01 / V-1 -> encabezado
      out.push(h(L.trim().replace(/^\*\*/,'').replace(/\*\*$/,''),H2)); i++; continue; }
    if(/^\s*[-*·]\s+[A-ZÁÉÍÓÚÑa-z][^:]{1,24}:\s/.test(L) && !/\*\*/.test(L.split(':')[0])){
      const filas=[]; let j=i;                              // lista "- Campo: valor" -> tabla
      while(j<lineas.length && /^\s*[-*·]\s+[A-ZÁÉÍÓÚÑa-z][^:]{1,24}:\s/.test(lineas[j]) && !/\*\*/.test(lineas[j].split(':')[0])){
        let t=limpia(lineas[j]).replace(/^\s*[-*·]\s+/,'');
        while(j+1<lineas.length && /^\s{2,}\S/.test(lineas[j+1]) && !/^\s*[-*·|>#]/.test(lineas[j+1])){ j++; t+=' '+limpia(lineas[j]).trim(); }
        const k=t.indexOf(':');
        filas.push([t.slice(0,k), t.slice(k+1).trim()]);
        j++;
      }
      if(filas.length>=3){ out.push(table(['Campo','Contenido'],filas,[18,82])); i=j; continue; }
    }
    if(/^\s*[-*·]\s+\*\*[^*]+:?\*\*/.test(L)){            // lista de campos -> tabla de dos columnas
      const filas=[]; let j=i;
      while(j<lineas.length && /^\s*[-*·]\s+\*\*[^*]+\*\*/.test(lineas[j])){
        let t=limpia(lineas[j]).replace(/^\s*[-*·]\s+/,'');
        while(j+1<lineas.length && /^\s{2,}\S/.test(lineas[j+1]) && !/^\s*[-*·|>#]/.test(lineas[j+1])){ j++; t+=' '+limpia(lineas[j]).trim(); }
        const m=t.match(/^\*\*([^*]+?)\*\*[::]?\s*(.*)$/);
        if(m) filas.push([m[1].replace(/[::]$/,''), m[2]]); else filas.push(['', t]);
        j++;
      }
      if(filas.length>=3){ out.push(table(['Campo','Contenido'],filas,[22,78])); i=j; continue; }
    }
    if(/^\s*[-*·]\s+/.test(L)){                           // vinetas
      while(i<lineas.length && /^\s*[-*·]\s+/.test(lineas[i])){
        let t=limpia(lineas[i]).replace(/^\s*[-*·]\s+/,'');
        // continuacion indentada
        while(i+1<lineas.length && /^\s{2,}\S/.test(lineas[i+1]) && !/^\s*[-*·|>#]/.test(lineas[i+1])){ i++; t+=' '+limpia(lineas[i]).trim(); }
        out.push(bullet(t)); i++; }
      continue; }
    if(/^\s*\d+\.\s+/.test(L)){                           // numeradas -> parrafo con su numero
      while(i<lineas.length && /^\s*\d+\.\s+/.test(lineas[i])){
        let t=limpia(lineas[i]).trim();
        while(i+1<lineas.length && /^\s{3,}\S/.test(lineas[i+1]) && !/^\s*[-*·|>#]/.test(lineas[i+1]) && !/^\s*\d+\./.test(lineas[i+1])){ i++; t+=' '+limpia(lineas[i]).trim(); }
        out.push(p(t,{indent:280})); i++; }
      continue; }
    let buf=[L]; i++;                                     // parrafo
    while(i<lineas.length && lineas[i].trim() && !/^\s*[|>#]/.test(lineas[i]) && !/^\s*[-*·]\s/.test(lineas[i]) && !/^\s*\d+\.\s/.test(lineas[i]) && !/^---+$/.test(lineas[i].trim())){ buf.push(limpia(lineas[i])); i++; }
    out.push(p(buf.join(' ')));
  }
  return {titulo:titulo||'Documento', subtitulo:subtitulo||'', hijos:out};
}
const [,,entrada,salida,tituloForzado,subForzado]=process.argv;
const md=fs.readFileSync(entrada,'utf8');
const c=convierte(md);
// Si se fuerza el subtitulo, el original NO se pierde: baja al cuerpo como descargo.
const hijos = (subForzado && c.subtitulo && c.subtitulo.trim())
  ? [box([c.subtitulo], "FFF2CC"), ...c.hijos]
  : c.hijos;
const D=doc(tituloForzado||c.titulo, subForzado||c.subtitulo, hijos);
Packer.toBuffer(D).then(b=>{fs.writeFileSync(salida,b);
  console.log(`OK  ${salida.split(/[\/]/).pop()}  ·  ${hijos.length} bloques`);});
