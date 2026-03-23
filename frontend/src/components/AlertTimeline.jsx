import { useState, useEffect } from 'react'
import { AlertTriangle, Shield, Clock, RefreshCw } from 'lucide-react'
import api from '../api/client'

export default function AlertTimeline() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchAlerts = async () => {
    try {
      const data = await api.getAlerts(50)
      setAlerts(data.alerts || [])
    } catch (err) {
      console.error('Failed to fetch alerts:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAlerts()
    const interval = setInterval(fetchAlerts, 5000)
    return () => clearInterval(interval)
  }, [])

  const severityConfig = {
    critical: { border: 'border-l-red-500', dot: 'bg-red-500', text: 'text-red-400' },
    high: { border: 'border-l-orange-500', dot: 'bg-orange-500', text: 'text-orange-400' },
    medium: { border: 'border-l-yellow-500', dot: 'bg-yellow-500', text: 'text-yellow-400' },
    low: { border: 'border-l-green-500', dot: 'bg-green-500', text: 'text-green-400' },
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-xl">
      <div className="p-4 border-b border-slate-700 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-yellow-500" />
          <h3 className="text-sm font-semibold text-white">Alert Timeline</h3>
          <span className="px-2 py-0.5 rounded-full bg-yellow-500/10 text-yellow-400 text-xs">{alerts.length}</span>
        </div>
        <button onClick={fetchAlerts} className="p-1.5 rounded-lg hover:bg-slate-700 text-slate-400">
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      <div className="max-h-[600px] overflow-y-auto">
        {loading ? (
          <div className="p-8 text-center text-slate-500">Loading alerts...</div>
        ) : alerts.length === 0 ? (
          <div className="p-12 text-center">
            <Shield className="w-10 h-10 mx-auto mb-3 text-green-500" />
            <p className="text-slate-400">No alerts — all clear</p>
            <p className="text-xs text-slate-600 mt-1">Alerts will appear when threats are detected</p>
          </div>
        ) : (
          <div className="p-4 space-y-3">
            {alerts.map((alert, i) => {
              const config = severityConfig[alert.severity] || severityConfig.low
              return (
                <div key={alert.alert_id || i} className={`border-l-2 ${config.border} bg-slate-800/30 rounded-r-lg pl-4 pr-4 py-3 animate-slide-in`}>
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${config.dot}`} />
                      <span className={`text-sm font-bold ${config.text}`}>{alert.threat_type}</span>
                      <span className="text-xs text-slate-500 px-1.5 py-0.5 rounded bg-slate-700">{alert.severity}</span>
                    </div>
                    <span className="text-xs text-slate-500 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {new Date(alert.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mb-2">{alert.description}</p>
                  <div className="flex items-center gap-4 text-xs text-slate-500 font-mono">
                    <span>SRC: {alert.src_ip}</span>
                    <span>DST: {alert.dst_ip}:{alert.dst_port}</span>
                    <span>Conf: {(alert.confidence * 100).toFixed(1)}%</span>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}