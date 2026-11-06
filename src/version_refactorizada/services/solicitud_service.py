"""
src/version_refactorizada/services/solicitud_service.py: mejoramos legibilidad extrayendo metodos

"""

from src.version_refactorizada.domain.dtos import RegistroSolicitudDTO, ActualizacionSolicitudDTO
from src.version_refactorizada.domain.models import Solicitud
from src.version_refactorizada.repository.base import SolicitudRepository
from src.version_refactorizada.services.estrategias_validacion import ValidadorFactory

class SolicitudService:			# Contiene los casos de uso principales del sistema (registrar, actualizar y generar reportes)
    """
    Servicio de Negocio refactorizado aplicando SRP (Responsabilidad Única).
    Se eliminaron los métodos masivos utilizando 'Extract Method' e inyección de dependencias (DIP).
    """
    def __init__(self, repositorio: SolicitudRepository):	# Recibe repositorio, sea JSON, SQL o archivo de testeo
        self.repositorio = repositorio

    def registrar_nueva_solicitud(self, dto: RegistroSolicitudDTO) -> int:	# Aplicación del Patrón Strategy mediante
        validador = ValidadorFactory.obtener_validador(dto.tipo)		# el uso de Factory Method
        validador.validar(dto)

        nueva_solicitud = Solicitud(						# Creación de la entidad tomando los atributos del DTO
            id=0,
            tipo=dto.tipo,
            estudiante_id=dto.estudiante_id,
            descripcion=dto.descripcion,
            prioridad=dto.prioridad,
            fecha_limite=dto.fecha_limite
        )

        return self.repositorio.guardar(nueva_solicitud)

    def actualizar_solicitud(self, dto: ActualizacionSolicitudDTO) -> bool:	# Usa 'ActualizacionSolicitudDTO' en vez de 7 parámetros 
        solicitud = self.repositorio.obtener_por_id(dto.solicitud_id)
        if not solicitud:
            raise KeyError(f"No se encontró la solicitud con ID {dto.solicitud_id}")

        solicitud.cambiar_estado(dto.nuevo_estado, dto.responsable, dto.observaciones)
        
        resultado = self.repositorio.actualizar(solicitud)

        if dto.notificar_alumno:
            print(f"[EMAIL SIMULADO] Notificando al alumno ID {solicitud.estudiante_id}: Estado cambiado a {dto.nuevo_estado}")

        return resultado

    def generar_reporte(self) -> dict:
        solicitudes = self.repositorio.obtener_todos()
        pendientes = sum(1 for s in solicitudes if s.estado == "Pendiente")
        aprobadas = sum(1 for s in solicitudes if s.estado == "Aprobada")
        
        return {
            "total_solicitudes": len(solicitudes),
            "pendientes": pendientes,
            "aprobadas": aprobadas
        }
