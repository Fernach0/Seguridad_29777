# REVISIÓN DE CONCEPTOS CRIPTOGRÁFICOS
## ESPE MedSafe - Semana 1

---

## 1. CIFRADO SIMÉTRICO

### 1.1 Concepto General
El cifrado simétrico es un método criptográfico donde se utiliza **la misma clave** tanto para cifrar como para descifrar la información. Es rápido y eficiente para grandes volúmenes de datos.

### 1.2 AES (Advanced Encryption Standard)
- **Descripción**: Estándar de cifrado adoptado por el gobierno de EE.UU. en 2001.
- **Tamaños de clave**: 128, 192 o 256 bits.
- **Características**:
  - Cifrado por bloques (128 bits por bloque)
  - Altamente seguro y ampliamente utilizado
  - Eficiente en hardware y software
- **Aplicación en ESPE MedSafe**: Cifrado de historias clínicas y diagnósticos médicos en la base de datos.

### 1.3 DES (Data Encryption Standard)
- **Descripción**: Predecesor de AES, desarrollado en los años 70.
- **Tamaño de clave**: 56 bits (actualmente considerado inseguro).
- **Características**:
  - Cifrado por bloques (64 bits)
  - Vulnerable a ataques de fuerza bruta
  - Obsoleto para aplicaciones críticas
- **Nota**: No se recomienda para ESPE MedSafe debido a su nivel de seguridad.

---

## 2. CIFRADO ASIMÉTRICO

### 2.1 Concepto General
Utiliza un **par de claves**: una pública (para cifrar) y una privada (para descifrar). Proporciona mayor seguridad pero es más lento que el cifrado simétrico.

### 2.2 RSA (Rivest-Shamir-Adleman)
- **Descripción**: Algoritmo basado en la factorización de números primos grandes.
- **Tamaños de clave**: 1024, 2048, 4096 bits (recomendado: 2048 o superior).
- **Características**:
  - Usado para intercambio seguro de claves
  - Firma digital
  - Ampliamente implementado en SSL/TLS
- **Aplicación en ESPE MedSafe**: 
  - Intercambio seguro de claves de sesión
  - Autenticación de usuarios (firma digital)
  - Cifrado de comunicaciones entre cliente-servidor

### 2.3 ECC (Elliptic Curve Cryptography)
- **Descripción**: Criptografía basada en curvas elípticas.
- **Características**:
  - Mayor seguridad con claves más cortas
  - Más eficiente que RSA
  - Una clave ECC de 256 bits ≈ RSA de 3072 bits
- **Aplicación en ESPE MedSafe**: Alternativa a RSA para dispositivos móviles o recursos limitados.

---

## 3. HASH SEGURO

### 3.1 Concepto General
Las funciones hash son algoritmos unidireccionales que convierten datos de cualquier tamaño en una cadena de longitud fija. **No se puede revertir** (no hay descifrado).

### 3.2 SHA-256 (Secure Hash Algorithm 256)
- **Descripción**: Parte de la familia SHA-2, desarrollada por la NSA.
- **Salida**: 256 bits (64 caracteres hexadecimales).
- **Características**:
  - Resistente a colisiones
  - Ampliamente usado en blockchain y certificados digitales
- **Aplicación en ESPE MedSafe**: 
  - Verificación de integridad de historias clínicas
  - Detección de modificaciones no autorizadas

### 3.3 SHA-2 y SHA-3
- **SHA-2**: Familia que incluye SHA-224, SHA-256, SHA-384, SHA-512.
- **SHA-3**: Estándar más reciente (2015), basado en construcción Keccak.
- **Diferencia principal**: SHA-3 usa una estructura diferente (esponja) más resistente a ciertos ataques.

### 3.4 bcrypt
- **Descripción**: Función hash diseñada específicamente para contraseñas.
- **Características**:
  - Incorpora **salt** automáticamente
  - Tiene un "factor de trabajo" ajustable (hace que el hash sea más lento intencionalmente)
  - Resistente a ataques de fuerza bruta con GPUs
- **Aplicación en ESPE MedSafe**: **Almacenamiento seguro de contraseñas** de administradores, doctores y pacientes.

### 3.5 Salting (Sal Criptográfica)
- **Concepto**: Valor aleatorio añadido a la contraseña antes de hacer el hash.
- **Propósito**:
  - Prevenir ataques con tablas rainbow
  - Hacer que contraseñas idénticas generen hashes diferentes
- **Implementación**: 
  - Generar salt único por usuario
  - Almacenar salt junto con el hash en la base de datos
- **Ejemplo**:
  ```
  Password: "MiPassword123"
  Salt: "a$9mK2pX"
  Hash: bcrypt("MiPassword123" + "a$9mK2pX")
  ```

---

## 4. CIFRADO CLÁSICO

### 4.1 Cifrado César
- **Descripción**: Sustitución simple donde cada letra se desplaza un número fijo de posiciones en el alfabeto.
- **Ejemplo**: 
  - Texto: "HOLA"
  - Desplazamiento: 3
  - Cifrado: "KROD"
- **Vulnerabilidad**: Solo hay 25 claves posibles (fácil de romper por fuerza bruta).
- **Aplicación en ESPE MedSafe**: Fines educativos/demostrativos, NO para datos reales.

### 4.2 Cifrado Vigenère
- **Descripción**: Cifrado polialfabético que usa una palabra clave repetida.
- **Mejora sobre César**: Más difícil de romper por análisis de frecuencia.
- **Ejemplo**:
  ```
  Texto: "MEDICINA"
  Clave: "ESPE" → "ESPEESPE"
  Cifrado: Suma de posiciones letra por letra
  ```
- **Aplicación en ESPE MedSafe**: Demostración histórica de evolución criptográfica.

### 4.3 Cifrado XOR
- **Descripción**: Operación bit a bit entre el texto y una clave.
- **Características**:
  - Simple y rápido
  - Reversible (XOR dos veces restaura el original)
  - Seguro solo si la clave es verdaderamente aleatoria y de un solo uso (One-Time Pad)
- **Vulnerabilidad**: Si la clave se reutiliza, es vulnerable.
- **Aplicación en ESPE MedSafe**: Ofuscación ligera de datos no críticos.

---

## 5. OpenSSH

### 5.1 Concepto
- **Descripción**: Conjunto de herramientas para comunicación segura usando el protocolo SSH (Secure Shell).
- **Componentes principales**:
  - `ssh`: Cliente para conexiones remotas
  - `sshd`: Servidor SSH
  - `ssh-keygen`: Generación de pares de claves
  - `scp/sftp`: Transferencia segura de archivos

### 5.2 Características de Seguridad
- Autenticación basada en claves públicas/privadas
- Cifrado de extremo a extremo
- Integridad de datos
- Tunneling seguro (port forwarding)

### 5.3 Aplicación en ESPE MedSafe
- **Acceso remoto seguro** al servidor de base de datos
- **Transferencia segura** de backups de historias clínicas
- **Tunneling SSH** para conectar a la base de datos desde el backend
- **Gestión de servidores** de forma segura por el equipo DevOps

---

## 6. SELinux (Security-Enhanced Linux)

### 6.1 Concepto
- **Descripción**: Módulo de seguridad del kernel de Linux que implementa Control de Acceso Obligatorio (MAC).
- **Desarrollado por**: NSA y la comunidad open-source.

### 6.2 Características
- **Políticas de seguridad**: Define qué procesos pueden acceder a qué recursos.
- **Confinamiento de procesos**: Limita el daño si un proceso es comprometido.
- **Etiquetado**: Todos los objetos (archivos, procesos, puertos) tienen etiquetas de seguridad.

### 6.3 Modos de Operación
1. **Enforcing**: Aplica políticas y bloquea acciones no permitidas.
2. **Permissive**: Solo registra violaciones sin bloquear.
3. **Disabled**: Desactivado.

### 6.4 Aplicación en ESPE MedSafe
- **Hardening del servidor**: Protección adicional en el servidor Linux donde corre el backend.
- **Aislamiento de procesos**: El proceso del backend solo puede acceder a archivos específicos.
- **Protección de base de datos**: Limitar qué procesos pueden conectarse a PostgreSQL/MySQL.
- **Compliance**: Cumplimiento de estándares de seguridad en salud (HIPAA, GDPR).

### 6.5 Ejemplo de Política
```bash
# Permitir que el proceso de la aplicación web acceda al puerto 8000
semanage port -a -t http_port_t -p tcp 8000

# Permitir conexión a la base de datos
setsebool -P httpd_can_network_connect_db on
```

---

## 7. SELECCIÓN DE TÉCNICAS PARA ESPE MedSafe

### Técnicas Implementadas (mínimo 3):

1. **AES-256 (Cifrado Simétrico)**: Para cifrar historias clínicas y diagnósticos en la base de datos.

2. **RSA-2048 (Cifrado Asimétrico)**: Para autenticación de sesiones y firma digital de documentos médicos.

3. **bcrypt con Salting (Hash Seguro)**: Para almacenamiento seguro de contraseñas de todos los usuarios.

### Técnicas Adicionales (Demostración/Educación):

4. **SHA-256**: Verificación de integridad de archivos médicos (PDF de resultados de laboratorio).

5. **Cifrado César/Vigenère**: Módulo educativo para mostrar la evolución histórica de la criptografía.

---

## 8. REFERENCIAS

1. NIST. (2001). *Advanced Encryption Standard (AES)*. FIPS PUB 197.
2. Rivest, R., Shamir, A., & Adleman, L. (1978). *A method for obtaining digital signatures and public-key cryptosystems*. Communications of the ACM, 21(2), 120-126.
3. NIST. (2015). *SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions*. FIPS PUB 202.
4. Provos, N., & Mazières, D. (1999). *A Future-Adaptable Password Scheme*. USENIX Annual Technical Conference.
5. OpenSSH Project. (2023). *OpenSSH Manual Pages*. https://www.openssh.com/
6. NSA. (2020). *Security-Enhanced Linux (SELinux)*. https://github.com/SELinuxProject
7. Katz, J., & Lindell, Y. (2020). *Introduction to Modern Cryptography* (3rd ed.). CRC Press.

---

**Fecha**: 8 de enero de 2026  
**Equipo**: ESPE MedSafe  
**Curso**: Ingeniería de Seguridad de Software
