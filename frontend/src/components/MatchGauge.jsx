import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

export default function MatchGauge({ percentage }) {
  const svgRef = useRef(null)

  const pct = Math.max(0, Math.min(100, percentage ?? 0))

  const color = pct >= 75 ? '#68d391' : pct >= 50 ? '#f6ad55' : '#fc8181'
  const label = pct >= 75 ? 'Strong Match' : pct >= 50 ? 'Moderate Match' : 'Needs Work'

  useEffect(() => {
    if (!svgRef.current) return

    const width = 280
    const height = 160
    const cx = width / 2
    const cy = height - 20
    const r = 120
    const strokeW = 18

    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('width', '100%')
      .attr('height', '100%')

    const arcBg = d3.arc()
      .innerRadius(r - strokeW)
      .outerRadius(r)
      .startAngle(-Math.PI / 2)
      .endAngle(Math.PI / 2)

    svg.append('path')
      .attr('d', arcBg)
      .attr('transform', `translate(${cx},${cy})`)
      .attr('fill', 'rgba(255,255,255,0.08)')

    const arcFg = d3.arc()
      .innerRadius(r - strokeW)
      .outerRadius(r)
      .startAngle(-Math.PI / 2)
      .cornerRadius(strokeW / 2)

    const endAngle = -Math.PI / 2 + (Math.PI * pct) / 100

    const path = svg.append('path')
      .attr('transform', `translate(${cx},${cy})`)
      .attr('fill', color)
      .style('filter', `drop-shadow(0 0 8px ${color}88)`)

    path.transition()
      .duration(1200)
      .ease(d3.easeCubicOut)
      .attrTween('d', () => {
        const interp = d3.interpolate(-Math.PI / 2, endAngle)
        return (t) => arcFg.endAngle(interp(t))()
      })

    const gradId = `gauge-grad-${Math.random().toString(36).slice(2)}`
    const defs = svg.append('defs')
    const grad = defs.append('linearGradient')
      .attr('id', gradId)
      .attr('gradientUnits', 'userSpaceOnUse')
      .attr('x1', cx - r).attr('y1', 0)
      .attr('x2', cx + r).attr('y2', 0)

    grad.append('stop').attr('offset', '0%').attr('stop-color', '#667eea')
    grad.append('stop').attr('offset', '100%').attr('stop-color', color)

    const ticks = [0, 25, 50, 75, 100]
    ticks.forEach((tick) => {
      const angle = -Math.PI / 2 + (Math.PI * tick) / 100
      const x = cx + (r + 10) * Math.cos(angle)
      const y = cy + (r + 10) * Math.sin(angle)
      svg.append('text')
        .attr('x', x).attr('y', y)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .attr('fill', 'rgba(255,255,255,0.3)')
        .attr('font-size', '9px')
        .text(tick)
    })

    svg.append('text')
      .attr('x', cx).attr('y', cy - 28)
      .attr('text-anchor', 'middle')
      .attr('fill', color)
      .attr('font-size', '38px')
      .attr('font-weight', '800')
      .attr('font-family', 'Outfit, sans-serif')
      .text('0%')
      .transition()
      .duration(1200)
      .ease(d3.easeCubicOut)
      .tween('text', function () {
        const interp = d3.interpolateNumber(0, pct)
        return (t) => { d3.select(this).text(`${Math.round(interp(t))}%`) }
      })

    svg.append('text')
      .attr('x', cx).attr('y', cy - 4)
      .attr('text-anchor', 'middle')
      .attr('fill', 'rgba(255,255,255,0.5)')
      .attr('font-size', '11px')
      .attr('letter-spacing', '2px')
      .text('ROLE FIT')

  }, [pct, color])

  return (
    <div className="glass-card animate-fadeIn" style={{ textAlign: 'center' }}>
      <div className="section-title" style={{ justifyContent: 'center' }}>
        <span className="icon">🎯</span>
        Role Match Score
      </div>
      <div style={{ position: 'relative', maxWidth: 280, margin: '0 auto' }}>
        <svg ref={svgRef} />
      </div>
      <div style={{
        display: 'inline-flex', alignItems: 'center', gap: '0.4rem',
        background: `${color}18`,
        border: `1px solid ${color}40`,
        borderRadius: 999,
        padding: '0.35rem 1rem',
        fontSize: '0.88rem', fontWeight: 600,
        color,
        marginTop: '0.5rem',
      }}>
        {label}
      </div>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.75rem' }}>
        {pct >= 75
          ? "You're well-prepared. A few advanced skills will close the gap."
          : pct >= 50
          ? "Good foundation. Focus on the intermediate skills next."
          : "Start with the foundational skills to build your base."}
      </p>
    </div>
  )
}
