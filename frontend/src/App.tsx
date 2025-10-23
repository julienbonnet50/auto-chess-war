import { useEffect, useState } from "react";
import { createBattle, getBattle } from "./api/battleApi";
import BattleBoard from "./components/BattleBoard";
import Controls from "./components/Controls";
import type { BattleSummary } from "./types/battle";

function App() {
  const [battleId, setBattleId] = useState<string | null>(null);
  const [battle, setBattle] = useState<BattleSummary | null>(null);

  // Only create the battle once when the app starts
  useEffect(() => {
    const init = async () => {
      if (battleId) return; // don't recreate if we already have an ID

      const id = await createBattle(
        ["Arthur", "Lancelot"],
        ["Mordred", "Morgana"],
        5
      );
      setBattleId(id);

      const b = await getBattle(id);
      setBattle(b);
    };

    init();
  }, [battleId]);

  return (
    <div className="p-4 text-white bg-gray-900 min-h-screen">
      <h1 className="text-xl font-bold mb-4">⚔️ Auto Battler Demo</h1>

      {battle && <BattleBoard battle={battle} />}
      {battleId && (
        <Controls
          battleId={battleId}
          onNextTurn={(data) => setBattle(data.summary)}
        />
      )}
    </div>
  );
}

export default App;
