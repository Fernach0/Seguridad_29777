import { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '../services/services'
import { jwtDecode } from 'jwt-decode'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Verificar si hay un usuario almacenado
    const storedUser = authService.getStoredUser()
    const token = authService.getToken()
    
    if (storedUser && token) {
      try {
        // Verificar si el token ha expirado
        const decoded = jwtDecode(token)
        if (decoded.exp * 1000 > Date.now()) {
          setUser(storedUser)
        } else {
          // Token expirado
          authService.logout()
        }
      } catch (error) {
        console.error('Error decoding token:', error)
        authService.logout()
      }
    }
    
    setLoading(false)
  }, [])

  const login = async (username, password) => {
    try {
      const response = await authService.login(username, password)
      if (response.success && response.data.user) {
        setUser(response.data.user)
        return { success: true }
      }
      return { success: false, error: 'Login failed' }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Error al iniciar sesión' 
      }
    }
  }

  const logout = async () => {
    await authService.logout()
    setUser(null)
  }

  const hasRole = (requiredRole) => {
    if (!user) return false
    if (Array.isArray(requiredRole)) {
      return requiredRole.includes(user.rol)
    }
    return user.rol === requiredRole
  }

  const value = {
    user,
    loading,
    login,
    logout,
    hasRole,
    isAuthenticated: !!user
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}
