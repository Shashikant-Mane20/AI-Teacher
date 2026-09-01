export default function Button({ children, outline = false, onClick, className = '' }) {
  const base = 'rounded-xl px-5 py-3 text-sm font-semibold transition-all active:scale-[.98]'
  const style = outline
    ? 'border border-white/20 text-white/75 hover:border-white/45 hover:text-white'
    : 'bg-gradient-to-r from-[#4f89ff] to-[#7c3aed] text-white shadow-lg shadow-blue-500/20 hover:opacity-90 hover:shadow-blue-500/40'

  return <button onClick={onClick} className={`${base} ${style} ${className}`}>{children}</button>
}
