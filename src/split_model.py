def split_file(file_path, part_size=50*1024*1024):
    """
    Divide un archivo en partes más pequeñas.
    
    :param file_path: Ruta del archivo a dividir.
    :param part_size: Tamaño de cada parte en bytes.
    """
    with open(file_path, 'rb') as file:
        part_num = 0
        while True:
            part_data = file.read(part_size)
            if not part_data:
                break
            part_file_name = f"{file_path}.part{part_num}"
            with open(part_file_name, 'wb') as part_file:
                part_file.write(part_data)
            part_num += 1

# Divide el archivo en partes de 50 MB
split_file('models/modelo_knn2.pkl', part_size=50*1024*1024)
