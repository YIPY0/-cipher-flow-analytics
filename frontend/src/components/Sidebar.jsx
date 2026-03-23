import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Shield, Activity, BarChart3, Bell } from 'lucide-react'

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/threats', icon: Shield, label: 'Threats' },
  { path: '/flows', icon: Activity, label: 'Flows' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  { path: '/alerts', icon: Bell, label: 'Alerts' },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-800 flex flex-col">
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center animate-pulse-glow">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">CipherFlow</h1>
            <p className="text-xs text-slate-400">Analytics Engine</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {navItems.map(({ path, icon: Icon, label }) => (
          <NavLink
            key={path}
            to={path}
            end={path === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`
            }
          >
            <Icon className="w-5 h-5" />
            <span className="font-medium">{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <div className="px-4 py-3 rounded-lg bg-slate-900/50">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-xs text-slate-400">System Active</span>
          </div>
          <p className="text-xs text-slate-500">ML Engine Online</p>
        </div>
      </div>
    </aside>
  )
}