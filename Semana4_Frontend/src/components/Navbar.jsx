import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';

function AppNavbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) return null;

  return (
    <Navbar bg="primary" variant="dark" expand="lg" className="mb-4">
      <Container>
        <Navbar.Brand as={Link} to="/">
          🏥 ESPE MedSafe
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">
              Dashboard
            </Nav.Link>
            
            {user.rol === 'admin' && (
              <Nav.Link as={Link} to="/users">
                Usuarios
              </Nav.Link>
            )}
            
            {(user.rol === 'admin' || user.rol === 'doctor') && (
              <Nav.Link as={Link} to="/patients">
                Pacientes
              </Nav.Link>
            )}
            
            <Nav.Link as={Link} to="/medical-records">
              Historias Clínicas
            </Nav.Link>
            
            <Nav.Link as={Link} to="/crypto-demo">
              Demo Cripto
            </Nav.Link>
            
            {user.rol === 'admin' && (
              <Nav.Link as={Link} to="/audit">
                Auditoría
              </Nav.Link>
            )}
          </Nav>
          
          <Nav>
            <Navbar.Text className="me-3">
              👤 {user.nombre_completo} ({user.rol})
            </Navbar.Text>
            <Button variant="outline-light" size="sm" onClick={handleLogout}>
              Salir
            </Button>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default AppNavbar;