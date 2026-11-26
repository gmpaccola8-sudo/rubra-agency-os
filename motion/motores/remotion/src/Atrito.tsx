import React, { useEffect, useRef, useState } from "react";
import { AbsoluteFill, Audio, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
// @ts-ignore — módulo JS compartilhado com o HyperFrames (mesma cena, mesmo código)
import { criarCena } from "./cena.js";

export const Atrito: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const canvas = useRef<HTMLCanvasElement>(null);
  const cena = useRef<{ render: (t: number) => void } | null>(null);
  const [handle] = useState(() => delayRender("montando a cena 3D"));
  const [pronta, setPronta] = useState(false);

  useEffect(() => {
    criarCena(canvas.current, { largura: width, altura: height, fonteUrl: staticFile("fraunces-900.woff2") })
      .then((c: any) => { cena.current = c; setPronta(true); continueRender(handle); });
  }, []);

  useEffect(() => { if (pronta && cena.current) cena.current.render(frame / fps); }, [frame, pronta]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#030202" }}>
      <canvas ref={canvas} width={width} height={height} style={{ width, height }} />
      <Audio src={staticFile("som.wav")} />
    </AbsoluteFill>
  );
};
