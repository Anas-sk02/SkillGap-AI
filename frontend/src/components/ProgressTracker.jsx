import { useState, useEffect } from 'react'
import { updateProgress, fetchProgress } from '../api/client'

const STAGE_CONFIG = {
  Foundational: { color: 'var(--accent-blue)', icon: '🔧' },
  Intermediate: { color: 'var(--accent-purple)', icon: '⚡' },
  Applied: { color: 'var(--accent-green)', icon: '🚀' },
}

export default function ProgressTracker({ roadmap, studentId, targetRole }) {
  const [completed, setCompleted] = useState(new Set())
  const [saving, setSaving] = useState(false)
  const [saveMsg, setSaveMsg] = useState('')

  const stages = ['Foundational', 'Intermediate', 'Applied'].filter((s) => roadmap && roadmap[s]?.length > 0)
  const allSkills = stages.flatMap((s) => roadmap[s].map((sk) => sk.skill))
  const totalCount = allSkills.length
  const completedCount = [...completed].filter((s) => allSkills.includes(s)).length
  const pct = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0

  useEffect(() => {
    if (!studentId || !targetRole || totalCount === 0) return
    fetchProgress(studentId, targetRole)
      .then((res) => {
        const skills = res.data.completed_skills || []
        setCompleted(new Set(skills.filter(Boolean)))
      })
      .catch(() => {})
  }, [studentId, targetRole, totalCount])

  const toggle = async (skill) => {
    const next = new Set(completed)
    if (next.has(skill)) next.delete(skill)
    else next.add(skill)
    setCompleted(next)

    setSaving(true)
    try {
      await updateProgress({ student_id: studentId, target_role: targetRole, completed_skills: [...next] })
      setSaveMsg('Saved ✓')
      setTimeout(() => setSaveMsg(''), 2000)
    } catch {
      setSaveMsg('Save failed')
    } finally {
      setSaving(false)
    }
  }

  if (!roadmap || totalCount === 0) return null

  return (
    <div className="glass-card animate-fadeIn">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <div className="section-title" style={{ margin: 0 }}>
          <span className="icon">📈</span>
          Progress Tracker
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {saveMsg && (
            <span style={{ fontSize: '0.8rem', color: 'var(--accent-green)', fontWeight: 600 }}>{saveMsg}</span>
          )}
          <span style={{
            background: 'var(--gradient-hero)',
            borderRadius: 999,
            padding: '0.3rem 0.85rem',
            fontSize: '0.85rem',
            fontWeight: 700,
            color: 'white',
          }}>
            {completedCount}/{totalCount}
          </span>
        </div>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Overall completion</span>
          <span style={{ fontSize: '0.82rem', fontWeight: 700, color: pct >= 75 ? 'var(--accent-green)' : pct >= 40 ? 'var(--accent-orange)' : 'var(--text-secondary)' }}>
            {pct}%
          </span>
        </div>
        <div className="progress-bar-track" style={{ height: 10 }}>
          <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
        </div>
      </div>

      {stages.map((stage) => {
        const cfg = STAGE_CONFIG[stage]
        const stageSkills = roadmap[stage]
        const stageDone = stageSkills.filter((s) => completed.has(s.skill)).length

        return (
          <div key={stage} style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <p style={{ fontSize: '0.85rem', fontWeight: 700, color: cfg.color, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                {cfg.icon} {stage}
              </p>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                {stageDone}/{stageSkills.length} done
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {stageSkills.map((sk) => {
                const isDone = completed.has(sk.skill)
                return (
                  <label
                    key={sk.skill}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.75rem',
                      padding: '0.65rem 0.9rem',
                      borderRadius: 'var(--radius-sm)',
                      background: isDone ? 'rgba(104,211,145,0.07)' : 'rgba(255,255,255,0.03)',
                      border: `1px solid ${isDone ? 'rgba(104,211,145,0.2)' : 'var(--border-subtle)'}`,
                      cursor: 'pointer',
                      transition: 'var(--transition)',
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={isDone}
                      onChange={() => toggle(sk.skill)}
                      disabled={saving}
                      style={{ width: 16, height: 16, accentColor: cfg.color, cursor: 'pointer' }}
                    />
                    <span style={{
                      flex: 1,
                      fontSize: '0.9rem',
                      fontWeight: isDone ? 600 : 400,
                      color: isDone ? 'var(--accent-green)' : 'var(--text-primary)',
                      textDecoration: isDone ? 'line-through' : 'none',
                      opacity: isDone ? 0.8 : 1,
                    }}>
                      {sk.skill}
                    </span>
                    <span style={{
                      fontSize: '0.72rem',
                      color: 'var(--text-muted)',
                      background: 'rgba(255,255,255,0.05)',
                      padding: '0.1rem 0.45rem',
                      borderRadius: 999,
                    }}>
                      {(sk.weight * 100).toFixed(0)}% impact
                    </span>
                    {isDone && <span style={{ color: 'var(--accent-green)', fontSize: '1rem' }}>✓</span>}
                  </label>
                )
              })}
            </div>
          </div>
        )
      })}

      {pct === 100 && (
        <div style={{
          textAlign: 'center',
          padding: '1.5rem',
          background: 'rgba(104,211,145,0.08)',
          border: '1px solid rgba(104,211,145,0.2)',
          borderRadius: 'var(--radius-md)',
          marginTop: '0.5rem',
        }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🎓</div>
          <p style={{ fontWeight: 700, color: 'var(--accent-green)', marginBottom: '0.25rem' }}>Roadmap Complete!</p>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>You've mastered all the recommended skills.</p>
        </div>
      )}
    </div>
  )
}
