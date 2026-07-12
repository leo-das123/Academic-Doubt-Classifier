import { useState } from "react";
import { ArrowUp } from "lucide-react";

export default function ChatInput({ onAsk, loading }) {
  const [question, setQuestion] = useState("");

  function handleSubmit() {
    const text = question.trim();

    if (!text || loading) return;

    onAsk(text);
    setQuestion("");
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  }

  return (
    <div className="border-t border-slate-800 bg-slate-900 p-5">
      <div
        className="
          flex
          items-end
          gap-3

          rounded-2xl

          border
          border-slate-700

          bg-slate-800

          px-5
          py-4

          transition-all
          duration-200

          focus-within:border-cyan-500
          focus-within:ring-2
          focus-within:ring-cyan-500/20
        "
      >
        <textarea
          rows={1}
          value={question}
          placeholder="Ask your academic doubt..."
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          className="
            flex-1

            resize-none

            bg-transparent

            text-white

            placeholder:text-slate-500

            outline-none

            text-[15px]

            leading-6

            disabled:opacity-60
          "
        />

        <button
          onClick={handleSubmit}
          disabled={loading || !question.trim()}
          className="
            flex

            h-11
            w-11

            shrink-0

            items-center
            justify-center

            rounded-full

            bg-cyan-500

            text-white

            transition-all
            duration-200

            hover:scale-105
            hover:bg-cyan-400

            active:scale-95

            disabled:cursor-not-allowed
            disabled:opacity-40
            disabled:hover:scale-100
          "
        >
          <ArrowUp size={18} strokeWidth={2.5} />
        </button>
      </div>
    </div>
  );
}