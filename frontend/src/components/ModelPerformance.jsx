import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'
import { Target } from 'lucide-react'
import api from '../api/client'

export default function ModelPerformance() {
  const [performance, setPerformance] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchPerformance = async () => {
      try {
        const data = await api.getModelPerformance()
        setPerformance(data)
      } catch (err) {
        console.error('Failed to fetch model performance:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchPerformance()
    const interval = setInterval(fetchPerformance, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div className="text-center text-slate-500 py-8">Loading model metrics...</div>
  if (!performance) return <div className="text-center text-slate-500 py-8">No metrics available</div>

  const metrics = performance.metrics || {}
  const radarData = [
    { metric: 'Accuracy', value: (metrics.accuracy || 0) * 100 },
    { metric: 'Precision', value: (metrics.precision || 0) * 100 },
    { metric: 'Recall', value: (metrics.recall || 0) * 100 },
    { metric: 'F1 Score', value: (metrics.f1_score || 0) * 100 },
    { metric: 'ROC AUC', value: (metrics.roc_auc || 0) * 100 },
  ]

  const distData = Object.entries(performance.prediction_distribution || {}).map(([name, count]) => ({ name, count }))

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {radarData.map(({ metric, value }) => (
          <div key={metric} className="bg-slate-800/50 border border-slate-700 rounded-xl p-4 text-center hover:border-cyan-500/30 transition-colors">
            <p className="text-xs text-slate-400 mb-1">{metric}</p>
            <p className="text-2xl font-bold text-cyan-400">{value.toFixed(2)}%</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-semibold text-white">Performance Radar</h3>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#334155" />
              <PolarAngleAxis dataKey="metric" stroke="#94a3b8" fontSize={11} />
              <PolarRadiusAxis domain={[90, 100]} stroke="#334155" fontSize={9} />
              <Radar dataKey="value" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.3} strokeWidth={2} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <h3 className="text-sm font-semibold text-white mb-4">Prediction Distribution</h3>
          {distData.length === 0 ? (
            <div className="h-[280px] flex items-center justify-center text-slate-500 text-sm">Collecting data...</div>
          ) : (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={distData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={10} angle={-20} textAnchor="end" height={60} />
                <YAxis stroke="#64748b" fontSize={10} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
                <Bar dataKey="count" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <h3 className="text-sm font-semibold text-white mb-3">Model Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mb-4">
          <div className="bg-slate-900/50 rounded-lg p-3">
            <span className="text-slate-400 text-xs">Algorithm</span>
            <p className="text-white font-medium mt-1">Random Forest + Isolation Forest</p>
          </div>
          <div className="bg-slate-900/50 rounded-lg p-3">
            <span className="text-slate-400 text-xs">Features</span>
            <p className="text-white font-medium mt-1">{performance.feature_count || 0} selected features</p>
          </div>
          <div className="bg-slate-900/50 rounded-lg p-3">
            <span className="text-slate-400 text-xs">Classes</span>
            <p className="text-white font-medium mt-1">{(performance.classes || []).length} categories</p>
          </div>
        </div>
        <div>
          <p className="text-xs text-slate-400 mb-2">Selected Features:</p>
          <div className="flex flex-wrap gap-1.5">
            {(performance.feature_names || []).map((f) => (
              <span key={f} className="px-2 py-1 bg-slate-700/50 rounded text-xs text-slate-300 font-mono border border-slate-600/50">
                {f}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}