// Teste de motion 01 — "Atrito" (marca fictícia BRASA). Ver docs/testes/motion-01-brief.md
//
// Cena 3D independente de motor: render(t) é função pura do tempo (determinística),
// então qualquer motor (HyperFrames, Remotion) só precisa chamar render(t) em cada quadro.
// Tudo é procedural e semeado: texturas, faíscas, cintilação. Sem Math.random, sem relógio.

import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

// ── Linha do tempo (segundos). O som é gerado a partir destes mesmos números. ──────────────
export const TEMPOS = {
  duracao: 6.0,
  gavetaInicio: 1.2, gavetaFim: 2.0,
  fosforoSobeInicio: 1.55, fosforoSobeFim: 2.25,
  riscoInicio: 2.3, riscoContato: 2.42, riscoFim: 2.85,
  ignicao: 2.88,
  dollyInicio: 3.2, dollyFim: 4.6,
  mergulhoInicio: 4.6, mergulhoFim: 5.25,
  cartaoInicio: 5.05, cartaoFim: 5.45,
  assinatura: 5.45,
};

// ── Utilidades determinísticas ─────────────────────────────────────────────────────────────
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function hash2(x, y, s = 0) {
  let h = (x * 374761393 + y * 668265263 + s * 2147483647) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
function ruido(x, y, s = 0) { // value noise suave
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const a = hash2(xi, yi, s), b = hash2(xi + 1, yi, s), c = hash2(xi, yi + 1, s), d = hash2(xi + 1, yi + 1, s);
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
}
function fbm(x, y, s = 0, oit = 4) {
  let soma = 0, amp = 0.5, f = 1;
  for (let i = 0; i < oit; i++) { soma += amp * ruido(x * f, y * f, s + i); amp *= 0.5; f *= 2; }
  return soma;
}
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const prog = (t, a, b) => clamp01((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const easeOut = (x) => 1 - Math.pow(1 - x, 3);
const easeIn = (x) => x * x * x;
const smooth = (x) => x * x * (3 - 2 * x);

// ── Texturas procedurais (canvas 2D) ───────────────────────────────────────────────────────
function canvasTextura(tam, pintar, cor = true) {
  const c = document.createElement("canvas");
  c.width = tam[0]; c.height = tam[1];
  const ctx = c.getContext("2d");
  pintar(ctx, c.width, c.height);
  const tx = new THREE.CanvasTexture(c);
  if (cor) tx.colorSpace = THREE.SRGBColorSpace;
  tx.anisotropy = 8;
  return tx;
}
function pixels(ctx, w, h, fn) {
  const img = ctx.createImageData(w, h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const [r, g, b] = fn(x, y);
    const i = (y * w + x) * 4;
    img.data[i] = r; img.data[i + 1] = g; img.data[i + 2] = b; img.data[i + 3] = 255;
  }
  ctx.putImageData(img, 0, 0);
}

function texMadeira() { // nogueira escura, veio irregular
  return canvasTextura([1024, 1024], (ctx, w, h) => pixels(ctx, w, h, (x, y) => {
    const dist = fbm(x * 0.004, y * 0.02, 11) * 18;
    const veio = Math.sin((y * 0.09 + dist) * 1.0) * 0.5 + 0.5;
    const fino = fbm(x * 0.05, y * 0.6, 12, 2);
    const k = 0.55 + 0.25 * Math.pow(veio, 3) + 0.2 * fino;
    return [48 * k + 10, 30 * k + 6, 20 * k + 4];
  }));
}
function texKraft(rotulo, fonte) { // papelão kraft com fibras e impressão gasta
  return canvasTextura([1100, 720], (ctx, w, h) => {
    pixels(ctx, w, h, (x, y) => {
      const n = fbm(x * 0.02, y * 0.02, 21) * 0.5 + fbm(x * 0.3, y * 0.3, 22, 2) * 0.5;
      return [156 + 40 * n, 112 + 32 * n, 74 + 22 * n];
    });
    const rnd = mulberry32(7);
    ctx.globalAlpha = 0.18;
    for (let i = 0; i < 2600; i++) { // fibras
      const x = rnd() * w, y = rnd() * h, a = rnd() * Math.PI, l = 4 + rnd() * 14;
      ctx.strokeStyle = rnd() > 0.5 ? "#5e3f22" : "#e2c39a";
      ctx.lineWidth = 0.6 + rnd();
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); ctx.stroke();
    }
    ctx.globalAlpha = 1;
    if (rotulo) {
      ctx.fillStyle = "#2a120c";
      ctx.textAlign = "center";
      ctx.font = `900 250px ${fonte}`;
      ctx.fillText("BRASA", w / 2, h * 0.56);
      ctx.font = `600 34px ${fonte}`;
      ctx.fillText("FÓSFOROS FEITOS À MÃO · 40", w / 2, h * 0.78);
      ctx.fillRect(w * 0.12, h * 0.17, w * 0.76, 5);
      ctx.fillRect(w * 0.12, h * 0.86, w * 0.76, 5);
      ctx.globalCompositeOperation = "destination-out"; // tinta gasta
      for (let i = 0; i < 9000; i++) {
        ctx.globalAlpha = 0.05 + rnd() * 0.35;
        ctx.beginPath(); ctx.arc(rnd() * w, rnd() * h, rnd() * 2.2, 0, 7); ctx.fill();
      }
      ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = 1;
      // repinta o kraft onde a tinta "saiu" (destination-out deixou transparente)
      ctx.globalCompositeOperation = "destination-over";
      ctx.fillStyle = "#a9805a"; ctx.fillRect(0, 0, w, h);
      ctx.globalCompositeOperation = "source-over";
    }
  });
}
function texLixa() {
  return canvasTextura([512, 128], (ctx, w, h) => pixels(ctx, w, h, (x, y) => {
    const g = hash2(x, y, 31), n = fbm(x * 0.05, y * 0.05, 32, 2);
    const k = 0.5 + 0.35 * n + (g > 0.93 ? 0.6 : 0);
    return [58 * k, 36 * k, 28 * k];
  }));
}
function texPalito() {
  return canvasTextura([256, 32], (ctx, w, h) => pixels(ctx, w, h, (x, y) => {
    const k = 0.85 + 0.15 * fbm(x * 0.08, y * 0.5, 41, 2);
    return [226 * k, 196 * k, 150 * k];
  }));
}

// ── Chama (shader) ─────────────────────────────────────────────────────────────────────────
const chamaVert = `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`;
const chamaFrag = `
varying vec2 vUv; uniform float uT; uniform float uForca;
float h(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7))) * 43758.5453); }
float n(vec2 p){ vec2 i=floor(p), f=fract(p); vec2 u=f*f*(3.-2.*f);
  return mix(mix(h(i),h(i+vec2(1,0)),u.x), mix(h(i+vec2(0,1)),h(i+vec2(1,1)),u.x), u.y); }
void main(){
  float y = vUv.y; float x = vUv.x - 0.5;
  float turb = (n(vec2(y*3.0 - uT*5.0, uT*1.7)) - 0.5) * 0.22 * y;
  x += turb;
  float larg = 0.38 * pow(sin(3.14159 * pow(clamp(y,0.0,1.0), 0.55)), 1.2) * (1.0 - 0.35*y) + 0.001;
  float corpo = smoothstep(larg, larg*0.15, abs(x)) * smoothstep(1.0, 0.55, y) * smoothstep(0.0, 0.10, y);
  float nucleo = smoothstep(larg*0.55, 0.0, abs(x)) * smoothstep(0.75, 0.2, y) * smoothstep(0.05,0.2,y);
  float azul = smoothstep(0.28, 0.06, y) * smoothstep(larg, larg*0.4, abs(x));
  vec3 cor = mix(vec3(0.9,0.22,0.03), vec3(1.0,0.62,0.18), corpo);
  cor = mix(cor, vec3(1.0,0.93,0.75), nucleo);
  cor = mix(cor, vec3(0.25,0.45,1.0), azul*0.6);
  float a = clamp(corpo*0.9 + nucleo, 0.0, 1.0) * uForca;
  gl_FragColor = vec4(cor * a * 2.2, a);
}`;

// ── Brasa do cartão final (shader sobre a máscara de texto) ────────────────────────────────
const brasaFrag = `
varying vec2 vUv; uniform sampler2D uMascara; uniform float uT; uniform float uAcende;
float h(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7))) * 43758.5453); }
float n(vec2 p){ vec2 i=floor(p), f=fract(p); vec2 u=f*f*(3.-2.*f);
  return mix(mix(h(i),h(i+vec2(1,0)),u.x), mix(h(i+vec2(0,1)),h(i+vec2(1,1)),u.x), u.y); }
void main(){
  float m = texture2D(uMascara, vUv).r;
  float pulso = n(vUv*vec2(18.0,6.0) + vec2(uT*0.6, -uT*0.9))*0.6 + n(vUv*vec2(60.0,20.0) - uT*1.3)*0.4;
  float calor = clamp(pulso * 1.35 * uAcende, 0.0, 1.0);
  vec3 cor = mix(vec3(0.10,0.015,0.0), vec3(0.85,0.16,0.02), smoothstep(0.15,0.6,calor));
  cor = mix(cor, vec3(1.0,0.62,0.2), smoothstep(0.6,0.95,calor));
  gl_FragColor = vec4(cor * m * (0.6 + 1.6*calor), m);
}`;

// ── Grão + vinheta (pós) ───────────────────────────────────────────────────────────────────
const graoShader = {
  uniforms: { tDiffuse: { value: null }, uSemente: { value: 0 }, uVinheta: { value: 1.0 } },
  vertexShader: chamaVert,
  fragmentShader: `varying vec2 vUv; uniform sampler2D tDiffuse; uniform float uSemente; uniform float uVinheta;
    float h(vec2 p){ return fract(sin(dot(p + uSemente, vec2(12.9898,78.233))) * 43758.5453); }
    void main(){ vec4 c = texture2D(tDiffuse, vUv);
      vec2 d = vUv - 0.5; d.x *= 0.5625;
      float v = 1.0 - uVinheta * smoothstep(0.25, 0.75, length(d));
      float g = (h(vUv*vec2(1080.,1920.)) - 0.5) * 0.035;
      gl_FragColor = vec4(c.rgb * v + g, c.a); }`,
};

// ── Construção da cena ─────────────────────────────────────────────────────────────────────
export async function criarCena(canvas, { largura = 1080, altura = 1920, fonteUrl } = {}) {
  let fonte = "serif";
  if (fonteUrl) {
    const ff = new FontFace("Fraunces", `url(${fonteUrl})`, { weight: "900" });
    await ff.load(); document.fonts.add(ff); fonte = "Fraunces";
  }

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(largura, altura, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const cena = new THREE.Scene();
  cena.background = new THREE.Color(0x030202);
  cena.fog = new THREE.Fog(0x030202, 22, 48);
  const camera = new THREE.PerspectiveCamera(36, largura / altura, 0.05, 200);

  // Mesa
  const madeira = texMadeira(); madeira.wrapS = madeira.wrapT = THREE.RepeatWrapping; madeira.repeat.set(10, 10);
  const mesa = new THREE.Mesh(new THREE.PlaneGeometry(400, 400),
    new THREE.MeshStandardMaterial({ map: madeira, roughness: 0.62, metalness: 0, bumpMap: madeira, bumpScale: 0.6 }));
  mesa.rotation.x = -Math.PI / 2; mesa.receiveShadow = true; cena.add(mesa);

  // Caixa: luva (4 paredes) + gaveta
  const L = 5.5, A = 1.6, P = 3.6, E = 0.05;
  const kraftRotulo = texKraft(true, fonte), kraftLiso = texKraft(false, fonte), lixa = texLixa();
  const matKraft = new THREE.MeshStandardMaterial({ map: kraftLiso, roughness: 0.9, bumpMap: kraftLiso, bumpScale: 0.3 });
  const matRotulo = new THREE.MeshStandardMaterial({ map: kraftRotulo, roughness: 0.88, bumpMap: kraftRotulo, bumpScale: 0.3 });
  const matLixa = new THREE.MeshStandardMaterial({ map: lixa, roughness: 1.0, bumpMap: lixa, bumpScale: 1.2 });
  const luva = new THREE.Group();
  const caixaParede = (w, h, d, mats) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mats); m.castShadow = m.receiveShadow = true; return m; };
  const topo = caixaParede(L, E, P, [matKraft, matKraft, matRotulo, matKraft, matKraft, matKraft]); topo.position.y = A - E / 2;
  const fundo = caixaParede(L, E, P, matKraft); fundo.position.y = E / 2;
  const frente = caixaParede(L, A, E, [matKraft, matKraft, matKraft, matKraft, matLixa, matKraft]); frente.position.set(0, A / 2, P / 2 - E / 2);
  const tras = caixaParede(L, A, E, [matKraft, matKraft, matKraft, matKraft, matKraft, matLixa]); tras.position.set(0, A / 2, -P / 2 + E / 2);
  luva.add(topo, fundo, frente, tras);
  cena.add(luva);

  const gaveta = new THREE.Group();
  const matInterno = new THREE.MeshStandardMaterial({ color: 0xd8c4a4, roughness: 0.95 });
  const gl = L - 0.12, ga = A - 2 * E - 0.04, gp = P - 2 * E - 0.04, ge = 0.035;
  const gFundo = caixaParede(gl, ge, gp, matInterno); gFundo.position.y = E + ge / 2 + 0.01;
  const gF = caixaParede(gl, ga, ge, matInterno); gF.position.set(0, E + ga / 2, gp / 2 - ge / 2);
  const gT = caixaParede(gl, ga, ge, matInterno); gT.position.set(0, E + ga / 2, -gp / 2 + ge / 2);
  const gE = caixaParede(ge, ga, gp, matInterno); gE.position.set(-gl / 2 + ge / 2, E + ga / 2, 0);
  const gD = caixaParede(ge, ga, gp, matKraft); gD.position.set(gl / 2 - ge / 2, E + ga / 2, 0);
  gaveta.add(gFundo, gF, gT, gE, gD);
  luva.add(gaveta);

  // Fósforos
  const palito = texPalito();
  const matPalito = new THREE.MeshStandardMaterial({ map: palito, roughness: 0.8 });
  const matCabeca = new THREE.MeshStandardMaterial({ color: 0x6e1a10, roughness: 0.75, bumpMap: lixa, bumpScale: 0.4 });
  const comp = 4.6, esp = 0.16;
  function fosforo() {
    const g = new THREE.Group();
    const s = new THREE.Mesh(new THREE.BoxGeometry(comp, esp, esp), matPalito);
    const c = new THREE.Mesh(new THREE.SphereGeometry(0.17, 20, 16), matCabeca);
    c.scale.set(1.5, 1.05, 1.05); c.position.x = comp / 2 + 0.08;
    s.castShadow = c.castShadow = true; s.receiveShadow = true;
    g.add(s, c); return g;
  }
  const rnd = mulberry32(99);
  const ocupantes = [];
  for (let fila = 0; fila < 2; fila++) for (let i = 0; i < 9; i++) {
    const f = fosforo();
    f.position.set(0.15 + (rnd() - 0.5) * 0.1, E + ge + 0.1 + fila * 0.17, -gp / 2 + 0.25 + i * 0.36 + fila * 0.12);
    f.rotation.y = (rnd() - 0.5) * 0.03;
    gaveta.add(f); ocupantes.push(f);
  }
  const heroi = fosforo(); cena.add(heroi);
  const heroiInicio = new THREE.Vector3(0.15, E + ge + 0.1 + 0.34, 0.55);

  // Chama
  const matChama = new THREE.ShaderMaterial({
    vertexShader: chamaVert, fragmentShader: chamaFrag, transparent: true, depthWrite: false,
    blending: THREE.AdditiveBlending, uniforms: { uT: { value: 0 }, uForca: { value: 0 } },
  });
  const chama = new THREE.Mesh(new THREE.PlaneGeometry(1.15, 1.9), matChama);
  chama.geometry.translate(0, 0.95 - 0.12, 0);
  cena.add(chama);

  // Faíscas: trajetórias calculadas uma vez (física simples), lidas em t
  const NF = 70, faiscas = [];
  const rf = mulberry32(2024);
  for (let i = 0; i < NF; i++) {
    faiscas.push({ t0: TEMPOS.riscoContato + 0.12 + rf() * 0.42, vida: 0.15 + rf() * 0.35,
      v: new THREE.Vector3((rf() - 0.2) * 9, rf() * 7 + 1, (rf() - 0.2) * 6) });
  }
  const geoF = new THREE.BufferGeometry();
  const posF = new Float32Array(NF * 3), corF = new Float32Array(NF * 3);
  geoF.setAttribute("position", new THREE.BufferAttribute(posF, 3));
  geoF.setAttribute("color", new THREE.BufferAttribute(corF, 3));
  const pontos = new THREE.Points(geoF, new THREE.PointsMaterial({ size: 0.07, vertexColors: true,
    blending: THREE.AdditiveBlending, transparent: true, depthWrite: false }));
  cena.add(pontos);

  // Luzes
  const ambiente = new THREE.HemisphereLight(0x2a3346, 0x0a0604, 0.05); cena.add(ambiente);
  // Recorte frio por trás e rasante: desenha a borda da caixa, ilumina pouco a mesa
  const contra = new THREE.SpotLight(0x8fb0ff, 320, 40, 0.2, 0.7, 1.6);
  contra.position.set(-3, 2.4, -15); contra.target.position.set(0.5, 1.4, 0); cena.add(contra, contra.target);
  const luzChama = new THREE.PointLight(0xff9a40, 0, 40, 1.6);
  luzChama.castShadow = true; luzChama.shadow.mapSize.set(1024, 1024); luzChama.shadow.bias = -0.002;
  luzChama.shadow.radius = 6; cena.add(luzChama);
  // Luz do atrito: as faíscas da lixa iluminam a própria lixa (luz motivada pela ação)
  const luzAtrito = new THREE.PointLight(0xffb070, 0, 6, 2); cena.add(luzAtrito);

  // Cartão final (cena própria, revelada pela luz da chama)
  const cenaCartao = new THREE.Scene();
  const camCartao = new THREE.OrthographicCamera(-0.5625, 0.5625, 1, -1, 0.1, 10); camCartao.position.z = 2;
  const mascara = canvasTextura([1600, 600], (ctx, w, h) => {
    ctx.fillStyle = "#000"; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = "#fff"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.font = `900 360px ${fonte}`; ctx.fillText("BRASA", w / 2, h * 0.52);
  }, false);
  const matBrasa = new THREE.ShaderMaterial({ vertexShader: chamaVert, fragmentShader: brasaFrag, transparent: true,
    uniforms: { uMascara: { value: mascara }, uT: { value: 0 }, uAcende: { value: 0 } } });
  const palavra = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 0.375), matBrasa); palavra.position.y = 0.08;
  const assinaturaTx = canvasTextura([1400, 160], (ctx, w, h) => {
    ctx.fillStyle = "#f3dcc0"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.font = `600 74px ${fonte}`; ctx.fillText("Toda ideia começa no atrito.", w / 2, h / 2);
  });
  const matAss = new THREE.MeshBasicMaterial({ map: assinaturaTx, transparent: true, opacity: 0 });
  const assinatura = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 0.114), matAss); assinatura.position.y = -0.17;
  // Fundo do cartão: o brilho remanescente da chama (radial), que se apaga e deixa a brasa
  const matHalo = new THREE.ShaderMaterial({ vertexShader: chamaVert, depthWrite: false,
    uniforms: { uBrilho: { value: 1 } },
    fragmentShader: `varying vec2 vUv; uniform float uBrilho;
      void main(){ vec2 d = vUv - vec2(0.5, 0.52); d.x *= 0.5625;
        float r = length(d); float halo = exp(-r*r*mix(7.0, 30.0, 1.0-uBrilho));
        vec3 quente = vec3(1.0, 0.72, 0.42); vec3 escuro = vec3(0.027, 0.012, 0.008);
        gl_FragColor = vec4(mix(escuro, quente, halo * uBrilho), 1.0); }` });
  const halo = new THREE.Mesh(new THREE.PlaneGeometry(1.125, 2), matHalo); halo.position.z = -1;
  cenaCartao.add(halo, palavra, assinatura);

  // Pós-produção
  const composer = new EffectComposer(renderer);
  composer.setSize(largura, altura);
  const passoCena = new RenderPass(cena, camera);
  const bloom = new UnrealBloomPass(new THREE.Vector2(largura, altura), 0.6, 0.55, 0.82);
  const grao = new ShaderPass(graoShader);
  composer.addPass(passoCena); composer.addPass(bloom); composer.addPass(new OutputPass()); composer.addPass(grao);

  const ondeAcende = new THREE.Vector3();

  function render(t) {
    const T = TEMPOS;
    // Gaveta desliza (inércia: acelera e assenta)
    const g = easeInOut(prog(t, T.gavetaInicio, T.gavetaFim));
    gaveta.position.x = g * 2.7;

    // Herói: coreografado pela CABEÇA do fósforo (o que o olho acompanha).
    // Fases: repouso na gaveta → arco até a lixa → risco acelerando → sobe aceso para o vazio do quadro.
    const OFF = new THREE.Vector3(comp / 2 + 0.08, 0, 0);       // cabeça no eixo local do fósforo
    const hRepouso = heroiInicio.clone().add(OFF).add(new THREE.Vector3(gaveta.position.x, 0, 0));
    const hPre = new THREE.Vector3(-2.5, 1.4, P / 2 + 0.95);
    const hC1 = new THREE.Vector3(-2.45, 0.78, P / 2 + 0.2);       // encosta na lixa (frente da caixa)
    const hC2 = new THREE.Vector3(2.35, 0.92, P / 2 + 0.2);
    const hAlto = new THREE.Vector3(1.0, 6.2, P / 2 + 1.2);
    const cab = new THREE.Vector3(); let yaw = 0, roll = 0;
    if (t < T.fosforoSobeInicio) { cab.copy(hRepouso); }
    else if (t < T.riscoInicio) {
      const k = easeInOut(prog(t, T.fosforoSobeInicio, T.riscoInicio));
      cab.lerpVectors(hRepouso, hPre, k); cab.y += Math.sin(k * Math.PI) * 1.6;
      yaw = lerp(0, 0.28, k); roll = lerp(0, 0.15, k);
    } else if (t < T.riscoContato) {
      const k = easeOut(prog(t, T.riscoInicio, T.riscoContato));
      cab.lerpVectors(hPre, hC1, k); yaw = 0.28; roll = lerp(0.15, -0.06, k);
    } else if (t < T.riscoFim) {
      const k = easeIn(prog(t, T.riscoContato, T.riscoFim));    // acelera: o atrito "pega"
      cab.lerpVectors(hC1, hC2, k); yaw = 0.28; roll = -0.06 + k * 0.08;
    } else {
      const k = easeInOut(prog(t, T.riscoFim, T.riscoFim + 0.95));
      cab.lerpVectors(hC2, hAlto, k); cab.z += Math.sin(k * Math.PI) * 0.8;
      yaw = lerp(0.28, 0.05, k); roll = lerp(0.02, 1.15, k);  // ergue a cabeça: a chama sobe
    }
    heroi.rotation.set(0, yaw, roll);
    heroi.updateMatrixWorld(true);
    const offMundo = OFF.clone().applyEuler(heroi.rotation);
    heroi.position.copy(cab).sub(offMundo);
    heroi.children[1].getWorldPosition(ondeAcende);

    // Chama: nasce na ignição, estabiliza, cresce no mergulho
    const nasce = smooth(prog(t, T.ignicao, T.ignicao + 0.35));
    const flash = Math.exp(-Math.max(0, t - T.ignicao) * 9) * (t >= T.ignicao ? 1 : 0);
    const cresce = easeIn(prog(t, T.mergulhoInicio, T.mergulhoFim));
    const cint = 1 + 0.12 * Math.sin(t * 23.1 + 1.3) + 0.08 * Math.sin(t * 37.7 + 0.4) + 0.05 * Math.sin(t * 71.3 + 2.2);
    matChama.uniforms.uT.value = t;
    matChama.uniforms.uForca.value = nasce * (1 + 0.6 * flash);
    chama.position.copy(ondeAcende);
    chama.scale.setScalar((0.35 + 0.65 * nasce) * (1 + flash * 0.5) * (1 + cresce * 5));
    chama.rotation.y = Math.atan2(camera.position.x - chama.position.x, camera.position.z - chama.position.z);
    luzChama.position.copy(ondeAcende).add(new THREE.Vector3(0, 0.6, 0));
    luzChama.intensity = (nasce * 38 * cint + flash * 140) * (1 + cresce * 3);

    // Atrito: crepita enquanto a cabeça corre na lixa, mais forte perto da ignição
    const atrito = t >= T.riscoContato && t < T.ignicao + 0.05 ? prog(t, T.riscoContato, T.ignicao) : 0;
    const crepita = 0.55 + 0.45 * Math.abs(Math.sin(t * 157.3) * Math.sin(t * 91.7 + 0.6));
    luzAtrito.position.copy(ondeAcende).add(new THREE.Vector3(0, 0.1, 0.35));
    luzAtrito.intensity = atrito > 0 ? (0.6 + 6 * atrito * atrito) * crepita : 0;

    // Faíscas
    for (let i = 0; i < NF; i++) {
      const f = faiscas[i], dt = t - f.t0, vivo = dt >= 0 && dt < f.vida;
      const p = vivo ? ondeAcende.clone().addScaledVector(f.v, dt * 0.35).add(new THREE.Vector3(0, -4.9 * dt * dt * 0.35, 0)) : ondeAcende;
      posF.set([p.x, p.y, p.z], i * 3);
      const k = vivo ? 1 - dt / f.vida : 0;
      corF.set([1.0 * k * 2, 0.55 * k * 2, 0.15 * k], i * 3);
    }
    geoF.attributes.position.needsUpdate = true; geoF.attributes.color.needsUpdate = true;

    // Câmera: parada → acompanha a chama subindo (tilt) → dolly-in → mergulho na luz
    const camIni = new THREE.Vector3(4.5, 11.5, 20.5), alvoIni = new THREE.Vector3(0.3, 1.6, 0.6);
    const segue = easeInOut(prog(t, T.riscoFim, T.dollyFim));
    const alvoChama = ondeAcende.clone().add(new THREE.Vector3(0, 0.6, 0));
    const alvo = new THREE.Vector3().lerpVectors(alvoIni, alvoChama, segue * 0.75);
    const d = easeInOut(prog(t, T.dollyInicio, T.dollyFim));
    const camPos = new THREE.Vector3().lerpVectors(camIni, hAlto.clone().add(new THREE.Vector3(1.4, 0.4, 7.5)), d);
    const mergulho = easeIn(prog(t, T.mergulhoInicio, T.mergulhoFim));
    camPos.lerp(alvoChama.clone().add(new THREE.Vector3(0.05, 0.1, 1.3)), mergulho * 0.9);
    alvo.lerp(alvoChama, Math.max(d, mergulho));
    const respira = Math.sin(t * 0.9) * 0.05; // câmera "na mão", quase imperceptível
    camera.position.copy(camPos).add(new THREE.Vector3(respira, respira * 0.6, 0));
    camera.lookAt(alvo);

    renderer.toneMappingExposure = 1.0 + cresce * 1.6;
    bloom.strength = 0.55 + flash * 1.2 + cresce * 2.2;
    grao.uniforms.uSemente.value = Math.floor(t * 30) * 0.137;
    grao.uniforms.uVinheta.value = 0.9 - cresce * 0.5;

    // Cartão: a luz da chama vira a brasa da palavra
    const c = smooth(prog(t, T.cartaoInicio, T.cartaoFim));
    matBrasa.uniforms.uT.value = t;
    matBrasa.uniforms.uAcende.value = smooth(prog(t, T.cartaoInicio + 0.1, T.duracao - 0.2)) * 0.8 + 0.2;
    matAss.opacity = smooth(prog(t, T.assinatura, T.assinatura + 0.4));
    if (c <= 0) {
      passoCena.scene = cena; passoCena.camera = camera;
    } else {
      passoCena.scene = cenaCartao; passoCena.camera = camCartao;
      renderer.toneMappingExposure = lerp(1.0 + cresce * 1.6, 1.0, c);
      bloom.strength = lerp(bloom.strength, 0.9, c);
      // brilho residual da chama dissolvendo sobre o cartão
      matHalo.uniforms.uBrilho.value = 1 - smooth(prog(t, T.cartaoInicio + 0.15, T.assinatura + 0.2));
    }
    composer.render();
  }

  await renderer.compileAsync(cena, camera);
  await renderer.compileAsync(cenaCartao, camCartao);
  // Quadro descartável: o primeiro desenho de um renderer difere dos seguintes (aquecimento).
  render(0); render(TEMPOS.duracao - 0.5); render(0);
  return { render, TEMPOS };
}
