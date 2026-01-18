import api from './api'

export const authService = {
  async login(username, password) {
    const response = await api.post('/auth/login', { username, password })
    if (response.data.success && response.data.data.token) {
      localStorage.setItem('token', response.data.data.token)
      localStorage.setItem('user', JSON.stringify(response.data.data.user))
    }
    return response.data
  },

  async logout() {
    try {
      await api.post('/auth/logout')
    } finally {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  getStoredUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },

  getToken() {
    return localStorage.getItem('token')
  },

  isAuthenticated() {
    return !!this.getToken()
  }
}

export const userService = {
  async getAll(params = {}) {
    const response = await api.get('/users', { params })
    // El backend devuelve data.users dentro de data
    if (response.data.success && response.data.data) {
      return response.data.data.users || []
    }
    return response.data.users || []
  },

  async getById(id) {
    const response = await api.get(`/users/${id}`)
    return response.data.data || response.data
  },

  async create(userData) {
    const response = await api.post('/users', userData)
    return response.data.data || response.data
  },

  async update(id, userData) {
    const response = await api.put(`/users/${id}`, userData)
    return response.data.data || response.data
  },

  async delete(id) {
    const response = await api.delete(`/users/${id}`)
    return response.data
  },

  // Alias para mantener compatibilidad
  getUsers(params) { return this.getAll(params) },
  getUserById(id) { return this.getById(id) },
  createUser(userData) { return this.create(userData) },
  updateUser(id, userData) { return this.update(id, userData) },
  deleteUser(id) { return this.delete(id) }
}

export const patientService = {
  async getAll(params = {}) {
    const response = await api.get('/patients', { params })
    return response.data.data || response.data
  },

  async getById(id) {
    const response = await api.get(`/patients/${id}`)
    return response.data.data || response.data
  },

  async create(patientData) {
    const response = await api.post('/patients', patientData)
    return response.data.data || response.data
  },

  async update(id, patientData) {
    const response = await api.put(`/patients/${id}`, patientData)
    return response.data.data || response.data
  },

  async delete(id) {
    const response = await api.delete(`/patients/${id}`)
    return response.data
  },

  // Alias para mantener compatibilidad
  getPatients(params) { return this.getAll(params) },
  getPatientById(id) { return this.getById(id) },
  createPatient(patientData) { return this.create(patientData) },
  updatePatient(id, patientData) { return this.update(id, patientData) },
  deletePatient(id) { return this.delete(id) }
}

export const medicalRecordService = {
  async getAll() {
    const response = await api.get('/medical-records')
    return response.data || []
  },

  async getById(id) {
    const response = await api.get(`/medical-records/${id}`)
    return response.data
  },

  async create(recordData) {
    const response = await api.post('/medical-records', recordData)
    return response.data
  },

  async update(id, recordData) {
    const response = await api.put(`/medical-records/${id}`, recordData)
    return response.data
  },

  async delete(id) {
    const response = await api.delete(`/medical-records/${id}`)
    return response.data
  },

  // Alias methods for backward compatibility
  async getRecordsByPatient(patientId) {
    const response = await api.get(`/medical-records/paciente/${patientId}`)
    return response.data
  },

  getRecordById(id) { return this.getById(id) },
  createRecord(recordData) { return this.create(recordData) },

  async getMyRecords() {
    const response = await api.get('/medical-records/mine')
    return response.data
  }
}

export const auditService = {
  async getAll(params = {}) {
    const response = await api.get('/audit-logs', { params })
    return response.data
  },

  async getAuditLogs(params = {}) {
    const response = await api.get('/audit-logs', { params })
    return response.data
  },

  async getUserAuditLogs(userId, params = {}) {
    const response = await api.get(`/audit-logs/user/${userId}`, { params })
    return response.data
  },

  async getAuditStats() {
    const response = await api.get('/audit-logs/stats')
    return response.data
  }
}

export const cryptoService = {
  async aesEncrypt(plaintext) {
    const response = await api.post('/crypto/aes/encrypt', { plaintext })
    return response.data
  },

  async aesDecrypt(ciphertext, iv) {
    const response = await api.post('/crypto/aes/decrypt', { ciphertext, iv })
    return response.data
  },

  async rsaGenerate() {
    const response = await api.post('/crypto/rsa/generate')
    return response.data
  },

  async rsaEncrypt(plaintext, public_key) {
    const response = await api.post('/crypto/rsa/encrypt', { plaintext, public_key })
    return response.data
  },

  async rsaDecrypt(ciphertext, private_key) {
    const response = await api.post('/crypto/rsa/decrypt', { ciphertext, private_key })
    return response.data
  },

  async sha256Hash(data) {
    const response = await api.post('/crypto/hash/sha256', { data })
    return response.data
  },

  async verifyHash(data, hash) {
    const response = await api.post('/crypto/hash/verify', { data, hash })
    return response.data
  },

  async hashPassword(password) {
    const response = await api.post('/crypto/password/hash', { password })
    return response.data
  },

  async verifyPassword(password, hash) {
    const response = await api.post('/crypto/password/verify', { password, hash })
    return response.data
  },

  async caesarCipher(text, shift = 3, encrypt = true) {
    const response = await api.post('/crypto/classic/caesar', { text, shift, encrypt })
    return response.data
  },

  async vigenereCipher(text, key, encrypt = true) {
    const response = await api.post('/crypto/classic/vigenere', { text, key, encrypt })
    return response.data
  }
}
