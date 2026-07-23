export default function ClassificationCard({ result }) {

  const {
    question,
    classification,
    references = [],
    confidence = 0,
  } = result;

  // Remove duplicate page numbers and sort them
  const pages = [
    ...new Set(
      references
        .map((reference) => reference.page)
        .filter((page) => page !== undefined && page !== null)
    ),
  ].sort((a, b) => a - b);

  return (

    <div
      className="
        w-full
        max-w-md

        rounded-2xl

        border
        border-slate-700

        bg-slate-800

        p-8

        shadow-lg
      "
    >

      {/* ---------------- Question ---------------- */}

      <p className="text-sm text-slate-400">
        Question
      </p>

      <h2
        className="
          mt-2
          text-2xl
          font-semibold
          leading-tight
          text-white
        "
      >
        {question}
      </h2>

      <div className="my-6 border-t border-slate-700" />

      {/* ---------------- Classification ---------------- */}

      <div className="space-y-4">

        <InfoRow
          label="Subject"
          value={classification.subject}
        />

        <InfoRow
          label="Topic"
          value={classification.topic}
        />

        <InfoRow
          label="Subtopic"
          value={classification.subtopic || "—"}
        />

        <InfoRow
          label="Difficulty"
          value={classification.difficulty}
        />

        <div className="flex items-center justify-between">

          <span className="text-slate-400">
            Confidence
          </span>

          <span
            className="
              rounded-full

              bg-cyan-500/15

              px-3
              py-1

              text-sm
              font-semibold

              text-cyan-400
            "
          >
            {(confidence * 100).toFixed(0)}%
          </span>

        </div>

      </div>

      <div className="my-6 border-t border-slate-700" />

      {/* ---------------- References ---------------- */}

      <div>

        <p
          className="
            mb-3

            text-sm
            font-medium

            text-slate-400
          "
        >
          References
        </p>

        {

          pages.length === 0 ? (

            <p className="text-sm text-slate-500">

              No references available.

            </p>

          ) : (

            <div className="flex flex-wrap gap-2">

              {

                pages.map((page) => (

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

                      transition

                      hover:border-cyan-400
                      hover:text-cyan-300
                    "

                  >

                    Page {page}

                  </span>

                ))

              }

            </div>

          )

        }

      </div>

    </div>

  );

}

/* ===================================== */

function InfoRow({ label, value }) {

  return (

    <div className="flex items-center justify-between">

      <span className="text-slate-400">

        {label}

      </span>

      <span
        className="
          max-w-[60%]

          text-right

          font-medium

          text-white
        "
      >

        {value || "—"}

      </span>

    </div>

  );

}