import ThreatTable from '../components/ThreatTable'
import { Shield } from 'lucide-react'

export default function ThreatsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <Shield className="w-7 h-7 text-red-500" />
          Threat Detection
        </h1>
        <p className="text-sm text-slate-400 mt-1">View and analyze detected network threats</p>
      </div>
      <ThreatTable />
    </div>
  )
}