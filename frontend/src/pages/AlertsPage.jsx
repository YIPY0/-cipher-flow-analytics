import AlertTimeline from '../components/AlertTimeline'
import { Bell } from 'lucide-react'

export default function AlertsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <Bell className="w-7 h-7 text-yellow-500" />
          Alert Center
        </h1>
        <p className="text-sm text-slate-400 mt-1">Security alerts and incident timeline</p>
      </div>
      <AlertTimeline />
    </div>
  )
}