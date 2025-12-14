import csv




def getNombresAsignaturas():
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
                indice_asignatura = 1 # Fallback usual si es la segunda columna

            # Recorremos fila por fila
            for fila in lector:
                if len(fila) > indice_asignatura:
                    materia = fila[indice_asignatura]
                    # Agregamos al set (si ya existe, el set la ignora)
                    if materia.strip(): # Verificamos que no esté vacía
                        asignaturas_unicas.add(materia)

        # Convertimos el set a una lista ordenada para mostrarla mejor
        lista_ordenada = sorted(list(asignaturas_unicas))

        #print(f"Total de asignaturas encontradas: {len(lista_ordenada)}")
        #for asig in lista_ordenada:
            #print(asig)
        return lista_ordenada
    except FileNotFoundError:
        print("El archivo no se encuentra. Revisa la ruta.")





def handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path = event["requestContext"]["http"]["path"]

    if method == "GET" and path == "/asignaturas":
        return {
            "statusCode": 200,
            "body": getNombresAsignaturas()
        }



    return {
        "statusCode": 200,
        "body": "Hello world!"
    }
