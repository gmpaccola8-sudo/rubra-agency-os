#!/usr/bin/env node
// RUBRA · render + inspeção objetiva de peças gráficas (HTML/SVG → PNG).
//
// Uso: node render.js <pasta_html> <pasta_saida> [--largura 1080] [--altura 1350] [--seguranca 60]
//
// Para cada .html da pasta gera:
//   <nome>.png            peça final
//   <nome>@miniatura.png  como aparece no feed do celular (~360 px de largura)
//   <nome>@desfoque.png   teste de hierarquia (o que domina desfocado)
// e um relatorio.json com falhas objetivas:
//   fonte_fallback · texto_transbordando · fora_da_area_segura · contraste_baixo
// Sai com código 1 se houver falha objetiva.

const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

function args() {
  const a = process.argv.slice(2);
  const opt = { largura: 1080, altura: 1350, seguranca: 60 };
  const pos = [];
  for (let i = 0; i < a.length; i++) {
    if (a[i].startsWith("--")) opt[a[i].slice(2)] = Number(a[++i]);
    else pos.push(a[i]);
  }
  if (pos.length < 2) { console.error("uso: node render.js <pasta_html> <pasta_saida> [opções]"); process.exit(2); }
  return { entrada: pos[0], saida: pos[1], ...opt };
}

// Roda dentro da página: coleta medidas de tipografia, transbordo, área segura e contraste.
function inspecionarPagina({ seguranca, largura, altura }) {
  const falhas = [];
  const rgb = (s) => { const m = s.match(/[\d.]+/g); return m ? m.map(Number) : [0, 0, 0, 0]; };
  const lum = ([r, g, b]) => {
    const f = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const contraste = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const fundo = (el) => {
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== "none") return null; // imagem: não dá para medir
      const c = rgb(cs.backgroundColor);
      if (c.length < 4 || c[3] > 0.5) return c;
    }
    return [255, 255, 255, 1];
  };
  const carregadas = new Set([...document.fonts].filter((f) => f.status === "loaded").map((f) => f.family.replace(/["']/g, "")));
  const vistas = new Set();

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const texto = n.textContent.trim();
    if (!texto) continue;
    const el = n.parentElement;
    const cs = getComputedStyle(el);
    if (cs.visibility === "hidden" || cs.display === "none" || Number(cs.opacity) === 0) continue;
    const trecho = texto.slice(0, 40);

    // Fonte: a primeira família declarada precisa estar carregada (senão é fallback do sistema).
    const familia = cs.fontFamily.split(",")[0].trim().replace(/["']/g, "");
    if (!carregadas.has(familia) && !vistas.has(familia)) {
      vistas.add(familia);
      falhas.push({ tipo: "fonte_fallback", detalhe: `"${familia}" não carregou (texto: "${trecho}")` });
    }

    // Área segura e corte pela borda da peça.
    const r = document.createRange(); r.selectNodeContents(n);
    for (const b of r.getClientRects()) {
      if (b.width === 0) continue;
      if (b.left < 0 || b.top < 0 || b.right > largura || b.bottom > altura) {
        falhas.push({ tipo: "texto_transbordando", detalhe: `"${trecho}" sai da peça` }); break;
      }
      if (b.left < seguranca || b.top < seguranca || b.right > largura - seguranca || b.bottom > altura - seguranca) {
        falhas.push({ tipo: "fora_da_area_segura", detalhe: `"${trecho}" a menos de ${seguranca}px da borda` }); break;
      }
    }

    // Contraste (WCAG): 3:1 para texto ≥ 24px (ou ≥ 18.66px negrito), 4.5:1 abaixo disso.
    const bg = fundo(el);
    if (bg) {
      const fg = rgb(cs.color);
      const px = parseFloat(cs.fontSize), negrito = Number(cs.fontWeight) >= 700;
      const minimo = px >= 24 || (negrito && px >= 18.66) ? 3 : 4.5;
      const c = contraste(fg, bg);
      if (c < minimo) falhas.push({ tipo: "contraste_baixo", detalhe: `"${trecho}" ${c.toFixed(2)}:1 (mínimo ${minimo}:1, ${px}px)` });
    }
  }

  // Elementos que cortam o próprio conteúdo (overflow escondido).
  for (const el of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(el);
    if (!/(hidden|clip)/.test(cs.overflow + cs.overflowX + cs.overflowY)) continue;
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) {
      if (el.textContent.trim()) falhas.push({ tipo: "texto_transbordando", detalhe: `<${el.tagName.toLowerCase()}> corta o conteúdo ("${el.textContent.trim().slice(0, 40)}")` });
    }
  }
  return { falhas, fontesCarregadas: [...carregadas] };
}

(async () => {
  const o = args();
  fs.mkdirSync(o.saida, { recursive: true });
  const arquivos = fs.readdirSync(o.entrada).filter((f) => /\.(html?|svg)$/i.test(f)).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: o.largura, height: o.altura }, deviceScaleFactor: 1 });
  const relatorio = { gerado_em: new Date().toISOString(), formato: `${o.largura}x${o.altura}`, pecas: {} };
  let total = 0;

  for (const arq of arquivos) {
    const nome = path.parse(arq).name;
    await page.goto("file://" + path.resolve(o.entrada, arq));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    const r = await page.evaluate(inspecionarPagina, o);
    const png = path.join(o.saida, `${nome}.png`);
    await page.screenshot({ path: png, clip: { x: 0, y: 0, width: o.largura, height: o.altura } });
    execFileSync("convert", [png, "-resize", "360x", path.join(o.saida, `${nome}@miniatura.png`)]);
    execFileSync("convert", [png, "-resize", "25%", "-blur", "0x6", "-resize", "400%", path.join(o.saida, `${nome}@desfoque.png`)]);
    // remove duplicatas (mesma falha reportada por vários nós)
    const vistos = new Set();
    r.falhas = r.falhas.filter((f) => { const k = f.tipo + f.detalhe; if (vistos.has(k)) return false; vistos.add(k); return true; });
    relatorio.pecas[nome] = r;
    total += r.falhas.length;
    console.log(`${r.falhas.length ? "✗" : "✓"} ${nome}: ${r.falhas.length} falha(s)`);
    for (const f of r.falhas) console.log(`    ${f.tipo}: ${f.detalhe}`);
  }
  await browser.close();
  relatorio.total_falhas = total;
  fs.writeFileSync(path.join(o.saida, "relatorio.json"), JSON.stringify(relatorio, null, 2));
  process.exit(total ? 1 : 0);
})();
