export default function ClassificationCard({ result }) {
  const { question, classification, references } = result;

  // Remove duplicate pages
  const pages = [...new Set(
  references.map((ref) => ref.page)
)].sort((a, b) => a - b);

  return (
    <div
      className="
        w-full
        max-w-md

        rounded-2xl

        border
        border-slate-700

        bg-slate-800

        p-6

        shadow-lg
      "
    >
      {/* Question */}
      <p className="text-sm text-slate-400">
            Question
        </p>

        <h2 className="mt-1 text-2xl font-semibold text-white leading-tight">
            {question}
        </h2>

      <div className="my-4 border-t border-slate-700" />

      {/* Classification */}
      <div className="space-y-3">

        <div className="flex justify-between">
          <span className="text-slate-400">Subject</span>
          <span className="font-medium text-white">
            {classification.subject}
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">Topic</span>
          <span className="font-medium text-white">
            {classification.topic || "—"}
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">Subtopic</span>
          <span className="font-medium text-white">
            {classification.subtopic || "—"}
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">Difficulty</span>
          <span className="font-medium text-white">
            {classification.difficulty}
          </span>
        </div>

        <div className="flex justify-between items-center">
        <span className="text-slate-400">
            Confidence
        </span>

        <span
            className="
            rounded-full
            bg-cyan-500/15
            px-2.5
            py-0.5
            text-sm
            font-semibold
            text-cyan-400
            "
        >
            {(classification.confidence * 100).toFixed(0)}%
        </span>
        </div>

      </div>

      <div className="my-6 border-t border-slate-700" />

      {/* References */}
      <div>

        <p className="mb-2 text-sm font-medium text-slate-400">
          References
        </p>

        <div className="flex flex-wrap gap-1">

          {pages.map((page) => (
            <span
              key={page}
              className="
                rounded-full

                border
                border-slate-600

                bg-slate-900

                px-3
                py-1

                text-xs

                text-slate-300
              "
            >
              Page {page}
            </span>
          ))}

        </div>

      </div>
    </div>
  );
}