export default function StatCard({ title, value, icon: Icon, color = 'cyan', subtitle }) {
  const colors = {
    cyan: 'from-cyan-500/10 to-cyan-500/5 border-cyan-500/20 text-cyan-400',
    red: 'from-red-500/10 to-red-500/5 border-red-500/20 text-red-400',
    green: 'from-green-500/10 to-green-500/5 border-green-500/20 text-green-400',
    yellow: 'from-yellow-500/10 to-yellow-500/5 border-yellow-500/20 text-yellow-400',
    purple: 'from-purple-500/10 to-purple-500/5 border-purple-500/20 text-purple-400',
  }

  const iconColor = {
    cyan: 'text-cyan-400',
    red: 'text-red-400',
    green: 'text-green-400',
    yellow: 'text-yellow-400',
    purple: 'text-purple-400',
  }

  return (
    <div className={`bg-gradient-to-br ${colors[color]} border rounded-xl p-5 transition-transform hover:scale-[1.02]`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-slate-400">{title}</span>
        {Icon && <Icon className={`w-5 h-5 ${iconColor[color]}`} />}
      </div>
      <p className="text-3xl font-bold text-white">{value}</p>
      {subtitle && <p className="text-xs text-slate-500 mt-2">{subtitle}</p>}
    </div>
  )
}