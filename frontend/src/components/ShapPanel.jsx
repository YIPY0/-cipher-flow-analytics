import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Brain } from 'lucide-react'
import api from '../api/client'

export default function ShapPanel({ flowId = null }) {
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchExplanation = async () => {
      try {
        const data = await api.getShapExplanation(flowId)
        setExplanation(data)
      } catch (err) {
        console.error('SHAP fetch failed:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchExplanation()
  }, [flowId])

  if (loading) {
    return (
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <div className="text-center text-slate-500 py-8">
          <Brain className="w-8 h-8 mx-auto mb-3 animate-pulse text-purple-400" />
          <p>Computing SHAP explanations...</p>
        </div>
      </div>
    )
  }

  if (!explanation || explanation.error) {
    return (
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <div className="text-center text-slate-500 py-8">
          <p>No explanation available yet. Waiting for threat detection...</p>
        </div>
      </div>
    )
  }

  const contributions = explanation.explanation?.top_contributions || []
  const chartData = contributions.map((c) => ({
    feature: c.feature.replace(/_/g, ' '),
    value: Math.round(c.shap_value * 10000) / 10000,
  }))

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-purple-400" />
          <h3 className="text-sm font-semibold text-white">SHAP Feature Contributions</h3>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Prediction:</span>
          <span className="px-2 py-1 rounded bg-cyan-500/10 text-cyan-400 text-xs font-bold">
            {explanation.prediction} ({(explanation.confidence * 100).toFixed(1)}%)
          </span>
        </div>
      </div>

      {chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={chartData} layout="vertical" margin={{ left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis type="number" stroke="#64748b" fontSize={10} />
            <YAxis type="category" dataKey="feature" width={180} stroke="#64748b" fontSize={10} />
            <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {chartData.map((entry, i) => (
                <Cell key={i} fill={entry.value >= 0 ? '#06b6d4' : '#ef4444'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <p className="text-slate-500 text-center py-8">No SHAP data available</p>
      )}
    </div>
  )
}