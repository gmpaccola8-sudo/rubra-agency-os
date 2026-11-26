import React from "react";
import { Composition } from "remotion";
import { Atrito } from "./Atrito";
export const Raiz: React.FC = () => (
  <Composition id="Atrito" component={Atrito} durationInFrames={180} fps={30} width={1080} height={1920} />
);
