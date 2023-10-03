import qrcode
from PIL import Image
import base64
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, HorizontalGradiantColorMask, VerticalGradiantColorMask


# taking image which user wants
# in the QR code center
def qrcodecarabineros(data):
    Logo_link = 'images/logo_carab_solid.jpg'
    logo = Image.open(Logo_link)
    # taking base width
    basewidth = 200

    # adjust image size
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    # print(data)
    for info in data:
        qrdata = []
        for liquidacion in info['dataliquidacion']:
            rut = str(liquidacion['rut']).strip() + str(liquidacion['rut_digito_verificador']).strip()
            tracernumber = str(liquidacion['tracernumber']).strip()
            qrdata.append({
                'nombre': str(liquidacion['nombre']).strip(),
                'rut': str(liquidacion['rut']).strip(),
                'rutDigitoVerificador': str(liquidacion['rut_digito_verificador']).strip(),
                'tracerNumber': str(liquidacion['tracernumber']).strip()
            })
            strqr = "rut:" + rut + "|tracernumber:" + tracernumber + "|nombre:" + str(liquidacion['nombre']).strip() + "|"
        for totales in info['totales']:
            # print(totales)
            qrdata.append({
                'totalHaber': totales['totalhaber'],
                'totalLiquido': totales['totalliquido']
            })
            strqr = strqr + "totalhaberes:" + str(totales['totalhaber']).strip() + "|" + "totalliquido:" + str(totales['totalliquido']).strip()

    # Codificar diccionario a base 64 cuando se pueda validar liquidacion en pagina de carabineros.cl
    # encode_dict = str(qrdata).encode('utf-8')
    # base64_dict = base64.b64encode(encode_dict)

    # Decodificar diccionario
    # decode_dict = eval(base64.b64decode(base64_dict))

    # adding URL or text to QRcode
    QRcode.add_data(str(strqr).strip())

    # generating QR code
    QRcode.make()

    # adding color to QR code
    QRimg = QRcode.make_image(fill_color='#287233').convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    # save the QR code generated
    QRimg.save('codigo_qr/qr_carabineros_' + rut + tracernumber + '.png')
    # print('QR code generated! ')
    qrfile = 'codigo_qr/qr_carabineros_' + rut + tracernumber + '.png'
    return qrfile
