export default function SkillGapReport({ data }) {
  if (!data) return null

  const { target_role, match_percentage, missing_skills, present_skills } = data

  const topMissing = missing_skills.slice(0, 5).map((s) => s.skill).join(', ')

  return (
    <div className="glass-card animate-fadeIn">
      <div className="section-title">
        <span className="icon">📊</span>
        Skill Gap Report
      </div>

      {present_skills && present_skills.length > 0 && (
        <div style={{ marginBottom: '1.5rem' }}>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Skills You Already Have
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
            {present_skills.map((s) => (
              <span key={s} style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.25rem',
                background: 'rgba(104,211,145,0.12)',
                color: 'var(--accent-green)',
                border: '1px solid rgba(104,211,145,0.25)',
                borderRadius: 999,
                padding: '0.2rem 0.65rem',
                fontSize: '0.8rem',
                fontWeight: 500,
              }}>
                ✓ {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {missing_skills.length > 0 ? (
        <>
          <div style={{
            background: 'rgba(246,173,85,0.08)',
            border: '1px solid rgba(246,173,85,0.2)',
            borderRadius: 'var(--radius-sm)',
            padding: '0.9rem 1.2rem',
            marginBottom: '1.5rem',
            fontSize: '0.92rem',
            color: 'var(--accent-orange)',
          }}>
            🔍 You are missing <strong>{topMissing}</strong>{missing_skills.length > 5 ? ` and ${missing_skills.length - 5} more` : ''} — learn these to boost your {target_role} readiness.
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {missing_skills.map((skill, i) => (
              <SkillRow key={skill.skill} skill={skill} rank={i + 1} />
            ))}
          </div>
        </>
      ) : (
        <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--accent-green)' }}>
          <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>🎉</div>
          <p style={{ fontWeight: 600 }}>You have all the skills for {target_role}!</p>
        </div>
      )}
    </div>
  )
}

function SkillRow({ skill, rank }) {
  const stageBadgeClass = {
    Foundational: 'badge-foundational',
    Intermediate: 'badge-intermediate',
    Applied: 'badge-applied',
  }[skill.stage] || 'badge-foundational'

  const fillColor = {
    Foundational: 'var(--accent-blue)',
    Intermediate: 'var(--accent-purple)',
    Applied: 'var(--accent-green)',
  }[skill.stage] || 'var(--accent-blue)'

  return (
    <div style={{
      background: 'rgba(255,255,255,0.03)',
      border: '1px solid var(--border-subtle)',
      borderRadius: 'var(--radius-sm)',
      padding: '0.9rem 1.1rem',
      animation: `fadeIn 0.3s ease ${rank * 0.05}s both`,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <span style={{
            width: 24, height: 24,
            background: 'var(--bg-card-hover)',
            borderRadius: 6,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)',
          }}>
            {rank}
          </span>
          <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>{skill.skill}</span>
        </div>
        <span className={`badge ${stageBadgeClass}`}>{skill.stage}</span>
      </div>
      <div className="progress-bar-track" style={{ marginBottom: '0.5rem' }}>
        <div className="progress-bar-fill" style={{
          width: `${skill.weight * 100}%`,
          background: fillColor,
        }} />
      </div>
      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{skill.reason}</p>
    </div>
  )
}
