import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap'
import { useAuth } from '../contexts/AuthContext'
import { FaLock, FaUser, FaShieldAlt } from 'react-icons/fa'

const Login = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const result = await login(username, password)
      if (result.success) {
        navigate('/')
      } else {
        setError(result.error || 'Credenciales inválidas')
      }
    } catch (err) {
      setError('Error al conectar con el servidor')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container fluid className="vh-100 d-flex align-items-center justify-content-center" style={{backgroundColor: '#f0f2f5'}}>
      <Row className="w-100 justify-content-center">
        <Col xs={12} sm={10} md={6} lg={4}>
          <Card className="shadow-lg border-0">
            <Card.Header className="text-center py-4" style={{backgroundColor: '#0d6efd', color: 'white'}}>
              <FaShieldAlt size={50} className="mb-3" />
              <h3 className="mb-0">ESPE MedSafe</h3>
              <small>Sistema de Gestión Médica Seguro</small>
            </Card.Header>
            <Card.Body className="p-4">
              {error && <Alert variant="danger" dismissible onClose={() => setError('')}>{error}</Alert>}
              
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    <FaUser className="me-2" />
                    Usuario
                  </Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Ingrese su usuario"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    autoFocus
                  />
                </Form.Group>

                <Form.Group className="mb-4">
                  <Form.Label>
                    <FaLock className="me-2" />
                    Contraseña
                  </Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Ingrese su contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </Form.Group>

                <Button 
                  variant="primary" 
                  type="submit" 
                  className="w-100 py-2"
                  disabled={loading}
                >
                  {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
                </Button>
              </Form>

              <div className="mt-4 text-center">
                <small className="text-muted">
                  <strong>Credenciales por defecto:</strong><br />
                  Usuario: admin | Contraseña: Admin123!
                </small>
              </div>
            </Card.Body>
            <Card.Footer className="text-center text-muted py-3">
              <small>
                Universidad de las Fuerzas Armadas ESPE<br />
                Ingeniería de Seguridad de Software - 2026
              </small>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default Login
