import { Container, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

const NotFound = () => {
  const navigate = useNavigate()

  return (
    <Container className="py-5 text-center">
      <h1 className="display-1">404</h1>
      <h2>Página no encontrada</h2>
      <p className="text-muted">La página que buscas no existe</p>
      <Button variant="primary" onClick={() => navigate('/')}>
        Volver al inicio
      </Button>
    </Container>
  )
}

export default NotFound
