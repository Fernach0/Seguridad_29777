import { useState, useEffect } from 'react'
import { Container, Table, Button, Modal, Form, Alert, Badge, Spinner, Card, Row, Col } from 'react-bootstrap'
import { patientService } from '../services/services'
import { validarCedulaEcuatoriana } from '../utils/validators'

const Patients = () => {
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [cedulaError, setCedulaError] = useState('')
  
  const [showModal, setShowModal] = useState(false)
  const [editingPatient, setEditingPatient] = useState(null)
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    cedula: '',
    fecha_nacimiento: '',
    genero: 'M',
    direccion: '',
    telefono: '',
    email: '',
    tipo_sangre: '',
    alergias: '',
    antecedentes: ''
  })

  useEffect(() => {
    loadPatients()
  }, [])

  const loadPatients = async () => {
    try {
      setLoading(true)
      const data = await patientService.getAll()
      setPatients(data)
      setError('')
    } catch (err) {
      setError('Error al cargar pacientes: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleShowModal = (patient = null) => {
    setCedulaError('')
    if (patient) {
      setEditingPatient(patient)
      setFormData({
        nombre: patient.nombre,
        apellido: patient.apellido,
        cedula: patient.cedula,
        fecha_nacimiento: patient.fecha_nacimiento,
        genero: patient.genero,
        direccion: patient.direccion || '',
        telefono: patient.telefono || '',
        email: patient.email || '',
        tipo_sangre: patient.tipo_sangre || '',
        alergias: patient.alergias || '',
        antecedentes: patient.antecedentes || ''
      })
    } else {
      setEditingPatient(null)
      setFormData({
        nombre: '',
        apellido: '',
        cedula: '',
        fecha_nacimiento: '',
        genero: 'M',
        direccion: '',
        telefono: '',
        email: '',
        tipo_sangre: '',
        alergias: '',
        antecedentes: ''
      })
    }
    setShowModal(true)
  }

  const handleCloseModal = () => {
    setShowModal(false)
    setCedulaError('')
    setEditingPatient(null)
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
      if (editingPatient) {
        await patientService.update(editingPatient.id, formData)
        setSuccess('Paciente actualizado exitosamente')
      } else {
        await patientService.create(formData)
        setSuccess('Paciente creado exitosamente')
      }
      
      handleCloseModal()
      loadPatients()
      
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Error al guardar paciente: ' + err.message)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este paciente y todos sus registros médicos?')) {
      try {
        await patientService.delete(id)
        setSuccess('Paciente eliminado exitosamente')
        loadPatients()
        setTimeout(() => setSuccess(''), 3000)
      } catch (err) {
        setError('Error al eliminar paciente: ' + err.message)
      }
    }
  }

  const calcularEdad = (fechaNacimiento) => {
    const hoy = new Date()
    const nacimiento = new Date(fechaNacimiento)
    let edad = hoy.getFullYear() - nacimiento.getFullYear()
    const mes = hoy.getMonth() - nacimiento.getMonth()
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--
    }
    return edad
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
        <h2>Gestión de Pacientes</h2>
        <Button variant="primary" onClick={() => handleShowModal()}>
          <i className="bi bi-plus-circle"></i> Nuevo Paciente
        </Button>
      </div>

      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')} dismissible>{success}</Alert>}

      <Row>
        {patients.map(patient => (
          <Col md={6} lg={4} key={patient.id} className="mb-4">
            <Card>
              <Card.Header className="bg-primary text-white">
                <h5 className="mb-0">{patient.nombre} {patient.apellido}</h5>
              </Card.Header>
              <Card.Body>
                <p className="mb-2"><strong>Cédula:</strong> {patient.cedula}</p>
                <p className="mb-2"><strong>Edad:</strong> {calcularEdad(patient.fecha_nacimiento)} años</p>
                <p className="mb-2"><strong>Género:</strong> {patient.genero === 'M' ? 'Masculino' : 'Femenino'}</p>
                <p className="mb-2"><strong>Tipo de Sangre:</strong> {patient.tipo_sangre || 'No especificado'}</p>
                <p className="mb-2"><strong>Teléfono:</strong> {patient.telefono || 'No especificado'}</p>
                <p className="mb-2"><strong>Email:</strong> {patient.email || 'No especificado'}</p>
                
                {patient.alergias && (
                  <div className="mb-2">
                    <Badge bg="warning" text="dark">
                      <i className="bi bi-exclamation-triangle"></i> Alergias
                    </Badge>
                    <small className="d-block mt-1 text-muted">
                      {patient.alergias.length > 50 ? patient.alergias.substring(0, 50) + '...' : patient.alergias}
                    </small>
                  </div>
                )}
                
                {patient.antecedentes && (
                  <div className="mb-2">
                    <Badge bg="info">
                      <i className="bi bi-clipboard-pulse"></i> Antecedentes
                    </Badge>
                    <small className="d-block mt-1 text-muted">
                      {patient.antecedentes.length > 50 ? patient.antecedentes.substring(0, 50) + '...' : patient.antecedentes}
                    </small>
                  </div>
                )}
              </Card.Body>
              <Card.Footer>
                <Button 
                  variant="warning" 
                  size="sm" 
                  className="me-2"
                  onClick={() => handleShowModal(patient)}
                >
                  <i className="bi bi-pencil"></i> Editar
                </Button>
                <Button 
                  variant="danger" 
                  size="sm"
                  onClick={() => handleDelete(patient.id)}
                >
                  <i className="bi bi-trash"></i> Eliminar
                </Button>
              </Card.Footer>
            </Card>
          </Col>
        ))}
      </Row>

      {patients.length === 0 && (
        <Alert variant="info">
          No hay pacientes registrados. Haga clic en "Nuevo Paciente" para agregar uno.
        </Alert>
      )}

      {/* Modal para Crear/Editar Paciente */}
      <Modal show={showModal} onHide={handleCloseModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>{editingPatient ? 'Editar Paciente' : 'Nuevo Paciente'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            <Row>
              <Col md={6}>
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
              </Col>
              <Col md={6}>
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
              </Col>
            </Row>

            <Row>
              <Col md={6}>
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
                    Cédula ecuatoriana válida de 10 dígitos
                  </Form.Text>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Fecha de Nacimiento *</Form.Label>
                  <Form.Label>Fecha de Nacimiento *</Form.Label>
                  <Form.Control
                    type="date"
                    required
                    value={formData.fecha_nacimiento}
                    onChange={(e) => setFormData({...formData, fecha_nacimiento: e.target.value})}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Género *</Form.Label>
                  <Form.Select
                    required
                    value={formData.genero}
                    onChange={(e) => setFormData({...formData, genero: e.target.value})}
                  >
                    <option value="M">Masculino</option>
                    <option value="F">Femenino</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Tipo de Sangre</Form.Label>
                  <Form.Select
                    value={formData.tipo_sangre}
                    onChange={(e) => setFormData({...formData, tipo_sangre: e.target.value})}
                  >
                    <option value="">Seleccionar...</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Dirección</Form.Label>
              <Form.Control
                type="text"
                value={formData.direccion}
                onChange={(e) => setFormData({...formData, direccion: e.target.value})}
                placeholder="Ingrese la dirección"
              />
            </Form.Group>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Teléfono</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.telefono}
                    onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                    placeholder="0987654321"
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    placeholder="paciente@ejemplo.com"
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Alergias 🔒 (Encriptado)</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                value={formData.alergias}
                onChange={(e) => setFormData({...formData, alergias: e.target.value})}
                placeholder="Describa las alergias del paciente (este campo será encriptado)"
              />
              <Form.Text className="text-muted">
                <i className="bi bi-lock-fill"></i> Esta información se almacena encriptada con AES-256
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Antecedentes Médicos 🔒 (Encriptado)</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.antecedentes}
                onChange={(e) => setFormData({...formData, antecedentes: e.target.value})}
                placeholder="Describa los antecedentes médicos del paciente (este campo será encriptado)"
              />
              <Form.Text className="text-muted">
                <i className="bi bi-lock-fill"></i> Esta información se almacena encriptada con AES-256
              </Form.Text>
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancelar
            </Button>
            <Button variant="primary" type="submit">
              {editingPatient ? 'Actualizar' : 'Crear'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </Container>
  )
}

export default Patients
