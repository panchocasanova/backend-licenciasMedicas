import barcode
from barcode.writer import ImageWriter


def codigobarrascarabineros(data):
    for info in data:
        codedata = []
        for liquidacion in info['dataliquidacion']:
            rut = str(liquidacion['rut']).strip() + str(liquidacion['rut_digito_verificador']).strip()
            tracernumber = str(liquidacion['tracernumber']).strip()
            # print('Rut: ', rut, 'TracerNumber: ', tracernumber)
            codedata.append({
                'nombre': str(liquidacion['nombre']).strip(),
                'rut': str(liquidacion['rut']).strip(),
                'rutDigitoVerificador': str(liquidacion['rut_digito_verificador']).strip(),
                'tracerNumber': str(liquidacion['tracernumber']).strip()
            })
        for totales in info['totales']:
            # print(totales)
            codedata.append({
                'totalHaber': totales['totalhaber'],
                'totalLiquido': totales['totalliquido']
            })

    code = rut + tracernumber
    sample_barcode = barcode.get('code39', code, writer=ImageWriter())
    generated_filename = sample_barcode.save('codigo_qr/' + code)
    # print('Codigo de barras generado con el nombre: ' + generated_filename)
    return generated_filename
