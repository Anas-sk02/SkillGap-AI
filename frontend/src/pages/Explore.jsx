import RolesCatalogue from '../components/RolesCatalogue'
import { useNavigate } from 'react-router-dom'

export default function Explore() {
  const navigate = useNavigate()

  return (
    <div className="animate-fadeIn">
      <div style={{ marginBottom: '2rem', display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize: '2rem',
            fontWeight: 800,
            letterSpacing: '-0.02em',
            marginBottom: '0.5rem',
          }}>
            Explore Roles
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: 520 }}>
            Browse the complete skill taxonomy for each tech role. Click a role card to see the full breakdown by stage.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>
          🎯 Analyze My Gap
        </button>
      </div>

      <RolesCatalogue />
    </div>
  )
}
