import ModelPerformance from '../components/ModelPerformance'
import ShapPanel from '../components/ShapPanel'
import { BarChart3 } from 'lucide-react'

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <BarChart3 className="w-7 h-7 text-purple-500" />
          Analytics & Explainability
        </h1>
        <p className="text-sm text-slate-400 mt-1">Model performance and SHAP explanations</p>
      </div>
      <ModelPerformance />
      <ShapPanel />
    </div>
  )
}