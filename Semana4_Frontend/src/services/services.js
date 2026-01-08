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
  async getUsers(params = {}) {
    const response = await api.get('/users', { params })
    return response.data
  },

  async getUserById(id) {
    const response = await api.get(`/users/${id}`)
    return response.data
  },

  async createUser(userData) {
    const response = await api.post('/users', userData)
    return response.data
  },

  async updateUser(id, userData) {
    const response = await api.put(`/users/${id}`, userData)
    return response.data
  },

  async deleteUser(id) {
    const response = await api.delete(`/users/${id}`)
    return response.data
  }
}

export const patientService = {
  async getPatients(params = {}) {
    const response = await api.get('/patients', { params })
    return response.data
  },

  async getPatientById(id) {
    const response = await api.get(`/patients/${id}`)
    return response.data
  },

  async createPatient(patientData) {
    const response = await api.post('/patients', patientData)
    return response.data
  },

  async updatePatient(id, patientData) {
    const response = await api.put(`/patients/${id}`, patientData)
    return response.data
  },

  async deletePatient(id) {
    const response = await api.delete(`/patients/${id}`)
    return response.data
  }
}

export const medicalRecordService = {
  async getRecordsByPatient(patientId) {
    const response = await api.get(`/medical-records/patient/${patientId}`)
    return response.data
  },

  async getRecordById(id) {
    const response = await api.get(`/medical-records/${id}`)
    return response.data
  },

  async createRecord(recordData) {
    const response = await api.post('/medical-records', recordData)
    return response.data
  },

  async getMyRecords() {
    const response = await api.get('/medical-records/mine')
    return response.data
  }
}

export const auditService = {
  async getAuditLogs(params = {}) {
    const response = await api.get('/audit', { params })
    return response.data
  },

  async getUserAuditLogs(userId, params = {}) {
    const response = await api.get(`/audit/user/${userId}`, { params })
    return response.data
  },

  async getAuditStats() {
    const response = await api.get('/audit/stats')
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
