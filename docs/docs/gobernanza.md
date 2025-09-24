docs/gobernanza.md
# Gobernanza de Datos

Este documento describe las reglas mínimas de gobernanza aplicables al laboratorio **“De CSVs heterogéneos a un almacén analítico confiable”**.

---

## 1. Origen y Linaje
- Todo archivo CSV ingerido debe registrarse en un **log de ingesta** (nombre, fecha, tamaño, hash SHA256).
- La capa **Bronze** conserva siempre el archivo crudo, garantizando trazabilidad.
- Cada transformación debe dejar rastro (timestamp, script/proceso aplicado, autor).

---

## 2. Validaciones mínimas
- **date**: debe cumplir formato ISO `YYYY-MM-DD`.  
- **partner**: no nulo, tipo `string`.  
- **amount**: numérico, en EUR, distinto de nulo.  
- Sin duplicados exactos de registros en capa Silver.  
- Valores fuera de rango (ej. montos negativos si no corresponden) deben ser señalados en un log de calidad.

---

## 3. Política de mínimos privilegios
- Separar roles: **lectura**, **escritura**, **administración**.  
- Los usuarios de análisis solo deben acceder a la capa Silver y Gold.  
- La capa Raw y Bronze queda restringida a administradores/ingenieros de datos.  
- Acceso a credenciales mediante variables de entorno, nunca en repositorio.

---

## 4. Trazabilidad
- Identificar cada dataset con **UUID** de carga.  
- Versionado de esquemas y scripts en Git.  
- Reporte de linaje desde origen → Bronze → Silver → KPIs.  
- Logs centralizados para auditar procesos ETL.

---

## 5. Roles
- **Ingeniero de Datos**: diseña pipeline, mantiene ingestión/transformaciones.  
- **Analista de Datos**: consume KPIs y capa Silver/Gold, reporta incidencias.  
- **Administrador**: gestiona permisos, credenciales y políticas de seguridad.  
- **Auditor**: revisa cumplimiento de normas de trazabilidad y calidad.  

