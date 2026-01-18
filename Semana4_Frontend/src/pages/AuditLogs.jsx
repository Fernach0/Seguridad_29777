import { useState, useEffect } from 'react'
import { Container, Table, Form, Alert, Spinner, Badge, Card, Row, Col } from 'react-bootstrap'
import { auditService } from '../services/services'

const AuditLogs = () => {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  
  // Filtros
  const [filterAction, setFilterAction] = useState('')
  const [filterTable, setFilterTable] = useState('')
  const [filterUser, setFilterUser] = useState('')

  // Estadísticas
  const [stats, setStats] = useState({
    total: 0,
    porAccion: {},
    porTabla: {},
    recientes: 0
  })

  useEffect(() => {
    loadLogs()
  }, [])

  useEffect(() => {
    calculateStats()
  }, [logs])

  const loadLogs = async () => {
    try {
      setLoading(true)
      const response = await auditService.getAll()
      // El backend devuelve data.data.logs
      const logsData = response.success && response.data ? response.data.logs : []
      setLogs(logsData)
      setError('')
    } catch (err) {
      setError('Error al cargar logs de auditoría: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const calculateStats = () => {
    const porAccion = {}
    const porTabla = {}
    const hoy = new Date()
    hoy.setHours(0, 0, 0, 0)
    let recientes = 0

    logs.forEach(log => {
      // Contar por acción
      porAccion[log.accion] = (porAccion[log.accion] || 0) + 1

      // Contar por tabla
      if (log.tabla_afectada) {
        porTabla[log.tabla_afectada] = (porTabla[log.tabla_afectada] || 0) + 1
      }

      // Contar recientes (últimas 24h)
      const logDate = new Date(log.timestamp)
      if (logDate >= hoy) {
        recientes++
      }
    })

    setStats({
      total: logs.length,
      porAccion,
      porTabla,
      recientes
    })
  }

  const filteredLogs = logs.filter(log => {
    if (filterAction && log.accion !== filterAction) return false
    if (filterTable && log.tabla_afectada !== filterTable) return false
    if (filterUser && !log.usuario?.username.toLowerCase().includes(filterUser.toLowerCase())) return false
    return true
  })

  const uniqueActions = [...new Set(logs.map(l => l.accion))].sort()
  const uniqueTables = [...new Set(logs.map(l => l.tabla_afectada).filter(Boolean))].sort()

  const getActionBadge = (action) => {
    const badges = {
      'LOGIN': 'success',
      'LOGOUT': 'secondary',
      'CREATE': 'primary',
      'UPDATE': 'warning',
      'DELETE': 'danger',
      'READ': 'info'
    }
    return badges[action] || 'secondary'
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
      <h2 className="mb-4">📋 Logs de Auditoría</h2>

      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}

      {/* Estadísticas */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <h3 className="text-primary">{stats.total}</h3>
              <p className="mb-0 text-muted">Total de Eventos</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <h3 className="text-success">{stats.recientes}</h3>
              <p className="mb-0 text-muted">Últimas 24 Horas</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <h3 className="text-warning">{Object.keys(stats.porAccion).length}</h3>
              <p className="mb-0 text-muted">Tipos de Acciones</p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <h3 className="text-info">{Object.keys(stats.porTabla).length}</h3>
              <p className="mb-0 text-muted">Tablas Afectadas</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Resumen por Acción */}
      <Card className="mb-4">
        <Card.Header>
          <h5 className="mb-0">Distribución por Acción</h5>
        </Card.Header>
        <Card.Body>
          {Object.entries(stats.porAccion).map(([accion, count]) => (
            <Badge key={accion} bg={getActionBadge(accion)} className="me-2 mb-2">
              {accion}: {count}
            </Badge>
          ))}
        </Card.Body>
      </Card>

      {/* Filtros */}
      <Card className="mb-4">
        <Card.Header>
          <h5 className="mb-0">Filtros</h5>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Acción:</Form.Label>
                <Form.Select
                  value={filterAction}
                  onChange={(e) => setFilterAction(e.target.value)}
                >
                  <option value="">Todas las acciones</option>
                  {uniqueActions.map(action => (
                    <option key={action} value={action}>{action}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Tabla Afectada:</Form.Label>
                <Form.Select
                  value={filterTable}
                  onChange={(e) => setFilterTable(e.target.value)}
                >
                  <option value="">Todas las tablas</option>
                  {uniqueTables.map(table => (
                    <option key={table} value={table}>{table}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Usuario:</Form.Label>
                <Form.Control
                  type="text"
                  value={filterUser}
                  onChange={(e) => setFilterUser(e.target.value)}
                  placeholder="Buscar por usuario..."
                />
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Tabla de Logs */}
      <Card>
        <Card.Header>
          <h5 className="mb-0">Registros de Auditoría ({filteredLogs.length})</h5>
        </Card.Header>
        <Card.Body className="p-0">
          <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
            <Table striped hover className="mb-0">
              <thead className="sticky-top bg-light">
                <tr>
                  <th>ID</th>
                  <th>Fecha/Hora</th>
                  <th>Usuario</th>
                  <th>Acción</th>
                  <th>Tabla</th>
                  <th>Registro ID</th>
                  <th>IP</th>
                  <th>Detalles</th>
                </tr>
              </thead>
              <tbody>
                {filteredLogs.map(log => (
                  <tr key={log.id}>
                    <td>{log.id}</td>
                    <td>
                      <small>{new Date(log.timestamp).toLocaleString('es-EC')}</small>
                    </td>
                    <td>
                      {log.usuario ? (
                        <>
                          <strong>{log.usuario.username}</strong>
                          <br />
                          <small className="text-muted">{log.usuario.nombre_completo}</small>
                        </>
                      ) : (
                        <span className="text-muted">Sistema</span>
                      )}
                    </td>
                    <td>
                      <Badge bg={getActionBadge(log.accion)}>
                        {log.accion}
                      </Badge>
                    </td>
                    <td>
                      {log.tabla_afectada ? (
                        <code className="small">{log.tabla_afectada}</code>
                      ) : (
                        <span className="text-muted">N/A</span>
                      )}
                    </td>
                    <td>{log.registro_id || '-'}</td>
                    <td>
                      <code className="small">{log.ip_address || '-'}</code>
                    </td>
                    <td>
                      {log.datos_nuevos && (
                        <details>
                          <summary className="text-primary" style={{ cursor: 'pointer' }}>
                            Ver datos
                          </summary>
                          <pre className="small mt-2 mb-0" style={{ maxWidth: '300px', fontSize: '0.75rem' }}>
                            {JSON.stringify(log.datos_nuevos, null, 2)}
                          </pre>
                        </details>
                      )}
                      {log.datos_anteriores && (
                        <details>
                          <summary className="text-warning" style={{ cursor: 'pointer' }}>
                            Ver datos anteriores
                          </summary>
                          <pre className="small mt-2 mb-0" style={{ maxWidth: '300px', fontSize: '0.75rem' }}>
                            {JSON.stringify(log.datos_anteriores, null, 2)}
                          </pre>
                        </details>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        </Card.Body>
      </Card>

      {filteredLogs.length === 0 && (
        <Alert variant="info" className="mt-3">
          No hay logs que coincidan con los filtros seleccionados.
        </Alert>
      )}
    </Container>
  )
}

export default AuditLogs
