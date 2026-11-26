# Pesquisa 01 — Geração e edição de imagens publicitárias

Data: 2026-11-26. Feita por agente de pesquisa (busca na web; `bfl.ai`, `huggingface.co` e
`docs.comfy.org` estavam fora da rede permitida para leitura direta, então parte dos dados vem de
trechos de páginas oficiais em buscas). **Confirmar todo preço na página oficial antes de contratar.**

## Conclusões

1. **Nada roda localmente.** PC da Gabriela (GPU integrada, 7,7 GB) e servidor da nuvem (sem GPU,
   15 GB RAM) não comportam os modelos de 2026. ComfyUI em CPU: SDXL leva 10–30 min por imagem;
   FLUX.2/Qwen nem cabem na memória.
2. **Caminho viável: APIs pagas, chamadas pelo Claude Code em nuvem.** Sem GPU própria, sem ComfyUI agora.
3. **Claude não gera fotos/ilustrações raster** (gera SVG/HTML/código). Ele orquestra; um modelo externo gera pixels.
4. **Canva (já pago)**: conta conectada é **Canva Business** (resposta do próprio Canva); geração de imagem
   consome a cota mensal de IA; uso comercial permitido pelos termos. O conector devolve só miniatura
   (160 px) — a imagem em resolução cheia fica no Canva (rota de exportação a testar). Modelo por trás não divulgado.

## Modelos abertos — licença comercial (resumo)

| Modelo | Licença | Uso comercial |
|---|---|---|
| FLUX.1 schnell | Apache 2.0 | livre |
| FLUX.1 dev / Kontext dev | FLUX Non-Commercial | não (modelo) |
| FLUX.2 dev | FLUX Non-Commercial | só com licença paga |
| FLUX.2 klein 4B | Apache 2.0 | livre |
| FLUX 3 Image Klein (out/2026) | FLUX Kommunity | livre abaixo de US$ 5 mi/ano de receita (ler texto) |
| Stable Diffusion 3.5 | Stability Community | livre abaixo de US$ 1 mi/ano |
| SDXL | Open RAIL++-M | permitido com restrições de uso (não verificado no texto oficial) |
| Qwen-Image / Qwen-Image-Edit-2511 | Apache 2.0 | livre; melhor texto dentro da imagem |
| Z-Image Turbo | Apache 2.0 | livre |
| HiDream-I1/E1 | MIT (componentes com licenças próprias) | livre |
| HunyuanImage 3.0 | Tencent Community | condicional; exclui UE/UK/Coreia |

## APIs hospedadas (preço indicativo por imagem)

| Serviço | Preço | Privacidade | Destaque |
|---|---|---|---|
| Google Gemini — Nano Banana Pro | ~US$ 0,134 (1K/2K), 0,24 (4K) | Pago: não treina. **Grátis: treina e há revisão humana — nunca usar com cliente.** SynthID invisível | até 14 imagens de referência (produto, logo, paleta) |
| FLUX.2 pro (BFL ou fal) | ~US$ 0,03–0,06 por 1–2 MP | BFL: direitos comerciais nas saídas; cláusula de treino não verificada | fotorrealismo; edição multi-referência |
| fal.ai (agregador) | por modelo; Qwen-Edit ~US$ 0,03/MP | guarda 30 dias; desligável com `X-Fal-Store-IO: 0` | uma conta dá acesso a FLUX.2, Qwen, Nano Banana |
| Replicate | ~US$ 0,02–0,075 | apaga após 1 h | |
| OpenAI gpt-image-2 | ~US$ 0,01–0,21 | API não treina por padrão | edição com máscara |
| Ideogram | ~US$ 0,03–0,10 | não verificado | tipografia na imagem |
| Recraft | US$ 0,08 (vetor) / 0,30 (pro) | plano pago: privado, direito comercial | **saída SVG editável** |
| Adobe Firefly API | enterprise (~US$ 1.000/mês) | indenização só enterprise | inviável para estúdio de uma pessoa |
| Midjourney | sem API oficial | APIs de terceiros violam os termos | descartado |

GPU alugada para modelos abertos (RunPod ~US$ 0,7–1,1/h; Modal ~US$ 2/h; Comfy Cloud US$ 20+/mês):
só compensa com volume alto, LoRA de produto, ou cliente com sigilo forte (GPU efêmera, apagada depois).

## Recomendação (aguarda decisão de custo da Gabriela)

| Uso | Ferramenta | Custo |
|---|---|---|
| Rascunho, moodboard | Canva generate-image | já pago (cota) |
| Fotografia conceitual/produto | Nano Banana Pro **ou** FLUX.2 pro | US$ 0,03–0,13/img |
| Edição de foto real (fundo, inpainting, luz) | FLUX.2 pro edit / Qwen-Image-Edit (Apache) | ~US$ 0,03–0,05 |
| Recorte | Canva remove-background | já pago |
| Vetores / elementos gráficos | Recraft (SVG) ou SVG/algoritmo do Claude | US$ 0,08–0,30 |

Estimativa para ~100 imagens finais/mês (~400 chamadas): **US$ 20–60/mês (~R$ 120–350)**.
Exige: chave de API (via formulário seguro do ambiente, nunca no chat) e liberação de hosts na rede.

Regras de privacidade propostas: nunca plano gratuito com material de cliente; preferir provedor com
política documentada de não-treino; foto sigilosa só com consentimento e provedor aprovado.

## Pendências não verificadas

Tabela oficial BFL; valor da licença self-serve FLUX.2 dev; preços oficiais gpt-image-2, Ideogram,
Leonardo; cláusulas de treino BFL e fal; termos de saída da API Recraft; VRAM oficial de Qwen e FLUX 3
Klein; modelo por trás do Canva; página oficial da Anthropic sobre geração de imagem.
