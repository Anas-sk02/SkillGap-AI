import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

const STAGE_CONFIG = {
  Foundational: { color: '#63b3ed', glow: '#63b3ed44', label: '① Foundational', icon: '🔧' },
  Intermediate: { color: '#b794f4', glow: '#b794f444', label: '② Intermediate', icon: '⚡' },
  Applied: { color: '#68d391', glow: '#68d39144', label: '③ Applied', icon: '🚀' },
}

const STAGE_ORDER = ['Foundational', 'Intermediate', 'Applied']

export default function VisualRoadmap({ roadmap }) {
  const svgRef = useRef(null)
  const containerRef = useRef(null)

  const stages = STAGE_ORDER.filter((s) => roadmap && roadmap[s] && roadmap[s].length > 0)
  const totalSkills = stages.reduce((acc, s) => acc + (roadmap[s]?.length || 0), 0)

  useEffect(() => {
    if (!svgRef.current || !roadmap || stages.length === 0) return

    const container = containerRef.current
    const containerWidth = container?.clientWidth || 800

    const nodeR = 32
    const colGap = 200
    const rowGap = 80
    const padX = 80
    const padY = 60

    const maxRows = Math.max(...stages.map((s) => roadmap[s].length))
    const width = padX * 2 + (stages.length - 1) * colGap
    const height = padY * 2 + maxRows * rowGap

    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('width', '100%')
      .attr('height', Math.min(height, 520))

    const defs = svg.append('defs')

    stages.forEach((stage) => {
      const cfg = STAGE_CONFIG[stage]
      const gradId = `grad-${stage}`
      const grad = defs.append('radialGradient').attr('id', gradId)
      grad.append('stop').attr('offset', '0%').attr('stop-color', cfg.color).attr('stop-opacity', 0.3)
      grad.append('stop').attr('offset', '100%').attr('stop-color', cfg.color).attr('stop-opacity', 0.08)

      const filterId = `glow-${stage}`
      const filter = defs.append('filter').attr('id', filterId)
      filter.append('feGaussianBlur').attr('stdDeviation', '3').attr('result', 'blur')
      const merge = filter.append('feMerge')
      merge.append('feMergeNode').attr('in', 'blur')
      merge.append('feMergeNode').attr('in', 'SourceGraphic')
    })

    const nodePositions = {}

    stages.forEach((stage, si) => {
      const skills = roadmap[stage]
      const cx = padX + si * colGap
      const cfg = STAGE_CONFIG[stage]

      svg.append('text')
        .attr('x', cx)
        .attr('y', 28)
        .attr('text-anchor', 'middle')
        .attr('fill', cfg.color)
        .attr('font-size', '11px')
        .attr('font-weight', '700')
        .attr('letter-spacing', '1.5px')
        .text(cfg.label.toUpperCase())

      skills.forEach((skill, ri) => {
        const cy = padY + ri * rowGap + rowGap / 2
        nodePositions[`${stage}-${ri}`] = { cx, cy, stage, skill }

        if (ri > 0) {
          const prev = nodePositions[`${stage}-${ri - 1}`]
          svg.append('line')
            .attr('x1', prev.cx).attr('y1', prev.cy + nodeR)
            .attr('x2', cx).attr('y2', cy - nodeR)
            .attr('stroke', cfg.color)
            .attr('stroke-width', 1.5)
            .attr('stroke-opacity', 0.4)
            .attr('stroke-dasharray', '4,4')
        }

        if (si > 0 && ri === 0) {
          const prevStage = stages[si - 1]
          const lastIdx = roadmap[prevStage].length - 1
          const prev = nodePositions[`${prevStage}-${lastIdx}`]
          if (prev) {
            const prevCfg = STAGE_CONFIG[prevStage]
            svg.append('line')
              .attr('x1', prev.cx + nodeR).attr('y1', prev.cy)
              .attr('x2', cx - nodeR).attr('y2', cy)
              .attr('stroke', `url(#grad-${stage})`)
              .attr('stroke-width', 2)
              .attr('stroke-opacity', 0.6)
              .attr('marker-end', `url(#arrow-${stage})`)
          }

          defs.append('marker')
            .attr('id', `arrow-${stage}`)
            .attr('markerWidth', 8).attr('markerHeight', 8)
            .attr('refX', 6).attr('refY', 3)
            .attr('orient', 'auto')
            .append('path')
            .attr('d', 'M0,0 L0,6 L8,3 z')
            .attr('fill', cfg.color)
        }

        const g = svg.append('g')
          .attr('transform', `translate(${cx},${cy})`)
          .style('cursor', 'default')

        g.append('circle')
          .attr('r', nodeR)
          .attr('fill', `url(#grad-${stage})`)
          .attr('stroke', cfg.color)
          .attr('stroke-width', 1.5)
          .attr('filter', `url(#glow-${stage})`)
          .style('opacity', 0)
          .transition()
          .delay(si * 200 + ri * 80)
          .duration(400)
          .style('opacity', 1)

        const words = skill.skill.split(' ')
        const line1 = words.slice(0, Math.ceil(words.length / 2)).join(' ')
        const line2 = words.length > 1 ? words.slice(Math.ceil(words.length / 2)).join(' ') : null

        g.append('text')
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('fill', cfg.color)
          .attr('font-size', '9px')
          .attr('font-weight', '600')
          .attr('dy', line2 ? '-6' : '0')
          .text(line1)
          .style('opacity', 0)
          .transition()
          .delay(si * 200 + ri * 80 + 200)
          .duration(300)
          .style('opacity', 1)

        if (line2) {
          g.append('text')
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .attr('fill', cfg.color)
            .attr('font-size', '9px')
            .attr('font-weight', '600')
            .attr('dy', '6')
            .text(line2)
            .style('opacity', 0)
            .transition()
            .delay(si * 200 + ri * 80 + 200)
            .duration(300)
            .style('opacity', 1)
        }

        g.append('title').text(`${skill.skill} (${(skill.weight * 100).toFixed(0)}% importance)`)
      })
    })

  }, [roadmap, stages.join(',')])

  if (!roadmap || totalSkills === 0) return null

  return (
    <div className="glass-card animate-fadeIn">
      <div className="section-title">
        <span className="icon">🗺️</span>
        Learning Roadmap
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        {stages.map((stage) => {
          const cfg = STAGE_CONFIG[stage]
          return (
            <div key={stage} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <span style={{
                width: 12, height: 12, borderRadius: '50%',
                background: cfg.color,
                boxShadow: `0 0 8px ${cfg.glow}`,
              }} />
              <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                {cfg.icon} {stage} ({roadmap[stage]?.length} skills)
              </span>
            </div>
          )
        })}
      </div>

      <div ref={containerRef} style={{ overflowX: 'auto', overflowY: 'hidden' }}>
        <svg ref={svgRef} style={{ display: 'block' }} />
      </div>

      <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {stages.map((stage) => {
          const cfg = STAGE_CONFIG[stage]
          return (
            <div key={stage}>
              <p style={{ fontSize: '0.8rem', fontWeight: 700, color: cfg.color, marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                {cfg.icon} {stage}
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                {roadmap[stage].map((s) => (
                  <span key={s.skill} style={{
                    background: `${cfg.color}18`,
                    color: cfg.color,
                    border: `1px solid ${cfg.color}30`,
                    borderRadius: 999,
                    padding: '0.22rem 0.7rem',
                    fontSize: '0.8rem',
                    fontWeight: 500,
                  }}>
                    {s.skill}
                  </span>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
