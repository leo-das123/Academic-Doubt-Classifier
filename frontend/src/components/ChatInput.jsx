import { useRef, useState } from "react";
import { ArrowUp } from "lucide-react";

export default function ChatInput({ onAsk, loading }) {
  const [question, setQuestion] = useState("");

  const textareaRef = useRef(null);

  // -----------------------------------------
  // Auto Resize Textarea
  // -----------------------------------------

  function autoResize() {
    const textarea = textareaRef.current;

    if (!textarea) return;

    textarea.style.height = "0px";

    textarea.style.height = `${textarea.scrollHeight}px`;
  }

  // -----------------------------------------
  // Submit
  // -----------------------------------------

  function handleSubmit() {
    const text = question.trim();

    if (!text || loading) return;

    onAsk(text);

    setQuestion("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "24px";
    }
  }

  // -----------------------------------------
  // Keyboard
  // -----------------------------------------

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  }

  // -----------------------------------------
  // Text Change
  // -----------------------------------------

  function handleChange(event) {
    setQuestion(event.target.value);

    autoResize();
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
          ref={textareaRef}

          rows={1}

          value={question}

          placeholder="Ask your academic doubt..."

          onChange={handleChange}

          onKeyDown={handleKeyDown}

          disabled={loading}

          className="
            flex-1

            resize-none

            overflow-y-auto

            max-h-48

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

          disabled={
            loading ||
            !question.trim()
          }

          className="
            flex

            h-11
            w-11

            shrink-0

            items-center
            justify-center

            self-end

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
          <ArrowUp
            size={18}
            strokeWidth={2.5}
          />
        </button>

      </div>

    </div>
  );
}