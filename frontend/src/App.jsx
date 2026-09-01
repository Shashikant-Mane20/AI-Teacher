import { useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import AuthModal from './components/AuthModal'
import Button from './components/Button'
import HeroSection from './components/HeroSection'
import Navbar from './components/Navbar'
import { AdaptiveTeaching, HowItWorks, LearningProfile, Multilingual } from './components/LandingSections'
import ProfileDashboard from './components/ProfileDashboard'

function Home({ openAuth }) {
  return <><HeroSection onAuth={openAuth} /><HowItWorks /><AdaptiveTeaching /><LearningProfile /><Multilingual /><section className="relative overflow-hidden py-28 text-center"><div className="absolute inset-0 bg-gradient-to-b from-transparent via-blue-600/[.07] to-transparent" /><div className="relative mx-auto max-w-3xl px-6"><div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-r from-[#4f89ff] to-[#7c3aed] text-3xl">✦</div><h2 className="font-display text-5xl font-bold lg:text-6xl">Stop studying alone.</h2><p className="mx-auto mt-5 max-w-xl text-lg text-white/45">Bring your learning material. Choose your goal. Meet your AI Teacher.</p><Button onClick={() => openAuth('register')} className="mt-8 px-9 py-4 text-base">Start Learning →</Button></div></section><footer className="border-t border-white/[.06] py-10"><div className="mx-auto flex max-w-7xl flex-col justify-between gap-4 px-6 text-xs text-white/30 sm:flex-row"><span>AI Teacher · Personalized learning powered by AI.</span><span>© 2026 AI Teacher</span></div></footer></>
}

function LearnPage() { return <ProfileDashboard /> }

export default function App() {
  const [authModal, setAuthModal] = useState(null)
  return <BrowserRouter><div className="min-h-screen overflow-x-hidden bg-[#030b18] text-[#e8edf8]"><Navbar onAuth={setAuthModal} /><Routes><Route path="/" element={<Home openAuth={setAuthModal} />} /><Route path="/learn" element={<LearnPage />} /></Routes>{authModal && <AuthModal mode={authModal} onClose={() => setAuthModal(null)} onAuthenticated={() => { setAuthModal(null); window.location.href = '/learn' }} />}</div></BrowserRouter>
}
