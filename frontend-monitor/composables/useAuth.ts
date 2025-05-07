export const useAuth = () => {
    const token = useState<string>('token', () => '')
    const setToken = (value: string) => {
      token.value = value
      if (process.client) {
        localStorage.setItem('token', value)
      }
    }
    const clearToken = () => {
      token.value = ''
      if (process.client) {
        localStorage.removeItem('token')
      }
    }
    if (process.client && !token.value) {
      const saved = localStorage.getItem('token')
      if (saved) token.value = saved
    }
    return {
      token,
      setToken,
      clearToken
    }
  }
  