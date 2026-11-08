# Sistema de Gestión de Solicitudes Académicas (TPI - Metodología de Sistemas II)

Repositorio del Trabajo Práctico Integrador para la materia **Metodología de Sistemas II** de la Universidad Tecnológica Nacional (UTN). El proyecto aborda el diagnóstico, refactorización y verificación de un sistema de gestión de solicitudes académicas, evolucionando desde un enfoque monolítico con deuda técnica (*Code Smells*) hacia una arquitectura en capas basada en principios SOLID, Clean Code y patrones de diseño orientados a objetos.

---

## 📂 Estructura del Repositorio

El repositorio separa claramente la versión inicial de la versión refactorizada:

```text
sistema-academico-core/
├── README.md                          # Documentación oficial del proyecto
├── requirements.txt                   # Dependencias del proyecto (Pydantic, pytest)
├── main.py                            # Script principal de demostración
├── tests/
│   └── test_solicitudes.py            # Suite de pruebas (CP-01 al CP-04)
└── src/
    ├── version_inicial/
    │   └── gestor_monolitico.py       # Versión base con los 5 code smells
    └── version_refactorizada/
        ├── domain/
        │   ├── enums.py               # Tipo, Prioridad y Estado de la solicitud
        │   ├── dtos.py                # RegistroSolicitudDTO y ActualizacionSolicitudDTO (Parameter Object)
        │   └── models.py              # Entidad Solicitud
        ├── repository/
        │   ├── base.py                # Interfaz abstracta SolicitudRepository (DIP)
        │   └── memory_repository.py   # JsonFileSolicitudRepository (persistencia en archivo JSON)
        └── services/
            ├── estrategias_validacion.py  # Strategy + Factory Method de validación
            └── solicitud_service.py       # Casos de uso: registrar, actualizar y reportar
```

---

## 🛠️ Tecnologías y Requisitos

* **Lenguaje:** Python 3.10 o superior.
* **Librerías principales:**
  * `pydantic` **2.x** (validación de datos y DTOs inmutables; se usa `ConfigDict`)
  * `pytest` (automatización de pruebas)

### Instalación de Dependencias

Cloná el repositorio e instalá las dependencias ejecutando en tu terminal:

```bash
pip install -r requirements.txt
```

---

## 🏗️ Arquitectura de la Versión Refactorizada

| Capa | Archivo(s) | Responsabilidad |
|------|-----------|-----------------|
| **Dominio** | `enums.py`, `dtos.py`, `models.py` | Enums del dominio, DTOs inmutables (`frozen=True`) y entidad `Solicitud` |
| **Repositorio** | `base.py`, `memory_repository.py` | Interfaz abstracta de persistencia e implementación concreta en archivo JSON |
| **Servicios** | `estrategias_validacion.py`, `solicitud_service.py` | Reglas de validación por tipo de trámite y casos de uso del sistema |

### Reglas de negocio implementadas

**Registro de solicitud** (`SolicitudService.registrar_nueva_solicitud`):

* El DTO valida que `estudiante_id` tenga al menos 3 caracteres y `descripcion` al menos 10. Además, `tipo` y `prioridad` deben pertenecer a sus enums. `fecha_limite` es opcional.
* La validación específica se elige con `ValidadorFactory` según el tipo de trámite:
  * **Equivalencia** (`ValidacionEquivalencia`): exige `fecha_limite` con formato `YYYY-MM-DD`.
  * **Resto de los tipos** (`ValidacionGenerica`): exige una descripción de al menos 15 caracteres.
* La solicitud se crea con estado `Pendiente` y responsable `Sin Asignar`. El repositorio le asigna un ID autoincremental.

**Actualización de solicitud** (`SolicitudService.actualizar_solicitud`):

* Recibe un único `ActualizacionSolicitudDTO` en lugar de 7 parámetros sueltos.
* Si la solicitud no existe, lanza `KeyError`.
* Actualiza estado, responsable y observaciones mediante `Solicitud.cambiar_estado()` y persiste el cambio.
* Si `notificar_alumno` es `True`, imprime por consola una notificación por email simulada.

**Reporte** (`SolicitudService.generar_reporte`): devuelve la cantidad total de solicitudes, las pendientes y las aprobadas.

### Code smells y su solución

| Code Smell (versión inicial) | Solución aplicada (versión refactorizada) |
|------------------------------|--------------------------------------------|
| **Large Class** | Separación en capas (dominio, repositorio, servicios) aplicando SRP |
| **Long Method** | Validaciones delegadas a estrategias (Strategy + Factory Method); el servicio queda con métodos cortos |
| **Primitive Obsession** | Enums (`TipoSolicitudEnum`, `PrioridadEnum`, `EstadoSolicitudEnum`) y DTOs validados con Pydantic |
| **Long Parameter List** | Parameter Object: `ActualizacionSolicitudDTO` |
| **Duplicated Code** | La validación de formato de fecha existe en un único lugar (`ValidacionEquivalencia`) |

### Patrones y principios aplicados

* **Strategy** (`ValidacionStrategy` y sus implementaciones): encapsula las reglas de validación por tipo de trámite (OCP).
* **Factory Method** (`ValidadorFactory.obtener_validador`): selecciona la estrategia correspondiente.
* **Parameter Object** (`ActualizacionSolicitudDTO`): agrupa los parámetros de actualización.
* **Inversión de Dependencias (DIP)**: `SolicitudService` depende de la interfaz abstracta `SolicitudRepository`, no de una implementación concreta.
* **Extract / Move Method**: lógica de validación extraída a las estrategias y cambio de estado encapsulado en la entidad (`Solicitud.cambiar_estado`).

---

## 🚀 Ejecución de la Demostración

Desde la raíz del proyecto:

```bash
python main.py
```

El script ejecuta dos demos consecutivas:

1. **Versión inicial:** registra una solicitud de *Equivalencia* con `GestorSolicitudesAcademicas` (archivo `db_legacy.json`).
2. **Versión refactorizada:** registra una solicitud de *Certificado* con `SolicitudService` + `RegistroSolicitudDTO` y luego la actualiza a *En Proceso* con `ActualizacionSolicitudDTO` (archivo `db_refactor.json`).

Ambos archivos JSON se generan en el directorio desde donde se ejecuta el script.

---

## 🧪 Ejecución de Pruebas Automatizadas

El sistema cuenta con pruebas implementadas con `pytest` que validan los casos de prueba fundamentales. Cada test usa un fixture (`service_and_repo`) que crea un repositorio JSON en un directorio temporal, por lo que los tests no se afectan entre sí ni tocan los archivos de la demo.

| Caso | Qué verifica |
|------|--------------|
| **CP-01** | Registro exitoso con datos válidos (ID = 1, estado inicial `Pendiente`) |
| **CP-02** | Rechazo de una descripción de menos de 15 caracteres (`ValueError`) |
| **CP-03** | Actualización de estado mediante Parameter Object (estado y responsable persistidos) |
| **CP-04** | Rechazo de una Equivalencia sin fecha límite (`ValueError`) |

```bash
python -m pytest tests/test_solicitudes.py -v
```

---

## 🏷️ Historial de Versiones y Tags de la Cátedra

El repositorio incluye los hitos de evolución del software marcados mediante commits y *Tags* de Git:

Commits:

* `estado-inicial`: versión monolítica original que concentra los 5 code smells oficiales (*Long Method*, *Large Class*, *Primitive Obsession*, *Long Parameter List*, *Duplicated Code*).
* `estado-refactorizado`: versión final estructurada en capas, aplicando SOLID, *Strategy*, *Factory Method*, *Parameter Object* e inversión de dependencias (DIP) mediante el patrón Repository.

Tags:

* etapa-diagnostico
* etapa-refactoring
* etapa-pruebas
* etapa-docs

Para visualizar los tags en tu repositorio local:

```bash
git tag -l
git checkout etapa-diagnostico
git checkout etapa-refactoring
git checkout etapa-pruebas
git checkout etapa-docs
```
