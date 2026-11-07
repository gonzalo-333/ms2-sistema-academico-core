"""
tests/test_solicitudes.py: Pruebas unitarias/integración para el sistema de solicitudes.
"""
import pytest
from src.version_refactorizada.domain.dtos import RegistroSolicitudDTO, ActualizacionSolicitudDTO
from src.version_refactorizada.domain.enums import TipoSolicitudEnum, PrioridadEnum, EstadoSolicitudEnum
from src.version_refactorizada.repository.memory_repository import JsonFileSolicitudRepository
from src.version_refactorizada.services.solicitud_service import SolicitudService


"""
FIXTURES (Gestión automática de recursos): son funciones de pytest que definen los pasos y datos que se usarán
para una prueba, proveyendo así un repositorio y un servicio limpios por cada test, evitando conflictos en
los mismos y evitando problemas de aislación y seguridad, ya que permite cerrar los recursos automáticamente.
"""

@pytest.fixture                                 # decorador: inyecta la funcion, evita boilerplate y da reproducibilidad
def service_and_repo(tmp_path):					# tmp_path: dir. temporal para la funcion (se auto-destruye al terminar)
    db_test_path = tmp_path / "test_db_solicitudes.json"		# Creamos un path temporal único (los json quedan aislados)
    
    repo = JsonFileSolicitudRepository(archivo_db=str(db_test_path))	# Creamos el repo
    service = SolicitudService(repositorio=repo)                    	# Lo inyectamos al servicio
    
    yield service, repo							# Inyecta el servicio y el repositorio al test que lo solicitew
    

# --- CASOS DE PRUEBA ---

def test_cp01_registro_exitoso(service_and_repo):			# CP-01: Registro exitoso con datos válidos
    service, repo = service_and_repo					# Desempaquetamos en orden la tupla que envia yield
    
    dto_registro = RegistroSolicitudDTO(				# Fase "Arrange" (Preparación) del patrón AAA (Arrange-Act-Assert)
        tipo=TipoSolicitudEnum.CERTIFICADO,
        estudiante_id="EST123",
        descripcion="Solicitud de certificado analítico parcial con promedio.",
        prioridad=PrioridadEnum.MEDIA,
        fecha_limite=None
    )
    
    sol_id = service.registrar_nueva_solicitud(dto_registro)		# Fase "Act" (Acción) del patrón AAA (Arrange-Act-Assert)
    assert sol_id == 1, "El ID de la solicitud creada debe ser 1"	# Fase "Assert" (Verificacion) del patrón AAA (Arrange-Act-Assert)
    
    solicitud_guardada = repo.obtener_por_id(sol_id)			# Nos aseguramos que efectivamente se realizaron los cambios
    assert solicitud_guardada is not None
    assert solicitud_guardada.estudiante_id == "EST123"
    assert solicitud_guardada.estado == EstadoSolicitudEnum.PENDIENTE	# Fin de fase "Assert"


def test_cp02_validacion_campo_descripcion_obligatorio(service_and_repo):	# CP-02: Rechazo por longitud mínima en descripción
    service, _ = service_and_repo						# ignoramos el repo ( _ ) porque no deberia guardarse nunca
    
    dto_invalido = RegistroSolicitudDTO(				# Fase "Arrange" (Preparación) del patrón AAA (Arrange-Act-Assert)
        tipo=TipoSolicitudEnum.CERTIFICADO,
        estudiante_id="EST123",
        descripcion="Texto corto",  					# Menor a 15 caracteres
        prioridad=PrioridadEnum.BAJA,
        fecha_limite=None
    )
    
    with pytest.raises(ValueError, match="al menos 15 caracteres"):	# admin. contexto, intercepta error que lleve match (marca exito)
        service.registrar_nueva_solicitud(dto_invalido)			# Fase "Act" + "Assert" del patrón AAA (Arrange-Act-Assert)


def test_cp03_actualizacion_estado_parameter_object(service_and_repo):	# CP-03: Actualización usando Parameter Object
    service, repo = service_and_repo

    dto_registro = RegistroSolicitudDTO(				# Fase "Arrange" (Preparación) del patrón AAA (Arrange-Act-Assert)
        tipo=TipoSolicitudEnum.EXAMEN,
        estudiante_id="EST789",
        descripcion="Inscripción condicional a examen final de sistemas.",
        prioridad=PrioridadEnum.ALTA,
        fecha_limite=None
    )
    sol_id = service.registrar_nueva_solicitud(dto_registro)		# Guarda una solicitud base con ID para que se pueda modificar
    
    dto_actualizacion = ActualizacionSolicitudDTO(			# Actualizamos usando Parameter Object
        solicitud_id=sol_id,
        nuevo_estado=EstadoSolicitudEnum.EN_PROCESO,
        responsable="Prof. Gómez",
        observaciones="Verificando correlativas en departamento.",
        area_asignada="Bedelía",
        notificar_alumno=True,
        fecha_actualizacion="2026-11-06"
    )
    
    resultado = service.actualizar_solicitud(dto_actualizacion)		# Fase "Act" (Acción) del patrón AAA (Arrange-Act-Assert)
    assert resultado is True						# Fase "Assert" (Verificacion) del patrón AAA (Arrange-Act-Assert)
    
    solicitud_actualizada = repo.obtener_por_id(sol_id)			# Nos aseguramos que efectivamente se realizaron los cambios
    assert solicitud_actualizada.estado == EstadoSolicitudEnum.EN_PROCESO
    assert solicitud_actualizada.responsable == "Prof. Gómez"		# Fin de fase "Assert"


def test_cp04_validacion_estrategia_equivalencias(service_and_repo):	# CP-04: Estrategia de validación específica de Equivalencias
    service, _ = service_and_repo
    
    dto_equivalencia_sin_fecha = RegistroSolicitudDTO(			# Fase "Arrange" (Preparación) del patrón AAA (Arrange-Act-Assert)
        tipo=TipoSolicitudEnum.EQUIVALENCIA,
        estudiante_id="EST456",
        descripcion="Solicitud de equivalencia de la materia Algoritmos.",
        prioridad=PrioridadEnum.MEDIA,
        fecha_limite=None  						# Faltante obligatorio
    )
    
    with pytest.raises(ValueError, match="requieren una fecha límite"):	# administrador de contexto (error si hay match)
        service.registrar_nueva_solicitud(dto_equivalencia_sin_fecha)	# Fase "Act" + "Assert" del patrón AAA (Arrange-Act-Assert)
