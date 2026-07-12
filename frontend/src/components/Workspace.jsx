export default function Workspace({ children }) {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6">

     <div
        className="
            w-full
            max-w-[520px]

            h-[93vh]

            rounded-3xl

            bg-slate-900

            border border-slate-800

            shadow-2xl

            overflow-hidden

            flex
            flex-col

            transition-all
            duration-300

            hover:-translate-y-1
            hover:shadow-cyan-500/10
        "
        >
      
        {children}
      </div>

    </div>
  );
}