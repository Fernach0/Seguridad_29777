import { useState } from 'react'
import { Container, Card, Form, Button, Alert, Tabs, Tab, Row, Col, Badge } from 'react-bootstrap'
import { cryptoService } from '../services/services'

const CryptoDemo = () => {
  const [activeTab, setActiveTab] = useState('aes')
  const [result, setResult] = useState('')
  const [error, setError] = useState('')

  // AES
  const [aesText, setAesText] = useState('')
  const [aesEncrypted, setAesEncrypted] = useState('')

  // RSA
  const [rsaPublicKey, setRsaPublicKey] = useState('')
  const [rsaPrivateKey, setRsaPrivateKey] = useState('')
  const [rsaText, setRsaText] = useState('')
  const [rsaEncrypted, setRsaEncrypted] = useState('')

  // Hash SHA-256
  const [hashText, setHashText] = useState('')
  const [hashResult, setHashResult] = useState('')

  // Bcrypt
  const [bcryptPassword, setBcryptPassword] = useState('')
  const [bcryptHash, setBcryptHash] = useState('')
  const [bcryptVerifyPassword, setBcryptVerifyPassword] = useState('')
  const [bcryptVerifyHash, setBcryptVerifyHash] = useState('')

  // Caesar
  const [caesarText, setCaesarText] = useState('')
  const [caesarShift, setCaesarShift] = useState(3)
  const [caesarEncrypted, setCaesarEncrypted] = useState('')

  // Vigenere
  const [vigenereText, setVigenereText] = useState('')
  const [vigenereKey, setVigenereKey] = useState('')
  const [vigenereEncrypted, setVigenereEncrypted] = useState('')

  const handleAesEncrypt = async () => {
    try {
      setError('')
      const response = await cryptoService.aesEncrypt(aesText)
      setAesEncrypted(response.encrypted)
      setResult('Texto encriptado con AES-256-CBC exitosamente')
    } catch (err) {
      setError('Error al encriptar: ' + err.message)
    }
  }

  const handleAesDecrypt = async () => {
    try {
      setError('')
      const response = await cryptoService.aesDecrypt(aesEncrypted)
      setResult(`Texto desencriptado: "${response.decrypted}"`)
    } catch (err) {
      setError('Error al desencriptar: ' + err.message)
    }
  }

  const handleRsaGenerate = async () => {
    try {
      setError('')
      const response = await cryptoService.rsaGenerate()
      setRsaPublicKey(response.public_key)
      setRsaPrivateKey(response.private_key)
      setResult('Par de claves RSA-2048 generado exitosamente')
    } catch (err) {
      setError('Error al generar claves: ' + err.message)
    }
  }

  const handleRsaEncrypt = async () => {
    try {
      setError('')
      const response = await cryptoService.rsaEncrypt(rsaText, rsaPublicKey)
      setRsaEncrypted(response.encrypted)
      setResult('Texto encriptado con RSA exitosamente')
    } catch (err) {
      setError('Error al encriptar: ' + err.message)
    }
  }

  const handleRsaDecrypt = async () => {
    try {
      setError('')
      const response = await cryptoService.rsaDecrypt(rsaEncrypted, rsaPrivateKey)
      setResult(`Texto desencriptado: "${response.decrypted}"`)
    } catch (err) {
      setError('Error al desencriptar: ' + err.message)
    }
  }

  const handleHashGenerate = async () => {
    try {
      setError('')
      const response = await cryptoService.hashGenerate(hashText)
      setHashResult(response.hash)
      setResult('Hash SHA-256 generado exitosamente')
    } catch (err) {
      setError('Error al generar hash: ' + err.message)
    }
  }

  const handleHashVerify = async () => {
    try {
      setError('')
      const response = await cryptoService.hashVerify(hashText, hashResult)
      setResult(`Verificación: ${response.valid ? '✅ Hash válido' : '❌ Hash inválido'}`)
    } catch (err) {
      setError('Error al verificar hash: ' + err.message)
    }
  }

  const handleBcryptHash = async () => {
    try {
      setError('')
      const response = await cryptoService.bcryptHash(bcryptPassword)
      setBcryptHash(response.hash)
      setResult('Contraseña hasheada con bcrypt (factor 12) exitosamente')
    } catch (err) {
      setError('Error al hashear: ' + err.message)
    }
  }

  const handleBcryptVerify = async () => {
    try {
      setError('')
      const response = await cryptoService.bcryptVerify(bcryptVerifyPassword, bcryptVerifyHash)
      setResult(`Verificación: ${response.valid ? '✅ Contraseña correcta' : '❌ Contraseña incorrecta'}`)
    } catch (err) {
      setError('Error al verificar: ' + err.message)
    }
  }

  const handleCaesarEncrypt = async () => {
    try {
      setError('')
      const response = await cryptoService.caesarEncrypt(caesarText, caesarShift)
      setCaesarEncrypted(response.encrypted)
      setResult('Texto encriptado con Cifrado César exitosamente')
    } catch (err) {
      setError('Error al encriptar: ' + err.message)
    }
  }

  const handleCaesarDecrypt = async () => {
    try {
      setError('')
      const response = await cryptoService.caesarDecrypt(caesarEncrypted, caesarShift)
      setResult(`Texto desencriptado: "${response.decrypted}"`)
    } catch (err) {
      setError('Error al desencriptar: ' + err.message)
    }
  }

  const handleVigenereEncrypt = async () => {
    try {
      setError('')
      const response = await cryptoService.vigenereEncrypt(vigenereText, vigenereKey)
      setVigenereEncrypted(response.encrypted)
      setResult('Texto encriptado con Cifrado Vigenère exitosamente')
    } catch (err) {
      setError('Error al encriptar: ' + err.message)
    }
  }

  const handleVigenereDecrypt = async () => {
    try {
      setError('')
      const response = await cryptoService.vigenereDecrypt(vigenereEncrypted, vigenereKey)
      setResult(`Texto desencriptado: "${response.decrypted}"`)
    } catch (err) {
      setError('Error al desencriptar: ' + err.message)
    }
  }

  return (
    <Container className="py-4">
      <h2 className="mb-4">🔐 Demostración de Técnicas Criptográficas</h2>
      
      {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}
      {result && <Alert variant="success" onClose={() => setResult('')} dismissible>{result}</Alert>}

      <Tabs activeKey={activeTab} onSelect={(k) => setActiveTab(k)} className="mb-3">
        {/* AES */}
        <Tab eventKey="aes" title="🔒 AES-256">
          <Card>
            <Card.Header className="bg-primary text-white">
              <h5 className="mb-0">Encriptación Simétrica AES-256-CBC</h5>
            </Card.Header>
            <Card.Body>
              <p className="text-muted">
                Advanced Encryption Standard con clave de 256 bits en modo CBC (Cipher Block Chaining).
                Usa la misma clave maestra configurada en el servidor.
              </p>
              
              <Form.Group className="mb-3">
                <Form.Label>Texto a Encriptar:</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={aesText}
                  onChange={(e) => setAesText(e.target.value)}
                  placeholder="Ingrese el texto que desea encriptar..."
                />
              </Form.Group>

              <Button variant="primary" onClick={handleAesEncrypt} className="me-2">
                🔒 Encriptar
              </Button>
              <Button variant="secondary" onClick={handleAesDecrypt} disabled={!aesEncrypted}>
                🔓 Desencriptar
              </Button>

              {aesEncrypted && (
                <div className="mt-3">
                  <Form.Label>Texto Encriptado (Base64):</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
                    value={aesEncrypted}
                    readOnly
                    className="bg-light"
                  />
                </div>
              )}
            </Card.Body>
          </Card>
        </Tab>

        {/* RSA */}
        <Tab eventKey="rsa" title="🔑 RSA-2048">
          <Card>
            <Card.Header className="bg-success text-white">
              <h5 className="mb-0">Encriptación Asimétrica RSA-2048</h5>
            </Card.Header>
            <Card.Body>
              <p className="text-muted">
                Rivest–Shamir–Adleman con claves de 2048 bits. Genera un par de claves (pública/privada).
              </p>

              <Button variant="success" onClick={handleRsaGenerate} className="mb-3">
                🎲 Generar Par de Claves RSA
              </Button>

              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Clave Pública:</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={5}
                      value={rsaPublicKey}
                      readOnly
                      className="bg-light font-monospace small"
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Clave Privada:</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={5}
                      value={rsaPrivateKey}
                      readOnly
                      className="bg-light font-monospace small"
                    />
                  </Form.Group>
                </Col>
              </Row>

              <Form.Group className="mb-3">
                <Form.Label>Texto a Encriptar:</Form.Label>
                <Form.Control
                  type="text"
                  value={rsaText}
                  onChange={(e) => setRsaText(e.target.value)}
                  placeholder="Mensaje corto (máx. 190 caracteres por limitación RSA)"
                />
              </Form.Group>

              <Button 
                variant="primary" 
                onClick={handleRsaEncrypt} 
                className="me-2"
                disabled={!rsaPublicKey || !rsaText}
              >
                🔒 Encriptar con Clave Pública
              </Button>
              <Button 
                variant="secondary" 
                onClick={handleRsaDecrypt}
                disabled={!rsaPrivateKey || !rsaEncrypted}
              >
                🔓 Desencriptar con Clave Privada
              </Button>

              {rsaEncrypted && (
                <div className="mt-3">
                  <Form.Label>Texto Encriptado (Base64):</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    value={rsaEncrypted}
                    readOnly
                    className="bg-light font-monospace small"
                  />
                </div>
              )}
            </Card.Body>
          </Card>
        </Tab>

        {/* SHA-256 */}
        <Tab eventKey="hash" title="🔗 SHA-256">
          <Card>
            <Card.Header className="bg-info text-white">
              <h5 className="mb-0">Hash Criptográfico SHA-256</h5>
            </Card.Header>
            <Card.Body>
              <p className="text-muted">
                Secure Hash Algorithm 256 bits. Genera un hash de longitud fija (64 caracteres hex) para cualquier entrada.
                Útil para verificar integridad de datos.
              </p>

              <Form.Group className="mb-3">
                <Form.Label>Texto para Hashear:</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={hashText}
                  onChange={(e) => setHashText(e.target.value)}
                  placeholder="Ingrese cualquier texto..."
                />
              </Form.Group>

              <Button variant="info" onClick={handleHashGenerate} className="me-2">
                🔗 Generar Hash
              </Button>
              <Button variant="secondary" onClick={handleHashVerify} disabled={!hashResult}>
                ✅ Verificar Integridad
              </Button>

              {hashResult && (
                <div className="mt-3">
                  <Form.Label>Hash SHA-256:</Form.Label>
                  <Form.Control
                    type="text"
                    value={hashResult}
                    readOnly
                    className="bg-light font-monospace"
                  />
                  <Form.Text className="text-muted">
                    Este hash es único para el contenido. Cualquier cambio generará un hash completamente diferente.
                  </Form.Text>
                </div>
              )}
            </Card.Body>
          </Card>
        </Tab>

        {/* Bcrypt */}
        <Tab eventKey="bcrypt" title="🔐 Bcrypt">
          <Card>
            <Card.Header className="bg-warning text-dark">
              <h5 className="mb-0">Hashing de Contraseñas con Bcrypt</h5>
            </Card.Header>
            <Card.Body>
              <p className="text-muted">
                Función de derivación de claves basada en el cifrado Blowfish. Factor de costo: 12 (4096 rondas).
                Incluye salt automático para proteger contra rainbow tables.
              </p>

              <h6>Generar Hash de Contraseña</h6>
              <Form.Group className="mb-3">
                <Form.Label>Contraseña:</Form.Label>
                <Form.Control
                  type="text"
                  value={bcryptPassword}
                  onChange={(e) => setBcryptPassword(e.target.value)}
                  placeholder="Ingrese una contraseña..."
                />
              </Form.Group>

              <Button variant="warning" onClick={handleBcryptHash} className="mb-4">
                🔐 Hashear Contraseña
              </Button>

              {bcryptHash && (
                <div className="mb-4">
                  <Form.Label>Hash Bcrypt:</Form.Label>
                  <Form.Control
                    type="text"
                    value={bcryptHash}
                    readOnly
                    className="bg-light font-monospace small"
                  />
                </div>
              )}

              <hr />

              <h6>Verificar Contraseña</h6>
              <Form.Group className="mb-3">
                <Form.Label>Contraseña a Verificar:</Form.Label>
                <Form.Control
                  type="text"
                  value={bcryptVerifyPassword}
                  onChange={(e) => setBcryptVerifyPassword(e.target.value)}
                  placeholder="Ingrese la contraseña..."
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Hash Bcrypt:</Form.Label>
                <Form.Control
                  type="text"
                  value={bcryptVerifyHash}
                  onChange={(e) => setBcryptVerifyHash(e.target.value)}
                  placeholder="Pegue el hash bcrypt..."
                />
              </Form.Group>

              <Button variant="success" onClick={handleBcryptVerify}>
                ✅ Verificar Contraseña
              </Button>
            </Card.Body>
          </Card>
        </Tab>

        {/* Caesar */}
        <Tab eventKey="caesar" title="📜 César">
          <Card>
            <Card.Header className="bg-secondary text-white">
              <h5 className="mb-0">Cifrado César (Clásico)</h5>
            </Card.Header>
            <Card.Body>
              <p className="text-muted">
                Uno de los cifrados más antiguos. Desplaza cada letra del alfabeto un número fijo de posiciones.
                Ejemplo histórico: Julio César usaba desplazamiento de 3.
              </p>

              <Form.Group className="mb-3">
                <Form.Label>Texto:</Form.Label>
                <Form.Control
                  type="text"
                  value={caesarText}
                  onChange={(e) => setCaesarText(e.target.value)}
                  placeholder="Solo letras (a-z, A-Z)"
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Desplazamiento (1-25):</Form.Label>
                <Form.Control
                  type="number"
                  min="1"
                  max="25"
                  value={caesarShift}
                  onChange={(e) => setCaesarShift(parseInt(e.target.value))}
                />
              </Form.Group>

              <Button variant="secondary" onClick={handleCaesarEncrypt} className="me-2">
                🔒 Encriptar
              </Button>
              <Button variant="dark" onClick={handleCaesarDecrypt} disabled={!caesarEncrypted}>
                🔓 Desencriptar
              </Button>

              {caesarEncrypted && (
                <div className="mt-3">
                  <Form.Label>Resultado:</Form.Label>
                  <Form.Control
                    type="text"
                    value={caesarEncrypted}
                    readOnly
                    className="bg-light"
                  />
                </div>
              )}
            </Card.Body>
          </Card>
        </Tab>

        {/* Vigenere */}
        <Tab eventKey="vigenere" title="📖 Vigenère">
          <Card>
            <Card.Header className="bg-dark text-white">
              <h5 className="mb-0">Cifrado Vigenère (Polialfabético)</h5>
            </Card.Header>
            <Card.Body>
              <p className="text-muted">
                Mejora del cifrado César usando una palabra clave. Cada letra de la clave determina un desplazamiento diferente.
                Más seguro que César pero aún vulnerable a análisis de frecuencia.
              </p>

              <Form.Group className="mb-3">
                <Form.Label>Texto:</Form.Label>
                <Form.Control
                  type="text"
                  value={vigenereText}
                  onChange={(e) => setVigenereText(e.target.value)}
                  placeholder="Solo letras (a-z, A-Z)"
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Palabra Clave:</Form.Label>
                <Form.Control
                  type="text"
                  value={vigenereKey}
                  onChange={(e) => setVigenereKey(e.target.value)}
                  placeholder="Ej: SECRETO"
                />
              </Form.Group>

              <Button variant="dark" onClick={handleVigenereEncrypt} className="me-2">
                🔒 Encriptar
              </Button>
              <Button variant="secondary" onClick={handleVigenereDecrypt} disabled={!vigenereEncrypted}>
                🔓 Desencriptar
              </Button>

              {vigenereEncrypted && (
                <div className="mt-3">
                  <Form.Label>Resultado:</Form.Label>
                  <Form.Control
                    type="text"
                    value={vigenereEncrypted}
                    readOnly
                    className="bg-light"
                  />
                </div>
              )}
            </Card.Body>
          </Card>
        </Tab>
      </Tabs>

      {/* Info adicional */}
      <Card className="mt-4 border-primary">
        <Card.Body>
          <h5 className="text-primary">
            <i className="bi bi-info-circle"></i> Información del Proyecto
          </h5>
          <p className="mb-2">
            <Badge bg="primary">AES-256-CBC</Badge> Encriptación simétrica moderna para datos sensibles (alergias, antecedentes, historias clínicas)
          </p>
          <p className="mb-2">
            <Badge bg="success">RSA-2048</Badge> Encriptación asimétrica para intercambio seguro de claves
          </p>
          <p className="mb-2">
            <Badge bg="info">SHA-256</Badge> Hash para verificar integridad de historias clínicas
          </p>
          <p className="mb-2">
            <Badge bg="warning" text="dark">Bcrypt</Badge> Hashing de contraseñas con factor de costo 12
          </p>
          <p className="mb-0">
            <Badge bg="secondary">César & Vigenère</Badge> Cifrados clásicos con propósito educativo
          </p>
        </Card.Body>
      </Card>
    </Container>
  )
}

export default CryptoDemo
