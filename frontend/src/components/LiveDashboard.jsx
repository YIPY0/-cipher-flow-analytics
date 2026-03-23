import { Activity } from 'lucide-react'
import useWebSocket from '../hooks/useWebSocket'

export default function LiveDashboard() {
  const { isConnected, recentFlows } = useWebSocket()

  const severityStyle = {
    critical: 'text-red-400 bg-red-500/10 border-red-500/30',
    high: 'text-orange-400 bg-orange-500/10 border-orange-500/30',
    medium: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30',
    low: 'text-green-400 bg-green-500/10 border-green-500/30',
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-xl">
      <div className="p-4 border-b border-slate-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={`w-2.5 h-2.5 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
          <Activity className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-semibold text-white">Live Network Monitor</h3>
        </div>
        <span className="text-xs text-slate-500">{recentFlows.length} flows captured</span>
      </div>

      <div className="max-h-[400px] overflow-y-auto">
        {recentFlows.length === 0 ? (
          <div className="p-12 text-center">
            <Activity className="w-8 h-8 text-slate-600 mx-auto mb-3 animate-pulse" />
            <p className="text-slate-500 text-sm">Waiting for network flows...</p>
            <p className="text-slate-600 text-xs mt-1">Flows will appear here in real-time</p>
          </div>
        ) : (
          recentFlows.map((flow, i) => (
            <div
              key={flow.flow_id || i}
              className="px-4 py-3 border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors animate-slide-in"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${severityStyle[flow.severity] || severityStyle.low}`}>
                    {flow.severity}
                  </span>
                  <span className="text-sm text-slate-300 font-mono">
                    {flow.src_ip} → {flow.dst_ip}:{flow.dst_port}
                  </span>
                  <span className="text-xs text-slate-600">{flow.protocol}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`text-xs font-bold ${flow.is_threat ? 'text-red-400' : 'text-green-400'}`}>
                    {flow.prediction}
                  </span>
                  <span className="text-xs text-slate-500 font-mono">
                    {(flow.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}