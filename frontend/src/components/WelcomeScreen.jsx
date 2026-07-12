import { Brain } from "lucide-react";

export default function WelcomeScreen() {
  return (
    <div className="flex h-full flex-col items-center justify-center px-8 text-center">

      <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-cyan-500/10 border border-cyan-500/20">
        <Brain className="h-8 w-8 text-cyan-400" />
      </div>

      <h2 className="text-2xl font-bold text-white">
        Welcome
      </h2>

      <p className="mt-4 max-w-md text-sm leading-7 text-slate-400">
        Classify your academic questions into
        <span className="text-white"> Subject</span>,
        <span className="text-white"> Topic</span>,
        <span className="text-white"> Subtopic</span>,
        and
        <span className="text-white"> Difficulty</span>
        using Retrieval-Augmented Generation.
      </p>

      <p className="mt-8 text-sm text-slate-500">
        Ask your first academic doubt below.
      </p>

    </div>
  );
}