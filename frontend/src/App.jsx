import { useEffect, useRef, useState } from 'react'
import { api, openLessonSocket } from './api'
import './App.css'

const initialLesson = {
  topic: "Ohm's Law",
  learner_level: 'beginner',
  language: 'en',
  available_time_minutes: 30,
  learning_goal: 'Understand voltage, current, and resistance.',
  teaching_style: 'simple',
}

function App() {
  const [lesson, setLesson] = useState(initialLesson)
  const [lessonData, setLessonData] = useState(null)
  const [question, setQuestion] = useState(null)
  const [answer, setAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [assessment, setAssessment] = useState(null)
  const [status, setStatus] = useState('Checking API connection...')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const socketRef = useRef(null)

  useEffect(() => {
    const checkHealth = () => api.health().then(() => setStatus('API connected')).catch(() => setStatus('API offline'))
    checkHealth()
    const timer = setInterval(checkHealth, 5000)
    return () => { clearInterval(timer); socketRef.current?.close() }
  }, [])

  const updateLesson = (field, value) => setLesson((current) => ({ ...current, [field]: value }))
  const run = async (action, success) => {
    setBusy(true); setMessage('')
    try { await action(); if (success) setMessage(success) } catch (error) { setMessage(error.message) } finally { setBusy(false) }
  }
  const createLesson = () => run(async () => setLessonData(await api.createLesson(lesson)), 'Lesson plan generated')
  const createQuestion = () => run(async () => {
    const data = await api.createQuestion(lessonData?.lesson_id || 'lesson_001', { lesson_id: lessonData?.lesson_id || 'lesson_001', concept: lessonData?.plan.objectives[0]?.concept || lesson.topic, question_type: 'mcq' })
    setQuestion(data); setFeedback(null); setAnswer('')
  }, 'Question ready')
  const submitAnswer = () => run(async () => setFeedback(await api.submitAnswer(question.lesson_id, { lesson_id: question.lesson_id, question_id: question.id, student_answer: answer })), 'Answer evaluated')
  const generateAssessment = () => run(async () => setAssessment(await api.generateAssessment({ student_id: 'student_001', lesson_id: lessonData?.lesson_id || 'lesson_001', question_ids: question ? [question.id] : [] })), 'Assessment updated')
  const startLiveLesson = () => run(async () => {
    const id = lessonData?.lesson_id || 'lesson_001'
    await api.lessonAction(id, 'start')
    socketRef.current?.close()
    socketRef.current = openLessonSocket(id, setMessage, () => setMessage('Teacher channel unavailable'))
  }, 'Live teacher channel ready')

  return <main className="min-h-screen bg-[#f5f6f0] text-slate-900">
    <header className="border-b border-slate-200 bg-white"><div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5"><div><p className="text-xs font-bold uppercase tracking-[0.24em] text-emerald-700">AI Teacher</p><h1 className="mt-1 text-2xl font-semibold">Adaptive learning studio</h1></div><span className={`rounded-full px-3 py-1 text-xs font-semibold ${status === 'API connected' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>{status}</span></div></header>
    <div className="mx-auto grid max-w-7xl gap-6 px-6 py-8 lg:grid-cols-[0.9fr_1.1fr]">
      <section className="space-y-6"><div className="rounded-3xl bg-[#0e3b32] p-8 text-white shadow-xl"><p className="text-sm text-emerald-200">Understand → Practice → Adapt</p><h2 className="mt-3 text-4xl font-semibold tracking-tight">A teacher that changes with you.</h2><p className="mt-4 text-sm leading-6 text-emerald-100">Ground a lesson in your topic, test understanding, and get a simpler explanation when you need one.</p></div>
        <Panel title="Create a lesson" detail="Choose the learner's goal and language."><input className="field" value={lesson.topic} onChange={(e) => updateLesson('topic', e.target.value)} placeholder="Topic" /><div className="grid grid-cols-2 gap-3"><select className="field" value={lesson.learner_level} onChange={(e) => updateLesson('learner_level', e.target.value)}><option>beginner</option><option>intermediate</option><option>advanced</option></select><select className="field" value={lesson.language} onChange={(e) => updateLesson('language', e.target.value)}><option value="en">English</option><option value="hi">Hindi</option><option value="hinglish">Hinglish</option></select></div><textarea className="field min-h-24" value={lesson.learning_goal} onChange={(e) => updateLesson('learning_goal', e.target.value)} /><button className="button" disabled={busy} onClick={createLesson}>Generate lesson plan</button></Panel>
        <Panel title="Teaching controls" detail="Start the live session or request a new question."><div className="flex flex-wrap gap-3"><button className="button" onClick={startLiveLesson}>Start live lesson</button><button className="button-secondary" disabled={!lessonData || busy} onClick={createQuestion}>Ask a question</button></div><p className="text-xs text-slate-500">The live channel uses the FastAPI WebSocket lesson session.</p></Panel>
      </section>
      <section className="space-y-6"><Panel title="Lesson workspace" detail={lessonData ? `${lessonData.plan.duration_minutes} minutes · ${lessonData.plan.language}` : 'Generate a plan to begin.'}>{lessonData ? <div className="space-y-4"><div><p className="text-xs font-bold uppercase tracking-widest text-emerald-700">{lessonData.plan.level}</p><h2 className="mt-1 text-3xl font-semibold">{lessonData.plan.topic}</h2></div><div className="rounded-2xl bg-emerald-50 p-5"><p className="font-semibold text-emerald-950">{lessonData.plan.objectives[0].concept}</p><p className="mt-2 text-sm leading-6 text-emerald-900">{lessonData.plan.objectives[0].explanation}</p></div><p className="text-sm text-slate-500">{lessonData.plan.questions_to_ask[0]}</p></div> : <EmptyState />}</Panel>
        <Panel title="Student interaction" detail="Answer honestly so the teacher can adapt.">{question ? <div className="space-y-4"><p className="font-semibold">{question.prompt}</p><div className="grid gap-2">{question.options?.map((option) => <button className={`rounded-xl border px-4 py-3 text-left text-sm transition ${answer === option ? 'border-emerald-600 bg-emerald-50' : 'border-slate-200 bg-white hover:border-emerald-400'}`} key={option} onClick={() => setAnswer(option)}>{option}</button>)}</div><div className="flex gap-3"><button className="button" disabled={!answer || busy} onClick={submitAnswer}>Submit answer</button><button className="button-secondary" onClick={createQuestion}>New question</button></div>{feedback && <div className={`rounded-2xl p-4 text-sm ${feedback.is_correct ? 'bg-emerald-50 text-emerald-900' : 'bg-amber-50 text-amber-900'}`}><strong>{feedback.is_correct ? 'Correct' : 'Let us re-learn this'}</strong><p className="mt-1">{feedback.explanation}</p><p className="mt-2 font-semibold">Next action: {feedback.next_action}</p>{feedback.misconception && <p className="mt-1">Misconception: {feedback.misconception}</p>}</div>}</div> : <EmptyState text="Ask a question after generating a lesson." />}</Panel>
        <Panel title="Learning report" detail="Turn attempts into the next recommendation.">{assessment ? <div className="space-y-3"><p className="text-5xl font-semibold text-emerald-700">{assessment.score}%</p><p className="text-sm"><strong>Strong:</strong> {assessment.strong_areas.join(', ') || 'Keep practicing'}</p><p className="text-sm"><strong>Focus:</strong> {assessment.weak_areas.join(', ') || 'Ready for the next concept'}</p></div> : <button className="button-secondary" onClick={generateAssessment}>Generate assessment</button>}</Panel>{message && <div className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-900">{message}</div>}</section>
    </div>
  </main>
}

function Panel({ title, detail, children }) { return <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="mb-5"><h2 className="text-lg font-semibold">{title}</h2><p className="mt-1 text-sm text-slate-500">{detail}</p></div><div className="space-y-3">{children}</div></div> }
function EmptyState({ text = 'Your generated lesson will appear here.' }) { return <div className="flex min-h-36 flex-col items-center justify-center rounded-2xl bg-slate-50 px-8 text-center"><span className="text-3xl">✦</span><p className="mt-3 text-sm text-slate-500">{text}</p></div> }

export default App
