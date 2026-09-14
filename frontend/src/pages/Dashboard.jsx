import { useState } from 'react'
import ProfileForm from '../components/ProfileForm'
import SkillGapReport from '../components/SkillGapReport'
import MatchGauge from '../components/MatchGauge'
import VisualRoadmap from '../components/VisualRoadmap'
import ProgressTracker from '../components/ProgressTracker'
import { getSkillGap, getRoadmap } from '../api/client'

export default function Dashboard() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [skillGapData, setSkillGapData] = useState(null)
  const [roadmapData, setRoadmapData] = useState(null)
  const [profile, setProfile] = useState(null)

  const handleSubmit = async (formProfile) => {
    setLoading(true)
    setError(null)
    setSkillGapData(null)
    setRoadmapData(null)
    setProfile(formProfile)

    try {
      const [gapRes, roadRes] = await Promise.all([
        getSkillGap(formProfile),
        getRoadmap(formProfile),
      ])
      setSkillGapData(gapRes.data)
      setRoadmapData(roadRes.data.roadmap)
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
        'Could not connect to the backend. Make sure the API is running on port 8000.'
      )
    } finally {
      setLoading(false)
    }
  }

  const hasResults = skillGapData && roadmapData

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{
          fontFamily: 'var(--font-display)',
          fontSize: '2rem',
          fontWeight: 800,
          letterSpacing: '-0.02em',
          marginBottom: '0.5rem',
        }}>
          Skill Gap Dashboard
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
          Fill in your profile below to receive your personalized gap analysis and learning roadmap.
        </p>
      </div>

      <ProfileForm onSubmit={handleSubmit} loading={loading} />

      {error && (
        <div className="error-banner animate-fadeIn" style={{ marginTop: '1.5rem' }}>
          ⚠️ {error}
        </div>
      )}

      {hasResults && (
        <div style={{ marginTop: '2.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="grid-2" style={{ alignItems: 'start' }}>
            <MatchGauge percentage={skillGapData.match_percentage} />
            <SkillGapReport data={skillGapData} />
          </div>

          <VisualRoadmap roadmap={roadmapData} />

          <ProgressTracker
            roadmap={roadmapData}
            studentId={profile?.student_id}
            targetRole={profile?.target_role}
          />
        </div>
      )}
    </div>
  )
}
