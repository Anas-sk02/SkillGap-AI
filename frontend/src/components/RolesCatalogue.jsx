import { useState, useEffect } from 'react'
import { getAllRoles } from '../api/client'

const STAGE_COLORS = {
  Foundational: { bg: 'rgba(99,179,237,0.12)', color: 'var(--accent-blue)', border: 'rgba(99,179,237,0.25)' },
  Intermediate: { bg: 'rgba(183,148,244,0.12)', color: 'var(--accent-purple)', border: 'rgba(183,148,244,0.25)' },
  Applied: { bg: 'rgba(104,211,145,0.12)', color: 'var(--accent-green)', border: 'rgba(104,211,145,0.25)' },
}

const ROLE_ICONS = {
  'Data Scientist': '📊',
  'Backend Developer': '⚙️',
  'ML Engineer': '🤖',
  'Frontend Developer': '🎨',
  'AI Engineer': '🧠',
  'DevOps Engineer': '🚀',
  'Java Developer': '☕',
  'Cloud Engineer': '☁️',
  'Data Engineer': '🌊',
  'Cybersecurity Analyst': '🛡️',
  'Full Stack Developer': '💻',
  'Mobile App Developer': '📱',
  'QA / Automation Engineer': '🧪',
  'Blockchain Developer': '⛓️',
  'Game Developer': '🎮',
  'Embedded Systems Engineer': '🔌',
}

const ROLE_DESCRIPTIONS = {
  'Data Scientist': 'Analyze complex data to drive business decisions using statistical modeling and ML.',
  'Backend Developer': 'Build scalable server-side systems, APIs, and databases that power applications.',
  'ML Engineer': 'Design, deploy, and maintain machine learning pipelines in production environments.',
  'Frontend Developer': 'Craft engaging, accessible user interfaces with modern web technologies.',
  'AI Engineer': 'Build cutting-edge LLMs, RAG systems, and autonomous agent workflows.',
  'DevOps Engineer': 'Automate CI/CD pipelines, container orchestration, and cloud infrastructure.',
  'Java Developer': 'Architect enterprise-grade microservices and robust Spring Boot applications.',
  'Cloud Engineer': 'Design resilient, highly scalable cloud architectures and serverless systems.',
  'Data Engineer': 'Build big data ETL pipelines, distributed streaming systems, and data lakes.',
  'Cybersecurity Analyst': 'Protect network infrastructure, monitor threat telemetry, and lead incident response.',
  'Full Stack Developer': 'Bridge frontend and backend to deliver complete end-to-end web applications.',
  'Mobile App Developer': 'Create fluid cross-platform mobile apps for iOS and Android using Flutter/React Native.',
  'QA / Automation Engineer': 'Build automated testing suites to guarantee software quality and reliability.',
  'Blockchain Developer': 'Engineer decentralized applications, smart contracts, and Web3 protocols.',
  'Game Developer': 'Build immersive gameplay systems, physics, and interactive 3D virtual worlds.',
  'Embedded Systems Engineer': 'Program microcontrollers, firmware, RTOS, and IoT hardware devices.',
}

export default function RolesCatalogue() {
  const [roles, setRoles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState(null)

  useEffect(() => {
    getAllRoles()
      .then((res) => setRoles(res.data.roles))
      .catch(() => setError('Failed to load roles. Make sure the backend is running.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="loading-overlay">
      <div className="spinner" />
      <span>Loading role catalogue...</span>
    </div>
  )

  if (error) return <div className="error-banner">{error}</div>

  const roleData = selected ? roles.find((r) => r.role === selected) : null

  return (
    <div className="animate-fadeIn">
      <div className="grid-2" style={{ gap: '1.5rem' }}>
        {roles.map((role) => {
          const icon = ROLE_ICONS[role.role] || '💼'
          const isActive = selected === role.role
          const skillCount = role.skills.length
          const foundational = role.skills.filter((s) => s.stage === 'Foundational').length
          const intermediate = role.skills.filter((s) => s.stage === 'Intermediate').length
          const applied = role.skills.filter((s) => s.stage === 'Applied').length

          return (
            <div
              key={role.role}
              className="glass-card"
              style={{
                cursor: 'pointer',
                border: isActive ? '1px solid var(--accent-blue)' : '1px solid var(--border-subtle)',
                boxShadow: isActive ? 'var(--shadow-glow)' : 'none',
                transition: 'var(--transition)',
              }}
              onClick={() => setSelected(isActive ? null : role.role)}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', marginBottom: '1rem' }}>
                <div style={{
                  width: 52, height: 52,
                  background: 'var(--gradient-hero)',
                  borderRadius: 'var(--radius-sm)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '1.6rem', flexShrink: 0,
                }}>
                  {icon}
                </div>
                <div>
                  <h3 style={{ fontFamily: 'var(--font-display)', fontWeight: 700, marginBottom: '0.25rem' }}>
                    {role.role}
                  </h3>
                  <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    {ROLE_DESCRIPTIONS[role.role]}
                  </p>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
                {[['Foundational', foundational], ['Intermediate', intermediate], ['Applied', applied]].map(([stage, count]) => (
                  count > 0 && (
                    <span key={stage} style={{
                      ...STAGE_COLORS[stage],
                      padding: '0.15rem 0.55rem',
                      borderRadius: 999,
                      fontSize: '0.72rem',
                      fontWeight: 600,
                      border: `1px solid ${STAGE_COLORS[stage].border}`,
                    }}>
                      {count} {stage}
                    </span>
                  )
                ))}
              </div>

              {isActive && (
                <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem', marginTop: '0.5rem' }}>
                  {['Foundational', 'Intermediate', 'Applied'].map((stage) => {
                    const stageSkills = role.skills.filter((s) => s.stage === stage)
                    if (!stageSkills.length) return null
                    const cfg = STAGE_COLORS[stage]
                    return (
                      <div key={stage} style={{ marginBottom: '0.75rem' }}>
                        <p style={{ fontSize: '0.75rem', fontWeight: 700, color: cfg.color, marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                          {stage}
                        </p>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem' }}>
                          {stageSkills.map((s) => (
                            <span key={s.name} style={{
                              background: cfg.bg,
                              color: cfg.color,
                              border: `1px solid ${cfg.border}`,
                              borderRadius: 999,
                              padding: '0.15rem 0.55rem',
                              fontSize: '0.78rem',
                              fontWeight: 500,
                            }}>
                              {s.name}
                            </span>
                          ))}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '0.5rem' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {skillCount} total skills
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--accent-blue)' }}>
                  {isActive ? '▲ Collapse' : '▼ Expand'}
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
