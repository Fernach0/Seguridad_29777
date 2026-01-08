import { Container, Row, Col, Card } from 'react-bootstrap'
import { useAuth } from '../contexts/AuthContext'
import { FaUsers, FaUserInjured, FaFileMedical, FaShieldAlt, FaCheckCircle } from 'react-icons/fa'

const Dashboard = () => {
  const { user } = useAuth()

  const getRoleColor = (role) => {
    switch(role) {
      case 'admin': return 'danger'
      case 'doctor': return 'primary'
      case 'paciente': return 'success'
      default: return 'secondary'
    }
  }

  return (
    <Container fluid className="py-4">
      <Row className="mb-4">
        <Col>
          <h1 className="display-4">
            <FaShieldAlt className="me-3" />
            Bienvenido, {user?.nombre || user?.username}
          </h1>
          <p className="lead text-muted">
            Sistema de Gestión de Historias Clínicas con Seguridad Criptográfica
            <span className={`badge bg-${getRoleColor(user?.rol)} ms-3`}>
              {user?.rol?.toUpperCase()}
            </span>
          </p>
        </Col>
      </Row>

      <Row className="g-4 mb-4">
        {user?.rol === 'admin' && (
          <>
            <Col md={6} lg={3}>
              <Card className="border-0 shadow-sm h-100">
                <Card.Body className="text-center">
                  <FaUsers size={50} className="text-primary mb-3" />
                  <h5>Gestión de Usuarios</h5>
                  <p className="text-muted">
                    Administrar doctores y personal médico
                  </p>
                </Card.Body>
              </Card>
            </Col>
            <Col md={6} lg={3}>
              <Card className="border-0 shadow-sm h-100">
                <Card.Body className="text-center">
                  <FaShieldAlt size={50} className="text-warning mb-3" />
                  <h5>Auditoría</h5>
                  <p className="text-muted">
                    Registro de todas las acciones del sistema
                  </p>
                </Card.Body>
              </Card>
            </Col>
          </>
        )}
        
        {(user?.rol === 'admin' || user?.rol === 'doctor') && (
          <>
            <Col md={6} lg={3}>
              <Card className="border-0 shadow-sm h-100">
                <Card.Body className="text-center">
                  <FaUserInjured size={50} className="text-info mb-3" />
                  <h5>Pacientes</h5>
                  <p className="text-muted">
                    Gestionar información de pacientes
                  </p>
                </Card.Body>
              </Card>
            </Col>
            <Col md={6} lg={3}>
              <Card className="border-0 shadow-sm h-100">
                <Card.Body className="text-center">
                  <FaFileMedical size={50} className="text-success mb-3" />
                  <h5>Historias Clínicas</h5>
                  <p className="text-muted">
                    Crear y consultar historias médicas
                  </p>
                </Card.Body>
              </Card>
            </Col>
          </>
        )}
      </Row>

      <Row className="g-4">
        <Col md={6}>
          <Card className="border-0 shadow-sm h-100">
            <Card.Header className="bg-primary text-white">
              <FaShieldAlt className="me-2" />
              Seguridad Criptográfica Implementada
            </Card.Header>
            <Card.Body>
              <ul className="list-unstyled">
                <li className="mb-2">
                  <FaCheckCircle className="text-success me-2" />
                  <strong>AES-256-CBC:</strong> Cifrado simétrico de datos médicos
                </li>
                <li className="mb-2">
                  <FaCheckCircle className="text-success me-2" />
                  <strong>RSA-2048:</strong> Cifrado asimétrico y firmas digitales
                </li>
                <li className="mb-2">
                  <FaCheckCircle className="text-success me-2" />
                  <strong>bcrypt:</strong> Hash seguro de contraseñas
                </li>
                <li className="mb-2">
                  <FaCheckCircle className="text-success me-2" />
                  <strong>SHA-256:</strong> Verificación de integridad
                </li>
                <li className="mb-2">
                  <FaCheckCircle className="text-success me-2" />
                  <strong>JWT:</strong> Autenticación basada en tokens
                </li>
              </ul>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="border-0 shadow-sm h-100">
            <Card.Header className="bg-info text-white">
              Información del Sistema
            </Card.Header>
            <Card.Body>
              <p><strong>Usuario:</strong> {user?.username}</p>
              <p><strong>Rol:</strong> {user?.rol}</p>
              <p><strong>Email:</strong> {user?.email}</p>
              <p><strong>Nombre:</strong> {user?.nombre_completo}</p>
              <hr />
              <p className="mb-0 text-muted small">
                <strong>Nota:</strong> Todos los datos sensibles (alergias, antecedentes, 
                historias clínicas) son cifrados automáticamente con AES-256 antes de 
                almacenarse en la base de datos.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col>
          <Card className="border-0 shadow-sm bg-light">
            <Card.Body>
              <h5>Módulo Educativo de Criptografía</h5>
              <p className="mb-0">
                Accede al módulo de <strong>Demo Criptografía</strong> para aprender y 
                experimentar con diferentes técnicas de cifrado, incluyendo los cifrados 
                clásicos César y Vigenère, además de las técnicas modernas implementadas.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default Dashboard
