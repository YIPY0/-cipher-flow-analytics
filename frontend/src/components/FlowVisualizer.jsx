import { useState, useEffect } from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { TrendingUp } from 'lucide-react'
import api from '../api/client'

const COLORS = ['#06b6d4', '#ef4444', '#f59e0b', '#8b5cf6', '#10b981', '#ec4899']

export default function FlowVisualizer() {
  const [timeline, setTimeline] = useState([])
  const [stats, setStats] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [tData, sData] = await Promise.all([api.getTimeline(30), api.getStats()])
        setTimeline(tData.timeline || [])
        setStats(sData)
      } catch (err) {
        console.error('FlowVisualizer fetch error:', err)
      }
    }
    fetchData()
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [])

  const pieData = stats?.threat_categories
    ? Object.entries(stats.threat_categories).map(([name, value]) => ({ name, value }))
    : []

  return (
    <div className="space-y-6">
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-semibold text-white">Traffic Timeline</h3>
        </div>
        {timeline.length === 0 ? (
          <div className="h-[250px] flex items-center justify-center text-slate-500 text-sm">
            Collecting timeline data...
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={timeline}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#64748b" fontSize={10} tickFormatter={(t) => t?.split('T')[1] || t} />
              <YAxis stroke="#64748b" fontSize={10} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', fontSize: '12px' }} />
              <Area type="monotone" dataKey="benign" stackId="1" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.3} name="Benign" />
              <Area type="monotone" dataKey="threats" stackId="1" stroke="#ef4444" fill="#ef4444" fillOpacity={0.4} name="Threats" />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>

      {pieData.length > 0 && (
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <h3 className="text-sm font-semibold text-white mb-4">Threat Distribution</h3>
          <div className="flex items-center gap-8">
            <ResponsiveContainer width="50%" height={200}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={85} dataKey="value" stroke="none">
                  {pieData.map((entry, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="space-y-3">
              {pieData.map((entry, i) => (
                <div key={entry.name} className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                  <span className="text-sm text-slate-300">{entry.name}</span>
                  <span className="text-sm text-slate-500 font-mono">{entry.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}