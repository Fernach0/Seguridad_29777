import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const PrivateRoute = ({ children, requiredRole }) => {
  const { isAuthenticated, hasRole, user } = useAuth()

  console.log('PrivateRoute - isAuthenticated:', isAuthenticated)
  console.log('PrivateRoute - user:', user)
  console.log('PrivateRoute - requiredRole:', requiredRole)

  if (!isAuthenticated) {
    console.log('PrivateRoute - Redirigiendo a login: no autenticado')
    return <Navigate to="/login" replace />
  }

  if (requiredRole && !hasRole(requiredRole)) {
    console.log('PrivateRoute - Redirigiendo a home: sin permisos')
    return <Navigate to="/" replace />
  }

  return children
}

export default PrivateRoute
