import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import PrivateRoute from './components/PrivateRoute'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Users from './pages/Users'
import Patients from './pages/Patients'
import MedicalRecords from './pages/MedicalRecords'
import AuditLogs from './pages/AuditLogs'
import NotFound from './pages/NotFound'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app-container">
          <Navbar />
          <Routes>
            <Route path="/login" element={<Login />} />
            
            <Route path="/" element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            } />
            
            <Route path="/users" element={
              <PrivateRoute requiredRole="admin">
                <Users />
              </PrivateRoute>
            } />
            
            <Route path="/patients" element={
              <PrivateRoute requiredRole={['admin', 'doctor']}>
                <Patients />
              </PrivateRoute>
            } />
            
            <Route path="/medical-records" element={
              <PrivateRoute>
                <MedicalRecords />
              </PrivateRoute>
            } />
            
            <Route path="/audit" element={
              <PrivateRoute requiredRole="admin">
                <AuditLogs />
              </PrivateRoute>
            } />
            
            <Route path="/404" element={<NotFound />} />
            <Route path="*" element={<Navigate to="/404" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
