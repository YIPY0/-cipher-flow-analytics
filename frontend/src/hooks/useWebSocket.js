import { useState, useEffect, useRef, useCallback } from 'react'

export default function useWebSocket() {
  const [isConnected, setIsConnected] = useState(false)
  const [recentFlows, setRecentFlows] = useState([])
  const [lastMessage, setLastMessage] = useState(null)
  const wsRef = useRef(null)
  const reconnectTimer = useRef(null)

  const connect = useCallback(() => {
    try {
      const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
      const wsUrl = `${protocol}://${window.location.host}/ws`
      wsRef.current = new WebSocket(wsUrl)

      wsRef.current.onopen = () => {
        setIsConnected(true)
      }

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          setLastMessage(data)
          if (data.type === 'new_flow' && data.data) {
            setRecentFlows((prev) => [data.data, ...prev].slice(0, 100))
          }
        } catch (e) {
          console.error('WS parse error:', e)
        }
      }

      wsRef.current.onclose = () => {
        setIsConnected(false)
        reconnectTimer.current = setTimeout(connect, 3000)
      }

      wsRef.current.onerror = () => {
        wsRef.current?.close()
      }
    } catch (e) {
      reconnectTimer.current = setTimeout(connect, 3000)
    }
  }, [])

  useEffect(() => {
    connect()
    return () => {
      clearTimeout(reconnectTimer.current)
      wsRef.current?.close()
    }
  }, [connect])

  return { isConnected, recentFlows, lastMessage }
}