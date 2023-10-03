class Funcionario:
    def informacion(arreglo):
        info = []
        for data in arreglo:
            info.append({
                'rut': str(data[0]).strip(),
                'digito': str(data[1]).strip(),
                'codigo': str(data[2]).strip(),
                'letra': str(data[3]).strip(),
                'paterno': str(data[4]).strip(),
                'materno': str(data[5]).strip(),
                'nombre1': str(data[6]).strip(),
                'nombre2': str(data[12]).strip(),
                'nacimiento': str(data[7]).strip(),
                'ingreso': str(data[8]).strip(),
                'retiro': str(data[9]).strip(),
                'sexo': str(data[10]).strip(),
                'civil': str(data[11]).strip()
            })
        return info
