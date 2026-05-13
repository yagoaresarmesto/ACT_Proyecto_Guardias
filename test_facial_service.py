from modules.presencia.facial import (
    capturar_referencia_profesor,
    capturar_verificacion_profesor,
)


def main():
    id_profesor = 1

    ref = capturar_referencia_profesor(id_profesor)
    print("Referencia guardada:", ref)

    check = capturar_verificacion_profesor(id_profesor)
    print("Verificación guardada:", check)


if __name__ == "__main__":
    main()