import { nextTurn } from "../api/battleApi";

interface ControlsProps {
  battleId: string;
  onNextTurn: (data: any) => void;
}

export default function Controls({ battleId, onNextTurn }: ControlsProps) {
  const handleNextTurn = async () => {
    const data = await nextTurn(battleId);
    onNextTurn(data);
  };

  return (
    <div className="flex gap-2 mt-4">
      <button onClick={handleNextTurn} className="bg-blue-600 text-white px-4 py-2 rounded-lg">
        Next Turn
      </button>
    </div>
  );
}
