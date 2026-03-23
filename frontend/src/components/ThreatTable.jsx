import { useState, useEffect } from 'react'
import { Shield, RefreshCw } from 'lucide-react'
import api from '../api/client'

export default function ThreatTable() {
  const [threats, setThreats] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [total, setTotal] = useState(0)

  const fetchThreats = async () => {
    try {
      const data = await api.getThreats(50, filter)
      setThreats(data.threats || [])
      setTotal(data.total || 0)
    } catch (err) {
      console.error('Failed to fetch threats:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchThreats()
    const interval = setInterval(fetchThreats, 5000)
    return () => clearInterval(interval)
  }, [filter])

  const severityColors = {
    critical: 'bg-red-500/10 text-red-400 border border-red-500/30',
    high: 'bg-orange-500/10 text-orange-400 border border-orange-500/30',
    medium: 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/30',
    low: 'bg-green-500/10 text-green-400 border border-green-500/30',
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-xl overflow-hidden">
      <div className="p-4 border-b border-slate-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Shield className="w-5 h-5 text-red-400" />
          <span className="text-sm font-semibold text-white">Detected Threats</span>
          <span className="px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 text-xs">{total}</span>
        </div>
        <div className="flex items-center gap-2">
          {['all', 'critical', 'high', 'medium'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filter === f
                  ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700'
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
          <button onClick={fetchThreats} className="p-1.5 rounded-lg hover:bg-slate-700 text-slate-400 transition-colors">
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700 bg-slate-800/30">
              {['Time', 'Source IP', 'Destination', 'Protocol', 'Attack Type', 'Severity', 'Confidence'].map((h) => (
                <th key={h} className="text-left text-xs font-medium text-slate-400 px-4 py-3">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="7" className="text-center text-slate-500 py-8">Loading...</td></tr>
            ) : threats.length === 0 ? (
              <tr><td colSpan="7" className="text-center text-slate-500 py-8">
                <Shield className="w-8 h-8 mx-auto mb-2 text-green-500" />
                No threats detected
              </td></tr>
            ) : (
              threats.map((t, i) => (
                <tr key={t.flow_id || i} className="border-b border-slate-700/50 hover:bg-slate-700/20 transition-colors">
                  <td className="px-4 py-3 text-xs text-slate-400 font-mono">
                    {new Date(t.timestamp).toLocaleTimeString()}
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-300 font-mono">{t.src_ip}</td>
                  <td className="px-4 py-3 text-sm text-slate-300 font-mono">{t.dst_ip}:{t.dst_port}</td>
                  <td className="px-4 py-3 text-xs text-slate-400">{t.protocol}</td>
                  <td className="px-4 py-3 text-sm text-white font-semibold">{t.prediction}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${severityColors[t.severity] || severityColors.low}`}>
                      {t.severity}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-300 font-mono">
                    {(t.confidence * 100).toFixed(1)}%
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}