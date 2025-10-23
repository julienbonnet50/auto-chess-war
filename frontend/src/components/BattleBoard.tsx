import { useEffect, useRef } from "react";
import * as PIXI from "pixi.js";
import type { BattleSummary } from "../types/battle";

interface BattleBoardProps {
  battle: BattleSummary;
}

export default function BattleBoard({ battle }: BattleBoardProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    const app = PIXI.Application.init({
      width: 800,
      height: 400,
      backgroundColor: 0x1e1e1e,
    });

    // Append the canvas to the div
    ref.current.appendChild(app.canvas);

    const style = new PIXI.TextStyle({
      fill: "white",
      fontSize: 14,
    });

    battle.team_a.forEach((bc, i) => {
      const txt = new PIXI.Text(`🛡️ ${bc.character.name}`, style);
      txt.x = 50;
      txt.y = 50 + i * 40;
      app.stage.addChild(txt);
    });

    battle.team_b.forEach((bc, i) => {
      const txt = new PIXI.Text(`⚔️ ${bc.character.name}`, style);
      txt.x = 500;
      txt.y = 50 + i * 40;
      app.stage.addChild(txt);
    });

    return () => {
      app.destroy(true);
    };
  }, [battle]);

  return <div ref={ref} style={{ width: "800px", height: "400px" }} />;
}
