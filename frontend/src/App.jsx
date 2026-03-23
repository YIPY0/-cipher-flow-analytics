import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ThreatsPage from './pages/ThreatsPage'
import FlowsPage from './pages/FlowsPage'
import AnalyticsPage from './pages/AnalyticsPage'
import AlertsPage from './pages/AlertsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="threats" element={<ThreatsPage />} />
        <Route path="flows" element={<FlowsPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="alerts" element={<AlertsPage />} />
      </Route>
    </Routes>
  )
}

export default App