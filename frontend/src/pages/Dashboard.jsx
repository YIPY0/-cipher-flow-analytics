import { useState, useEffect } from 'react'
import { Activity, Shield, AlertTriangle, Target, Wifi } from 'lucide-react'
import StatCard from '../components/StatCard'
import LiveDashboard from '../components/LiveDashboard'
import FlowVisualizer from '../components/FlowVisualizer'
import api from '../api/client'

export default function Dashboard() {
  const [stats, setStats] = useState({
    total_flows: 0,
    threats_detected: 0,
    anomaly_rate: 0,
    model_accuracy: 0.9969,
  })
  const [health, setHealth] = useState(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [statsData, healthData] = await Promise.all([
          api.getStats(),
          api.getHealth(),
        ])
        setStats(statsData)
        setHealth(healthData)
      } catch (err) {
        // Try health endpoint at least
        try {
          const healthData = await api.getHealth()
          setHealth(healthData)
          setStats(prev => ({
            ...prev,
            total_flows: healthData.total_flows || prev.total_flows,
            threats_detected: healthData.threats_detected || prev.threats_detected,
          }))
        } catch (e) {
          console.error('API error:', e)
        }
      }
    }
    fetchStats()
    const interval = setInterval(fetchStats, 3000)
    return () => clearInterval(interval)
  }, [])

  const totalFlows = stats.total_flows || health?.total_flows || 0
  const threats = stats.threats_detected || health?.threats_detected || 0
  const anomalyRate = totalFlows > 0 ? ((threats / totalFlows) * 100).toFixed(1) : '0'
  const accuracy = ((stats.model_accuracy || 0.9969) * 100).toFixed(1)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-sm text-slate-400 mt-1">Real-time network threat monitoring — LIVE CAPTURE MODE</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-red-500/10 border border-red-500/20">
            <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            <span className="text-xs text-red-400 font-medium">LIVE CAPTURE</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-500/10 border border-green-500/20">
            <Wifi className="w-3 h-3 text-green-400" />
            <span className="text-xs text-green-400 font-medium">
              {health?.uptime_seconds ? `${Math.floor(health.uptime_seconds)}s uptime` : 'Connecting...'}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Flows Analyzed"
          value={totalFlows.toLocaleString()}
          icon={Activity}
          color="cyan"
          subtitle="Real network flows captured"
        />
        <StatCard
          title="Threats Detected"
          value={threats.toLocaleString()}
          icon={Shield}
          color="red"
          subtitle="Malicious flows identified"
        />
        <StatCard
          title="Anomaly Rate"
          value={`${anomalyRate}%`}
          icon={AlertTriangle}
          color="yellow"
          subtitle="Of total network traffic"
        />
        <StatCard
          title="Model Accuracy"
          value={`${accuracy}%`}
          icon={Target}
          color="green"
          subtitle="Random Forest classifier"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LiveDashboard />
        <FlowVisualizer />
      </div>
    </div>
  )
}