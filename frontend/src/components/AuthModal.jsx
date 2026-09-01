import { useState } from 'react'
import Button from './Button'

function Field({ label, placeholder, type = 'text' }) {
  return <label className="block"><span className="mb-1.5 block text-xs text-white/50">{label}</span><input type={type} placeholder={placeholder} className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-white/25 focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20" /></label>
}

export default function AuthModal({ mode, onClose }) {
  const [tab, setTab] = useState(mode)

  return <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
    <div className="absolute inset-0 bg-black/75 backdrop-blur-md" />
    <div className="relative w-full max-w-md rounded-2xl border border-white/10 bg-[#07121f] p-8 shadow-2xl" onClick={(event) => event.stopPropagation()}>
      <button className="absolute right-5 top-4 text-xl text-white/35 hover:text-white" onClick={onClose} aria-label="Close dialog">×</button>
      <div className="mb-7 flex items-center gap-2.5"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-r from-[#4f89ff] to-[#7c3aed]">✦</div><span className="font-display text-lg font-bold">AI Teacher</span></div>
      <div className="mb-6 flex rounded-xl border border-white/10 bg-white/5 p-1">{['login', 'register'].map((item) => <button key={item} onClick={() => setTab(item)} className={`flex-1 rounded-lg py-2 text-sm ${tab === item ? 'bg-gradient-to-r from-[#4f89ff] to-[#7c3aed] text-white' : 'text-white/45'}`}>{item === 'login' ? 'Sign In' : 'Sign Up'}</button>)}</div>
      <div className="space-y-4">{tab === 'register' && <Field label="Full name" placeholder="Your name" />}<Field label="Email" placeholder="you@example.com" type="email" /><Field label="Password" placeholder="••••••••" type="password" /></div>
      <Button className="mt-6 w-full">{tab === 'login' ? 'Sign In ->' : 'Create Account ->'}</Button>
      <p className="mt-5 text-center text-xs text-white/35">{tab === 'login' ? "Don't have an account? " : 'Already have an account? '}<button className="text-blue-400 hover:text-blue-300" onClick={() => setTab(tab === 'login' ? 'register' : 'login')}>{tab === 'login' ? 'Sign up free' : 'Sign in'}</button></p>
    </div>
  </div>
}
