import React, { useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import {
  ArrowRight,
  BrainCircuit,
  Check,
  ChevronDown,
  CheckCircle2,
  CircleAlert,
  ListChecks,
  RotateCcw,
  Sparkles,
  Target,
  Trophy,
  Zap,
  Phone,
  Mail,
  X,
  Lock,
  User,
  LogOut,
} from 'lucide-react'
import './styles.css'
import careerHero from './career_hero.png'

const API_URL = ''

const educationOptions = [
  ['12th', '12th Standard'],
  ['BA', 'B.A. (Bachelor of Arts)'],
  ['BCA', 'B.C.A. (Computer Applications)'],
  ['B.Com', 'B.Com (Bachelor of Commerce)'],
  ['B.Tech', 'B.Tech (Bachelor of Technology)'],
  ['M.Sc', 'M.Sc (Master of Science)'],
  ['MBA', 'M.B.A. (Master of Business Admin)'],
  ['MBBS', 'M.B.B.S.'],
  ['M.Tech', 'M.Tech (Master of Technology)'],
  ['M.Ed', 'M.Ed (Master of Education)'],
]

const specializationOptions = [
  ['Commerce', 'Commerce / Accountancy'],
  ['Finance', 'Finance'],
  ['Marketing', 'Marketing'],
  ['Computer Science', 'Computer Science / IT'],
  ['Computer Applications', 'Computer Applications'],
  ['Electronics', 'Electronics'],
  ['Political Science', 'Political Science'],
  ['English', 'English Literature'],
  ['Physics', 'Physics'],
  ['Medicine', 'Medicine & Surgery'],
  ['Administration', 'Administration'],
]

const skillOptions = [
  ['Python, Web Development, Databases', 'Python, Web Development, Databases'],
  ['Python, MATLAB, CAD', 'Python, MATLAB, CAD'],
  ['Communication, Tax Filing', 'Communication, Tax Filing'],
  ['Leadership, Strategy, Analytics', 'Leadership, Strategy, Analytics'],
  ['Writing, Communication', 'Writing, Communication'],
  ['Research, Data Collection', 'Research, Data Collection'],
  ['Diagnosis, Surgery, Patient Care', 'Diagnosis, Surgery, Patient Care'],
  ['Design Optimization', 'Design Optimization'],
  ['Typing, Customer Handling', 'Typing, Customer Handling'],
  ['Assessment Design', 'Assessment Design'],
]

const interestOptions = [
  ['Technology', 'Technology & Coding'],
  ['Management', 'Management & Leadership'],
  ['Social Work', 'Social Work & Community Service'],
  ['Research', 'Research & Analytics'],
  ['Design', 'Creative & UI/UX Design'],
  ['Creativity', 'Artistic Creativity'],
  ['Teaching', 'Education & Mentorship'],
  ['Healthcare', 'Health & Medical Sciences'],
  ['Helping People', 'Human Services / Helping People'],
]

const initialForm = {
  education: '',
  specialization: '',
  skills: '',
  interests: '',
}

function SelectField({ label, value, onChange, options, placeholder }) {
  return (
    <label className="field">
      <span>{label}</span>
      <div className="select-wrap">
        <select value={value} onChange={(e) => onChange(e.target.value)} required>
          <option value="" disabled>{placeholder}</option>
          {options.map(([optionValue, text]) => (
            <option key={optionValue} value={optionValue}>{text}</option>
          ))}
        </select>
        <ChevronDown size={18} />
      </div>
    </label>
  )
}

function App() {
  const [page, setPage] = useState('landing')
  const [form, setForm] = useState(initialForm)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [roadmap, setRoadmap] = useState(null)
  const [roadmapLoading, setRoadmapLoading] = useState(false)
  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem('currentUser')
    return saved ? JSON.parse(saved) : null
  })
  const [authMode, setAuthMode] = useState('login')
  const [authError, setAuthError] = useState('')
  const [authSuccess, setAuthSuccess] = useState('')
  const [isAboutOpen, setIsAboutOpen] = useState(false)
  const [isLoginOpen, setIsLoginOpen] = useState(false)
  const [loginEmail, setLoginEmail] = useState('')
  const [loginPassword, setLoginPassword] = useState('')
  const [checkedSteps, setCheckedSteps] = useState({})

  const handleLogout = () => {
    setCurrentUser(null)
    localStorage.removeItem('currentUser')
    setCheckedSteps({})
    setPage('landing')
  }

  const toggleStep = async (step) => {
    const nextVal = !checkedSteps[step]
    const updatedChecked = { ...checkedSteps, [step]: nextVal }
    setCheckedSteps(updatedChecked)

    if (currentUser && roadmap?.career) {
      try {
        await fetch(`${API_URL}/api/save_progress`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: currentUser.email,
            career: roadmap.career,
            checked_steps: updatedChecked
          })
        })

        // Sync local user state
        const updatedUser = {
          ...currentUser,
          progress: {
            ...(currentUser.progress || {}),
            [roadmap.career]: updatedChecked
          }
        }
        setCurrentUser(updatedUser)
        localStorage.setItem('currentUser', JSON.stringify(updatedUser))
      } catch (err) {
        console.error("Failed to sync progress with DB:", err)
      }
    }
  }

  const loadSavedRoadmap = async (career) => {
    setRoadmapLoading(true)
    setPage('result')
    setError('')
    try {
      const response = await fetch(`${API_URL}/roadmap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ career }),
      })
      if (!response.ok) {
        throw new Error('Failed to load roadmap.')
      }
      const data = await response.json()

      // Reconstruct prediction result context from user predictions history
      const matchedPred = currentUser?.predictions?.find(p => p.career === data.career)
      setResult({
        career: data.career,
        category: matchedPred ? matchedPred.category : 'Saved Track',
        predictions: [{ title: data.career, confidence: 100 }]
      })

      setRoadmap({
        career: data.career,
        roadmap_for: data.roadmap_for,
        roadmap: data.roadmap || [],
      })

      // Load progress checkboxes
      if (currentUser && currentUser.progress && currentUser.progress[data.career]) {
        setCheckedSteps(currentUser.progress[data.career])
      } else {
        setCheckedSteps({})
      }
    } catch (err) {
      setError(err.message)
      setPage('profile')
    } finally {
      setRoadmapLoading(false)
    }
  }

  const roadmapProgress = useMemo(() => {
    if (!roadmap?.roadmap?.length) return 0
    const done = roadmap.roadmap.filter((item) => checkedSteps[item.step]).length
    return Math.round((done / roadmap.roadmap.length) * 100)
  }, [roadmap, checkedSteps])

  const progress = useMemo(() => {
    return Object.values(form).filter(Boolean).length * 25
  }, [form])

  const update = (key, value) => {
    setForm((current) => ({ ...current, [key]: value }))
    setError('')
  }

  const submit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)
    setPage('loading')

    try {
      const payload = currentUser ? { ...form, email: currentUser.email } : form
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        throw new Error(body.error || 'The ML backend could not process this profile.')
      }

      const data = await response.json()
      setResult(data)
      setRoadmap({
        career: data.career,
        roadmap_for: data.roadmap_for,
        roadmap: data.roadmap || [],
      })
      setRoadmapLoading(false)
      setPage('result')

      // Sync checkboxes
      if (currentUser && currentUser.progress && currentUser.progress[data.career]) {
        setCheckedSteps(currentUser.progress[data.career])
      } else {
        setCheckedSteps({})
      }

      // Sync local state predictions if user is logged in
      if (currentUser) {
        const newPred = {
          career: data.career,
          category: data.category,
          timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
          total_steps: (data.roadmap || []).length
        }
        const updatedPredictions = [
          ...(currentUser.predictions || []).filter(p => p.career !== data.career),
          newPred
        ]
        const updatedUser = {
          ...currentUser,
          predictions: updatedPredictions
        }
        setCurrentUser(updatedUser)
        localStorage.setItem('currentUser', JSON.stringify(updatedUser))
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch from the Flask backend.')
      setPage('assessment')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setForm(initialForm)
    setResult(null)
    setRoadmap(null)
    setCheckedSteps({})
    setError('')
    setPage('assessment')
  }

  return (
    <div className="app-shell">
      <div className="background-grid" />
      <div className="orb orb-one" />
      <div className="orb orb-two" />
      <div className="noise" />

      <header className="topbar">
        <button className="brand" onClick={() => { setPage('landing'); }}>
          <span className="brand-icon"><BrainCircuit size={20} /></span>
          <span>Skill2<span>Career</span></span>
        </button>
        <nav className="header-nav">
          <button className="nav-link" onClick={() => setPage('landing')}>Home</button>
          <button className="nav-link" onClick={() => setIsAboutOpen(true)}>About Us</button>
          {currentUser ? (
            <>
              <button className={`nav-link profile-pill ${page === 'profile' ? 'active' : ''}`} onClick={() => setPage('profile')} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <User size={16} />
                <span>My Profile</span>
              </button>
              <button className="nav-link logout-pill" onClick={handleLogout} title="Log Out" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '9px 12px' }}>
                <LogOut size={16} />
              </button>
            </>
          ) : (
            <button className="nav-link login-pill" onClick={() => { setAuthMode('login'); setAuthError(''); setAuthSuccess(''); setIsLoginOpen(true); }}>Login</button>
          )}
        </nav>
      </header>

      {page === 'landing' && (
        <main className="landing page-enter">
          {/* Tagline Section */}
          <div className="tagline-section">
            <div className="eyebrow"><Sparkles size={14} /> AI-powered career discovery</div>
            <h2>AI-Powered Career Compass & Personalized Learning Roadmaps</h2>
          </div>

          {/* Hero Section */}
          <div className="hero-grid">
            <div className="hero-left">
              <h1>Skill2<span>Career</span></h1>
              <p className="hero-copy">
                Discover the career track that perfectly fits your profile. Pass your academic specialization, skills, and interests to our neural classifiers to get instant top predictions and guided skill roadmaps.
              </p>
              <button className="primary-btn hero-btn" onClick={() => setPage('assessment')}>
                Start assessment <ArrowRight size={19} />
              </button>
            </div>
            <div className="hero-right">
              <div className="hero-image-wrap">
                <img src={careerHero} alt="AI Career Illustration" className="hero-image" />
                <div className="hero-image-glow" />
              </div>
            </div>
          </div>

          <div className="feature-row">
            <div className="mini-feature"><div><BrainCircuit size={20} /></div><span><b>ML powered</b> profile analysis</span></div>
            <div className="mini-feature"><div><Zap size={20} /></div><span><b>Real-time</b> prediction</span></div>
            <div className="mini-feature"><div><Target size={20} /></div><span><b>Top 3</b> career matches</span></div>
          </div>
        </main>
      )}

      {page === 'assessment' && (
        <main className="assessment page-enter">
          <div className="assessment-heading">
            <div>
              <div className="eyebrow"><Target size={14} /> Profile assessment</div>
              <h2>Tell us about yourself.</h2>
              <p>Use the same inputs your existing Flask ML model expects.</p>
            </div>
            <div className="progress-box"><strong>{progress}%</strong><span>complete</span></div>
          </div>

          <div className="progress-track"><span style={{ width: `${progress}%` }} /></div>

          <form className="assessment-card" onSubmit={submit}>
            <div className="form-grid">
              <SelectField label="Education level" value={form.education} onChange={(v) => update('education', v)} options={educationOptions} placeholder="Choose education" />
              <SelectField label="Specialization" value={form.specialization} onChange={(v) => update('specialization', v)} options={specializationOptions} placeholder="Choose domain" />
              <SelectField label="Core skills" value={form.skills} onChange={(v) => update('skills', v)} options={skillOptions} placeholder="Choose skill set" />
              <SelectField label="Field of interest" value={form.interests} onChange={(v) => update('interests', v)} options={interestOptions} placeholder="Choose interest" />
            </div>

            {error && <div className="error-box"><CircleAlert size={18} /><span>{error}<small> Make sure your Flask server is running on 127.0.0.1:5000.</small></span></div>}

            <button className="primary-btn submit-btn" disabled={progress !== 100 || loading}>
              {loading ? 'Analyzing profile...' : <>Predict my career <ArrowRight size={19} /></>}
            </button>
          </form>
        </main>
      )}

      {page === 'loading' && (
        <main className="loading-page page-enter">
          <div className="loader"><div className="loader-core"><BrainCircuit size={28} /></div></div>
          <div className="eyebrow"><Sparkles size={14} /> Running inference</div>
          <h2>Analyzing your profile...</h2>
          <p>Your inputs are being passed to the existing Flask + ML pipeline.</p>
        </main>
      )}

      {page === 'result' && result && (
        <main className="results page-enter">
          <div className="result-top">
            <div>
              <div className="eyebrow"><Check size={14} /> Prediction complete</div>
              <h2>Your career matches.</h2>
            </div>
            <button className="ghost-btn" onClick={reset}><RotateCcw size={16} /> Try again</button>
          </div>

          <section className="result-hero-card">
            <div className="result-icon"><Target size={25} /></div>
            <div className="result-main">
              <span>Predicted field</span>
              <h3>{result.category}</h3>
              <p>Top career match: <strong>{result.career}</strong></p>
            </div>
          </section>

          <section className="matches">
            <div className="section-label">Top career matches</div>
            <div className="match-list">
              {result.predictions?.map((prediction, index) => (
                <div className={`match-card ${index === 0 ? 'top-match' : ''}`} key={prediction.title}>
                  <div className="rank">0{index + 1}</div>
                  <div className="match-info">
                    <strong>{prediction.title}</strong>
                    <div className="confidence-track"><span style={{ width: `${prediction.confidence}%` }} /></div>
                  </div>
                  <b>{prediction.confidence}%</b>
                </div>
              ))}
            </div>
          </section>

          <section className="roadmap-section">
            <div className="section-label">Personalized roadmap</div>

            {roadmapLoading ? (
              <div className="roadmap-loading">Preparing your learning path...</div>
            ) : roadmap?.roadmap?.length ? (
              <>
                {/* ── Progress Dashboard ─────────────── */}
                <div className="roadmap-dashboard">
                  <div className="rdash-stat">
                    <span className="rdash-label">Plan Progress</span>
                    <strong className="rdash-value">{roadmapProgress}%</strong>
                    <div className="rdash-bar"><span style={{ width: `${roadmapProgress}%` }} /></div>
                  </div>
                  <div className="rdash-stat">
                    <span className="rdash-label">Steps Done</span>
                    <strong className="rdash-value">{roadmap.roadmap.filter((i) => checkedSteps[i.step]).length} / {roadmap.roadmap.length}</strong>
                  </div>
                  <div className="rdash-gauge-wrap">
                    <svg className="rdash-gauge" viewBox="0 0 120 120">
                      <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(90,140,255,.12)" strokeWidth="8" />
                      <circle cx="60" cy="60" r="52" fill="none" stroke="url(#gaugeGrad)" strokeWidth="8" strokeLinecap="round" strokeDasharray={`${roadmapProgress * 3.267} 326.7`} transform="rotate(-90 60 60)" style={{ transition: 'stroke-dasharray .5s ease' }} />
                      <defs><linearGradient id="gaugeGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stopColor="#5b8cff" /><stop offset="100%" stopColor="#48d4c0" /></linearGradient></defs>
                    </svg>
                    <div className="rdash-gauge-text">
                      <strong>{roadmapProgress}</strong>
                      <span>%</span>
                    </div>
                  </div>
                </div>

                {/* ── Step Cards with Checkboxes ─────── */}
                <div className="roadmap-list">
                  {roadmap.roadmap.map((item) => {
                    const done = !!checkedSteps[item.step]
                    return (
                      <div className={`roadmap-card ${done ? 'roadmap-done' : ''}`} key={item.step} onClick={() => toggleStep(item.step)}>
                        <button className={`roadmap-check ${done ? 'checked' : ''}`} type="button" aria-label={done ? 'Mark incomplete' : 'Mark complete'}>
                          {done && <CheckCircle2 size={20} />}
                        </button>
                        <div className="roadmap-number">{String(item.step).padStart(2, '0')}</div>
                        <div className="roadmap-content">
                          <strong>{item.title}</strong>
                          <span>Focus skill: {item.skill}</span>
                          <small>Project: {item.project}</small>
                        </div>
                        <span className={`roadmap-badge ${done ? 'badge-done' : 'badge-pending'}`}>
                          {done ? <><CheckCircle2 size={12} /> Completed</> : <><ListChecks size={12} /> Pending</>}
                        </span>
                      </div>
                    )
                  })}
                </div>

                {roadmapProgress === 100 && (
                  <div className="roadmap-congrats page-enter">
                    <Trophy size={22} />
                    <p>Congratulations! You've completed all roadmap steps for <strong>{roadmap.career}</strong>.</p>
                  </div>
                )}
              </>
            ) : (
              <div className="roadmap-loading">No roadmap is available for this career yet.</div>
            )}
          </section>


        </main>
      )}

      {page === 'profile' && currentUser && (
        <main className="profile-page page-enter">
          <div className="assessment-heading">
            <div>
              <div className="eyebrow"><Sparkles size={12} /> Dashboard</div>
              <h2>My Profile</h2>
              <p>Logged in as: <strong>{currentUser.email}</strong></p>
            </div>
            <button className="ghost-btn" onClick={() => setPage('landing')}>
              <ArrowRight style={{ transform: 'rotate(180deg)' }} size={16} /> Back to Home
            </button>
          </div>

          <section className="profile-section" style={{ marginTop: '30px' }}>
            <div className="section-label">Your Saved Career Paths</div>

            {!(currentUser.predictions && currentUser.predictions.length) ? (
              <div className="profile-empty-card">
                <Target size={32} />
                <h3>No predictions saved yet</h3>
                <p>Start your career assessment to discover your path and track your roadmap progress.</p>
                <button className="primary-btn" onClick={() => setPage('assessment')} style={{ marginTop: '16px' }}>
                  Start Assessment
                </button>
              </div>
            ) : (
              <div className="profile-grid">
                {currentUser.predictions.map((pred, index) => {
                  const careerProgress = currentUser.progress?.[pred.career] || {}
                  const totalSteps = pred.total_steps || 5
                  const doneSteps = Object.values(careerProgress).filter(Boolean).length
                  const pct = Math.round((doneSteps / totalSteps) * 100)

                  return (
                    <div className="profile-card" key={index}>
                      <div className="profile-card-header">
                        <div className="result-icon">
                          <Target size={24} />
                        </div>
                        <div className="profile-card-title">
                          <h3>{pred.career}</h3>
                          <span>Category: {pred.category}</span>
                        </div>
                      </div>

                      <div className="profile-card-body">
                        <div className="pcard-progress">
                          <div className="pcard-progress-text">
                            <span>Roadmap Progress</span>
                            <strong>{pct}% ({doneSteps}/{totalSteps} steps)</strong>
                          </div>
                          <div className="pcard-progress-bar">
                            <span style={{ width: `${pct}%` }} />
                          </div>
                        </div>
                      </div>

                      <div className="profile-card-footer">
                        <small className="pcard-date">Predicted on {pred.timestamp}</small>
                        <button className="ghost-btn pcard-btn" onClick={() => loadSavedRoadmap(pred.career)}>
                          View Roadmap <ArrowRight size={14} />
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </section>
        </main>
      )}

      {/* About Us Modal */}
      {isAboutOpen && (
        <div className="modal-overlay page-enter" onClick={() => setIsAboutOpen(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setIsAboutOpen(false)}><X size={20} /></button>
            <div className="eyebrow"><Sparkles size={12} /> Who we are</div>
            <h2>About Skill2Career</h2>
            <p>
              Skill2Career is a state-of-the-art career prediction and planning platform. By processing variables like education, domain specialization, skills, and interests through our pre-trained machine learning classifiers, we help students navigate the evolving professional landscape.
            </p>
            <p>
              Once a prediction is generated, Skill2Career instantly builds a personalized step-by-step roadmap to guide you in mastering the skills and completing projects required for that role.
            </p>
            <button className="primary-btn" onClick={() => setIsAboutOpen(false)}>Close Overview</button>
          </div>
        </div>
      )}

      {/* Login Modal */}
      {isLoginOpen && (
        <div className="modal-overlay page-enter" onClick={() => setIsLoginOpen(false)}>
          <div className="modal-card login-card" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setIsLoginOpen(false)}><X size={20} /></button>
            <div className="eyebrow"><Lock size={12} /> Authentication</div>
            <h2>{authMode === 'login' ? 'Sign In' : 'Create Account'}</h2>
            <p>{authMode === 'login' ? 'Access your saved profiles and predictions.' : 'Sign up to track your learning roadmaps.'}</p>

            {authError && (
              <div className="error-box" style={{ marginTop: '12px', marginBottom: '12px' }}>
                <CircleAlert size={18} />
                <span>{authError}</span>
              </div>
            )}

            {authSuccess && (
              <div className="error-box" style={{ marginTop: '12px', marginBottom: '12px', color: '#beffcc', background: 'rgba(82, 232, 114, 0.1)', borderColor: 'rgba(82, 232, 114, 0.25)' }}>
                <CheckCircle2 size={18} />
                <span>{authSuccess}</span>
              </div>
            )}

            <form onSubmit={async (e) => {
              e.preventDefault()
              setAuthError('')
              setAuthSuccess('')
              const endpoint = authMode === 'login' ? '/api/login' : '/api/signup'
              try {
                const response = await fetch(`${API_URL}${endpoint}`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ email: loginEmail, password: loginPassword })
                })
                const data = await response.json()
                if (!response.ok) {
                  throw new Error(data.error || 'Authentication failed.')
                }

                if (authMode === 'login') {
                  setCurrentUser(data.user)
                  localStorage.setItem('currentUser', JSON.stringify(data.user))
                  setIsLoginOpen(false)
                  setLoginEmail('')
                  setLoginPassword('')
                  // Load active progress if showing a roadmap matching this career
                  if (roadmap?.career && data.user.progress && data.user.progress[roadmap.career]) {
                    setCheckedSteps(data.user.progress[roadmap.career])
                  }
                } else {
                  setAuthSuccess('Registration successful! Please sign in.')
                  setAuthMode('login')
                  setLoginPassword('')
                }
              } catch (err) {
                setAuthError(err.message)
              }
            }} className="login-form">
              <label className="field">
                <span>Email Address</span>
                <div className="select-wrap">
                  <input type="email" value={loginEmail} onChange={(e) => setLoginEmail(e.target.value)} placeholder="name@domain.com" required className="modal-input" />
                </div>
              </label>
              <label className="field" style={{ marginTop: '16px' }}>
                <span>Password</span>
                <div className="select-wrap">
                  <input type="password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} placeholder="••••••••" required className="modal-input" />
                </div>
              </label>
              <button className="primary-btn submit-btn" type="submit">
                {authMode === 'login' ? 'Sign In to Dashboard' : 'Register Account'}
              </button>

              <div style={{ marginTop: '16px', textAlign: 'center', fontSize: '13px', color: '#8fa5c4' }}>
                {authMode === 'login' ? (
                  <span>Don't have an account? <button type="button" onClick={() => { setAuthMode('signup'); setAuthError(''); setAuthSuccess(''); }} style={{ background: 'none', border: 'none', color: '#5b8cff', cursor: 'pointer', fontWeight: 600, padding: 0 }}>Sign Up</button></span>
                ) : (
                  <span>Already have an account? <button type="button" onClick={() => { setAuthMode('login'); setAuthError(''); setAuthSuccess(''); }} style={{ background: 'none', border: 'none', color: '#5b8cff', cursor: 'pointer', fontWeight: 600, padding: 0 }}>Sign In</button></span>
                )}
              </div>
            </form>
          </div>
        </div>
      )}

      <footer className="footer-grid">
        <div className="footer-left">
          <div className="footer-brand"><BrainCircuit size={16} /> Skill2<span>Career</span></div>
          <span className="footer-tag">Future-proof your career choices.</span>
        </div>
        <div className="footer-center">
          <div className="footer-item"><Phone size={14} /> <span>+91 9876X XXXXX</span></div>
        </div>
        <div className="footer-right">
          <div className="footer-item"><Mail size={14} /> <span>support@careerai.io</span></div>
        </div>
      </footer>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
