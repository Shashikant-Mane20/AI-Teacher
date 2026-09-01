import { useState } from 'react'
import Button from './Button'
import { api } from '../api'

function Field({ label, placeholder, type = 'text', value, onChange }) {
  return <label className="block"><span className="mb-1.5 block text-xs text-white/50">{label}</span><input required type={type} value={value} onChange={(event) => onChange(event.target.value)} placeholder={placeholder} className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-white/25 focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20" /></label>
}

export default function AuthModal({ mode, onClose, onAuthenticated }) {
  const [tab, setTab] = useState(mode)
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const update = (field, value) => setForm((current) => ({ ...current, [field]: value }))
  const submit = async (event) => {
    event.preventDefault(); setLoading(true); setError('')
    try {
      const result = tab === 'login' ? await api.login({ email: form.email, password: form.password }) : await api.register(form)
      localStorage.setItem('ai_teacher_token', result.access_token)
      onAuthenticated(result)
    } catch (requestError) { setError(requestError.message) } finally { setLoading(false) }
  }

  return <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}><div className="absolute inset-0 bg-black/75 backdrop-blur-md" /><div className="relative w-full max-w-md rounded-2xl border border-white/10 bg-[#07121f] p-8 shadow-2xl" onClick={(event) => event.stopPropagation()}><button className="absolute right-5 top-4 text-xl text-white/35 hover:text-white" onClick={onClose} aria-label="Close dialog">×</button><div className="mb-7 flex items-center gap-2.5"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-r from-[#4f89ff] to-[#7c3aed]">✦</div><span className="font-display text-lg font-bold">AI Teacher</span></div><div className="mb-6 flex rounded-xl border border-white/10 bg-white/5 p-1">{['login', 'register'].map((item) => <button key={item} onClick={() => setTab(item)} className={`flex-1 rounded-lg py-2 text-sm ${tab === item ? 'bg-gradient-to-r from-[#4f89ff] to-[#7c3aed] text-white' : 'text-white/45'}`}>{item === 'login' ? 'Sign In' : 'Sign Up'}</button>)}</div><form className="space-y-4" onSubmit={submit}>{tab === 'register' && <Field label="Full name" placeholder="Your name" value={form.name} onChange={(value) => update('name', value)} />}<Field label="Email" placeholder="you@example.com" type="email" value={form.email} onChange={(value) => update('email', value)} /><Field label="Password" placeholder="••••••••" type="password" value={form.password} onChange={(value) => update('password', value)} /><Button className="mt-2 w-full" disabled={loading}>{loading ? 'Working...' : tab === 'login' ? 'Sign In ->' : 'Create Account ->'}</Button></form>{error && <p className="mt-3 text-center text-xs text-red-300">{error}</p>}<p className="mt-5 text-center text-xs text-white/35">{tab === 'login' ? "Don't have an account? " : 'Already have an account? '}<button className="text-blue-400 hover:text-blue-300" onClick={() => setTab(tab === 'login' ? 'register' : 'login')}>{tab === 'login' ? 'Sign up free' : 'Sign in'}</button></p></div></div>
}
