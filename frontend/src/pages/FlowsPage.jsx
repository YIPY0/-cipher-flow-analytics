import FlowVisualizer from '../components/FlowVisualizer'
import LiveDashboard from '../components/LiveDashboard'
import { Activity } from 'lucide-react'

export default function FlowsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <Activity className="w-7 h-7 text-cyan-500" />
          Network Flows
        </h1>
        <p className="text-sm text-slate-400 mt-1">Monitor and visualize network traffic</p>
      </div>
      <FlowVisualizer />
      <LiveDashboard />
    </div>
  )
}