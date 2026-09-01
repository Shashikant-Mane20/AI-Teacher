export default function Toast({ message, type = 'success', onClose }) {
  if (!message) return null
  const tone = type === 'error' ? 'border-red-400/30 bg-red-500/10 text-red-100' : 'border-emerald-400/30 bg-emerald-500/10 text-emerald-100'
  return <div className={`fixed bottom-6 right-6 z-[60] flex max-w-sm items-center gap-3 rounded-xl border px-4 py-3 text-sm shadow-2xl backdrop-blur-xl ${tone}`} role="status"><span>{type === 'error' ? '!' : '✓'}</span><span className="flex-1">{message}</span><button onClick={onClose} className="text-white/50 hover:text-white" aria-label="Dismiss notification">×</button></div>
}
