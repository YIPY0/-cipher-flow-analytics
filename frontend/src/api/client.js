const API_BASE = '/api'

async function fetchApi(endpoint) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'Content-Type': 'application/json' },
    })
    if (!response.ok) throw new Error(`API error: ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error(`API call failed: ${endpoint}`, error)
    throw error
  }
}

const api = {
  getHealth: () => fetchApi('/health'),
  getStats: () => fetchApi('/stats'),
  getThreats: (limit = 50, severity = null) => {
    let url = `/threats?limit=${limit}`
    if (severity && severity !== 'all') url += `&severity=${severity}`
    return fetchApi(url)
  },
  getFlows: (limit = 100) => fetchApi(`/flows?limit=${limit}`),
  getAlerts: (limit = 50) => fetchApi(`/alerts?limit=${limit}`),
  getModelPerformance: () => fetchApi('/model/performance'),
  getShapExplanation: (flowId) => {
    let url = '/shap/explain'
    if (flowId) url += `?flow_id=${flowId}`
    return fetchApi(url)
  },
  getTimeline: (minutes = 30) => fetchApi(`/flow/timeline?minutes=${minutes}`),
}

export default api