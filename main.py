"""
main.py: punto de entrada a la app. Demuestra version incial y refactorizada
"""
from src.version_inicial.gestor_monolitico import GestorSolicitudesAcademicas
from src.version_refactorizada.domain.dtos import RegistroSolicitudDTO, ActualizacionSolicitudDTO
from src.version_refactorizada.domain.enums import TipoSolicitudEnum, PrioridadEnum, EstadoSolicitudEnum
from src.version_refactorizada.repository.memory_repository import JsonFileSolicitudRepository
from src.version_refactorizada.services.solicitud_service import SolicitudService

def main():
    print("=" * 70)
    print(" UTN - SISTEMA DE GESTIÓN DE SOLICITUDES ACADÉMICAS - TPI MS2 ")
    print("=" * 70)
    
    # --- DEMO 1: VERSIÓN INICIAL (Monolítica con Code Smells) ---
    print("\n[1] Probando Versión Inicial (Large Class & Code Smells)...")
    gestor_legacy = GestorSolicitudesAcademicas("db_legacy.json")
    id_legacy = gestor_legacy.registrar_solicitud(
        tipo="Equivalencia",
        estudiante_id="EST001",
        descripcion="Equivalencia de la materia Metodología de Sistemas II.",
        prioridad="Alta",
        fecha_limite="2026-12-31"
    )
    print(f"-> Solicitud inicial registrada exitosamente con ID: {id_legacy}")

    # --- DEMO 2: VERSIÓN REFACTORIZADA (SOLID, Strategy, Factory, Parameter Object) ---
    print("\n[2] Probando Versión Refactorizada (Clean Architecture & DTOs)...")
    repo = JsonFileSolicitudRepository("db_refactor.json")
    service = SolicitudService(repositorio=repo)

    dto_reg = RegistroSolicitudDTO(					# Registro usando DTO (Pydantic)
        tipo=TipoSolicitudEnum.CERTIFICADO,
        estudiante_id="EST002",
        descripcion="Solicitud formal de certificado analítico parcial.",
        prioridad=PrioridadEnum.MEDIA,
        fecha_limite=None
    )
    id_refactor = service.registrar_nueva_solicitud(dto_reg)		# Factory Method (y Strategy)
    print(f"-> Solicitud refactorizada registrada exitosamente con ID: {id_refactor}")

    dto_act = ActualizacionSolicitudDTO(				# Actualización usando Parameter Object (ActualizacionSolicitudDTO)
        solicitud_id=id_refactor,
        nuevo_estado=EstadoSolicitudEnum.EN_PROCESO,
        responsable="Lic. Pérez",
        observaciones="Trámite derivado al departamento de alumnos.",
        area_asignada="Bedelía",
        notificar_alumno=True,
        fecha_actualizacion="2026-11-06"
    )
    
    service.actualizar_solicitud(dto_act)
    print("-> Actualización de estado completada mediante Parameter Object sin acoplamiento.")
    
    print("\n" + "=" * 70)
    print(" Demostración finalizada. Todos los componentes están listos.")
    print("=" * 70)

if __name__ == "__main__":					# orden expresa: main() se ejecuta solo si se lo ordeno (python main.py)
    main()
