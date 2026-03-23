import { useState, useEffect } from 'react'
import { Wifi, WifiOff, Search, Clock } from 'lucide-react'
import api from '../api/client'

export default function TopBar() {
  const [time, setTime] = useState(new Date())
  const [health, setHealth] = useState(null)

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    const check = async () => {
      try {
        const data = await api.getHealth()
        setHealth(data)
      } catch {
        setHealth(null)
      }
    }
    check()
    const interval = setInterval(check, 10000)
    return () => clearInterval(interval)
  }, [])

  const isOnline = health?.status === 'healthy'

  return (
    <header className="h-16 bg-slate-950 border-b border-slate-800 flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search flows, IPs, threats..."
            className="pl-10 pr-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-sm text-slate-300 placeholder-slate-500 focus:outline-none focus:border-cyan-500 w-80 transition-colors"
          />
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900">
          {isOnline ? (
            <>
              <Wifi className="w-4 h-4 text-green-500" />
              <span className="text-xs text-green-400 font-medium">LIVE</span>
            </>
          ) : (
            <>
              <WifiOff className="w-4 h-4 text-red-500" />
              <span className="text-xs text-red-400 font-medium">OFFLINE</span>
            </>
          )}
        </div>

        <div className="flex items-center gap-2 text-slate-400">
          <Clock className="w-4 h-4" />
          <span className="text-sm font-mono">{time.toLocaleTimeString()}</span>
        </div>

        {health && (
          <div className="text-xs text-slate-500">
            Flows: {health.total_flows?.toLocaleString() || 0}
          </div>
        )}
      </div>
    </header>
  )
}