import { useState, useEffect } from 'react'
import { Container, Table, Button, Modal, Form, Alert, Badge, Spinner } from 'react-bootstrap'
import { userService } from '../services/services'
import { validarCedulaEcuatoriana } from '../utils/validators'

const Users = () => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [cedulaError, setCedulaError] = useState('')
  
  const [showModal, setShowModal] = useState(false)
  const [editingUser, setEditingUser] = useState(null)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    nombre: '',
    apellido: '',
    cedula: '',
    rol: 'doctor'
  })

  useEffect(() => {
    loadUsers()
  }, [])

  const loadUsers = async () => {
    try {
      setLoading(true)
      const data = await userService.getAll()
      setUsers(data)
      setError('')
    } catch (err) {
      setError('Error al cargar usuarios: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleShowModal = (user = null) => {
    setCedulaError('')
    if (user) {
      setEditingUser(user)
      setFormData({
        username: user.username,
        password: '',
        email: user.email,
        nombre: user.nombre,
        apellido: user.apellido,
        cedula: user.cedula,
        rol: user.rol
      })
    } else {
      setEditingUser(null)
      setFormData({
        username: '',
        password: '',
        email: '',
        nombre: '',
        apellido: '',
        cedula: '',
        rol: 'doctor'
      })
    }
    setShowModal(true)
  }

  const handleCloseModal = () => {
    setShowModal(false)
    setCedulaError('')
    setEditingUser(null)
    setFormData({
      username: '',
      password: '',
      email: '',
      nombre: '',
      apellido: '',
      cedula: '',
      rol: 'doctor'
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setCedulaError('')

    // Validar cédula ecuatoriana
    const resultadoCedula = validarCedulaEcuatoriana(formData.cedula)
    if (!resultadoCedula.valida) {
      setCedulaError(resultadoCedula.mensaje)
      setError(resultadoCedula.mensaje)
      return
    }
    setError('')
    setSuccess('')

    try {
      if (editingUser) {
        // Si no se ingresó password, no lo incluimos en la actualización
        const updateData = { ...formData }
        if (!updateData.password) {
          delete updateData.password
        }
        await userService.update(editingUser.id, updateData)
        setSuccess('Usuario actualizado exitosamente')
      } else {
        await userService.create(formData)
        setSuccess('Usuario creado exitosamente')
      }
      
      handleCloseModal()
      loadUsers()
      
      // Limpiar mensaje después de 3 segundos
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Error al guardar usuario: ' + err.message)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este usuario?')) {
      try {
        await userService.delete(id)
        setSuccess('Usuario eliminado exitosamente')
        loadUsers()
        setTimeout(() => setSuccess(''), 3000)
      } catch (err) {
        setError('Error al eliminar usuario: ' + err.message)
      }
    }
  }

  const handleToggleActive = async (user) => {
    try {
      await userService.update(user.id, { activo: !user.activo })
      setSuccess(`Usuario ${!user.activo ? 'activado' : 'desactivado'} exitosamente`)
      loadUsers()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Error al cambiar estado: ' + err.message)
    }
  }

  if (loading) {
    return (
      <Container className="py-4 text-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando...</span>
        </Spinner>
      </Container>
    )
  }

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Gestión de Usuarios</h2>
        <Button variant="primary" onClick={() => handleShowModal()}>
          <i className="bi bi-plus-circle"></i> Nuevo Usuario
        </Button>
      </div>

      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')} dismissible>{success}</Alert>}

      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>ID</th>
            <th>Usuario</th>
            <th>Nombre Completo</th>
            <th>Email</th>
            <th>Cédula</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.nombre_completo}</td>
              <td>{user.email}</td>
              <td>{user.cedula}</td>
              <td>
                <Badge bg={user.rol === 'admin' ? 'danger' : 'primary'}>
                  {user.rol}
                </Badge>
              </td>
              <td>
                <Badge bg={user.activo ? 'success' : 'secondary'}>
                  {user.activo ? 'Activo' : 'Inactivo'}
                </Badge>
              </td>
              <td>
                <Button 
                  variant="warning" 
                  size="sm" 
                  className="me-2"
                  onClick={() => handleShowModal(user)}
                >
                  <i className="bi bi-pencil"></i>
                </Button>
                <Button 
                  variant={user.activo ? 'secondary' : 'success'}
                  size="sm" 
                  className="me-2"
                  onClick={() => handleToggleActive(user)}
                >
                  <i className={`bi bi-${user.activo ? 'x-circle' : 'check-circle'}`}></i>
                </Button>
                <Button 
                  variant="danger" 
                  size="sm"
                  onClick={() => handleDelete(user.id)}
                >
                  <i className="bi bi-trash"></i>
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Modal para Crear/Editar Usuario */}
      <Modal show={showModal} onHide={handleCloseModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>{editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Usuario *</Form.Label>
              <Form.Control
                type="text"
                required
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                placeholder="Ingrese el nombre de usuario"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Contraseña {!editingUser && '*'}</Form.Label>
              <Form.Control
                type="password"
                required={!editingUser}
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                placeholder={editingUser ? "Dejar vacío para no cambiar" : "Ingrese la contraseña"}
              />
              {editingUser && <Form.Text className="text-muted">Dejar vacío para mantener la contraseña actual</Form.Text>}
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Email *</Form.Label>
              <Form.Control
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                placeholder="correo@ejemplo.com"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Nombre *</Form.Label>
              <Form.Control
                type="text"
                required
                value={formData.nombre}
                onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                placeholder="Ingrese el nombre"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Apellido *</Form.Label>
              <Form.Control
                type="text"
                required
                value={formData.apellido}
                onChange={(e) => setFormData({...formData, apellido: e.target.value})}
                placeholder="Ingrese el apellido"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Cédula Ecuatoriana *</Form.Label>
              <Form.Control
                type="text"
                required
                maxLength={10}
                value={formData.cedula}
                onChange={(e) => {
                  const valor = e.target.value.replace(/\D/g, '')
                  setFormData({...formData, cedula: valor})
                  if (valor.length === 10) {
                    const resultado = validarCedulaEcuatoriana(valor)
                    setCedulaError(resultado.valida ? '' : resultado.mensaje)
                  } else {
                    setCedulaError('')
                  }
                }}
                placeholder="1234567890"
                isInvalid={!!cedulaError}
                isValid={formData.cedula.length === 10 && !cedulaError}
              />
              <Form.Control.Feedback type="invalid">
                {cedulaError}
              </Form.Control.Feedback>
              <Form.Control.Feedback type="valid">
                ✓ Cédula ecuatoriana válida
              </Form.Control.Feedback>
              <Form.Text className="text-muted">
                Ingrese una cédula ecuatoriana válida de 10 dígitos
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Rol *</Form.Label>
              <Form.Select
                required
                value={formData.rol}
                onChange={(e) => setFormData({...formData, rol: e.target.value})}
              >
                <option value="doctor">Doctor</option>
                <option value="admin">Administrador</option>
              </Form.Select>
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancelar
            </Button>
            <Button variant="primary" type="submit">
              {editingUser ? 'Actualizar' : 'Crear'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </Container>
  )
}

export default Users
