import { useState, useEffect } from 'react'
import { Container, Table, Button, Modal, Form, Alert, Badge, Spinner, Card, Row, Col } from 'react-bootstrap'
import { medicalRecordService, patientService } from '../services/services'

const MedicalRecords = () => {
  const [records, setRecords] = useState([])
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  
  const [showModal, setShowModal] = useState(false)
  const [editingRecord, setEditingRecord] = useState(null)
  const [formData, setFormData] = useState({
    paciente_id: '',
    fecha_consulta: new Date().toISOString().split('T')[0], // Fecha de hoy por defecto
    sintomas: '',
    diagnostico: '',
    tratamiento: '',
    recetas: [{ medicamento: '', dosis: '', frecuencia: '', duracion: '' }]
  })

  const [selectedPatient, setSelectedPatient] = useState('')

  useEffect(() => {
    loadRecords()
    loadPatients()
  }, [])

  const loadRecords = async () => {
    try {
      setLoading(true)
      const data = await medicalRecordService.getAll()
      setRecords(data)
      setError('')
    } catch (err) {
      setError('Error al cargar historias clínicas: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const loadPatients = async () => {
    try {
      const data = await patientService.getAll()
      setPatients(data)
    } catch (err) {
      console.error('Error al cargar pacientes:', err)
    }
  }

  const handleShowModal = (record = null) => {
    if (record) {
      setEditingRecord(record)
      setFormData({
        paciente_id: record.paciente_id,
        fecha_consulta: record.fecha_consulta || new Date().toISOString().split('T')[0],
        sintomas: record.sintomas || '',
        diagnostico: record.diagnostico || '',
        tratamiento: record.tratamiento || '',
        recetas: record.recetas && record.recetas.length > 0 ? record.recetas : [{ medicamento: '', dosis: '', frecuencia: '', duracion: '' }]
      })
    } else {
      setEditingRecord(null)
      setFormData({
        paciente_id: '',
        fecha_consulta: new Date().toISOString().split('T')[0],
        sintomas: '',
        diagnostico: '',
        tratamiento: '',
        recetas: [{ medicamento: '', dosis: '', frecuencia: '', duracion: '' }]
      })
    }
    setShowModal(true)
  }

  const handleCloseModal = () => {
    setShowModal(false)
    setEditingRecord(null)
  }

  const handleAddReceta = () => {
    setFormData({
      ...formData,
      recetas: [...formData.recetas, { medicamento: '', dosis: '', frecuencia: '', duracion: '' }]
    })
  }

  const handleRemoveReceta = (index) => {
    const newRecetas = formData.recetas.filter((_, i) => i !== index)
    setFormData({ ...formData, recetas: newRecetas })
  }

  const handleRecetaChange = (index, field, value) => {
    const newRecetas = [...formData.recetas]
    newRecetas[index][field] = value
    setFormData({ ...formData, recetas: newRecetas })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    // Filtrar recetas vacías
    const recetasValidas = formData.recetas.filter(r => 
      r.medicamento.trim() !== '' || r.dosis.trim() !== '' || r.frecuencia.trim() !== '' || r.duracion.trim() !== ''
    )

    const dataToSend = {
      ...formData,
      recetas: recetasValidas
    }

    try {
      if (editingRecord) {
        await medicalRecordService.update(editingRecord.id, dataToSend)
        setSuccess('Historia clínica actualizada exitosamente')
      } else {
        await medicalRecordService.create(dataToSend)
        setSuccess('Historia clínica creada exitosamente')
      }
      
      handleCloseModal()
      loadRecords()
      
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError('Error al guardar historia clínica: ' + err.message)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar esta historia clínica?')) {
      try {
        await medicalRecordService.delete(id)
        setSuccess('Historia clínica eliminada exitosamente')
        loadRecords()
        setTimeout(() => setSuccess(''), 3000)
      } catch (err) {
        setError('Error al eliminar historia clínica: ' + err.message)
      }
    }
  }

  const getPatientName = (pacienteId) => {
    const patient = patients.find(p => p.id === pacienteId)
    return patient ? `${patient.nombre} ${patient.apellido}` : 'Paciente Desconocido'
  }

  const filteredRecords = selectedPatient 
    ? records.filter(r => r.paciente_id === parseInt(selectedPatient))
    : records

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
        <h2>Historias Clínicas</h2>
        <Button variant="primary" onClick={() => handleShowModal()}>
          <i className="bi bi-plus-circle"></i> Nueva Historia
        </Button>
      </div>

      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      {success && <Alert variant="success" onClose={() => setSuccess('')} dismissible>{success}</Alert>}

      {/* Filtro por Paciente */}
      <Row className="mb-4">
        <Col md={6}>
          <Form.Group>
            <Form.Label>Filtrar por Paciente:</Form.Label>
            <Form.Select
              value={selectedPatient}
              onChange={(e) => setSelectedPatient(e.target.value)}
            >
              <option value="">Todos los pacientes</option>
              {patients.map(patient => (
                <option key={patient.id} value={patient.id}>
                  {patient.nombre} {patient.apellido} - {patient.cedula}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
        </Col>
      </Row>

      {/* Lista de Historias Clínicas */}
      <Row>
        {filteredRecords.map(record => (
          <Col md={6} key={record.id} className="mb-4">
            <Card>
              <Card.Header className="bg-success text-white">
                <div className="d-flex justify-content-between align-items-center">
                  <h5 className="mb-0">
                    <i className="bi bi-file-medical"></i> {getPatientName(record.paciente_id)}
                  </h5>
                  <Badge bg="light" text="dark">
                    {new Date(record.fecha_consulta).toLocaleDateString()}
                  </Badge>
                </div>
              </Card.Header>
              <Card.Body>
                <div className="mb-3">
                  <strong className="text-primary">
                    <i className="bi bi-thermometer"></i> Síntomas:
                  </strong>
                  <p className="mb-0 ms-3">{record.sintomas}</p>
                </div>

                <div className="mb-3">
                  <strong className="text-success">
                    <i className="bi bi-clipboard-check"></i> Diagnóstico:
                  </strong>
                  <p className="mb-0 ms-3">{record.diagnostico}</p>
                </div>

                <div className="mb-3">
                  <strong className="text-info">
                    <i className="bi bi-prescription2"></i> Tratamiento:
                  </strong>
                  <p className="mb-0 ms-3">{record.tratamiento}</p>
                </div>

                {record.recetas && record.recetas.length > 0 && (
                  <div className="mb-3">
                    <strong className="text-warning">
                      <i className="bi bi-capsule"></i> Recetas:
                    </strong>
                    <ul className="ms-3 mb-0">
                      {record.recetas.map((receta, idx) => (
                        <li key={idx}>
                          <strong>{receta.medicamento}</strong> - {receta.dosis}, {receta.frecuencia}, por {receta.duracion}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {record.hash_integridad && (
                  <div className="mt-3">
                    <Badge bg="secondary">
                      <i className="bi bi-shield-check"></i> Integridad Verificada (SHA-256)
                    </Badge>
                  </div>
                )}
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">
                  Doctor: {record.doctor?.nombre_completo || 'N/A'}
                </small>
                <div className="mt-2">
                  <Button 
                    variant="warning" 
                    size="sm" 
                    className="me-2"
                    onClick={() => handleShowModal(record)}
                  >
                    <i className="bi bi-pencil"></i> Editar
                  </Button>
                  <Button 
                    variant="danger" 
                    size="sm"
                    onClick={() => handleDelete(record.id)}
                  >
                    <i className="bi bi-trash"></i> Eliminar
                  </Button>
                </div>
              </Card.Footer>
            </Card>
          </Col>
        ))}
      </Row>

      {filteredRecords.length === 0 && (
        <Alert variant="info">
          No hay historias clínicas registradas para este filtro.
        </Alert>
      )}

      {/* Modal para Crear/Editar Historia Clínica */}
      <Modal show={showModal} onHide={handleCloseModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>{editingRecord ? 'Editar Historia Clínica' : 'Nueva Historia Clínica'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Paciente *</Form.Label>
              <Form.Select
                required
                value={formData.paciente_id}
                onChange={(e) => setFormData({...formData, paciente_id: e.target.value})}
                disabled={editingRecord}
              >
                <option value="">Seleccione un paciente...</option>
                {patients.map(patient => (
                  <option key={patient.id} value={patient.id}>
                    {patient.nombre} {patient.apellido} - {patient.cedula}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Fecha de Consulta *</Form.Label>
              <Form.Control
                type="date"
                required
                value={formData.fecha_consulta}
                onChange={(e) => setFormData({...formData, fecha_consulta: e.target.value})}
                max={new Date().toISOString().split('T')[0]}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Síntomas 🔒 (Encriptado) *</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                required
                value={formData.sintomas}
                onChange={(e) => setFormData({...formData, sintomas: e.target.value})}
                placeholder="Describa los síntomas del paciente"
              />
              <Form.Text className="text-muted">
                <i className="bi bi-lock-fill"></i> Esta información se almacena encriptada con AES-256
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Diagnóstico 🔒 (Encriptado) *</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                required
                value={formData.diagnostico}
                onChange={(e) => setFormData({...formData, diagnostico: e.target.value})}
                placeholder="Ingrese el diagnóstico médico"
              />
              <Form.Text className="text-muted">
                <i className="bi bi-lock-fill"></i> Esta información se almacena encriptada con AES-256
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Tratamiento 🔒 (Encriptado) *</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                required
                value={formData.tratamiento}
                onChange={(e) => setFormData({...formData, tratamiento: e.target.value})}
                placeholder="Describa el tratamiento recomendado"
              />
              <Form.Text className="text-muted">
                <i className="bi bi-lock-fill"></i> Esta información se almacena encriptada con AES-256
              </Form.Text>
            </Form.Group>

            <hr />
            <h5>Recetas Médicas</h5>
            {formData.recetas.map((receta, index) => (
              <Card key={index} className="mb-3">
                <Card.Body>
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-2">
                        <Form.Label>Medicamento</Form.Label>
                        <Form.Control
                          type="text"
                          value={receta.medicamento}
                          onChange={(e) => handleRecetaChange(index, 'medicamento', e.target.value)}
                          placeholder="Nombre del medicamento"
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-2">
                        <Form.Label>Dosis</Form.Label>
                        <Form.Control
                          type="text"
                          value={receta.dosis}
                          onChange={(e) => handleRecetaChange(index, 'dosis', e.target.value)}
                          placeholder="Ej: 500mg"
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-2">
                        <Form.Label>Frecuencia</Form.Label>
                        <Form.Control
                          type="text"
                          value={receta.frecuencia}
                          onChange={(e) => handleRecetaChange(index, 'frecuencia', e.target.value)}
                          placeholder="Ej: Cada 8 horas"
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-2">
                        <Form.Label>Duración</Form.Label>
                        <Form.Control
                          type="text"
                          value={receta.duracion}
                          onChange={(e) => handleRecetaChange(index, 'duracion', e.target.value)}
                          placeholder="Ej: 7 días"
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  {formData.recetas.length > 1 && (
                    <Button 
                      variant="danger" 
                      size="sm" 
                      onClick={() => handleRemoveReceta(index)}
                    >
                      <i className="bi bi-trash"></i> Eliminar Receta
                    </Button>
                  )}
                </Card.Body>
              </Card>
            ))}
            <Button variant="secondary" size="sm" onClick={handleAddReceta}>
              <i className="bi bi-plus-circle"></i> Agregar Receta
            </Button>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancelar
            </Button>
            <Button variant="primary" type="submit">
              {editingRecord ? 'Actualizar' : 'Crear'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </Container>
  )
}

export default MedicalRecords
