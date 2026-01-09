/**
 * Validar cédula ecuatoriana
 * Algoritmo del módulo 10
 */
export const validarCedulaEcuatoriana = (cedula) => {
  // Verificar que sea string y tenga exactamente 10 dígitos
  if (!cedula || typeof cedula !== 'string') {
    return { valida: false, mensaje: 'La cédula debe ser un texto' }
  }

  const cedulaLimpia = cedula.replace(/\s/g, '')

  if (!/^\d+$/.test(cedulaLimpia)) {
    return { valida: false, mensaje: 'La cédula debe contener solo números' }
  }

  if (cedulaLimpia.length !== 10) {
    return { valida: false, mensaje: 'La cédula ecuatoriana debe tener exactamente 10 dígitos' }
  }

  // Verificar que los dos primeros dígitos correspondan a una provincia válida (01-24)
  const provincia = parseInt(cedulaLimpia.substring(0, 2))
  if (provincia < 1 || provincia > 24) {
    return { 
      valida: false, 
      mensaje: 'Los dos primeros dígitos deben corresponder a una provincia válida (01-24)' 
    }
  }

  // Verificar el tercer dígito (debe ser menor a 6 para personas naturales)
  const tercerDigito = parseInt(cedulaLimpia[2])
  if (tercerDigito > 5) {
    return { 
      valida: false, 
      mensaje: 'El tercer dígito debe ser menor a 6 (cédula de persona natural)' 
    }
  }

  // Algoritmo del módulo 10 para validar el dígito verificador
  const coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
  const digitoVerificador = parseInt(cedulaLimpia[9])
  let suma = 0

  for (let i = 0; i < 9; i++) {
    let valor = parseInt(cedulaLimpia[i]) * coeficientes[i]
    // Si el resultado es mayor a 9, se resta 9
    if (valor > 9) {
      valor = valor - 9
    }
    suma += valor
  }

  // Calcular el dígito verificador esperado
  const residuo = suma % 10
  const resultado = residuo === 0 ? 0 : 10 - residuo

  if (resultado !== digitoVerificador) {
    return { 
      valida: false, 
      mensaje: 'Cédula inválida: el dígito verificador no coincide' 
    }
  }

  return { valida: true, mensaje: 'Cédula válida' }
}

/**
 * Formatear cédula con guiones (ej: 1234567890 -> 1234567-890)
 */
export const formatearCedula = (cedula) => {
  if (!cedula) return ''
  const limpia = cedula.replace(/\D/g, '')
  if (limpia.length <= 7) return limpia
  return `${limpia.slice(0, 7)}-${limpia.slice(7, 10)}`
}

/**
 * Validar email
 */
export const validarEmail = (email) => {
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!regex.test(email)) {
    return { valido: false, mensaje: 'Formato de email inválido' }
  }
  return { valido: true, mensaje: 'Email válido' }
}

/**
 * Validar teléfono ecuatoriano (10 dígitos)
 */
export const validarTelefono = (telefono) => {
  if (!telefono) return { valido: true, mensaje: '' } // Campo opcional
  
  const telefonoLimpio = telefono.replace(/\D/g, '')
  
  if (telefonoLimpio.length !== 10) {
    return { valido: false, mensaje: 'El teléfono debe tener 10 dígitos' }
  }
  
  return { valido: true, mensaje: 'Teléfono válido' }
}
