// Banco de pruebas de la consola. Corre sin navegador:  node front/probar.mjs
//
// Carga el JavaScript de consola.html en un DOM mínimo simulado y le da de comer entradas
// reales: un .zip armado acá mismo, una hoja de calificaciones con la cabecera del campus, y
// un informe saboteado a propósito. Está documentado en
// corridas/2026-09-08_prueba-de-la-consola.md
//
// No prueba la vara —eso lo prueba el caso testigo—. Prueba la herramienta.

import fs from "node:fs";
import path from "node:path";
import url from "node:url";
import vm from "node:vm";

const aca = path.dirname(url.fileURLToPath(import.meta.url));
const ok = [], mal = [];
const check = (c, t) => { (c ? ok : mal).push(t); console.log((c ? "  ok   " : "  MAL  ") + t); };

/* ================================================ 0 · cargar la consola */
const html = fs.readFileSync(path.join(aca, "consola.html"), "utf8");
const js = /<script>\n([\s\S]*)<\/script>/.exec(html)[1];

const elem = () => new Proxy(
  { innerHTML:"", textContent:"", value:"", style:{}, dataset:{}, files:[],
    classList:{ toggle(){}, add(){}, remove(){} } },
  { get:(t,k)=> k in t ? t[k] : (()=>{}), set:(t,k,v)=>{ t[k]=v; return true; } });
const memoria = {};
const g = {
  document:{ querySelector:()=>elem(), querySelectorAll:()=>[], createElement:()=>elem() },
  localStorage:{ getItem:k=>k in memoria?memoria[k]:null, setItem:(k,v)=>{memoria[k]=v;},
                 removeItem:k=>{delete memoria[k];} },
  alert:()=>{}, confirm:()=>true,
  // la consola se comporta distinto servida que como archivo suelto; el banco prueba
  // el camino de archivo suelto, que es el que no puede leer nada de al lado
  location:{ protocol:"file:", href:"file:///consola.html" },
  fetch:async()=>{ throw new Error("sin red en el banco de pruebas"); },
  navigator:{ clipboard:{ writeText:async()=>{} } },
  URL, Blob, Response, DecompressionStream, TextDecoder, TextEncoder, console,
};
g.window = g; g.globalThis = g;
const ctx = vm.createContext(g);
vm.runInContext(js, ctx);
const { abrirZip, parseCsv, buscaCol, validar, cortoDe, norm, partirCarpeta } = ctx;

/* ============================== armar un .zip de verdad, sin librerías */
const TABLA = (() => { const t=new Uint32Array(256);
  for(let n=0;n<256;n++){ let c=n; for(let k=0;k<8;k++) c = c&1 ? 0xEDB88320^(c>>>1) : c>>>1; t[n]=c>>>0; }
  return t; })();
const crc32 = b => { let c=0xFFFFFFFF;
  for(let i=0;i<b.length;i++) c = TABLA[(c^b[i])&0xFF] ^ (c>>>8);
  return (c^0xFFFFFFFF)>>>0; };

async function armarZip(entradas){          // [{ruta, texto|bytes, comprimir}]
  const enc = new TextEncoder(), partes = [], central = [];
  let off = 0;
  for (const e of entradas) {
    const crudo = e.bytes || enc.encode(e.texto);
    const datos = e.comprimir
      ? new Uint8Array(await new Response(
          new Blob([crudo]).stream().pipeThrough(new CompressionStream("deflate-raw"))
        ).arrayBuffer())
      : crudo;
    const nom = enc.encode(e.ruta), c = crc32(crudo), metodo = e.comprimir ? 8 : 0;
    const lh = new DataView(new ArrayBuffer(30));
    lh.setUint32(0,0x04034b50,true); lh.setUint16(4,20,true); lh.setUint16(6,0x800,true);
    lh.setUint16(8,metodo,true); lh.setUint32(14,c,true);
    lh.setUint32(18,datos.length,true); lh.setUint32(22,crudo.length,true);
    lh.setUint16(26,nom.length,true);
    partes.push(new Uint8Array(lh.buffer), nom, datos);

    const cd = new DataView(new ArrayBuffer(46));
    cd.setUint32(0,0x02014b50,true); cd.setUint16(4,20,true); cd.setUint16(6,20,true);
    cd.setUint16(8,0x800,true); cd.setUint16(10,metodo,true); cd.setUint32(16,c,true);
    cd.setUint32(20,datos.length,true); cd.setUint32(24,crudo.length,true);
    cd.setUint16(28,nom.length,true); cd.setUint32(42,off,true);
    central.push(new Uint8Array(cd.buffer), nom);
    off += 30 + nom.length + datos.length;
  }
  const tamCentral = central.reduce((a,b)=>a+b.length,0);
  const eo = new DataView(new ArrayBuffer(22));
  eo.setUint32(0,0x06054b50,true);
  eo.setUint16(8,entradas.length,true); eo.setUint16(10,entradas.length,true);
  eo.setUint32(12,tamCentral,true); eo.setUint32(16,off,true);
  const b = new Blob([...partes, ...central, new Uint8Array(eo.buffer)]);
  b.name = "entrega.zip";
  return b;
}

/* ------------------------------------------------------------ 1 · el zip */
console.log("\n1 · abrir un .zip real");
const zipFile = await armarZip([
  { ruta:"trabajo-final/README.md",            texto:"# Radar de licitaciones\n".repeat(40), comprimir:true },
  { ruta:"trabajo-final/DECISIONES.md",        texto:"Decision 1: separar system y user.\n".repeat(20), comprimir:true },
  { ruta:"trabajo-final/prompts/system.md",    texto:"Rol: analista de licitaciones.\n".repeat(10), comprimir:true },
  { ruta:"trabajo-final/corridas/2026-08-31.md", texto:"Entrada, salida y fecha.\n".repeat(10), comprimir:true },
  { ruta:"trabajo-final/img/captura.png",      bytes:new Uint8Array(5120).map((_,i)=>i%256), comprimir:false },
  { ruta:"trabajo-final/notas.txt",            texto:"x".repeat(90000), comprimir:false },
]);
zipFile.name = "Ana Beltran_1234567_assignsubmission_file.zip";
const z = await abrirZip(zipFile);
check(z.archivos.length === 6, `encuentra los 6 archivos (${z.archivos.length})`);
check(z.texto.includes("Radar de licitaciones"), "lee los archivos comprimidos (deflate)");
check(z.texto.includes("Rol: analista"), "lee los que están en subcarpetas");
check(z.texto.includes("xxxx"), "lee el guardado sin comprimir (stored)");
check(z.omitidos.some(o=>o.includes("captura.png")), "omite el binario y lo dice");
check(z.omitidos.some(o=>o.includes("recortado")), "recorta el largo y lo dice");

console.log("\n2 · el nombre de la carpeta del campus");
const p1 = partirCarpeta("Ana Beltran_1234567_assignsubmission_file");
check(p1.nombre==="Ana Beltran" && p1.identificador==="Participante 1234567",
  `saca nombre e identificador: ${p1.nombre} / ${p1.identificador}`);
const p2 = partirCarpeta("Bruno Cazenave");
check(p2.nombre==="Bruno Cazenave" && p2.identificador===null,
  "de una carpeta simple saca el nombre y deja el identificador en nulo, no lo inventa");

/* ------------------------------------------------------- 3 · la hoja */
console.log("\n3 · la hoja de calificaciones");
const hojaCsv =
  '﻿"Identificador","Nombre completo","Dirección de correo","Estado","Calificación","Comentarios de retroalimentación"\r\n' +
  '"Participante 1234567","Ana Beltrán","ana@ucema.edu.ar","Enviado para calificar","",""\r\n' +
  '"Participante 7654321","Bruno Cazenave","bruno@ucema.edu.ar","Enviado para calificar","",""\r\n' +
  '"Participante 1112223","Cecilia Díaz","ceci@ucema.edu.ar","Sin entrega","",""\r\n';
const filas = parseCsv(hojaCsv);
check(filas.length===4, `4 filas: cabecera + 3 alumnos (${filas.length})`);
const cab = filas[0];
const iId=buscaCol(cab,"identificador"), iNom=buscaCol(cab,"nombre completo","nombre"),
      iCal=buscaCol(cab,"calificacion"),
      iCom=buscaCol(cab,"comentarios de retroalimentacion","comentarios");
check(iId===0&&iNom===1&&iCal===4&&iCom===5,
  `reconoce las columnas con tildes: id=${iId} nom=${iNom} cal=${iCal} com=${iCom}`);
check(norm(filas[1][1])===norm("Ana Beltran"),
  "'Ana Beltrán' y 'Ana Beltran' son la misma persona");

/* --------------------------------------------- 4 · el csv que vuelve */
console.log("\n4 · el csv que vuelve al campus");
ctx.HOJA = { cabecera:cab, filas:filas.slice(1), iId, iNom, iCal, iCom, iMail:2, archivo:"hoja.csv" };
const informe = { estado:"evaluado", puntaje_final:74, puntaje_bruto:73.75,
  dimensiones:[{ id:"D1", nivel:3, peso:30, puntos:22.5,
    que_falta_para_el_nivel_siguiente:"Falta una corrida con la salida usada. Lo demás está." }],
  sugerencia_mejora:{ dimension:"D4", puntos_potenciales:7, accion:"Poner el precio con su fecha." } };
ctx.TRABAJOS = [
  { id:1, nombre:"Ana Beltrán",     identificador:"Participante 1234567", testigo:false, informe },
  { id:2, nombre:"Bruno Cazenave",  identificador:"Participante 7654321", testigo:false,
    informe:{ estado:"integridad_comprometida", puntaje_final:0, dimensiones:[] } },
  { id:3, nombre:"Dario Sin Hoja",  identificador:null, testigo:false,
    informe:{ estado:"evaluado", puntaje_final:61, dimensiones:[] } },
  { id:4, nombre:"casos/excelente/", testigo:true,
    informe:{ estado:"evaluado", puntaje_final:89, dimensiones:[] } },
];
let csv = null;
ctx.document.createElement = () => ({ set href(v){}, click(){}, download:"" });
ctx.URL.createObjectURL = () => "blob:x";
const BlobReal = ctx.Blob;
ctx.Blob = class extends BlobReal { constructor(p,o){ super(p,o); csv = p.join(""); } };
ctx.bajarCsv();
ctx.Blob = BlobReal;
const lin = csv.split("\r\n");
check(lin.length===5, `cabecera + las 3 filas de la hoja + 1 agregada (${lin.length})`);
check(lin[1].includes('"74"'), "el corregido sale con su nota");
check(lin[2].includes('"Bruno Cazenave"') && /,"",""\s*$/.test(lin[2]),
  "el integridad_comprometida sale SIN nota, con su fila intacta");
check(lin[3].includes("Cecilia"), "el alumno sin corregir queda intacto");
check(lin[4].includes("SIN IDENTIFICADOR") && lin[4].includes("Dario"),
  "el corregido que no está en la hoja se agrega al final, marcado");
check(!csv.includes("89"), "el caso testigo NO entra en la devolución");

/* --------------------------------------------------- 5 · la validación */
console.log("\n5 · la validación del informe");
ctx.ESQUEMA = { required:["estado","puntaje_final","cruces_realizados","nota_al_margen"] };
const ev = ["E1"];
const sano = { estado:"evaluado", puntaje_final:44, puntaje_bruto:43.75, nota_al_margen:null,
  cruces_realizados:["C1","C2","C3","C4","C5","C6","C7"],
  inventario:{ evidencia:[{ id:"E1" }] }, banderas:[],
  dimensiones:[
    { id:"D1", nivel:1, peso:30, puntos:7.5,  requisitos:[{cumple:true,evidencia:ev}], qf:1 },
    { id:"D2", nivel:1, peso:25, puntos:6.25, requisitos:[{cumple:true,evidencia:ev}], qf:1 },
    { id:"D3", nivel:4, peso:15, puntos:15,   requisitos:Array(4).fill({cumple:true,evidencia:ev}), qf:1 },
    { id:"D4", nivel:4, peso:15, puntos:15,   requisitos:Array(4).fill({cumple:true,evidencia:ev}), qf:1 },
    { id:"D5", nivel:0, peso:15, puntos:0,    requisitos:[], qf:1 }]};
// el campo que le llega al alumno: nunca vacio, ni en nivel 4
sano.dimensiones.forEach(d => { delete d.qf;
  d.que_falta_para_el_nivel_siguiente = "Guardar tres corridas con entrada, salida y fecha."; });
let r = validar(sano);
check(r.falla.length===0,
  "sobre un informe coherente no inventa problemas" + (r.falla.length ? ": "+r.falla.join(" | ") : ""));

const roto = JSON.parse(JSON.stringify(sano));
roto.dimensiones[0].nivel = 4;                                            // A4
roto.dimensiones[1].requisitos[0].evidencia = [];                         // A1
roto.dimensiones[2].puntos = 99;                                          // A5
roto.cruces_realizados = ["C1","C2"];                                     // A9
roto.banderas = [{ id:"G3a", nombre:"instrucción directa", evidencia:["E9"] }]; // A2 + estado
roto.puntaje_final = 95;                                                  // extremo sin nota al margen
r = validar(roto);
const dice = s => r.falla.some(f => f.includes(s));
check(dice("A4"), "A4 · nivel por encima de los requisitos cumplidos");
check(dice("A1"), "A1 · un SI sin evidencia citada");
check(dice("A5"), "A5 · puntos mal calculados");
check(dice("A9"), "A9 · faltan cruces reportados");
check(dice("A2"), "A2 · cita a evidencia que no está en el inventario");
check(dice("G3"), "una G3 con estado que no es integridad_comprometida");
check(dice("nota_al_margen"), "puntaje extremo sin nota al margen");

const sinTexto = JSON.parse(JSON.stringify(sano));
sinTexto.dimensiones[2].que_falta_para_el_nivel_siguiente = "";
check(validar(sinTexto).falla.some(f => f.includes("A7") && f.includes("D3")),
  "A7 · detecta la dimensión que vino sin el texto que le llega al alumno");

// A4 bis: el nivel tambien puede estar por DEBAJO de la cuenta, y eso solo lo puede hacer una compuerta
const bajado = JSON.parse(JSON.stringify(sano));
bajado.dimensiones[2].nivel = 2;                       // 4 requisitos en SI, nivel 2, sin explicacion
bajado.dimensiones[2].puntos = 7.5;
check(validar(bajado).falla.some(f => f.includes("A4 bis") && f.includes("D3")),
  "A4 bis · nivel por debajo de la cuenta, sin compuerta nombrada");

const bajadoConRegla = JSON.parse(JSON.stringify(bajado));
bajadoConRegla.dimensiones[2].justificacion =
  "Los 4 requisitos en SI darían nivel 4, pero la compuerta de menos de 3 corridas fija D3 <= 2.";
check(!validar(bajadoConRegla).falla.some(f => f.includes("A4 bis")),
  "A4 bis · no protesta cuando la compuerta está nombrada");

/* ---------------------------------------------------- 6 · el comentario */
console.log("\n6 · el comentario que le llega al alumno");
const corto = cortoDe(informe);
check(corto.split(/\s+/).length <= 180, `no pasa de 180 palabras (${corto.split(/\s+/).length})`);
check(!/\b74\b/.test(corto), "el número NO va adentro del texto: va en su columna");

/* ------------------------------------------- 7 · el orden del lote */
console.log("\n7 · el orden del lote (una vista, no una nota)");
const dims = n => [0,1,2,3,4].map(i => ({ id:"D"+(i+1), nivel:n[i] }));
ctx.TRABAJOS = [
  { id:1, nombre:"Zulema Alta", testigo:false, informe:{ estado:"evaluado",
    puntaje_final:81, puntaje_bruto:81, dimensiones:dims([4,3,3,2,2]), banderas:[] } },
  { id:2, nombre:"Ana Media", testigo:false, informe:{ estado:"evaluado",
    puntaje_final:74, puntaje_bruto:74, dimensiones:dims([3,3,3,2,2]), banderas:[] } },
  // mismo final que Ana, pero hizo más y lo penalizaron: va primero
  { id:3, nombre:"Beto Penado", testigo:false, informe:{ estado:"evaluado_con_reservas",
    puntaje_final:74, puntaje_bruto:79, dimensiones:dims([3,3,3,2,2]), banderas:[{id:"G7"}] } },
  { id:4, nombre:"Carlos Bajo", testigo:false, informe:{ estado:"evaluado",
    puntaje_final:31, puntaje_bruto:31, dimensiones:dims([1,1,1,0,1]), banderas:[] } },
  { id:5, nombre:"Delia Tramposa", testigo:false, informe:{ estado:"integridad_comprometida",
    puntaje_final:0, puntaje_bruto:46.25, dimensiones:dims([3,2,2,1,0]), banderas:[{id:"G3a"}] } },
  { id:6, nombre:"casos/excelente/", testigo:true, esperado:89, informe:{ estado:"evaluado",
    puntaje_final:89, puntaje_bruto:88.75, dimensiones:dims([4,4,4,2,3]), banderas:[] } },
];
const tabla  = ctx.ordenDelLote();
const cuerpo = tabla.split("Sin posición")[0];
const cola   = tabla.split("Sin posición")[1] || "";
const pos = n => cuerpo.indexOf(n);
check(pos("Zulema Alta") < pos("Beto Penado") && pos("Beto Penado") < pos("Carlos Bajo"),
  "ordena de mejor a peor por puntaje final");
check(pos("Beto Penado") < pos("Ana Media"),
  "empatados en 74, primero el de bruto mayor: hizo más y fue penalizado");
check(!cuerpo.includes("casos/excelente/"),
  "el caso testigo NO entra en el orden: no es un alumno");
check(cola.includes("Delia Tramposa"),
  "el integridad_comprometida va aparte, sin posición: la nota está suspendida, no es la peor");
check(cuerpo.includes("-8") && cuerpo.includes("-15"),
  "la distancia al testigo sale con signo (81 y 74 contra 89)");
check(/no hay una segunda nota/.test(tabla),
  "la tabla dice, en la propia pantalla, que no produce una segunda nota");


console.log(`\n${ok.length} bien, ${mal.length} mal`);
process.exit(mal.length ? 1 : 0);
