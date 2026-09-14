import { useNavigate } from 'react-router-dom'

const FEATURES = [
  { icon: '🎯', title: 'Precise Gap Analysis', desc: 'Our Random Forest model (90%+ accuracy) identifies exactly which skills you\'re missing for your target role.' },
  { icon: '📊', title: 'Match Score', desc: 'Get a real-time percentage showing how ready you are — powered by trained ML on thousands of student profiles.' },
  { icon: '🗺️', title: 'Visual Roadmap', desc: 'See a stage-by-stage learning path from Foundational to Applied, ranked by impact.' },
  { icon: '📈', title: 'Track Progress', desc: 'Mark skills as learned and watch your readiness score grow over time.' },
]

const ROLES = [
  { name: 'Data Scientist', icon: '📊', color: '#63b3ed' },
  { name: 'ML Engineer', icon: '🤖', color: '#b794f4' },
  { name: 'Backend Developer', icon: '⚙️', color: '#68d391' },
  { name: 'Frontend Developer', icon: '🎨', color: '#f6ad55' },
]

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="animate-fadeIn">
      <div style={{
        textAlign: 'center',
        padding: '5rem 1rem 4rem',
        position: 'relative',
      }}>
        <div style={{
          position: 'absolute', inset: 0, zIndex: 0,
          background: 'radial-gradient(ellipse at 50% 0%, rgba(102,126,234,0.15) 0%, transparent 70%)',
          pointerEvents: 'none',
        }} />

        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
          background: 'rgba(99,179,237,0.1)',
          border: '1px solid rgba(99,179,237,0.25)',
          borderRadius: 999,
          padding: '0.35rem 1rem',
          fontSize: '0.82rem', fontWeight: 600,
          color: 'var(--accent-blue)',
          marginBottom: '1.5rem',
          position: 'relative', zIndex: 1,
        }}>
          ✨ ML-Powered Skill Gap Analysis
        </div>

        <h1 style={{
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(2.2rem, 6vw, 4rem)',
          fontWeight: 800,
          lineHeight: 1.15,
          letterSpacing: '-0.03em',
          marginBottom: '1.25rem',
          position: 'relative', zIndex: 1,
        }}>
          Know Exactly What Skills
          <br />
          <span style={{ background: 'var(--gradient-hero)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
            Stand Between You and Your Dream Role
          </span>
        </h1>

        <p style={{
          fontSize: 'clamp(1rem, 2vw, 1.2rem)',
          color: 'var(--text-secondary)',
          maxWidth: 580,
          margin: '0 auto 2.5rem',
          lineHeight: 1.7,
          position: 'relative', zIndex: 1,
        }}>
          Enter your skills, target role, and projects. Our AI identifies your gaps,
          ranks what to learn next, and builds a visual roadmap just for you.
        </p>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap', position: 'relative', zIndex: 1 }}>
          <button className="btn btn-primary btn-lg" onClick={() => navigate('/dashboard')}>
            🚀 Analyze My Skills
          </button>
          <button className="btn btn-secondary btn-lg" onClick={() => navigate('/explore')}>
            🔍 Explore Roles
          </button>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '4rem' }}>
        {ROLES.map((role) => (
          <div key={role.name} style={{
            display: 'flex', alignItems: 'center', gap: '0.5rem',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 999,
            padding: '0.45rem 1rem',
            fontSize: '0.85rem',
            color: role.color,
            fontWeight: 500,
            cursor: 'pointer',
            transition: 'var(--transition)',
          }}
          onClick={() => navigate('/dashboard')}
          onMouseEnter={(e) => { e.currentTarget.style.borderColor = role.color; e.currentTarget.style.background = `${role.color}12` }}
          onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--border-subtle)'; e.currentTarget.style.background = 'var(--bg-card)' }}
          >
            {role.icon} {role.name}
          </div>
        ))}
      </div>

      <div style={{ marginBottom: '5rem' }}>
        <h2 style={{
          fontFamily: 'var(--font-display)',
          textAlign: 'center',
          fontSize: '1.8rem',
          fontWeight: 700,
          marginBottom: '2.5rem',
          color: 'var(--text-primary)',
        }}>
          Everything You Need to Level Up
        </h2>
        <div className="grid-2" style={{ gap: '1.5rem' }}>
          {FEATURES.map((f, i) => (
            <div key={i} className="glass-card" style={{ animationDelay: `${i * 0.1}s` }}>
              <div style={{ fontSize: '2.2rem', marginBottom: '0.75rem' }}>{f.icon}</div>
              <h3 style={{ fontWeight: 700, marginBottom: '0.5rem', fontSize: '1.05rem' }}>{f.title}</h3>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </div>

      <div style={{
        textAlign: 'center',
        padding: '3rem 1rem',
        background: 'var(--gradient-card)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-xl)',
        marginBottom: '3rem',
      }}>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '4rem', flexWrap: 'wrap', marginBottom: '2rem' }}>
          {[['90%+', 'Model Accuracy'], ['4', 'Tech Roles'], ['2,500+', 'Training Samples'], ['3', 'Learning Stages']].map(([val, label]) => (
            <div key={label} style={{ textAlign: 'center' }}>
              <div style={{
                fontFamily: 'var(--font-display)',
                fontSize: '2.2rem', fontWeight: 800,
                background: 'var(--gradient-hero)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
              }}>
                {val}
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>{label}</div>
            </div>
          ))}
        </div>
        <button className="btn btn-primary btn-lg" onClick={() => navigate('/dashboard')}>
          Get Started Free →
        </button>
      </div>
    </div>
  )
}
