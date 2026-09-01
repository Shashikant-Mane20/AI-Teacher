import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Button from './Button'

const links = [
  ['Features', 'features'],
  ['How It Works', 'how-it-works'],
  ['AI Teaching', 'ai-teaching'],
  ['Learning', 'learning-profile'],
]

export default function Navbar({ onAuth }) {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  useEffect(() => { const onScroll = () => setScrolled(window.scrollY > 20); window.addEventListener('scroll', onScroll); return () => window.removeEventListener('scroll', onScroll) }, [])

  return <header className={`fixed top-0 z-40 w-full transition-all ${scrolled ? 'border-b border-white/[.07] bg-[#030b18]/90 backdrop-blur-xl' : ''}`}><div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4"><Link to="/" className="flex items-center gap-2.5"><span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-r from-[#4f89ff] to-[#7c3aed]">✦</span><span className="font-display text-lg font-bold">AI Teacher</span></Link><nav className="hidden gap-7 lg:flex">{links.map(([label, id]) => <a href={`#${id}`} key={id} className="text-sm text-white/50 hover:text-white">{label}</a>)}</nav><div className="hidden items-center gap-4 lg:flex"><button className="text-sm text-white/60 hover:text-white" onClick={() => onAuth('login')}>Sign In</button><Link to="/learn"><Button className="px-4 py-2 text-xs">Start Learning</Button></Link></div><button className="text-2xl text-white/70 lg:hidden" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle menu">{menuOpen ? '×' : '☰'}</button></div>{menuOpen && <div className="border-t border-white/[.07] bg-[#030b18] px-6 py-5 lg:hidden"><div className="flex flex-col gap-4">{links.map(([label, id]) => <a href={`#${id}`} key={id} onClick={() => setMenuOpen(false)} className="text-sm text-white/65">{label}</a>)}<Link to="/learn"><Button onClick={() => setMenuOpen(false)}>Start Learning</Button></Link></div></div>}</header>
}
