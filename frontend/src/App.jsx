import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Explore from './pages/Explore'

function Nav() {
  return (
    <nav className="nav">
      <div className="nav-inner">
        <NavLink to="/" className="nav-logo">SkillGap AI</NavLink>
        <ul className="nav-links">
          <li>
            <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''} end>
              🏠 Home
            </NavLink>
          </li>
          <li>
            <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'active' : ''}>
              🎯 Dashboard
            </NavLink>
          </li>
          <li>
            <NavLink to="/explore" className={({ isActive }) => isActive ? 'active' : ''}>
              🔍 Explore
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Nav />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/explore" element={<Explore />} />
          </Routes>
        </main>
        <footer style={{
          borderTop: '1px solid var(--border-subtle)',
          padding: '1.5rem 2rem',
          textAlign: 'center',
          color: 'var(--text-muted)',
          fontSize: '0.82rem',
        }}>
          SkillGap AI — ML-Powered Career Readiness Platform · Random Forest Model · 90%+ Accuracy
        </footer>
      </div>
    </BrowserRouter>
  )
}
