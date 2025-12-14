import csv


def getNombresAsignaturas() -> list[str]:
    try:
        # Usamos un conjunto (set) para guardar las materias porque no permite duplicados
        asignaturas_unicas = set()
        with open('horarios26_1_v2.csv', mode='r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)

            # Leemos la cabecera (primera fila) para saber en qué posición está 'Asignatura'
            cabecera = next(lector)
            try:
                indice_asignatura = cabecera.index('Asignatura')
            except ValueError:
                print("No se encontró la columna 'Asignatura'. Verifica el nombre.")
                indice_asignatura = 1  # Fallback usual si es la segunda columna

            # Recorremos fila por fila
            for fila in lector:
                if len(fila) > indice_asignatura:
                    materia = fila[indice_asignatura]
                    # Agregamos al set (si ya existe, el set la ignora)
                    if materia.strip():  # Verificamos que no esté vacía
                        asignaturas_unicas.add(materia)

        # Convertimos el set a una lista ordenada para mostrarla mejor
        lista_ordenada = sorted(list(asignaturas_unicas))

        # print(f"Total de asignaturas encontradas: {len(lista_ordenada)}")
        # for asig in lista_ordenada:
        # print(asig)

        return lista_ordenada

    except FileNotFoundError:
        print("El archivo no se encuentra. Revisa la ruta.")

    return []


def getAsignaturasYProfesores() -> list[dict]:
    """
    Retorna una lista con las asignaturas y los profesores que las imparten
    """
    try:
        asignatura_profes_map: dict[str, set[str]] = {}

        with open('horarios26_1_v2.csv', mode='r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)

            # Cabecera para ubicar columnas relevantes
            cabecera = next(lector)

            # Índice de asignatura (similar al de getNombresAsignaturas)
            try:
                idx_asignatura = cabecera.index('Asignatura')
            except ValueError:
                # Fallback común si cambia el nombre o no existe
                try:
                    # Buscar por aproximación
                    idx_asignatura = next(i for i, h in enumerate(cabecera) if 'asignatura' in h.lower() or 'materia' in h.lower())
                except StopIteration:
                    idx_asignatura = 1  # fallback conservador

            # Índice de profesor/docente: intentamos varias posibilidades
            posibles_prof = ['Profesor', 'Profesores', 'Docente', 'Docentes', 'Profesor(es)']
            idx_profesor = None
            for nombre in posibles_prof:
                if nombre in cabecera:
                    idx_profesor = cabecera.index(nombre)
                    break
            if idx_profesor is None:
                # Búsqueda por aproximación en minúsculas
                for i, h in enumerate(cabecera):
                    low = h.lower()
                    if 'profesor' in low or 'docente' in low:
                        idx_profesor = i
                        break
            if idx_profesor is None:
                # Fallback conservador (tercera columna suele ser profesor en algunos formatos)
                idx_profesor = 2 if len(cabecera) > 2 else min(1, len(cabecera) - 1)

            # Leer filas
            for fila in lector:
                if len(fila) <= max(idx_asignatura, idx_profesor):
                    continue
                materia = (fila[idx_asignatura] or '').strip()
                profes_raw = (fila[idx_profesor] or '').strip()
                if not materia:
                    continue
                if materia not in asignatura_profes_map:
                    asignatura_profes_map[materia] = set()

                # Separar posibles múltiples profesores por delimitadores comunes
                partes = [profes_raw]
                for sep in ['/', ';', ',', '|']:
                    if any(sep in p for p in partes):
                        nuevas = []
                        for p in partes:
                            nuevas.extend(p.split(sep))
                        partes = nuevas
                for p in partes:
                    p = p.strip()
                    if p:
                        asignatura_profes_map[materia].add(p)

        # Transformar a lista ordenada
        resultado: list[dict] = []
        for materia in sorted(asignatura_profes_map.keys()):
            profesores_ordenados = sorted(asignatura_profes_map[materia])
            resultado.append({
                'asignatura': materia,
                'profesores': profesores_ordenados
            })

        return resultado

    except FileNotFoundError:
        print("El archivo no se encuentra. Revisa la ruta.")
    except Exception as e:
        # No interrumpir la lambda; retornar vacío y loguear
        print(f"Error al procesar CSV: {e}")

    return []


def handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path = event["requestContext"]["http"]["path"]

    if method == "GET" and path == "/asignaturas":
        return {
            "statusCode": 200,
            "body": getNombresAsignaturas()
        }
    elif method == "GET" and path == "/asignaturas-profesores":
        return {
            "statusCode": 200,
            "body": getAsignaturasYProfesores()
        }

    return {
        "statusCode": 200,
        "body": "Hello world!"
    }
