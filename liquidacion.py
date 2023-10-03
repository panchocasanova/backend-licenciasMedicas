from conector import conectorbd
from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from qr import qrcodecarabineros
import os
from barra import codigobarrascarabineros
from literal import numero_a_letras
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from fpdf import FPDF


def liquidacionmes(rut, fecha_desde, fecha_hasta, censura):
    global descuentosparticulares
    global descuentoslegales

    def rayado(numpag, totalpag):
        pdfliq.set_line_width(0.1)
        pdfliq.set_draw_color(25)
        # rectangulo grande
        pdfliq.set_fill_color(255)
        pdfliq.rect(15, 37, 190, 20, 'DF')
        # rectángulos rellenos (DF)
        pdfliq.set_fill_color(222, 240, 217)
        pdfliq.rect(15, 37, 190, 5, 'DF')
        pdfliq.rect(15, 47, 190, 5, 'DF')
        # Cuadro Izquierda
        pdfliq.rect(15, 58, 75, 153, '')
        pdfliq.rect(15, 58, 75, 5, 'DF')
        pdfliq.rect(15, 63, 11, 148, '')
        # Cuadro Derecha
        pdfliq.rect(91, 58, 114, 153, '')
        pdfliq.rect(91, 58, 114, 5, 'DF')
        # Cuadro totales y observaciones
        pdfliq.rect(15, 211, 190, 61, '')
        # Cuadro izquierda
        pdfliq.rect(15, 211, 75, 4, '')
        pdfliq.rect(15, 219, 75, 4, '')
        pdfliq.rect(15, 227, 75, 4, '')
        pdfliq.rect(15, 235, 75, 4, '')
        pdfliq.rect(15, 239, 75, 4, '')
        # Cuadro Derecha
        pdfliq.rect(91, 211, 114, 4, '')
        pdfliq.rect(91, 219, 114, 4, '')
        pdfliq.rect(91, 227, 114, 4, '')
        pdfliq.rect(91, 211, 114, 4, '')
        pdfliq.rect(91, 235, 114, 4, '')
        pdfliq.rect(91, 211, 114, 24, '')
        pdfliq.rect(15, 211, 75, 24, '')
        pdfliq.rect(15, 247, 190, 4, '')
        pdfliq.rect(91, 239, 114, 4, '')
        pdfliq.rect(15, 251, 190, 4, 'DF')
        # Titulos liquidacion
        pdfliq.rect(15, 273, 190, 35, '')
        pdfliq.rect(15, 273, 190, 4, 'DF')
        pdfliq.set_font('Times', 'B', 8)
        pdfliq.set_xy(95, 273)
        pdfliq.cell(35, 5, 'INFORMACION GENERAL', 0, 0, 'C')
        # Marca de agua
        pdfliq.set_font('Arial', '', 14)
        pdfliq.set_text_color(255, 0, 0)
        pdfliq.rotate(40)
        pdfliq.set_xy(140, 150)
        pdfliq.cell(140, 10, 'ESTA LIQUIDACION NO ES VALIDA COMO CERTIFICADO DE REMUNERACIONES', 0, 0, 'C')
        # nombres cuadro primera linea
        pdfliq.rotate(0)
        pdfliq.set_text_color(0, 0, 0)
        pdfliq.set_font('Times', 'B', 8)
        # RUT
        pdfliq.set_xy(18, 37)
        pdfliq.cell(35, 5, 'R.U.T.', 0, 0, 'L')
        # Grado
        pdfliq.set_xy(40, 37)
        pdfliq.cell(35, 5, 'GRADO', 0, 0, 'L')
        # nombres
        pdfliq.set_xy(75, 37)
        pdfliq.cell(72, 5, 'APELLIDOS Y NOMBRES', 0, 0, 'L')
        # reparticion
        pdfliq.set_xy(60, 47)
        pdfliq.cell(45, 5, 'REPARTICION', 0, 0, 'L')
        # unidad
        pdfliq.set_xy(120, 47)
        pdfliq.cell(45, 5, 'UNIDAD', 0, 0, 'L')
        # GE
        pdfliq.set_xy(18, 47)
        pdfliq.cell(15, 5, 'GE', 0, 0, 'L')
        # GS
        pdfliq.set_xy(26, 47)
        pdfliq.cell(15, 5, 'GS', 0, 0, 'L')
        # TR
        pdfliq.set_xy(34, 47)
        pdfliq.cell(15, 5, 'TR', 0, 0, 'L')
        # CF
        pdfliq.set_xy(42, 47)
        pdfliq.cell(15, 5, 'CF', 0, 0, 'L')
        # SS
        pdfliq.set_xy(50, 47)
        pdfliq.cell(15, 5, 'SS', 0, 0, 'L')
        # tipo sueldo
        pdfliq.set_xy(140, 37)
        pdfliq.cell(35, 5, 'TIPO SUELDO', 0, 0, 'L')
        # titulos cuadro izquierdo
        pdfliq.set_xy(15, 58)
        pdfliq.cell(60, 5, 'DETALLE DE HABERES', 0, 0, 'C')
        pdfliq.set_xy(60, 58)
        pdfliq.cell(35, 5, 'VALOR $', 0, 0, 'C')
        # titulo derecha
        pdfliq.set_xy(91, 58)
        pdfliq.cell(45, 5, 'DETALLE DE DESCUENTOS', 0, 0, 'L')
        pdfliq.set_xy(135, 58)
        pdfliq.cell(22, 5, 'F.TERMINO', 0, 0, 'L')
        pdfliq.set_xy(160, 58)
        pdfliq.cell(25, 5, 'ORIGEN.', 0, 0, 'L')
        pdfliq.set_xy(185, 58)
        pdfliq.cell(22, 5, 'VAL. DESC. $', 0, 0, 'L')
        # titulos cuadro totales
        pdfliq.set_font('Arial', '', 6)
        if totalpag == 1:
            if numpag == 2:
                pdfliq.set_font('Arial', 'B', 8)
                pdfliq.set_xy(123, 10)
                pdfliq.cell(145, 5, 'PAGINAS 2/2', 0, 0, 'C')
                numeropagina = 0

            pdfliq.set_xy(18, 248)
            pdfliq.cell(22, 3, 'SON:', 0, 0, 'L')
        else:
            pdfliq.set_font('Arial', 'B', 8)
            pdfliq.set_xy(123, 10)
            pdfliq.cell(145, 5, 'PAGINAS 1/2', 0, 0, 'C')

        pdfliq.set_font('Times', 'B', 8)
        pdfliq.set_xy(18, 251)
        pdfliq.cell(22, 5, 'OBSERVACIONES:', 0, 0, 'L')
        pdfliq.set_font('Arial', 'B', 4)

    def cabecera(encabezado, serie, mes, anno):
        # CABECERA
        titulo = encabezado
        usuario = 'usuariomasrut'
        ipusuario = 'ipdelusuario'
        pdfliq.set_font("Times", "B", 12)
        pdfliq.set_xy(45, 20)
        pdfliq.cell(130, 5, titulo + " " + serie, 0, 0, "C")
        pdfliq.set_xy(90, 25)
        pdfliq.cell(45, 5, str(mes + " " + anno).strip(), 0, 0, 'C')
        pdfliq.image('images/sello.jpg', 35, 65, 150)
        pdfliq.image('images/logo_carab_solid.jpg', 28, 5, 20)
        pdfliq.set_font("Times", "B", 8)
        pdfliq.set_xy(15, 25)
        pdfliq.cell(45, 5, 'CARABINEROS DE CHILE', 0, 0, 'C')
        pdfliq.set_xy(15, 28)
        pdfliq.cell(45, 5, 'DPTO. REMUNERACIONES P.9', 0, 0, 'C')
        # segunda linea debajo de dpto remuneraciones en caso de agregar un nuevo parrafo.
        # pdfliq.set_xy(15, 31)
        # pdfliq.cell(45, 5, 'P9', 0, 0, 'C')
        pdfliq.set_xy(100, 5)

    def crearliquidacion(tipo, rut1, fecha, tf, df):
        finalLiquidacion = []
        previsionotros = []
        previsiondipreca = []
        observa = []
        totales = []
        dataliquidacion = []
        try:
            conn = conectorbd()
            cursor1 = conn.cursor()
            cursor1.execute("EXEC BD_REMUNE.dbo.sp_consultar_cabliq" + tipo + " " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "'")
            resultado = cursor1.fetchall()
            tfuncionario = tipofuncionario(tf)
            if str(tf).strip() == 'I':
                tdetalle = tipodetallecivil(df)
            elif str(tf).strip() == 'M':
                tdetalle = tipodetallemedico(df)
            else:
                tdetalle = tipodetallecivil(df)
            gradofuncionario = str(tfuncionario + " " + tdetalle).strip().upper()
            # if gradofuncionario == 'UNIFORMADO':
            #    gradofuncionario = str(dataliq[19]).strip()
            if resultado:
                for dataliq in resultado:
                    rut_print = dataliq[0]
                    dv_print = dataliq[1]
                    prevision = str(dataliq[12]).strip()
                    salud = dataliq[15]
                    tracernumber_print = str(dataliq[18]).strip()
                    dataliquidacion.append({
                        'rut': int(dataliq[0]),
                        'rut_digito_verificador': str(dataliq[1]).strip(),
                        'codigo_funcionario': str(dataliq[2]).strip(),
                        'nombre': str(dataliq[3]).strip(),
                        'fecha_ingreso': str(dataliq[4]).strip(),
                        'fecha_ingreso_formateada': str(dataliq[5]).strip(),
                        'ge': str(dataliq[6]).strip(),
                        'gs': str(dataliq[7]).strip(),
                        'tr': str(dataliq[8]).strip(),
                        'cf': str(dataliq[9]).strip(),
                        'ssn': str(dataliq[10]).strip(),
                        'ss': str(dataliq[11]).strip(),
                        'prevision': str(dataliq[12]).strip(),
                        'prevision_porcentaje': float(dataliq[13]),
                        'dotacion': str(dataliq[14]).strip(),
                        'salud': str(dataliq[15]).strip(),
                        'tipo_sueldo_codigo': str(dataliq[16]).strip(),
                        'tipo_sueldo_descripcion': str(dataliq[17]).strip(),
                        'tracernumber': str(dataliq[18]).strip(),
                        # 'grado': str(dataliq[19]).strip(),
                        'grado': str(dataliq[19]).strip().upper() if gradofuncionario == 'UNIFORMADO' else gradofuncionario,
                        'reparticion': str(dataliq[20]).strip(),
                        'porcentaje': float(dataliq[21]) if dataliq[21] is not None else 0,
                        'unidad': str(dataliq[22]).strip(),
                    })

        except Exception as error1:
            return jsonify({'msg': error1}), 400
        finally:
            if cursor1:
                cursor1.close()

        try:
            # Totales liquidacion
            conn = conectorbd()
            cursor2 = conn.cursor()

            cursor2.execute("EXEC BD_REMUNE.dbo.sp_consultar_TotLiq" + tipo + " " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "'")
            resultadototales = cursor2.fetchone()
            if resultadototales:
                totales.append({
                    'totalhaber': int(resultadototales[0]),
                    'totaldescuentos': int(resultadototales[1]),
                    'totalliquido': int(resultadototales[2]),
                    'totalimponible': int(resultadototales[3]),
                    'totalimpuestos': int(resultadototales[4]),
                    'totalzona': int(resultadototales[5])
                })
        except Exception as error2:
            return jsonify({'msg': error2}), 400
        finally:
            if cursor2:
                cursor2.close()

        try:
            conn = conectorbd()
            cursor3 = conn.cursor()
            cursor3.execute("EXEC BD_REMUNE.dbo.sp_consultar_DetLiq" + tipo + " " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "'")
            detallesliquidacion = cursor3.fetchall()
            lineahaber = lineadebe = 0
            haberes = []
            deberes = []
            if detallesliquidacion:
                # print("entro a detalles de liquidacion")
                for dl in detallesliquidacion:
                    if str(dl[0]).strip() == 'H':
                        haberes.append({'prop': dl[1], 'descripcion': dl[2], 'origen': dl[3], 'fechatermino': dl[4], 'monto': dl[5], 'codigo': dl[6]})
                        lineahaber += 1
                    if str(dl[0]).strip() == 'D':
                        deberes.append({'prop': dl[1], 'descripcion': dl[2], 'origen': dl[3], 'fechatermino': dl[4], 'monto': dl[5], 'codigo': dl[6]})
                        lineadebe += 1
        except Exception as error3:
            return jsonify({'msg': error3}), 400
        finally:
            if cursor3:
                cursor3.close()

        if str(tipo).strip() == 'Seg':
            try:
                conn = conectorbd()
                cursor4 = conn.cursor()
                cursor4.execute("EXEC BD_REMUNE.dbo.sp_consultar_Observacion " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "', 'S'")
                observaciones = cursor4.fetchall()
                for obs in observaciones:
                    observa.append({'obs': obs[0], 'tipo': obs[1]})

            except Exception as error4:
                return jsonify({'msg': error4}), 400
            finally:
                if cursor4:
                    cursor4.close()
        elif str(tipo).strip() == 'Reno':
            try:
                conn = conectorbd()
                cursor5 = conn.cursor()

                cursor5.execute("EXEC BD_REMUNE.dbo.sp_consultar_Observacion " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "', 'R'")
                observaciones = cursor5.fetchall()
                ## print('Observaciones reno ', observaciones)
                for obs in observaciones:
                    observa.append({'obs': obs[0], 'tipo': obs[1]})

            except Exception as error5:
                return jsonify({'msg': error5}), 400
            finally:
                if cursor5:
                    cursor5.close()
        elif str(tipo).strip() == 'ManualP' or str(tipo).strip() == 'ManualS' or str(tipo).strip() == 'ManualR':
            try:
                conn = conectorbd()
                cursor6 = conn.cursor()
                cursor6.execute("EXEC BD_REMUNE.dbo.sp_consultar_Observacion " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "', 'M'")
                observaciones = cursor6.fetchall()
                for obs in observaciones:
                    observa.append({'obs': obs[0], 'tipo': obs[1]})

            except Exception as error6:
                return jsonify({'msg': error6}), 400
            finally:
                if cursor6:
                    cursor6.close()
        else:
            try:
                conn = conectorbd()
                cursor7 = conn.cursor()
                cursor7.execute("EXEC BD_REMUNE.dbo.sp_consultar_Observacion " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "', 'P'")
                observaciones = cursor7.fetchall()
                for obs in observaciones:
                    observa.append({'obs': obs[0], 'tipo': obs[1]})

            except Exception as error7:
                return jsonify({'msg': error7}), 400
            finally:
                if cursor7:
                    cursor7.close()

        if prevision:
            if prevision == 'DIPRECA':
                try:
                    conn = conectorbd()
                    cursor8 = conn.cursor()
                    cursor8.execute("EXEC BD_REMUNE.dbo.sp_consultar_PreDip" + tipo + " " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "'")
                    previsionalldipreca = cursor8.fetchall()

                    for prev in previsionalldipreca:
                        previsiondipreca.append({
                            'fondo_hoscar': int(prev[0]),
                            'fondo_rev_pension': int(prev[1]),
                            'fondo_hospital_dipreca': int(prev[2]),
                            'fondo_retiro_dipreca': int(prev[3]),
                            'fondo_desahucio': int(prev[4]),
                            'impuesto_unico': int(prev[5]),
                            'provision_impuesto': int(prev[7])
                        })

                except Exception as error8:
                    return jsonify({'msg': error8}), 400
                finally:
                    if cursor8:
                        cursor8.close()
            else:
                try:
                    conn = conectorbd()
                    cursor9 = conn.cursor()
                    # print("EXEC BD_REMUNE.dbo.sp_consultar_PrePre" + tipo + " " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "'")
                    cursor9.execute("SET NOCOUNT ON; EXEC BD_REMUNE.dbo.sp_consultar_PrePre" + tipo + " " + rut1 + ", " + fecha + ",'" + tf + "'" + ",'" + df + "'")
                    datosprevision = cursor9.fetchall()
                    if datosprevision:
                        for prev in datosprevision:

                            if str(prev[6].strip() != 'NO COTIZA A.P.V.'):
                                apv = 0

                            previsionotros.append({
                                'afp_nombre': str(prevision).strip(),
                                'afp_valor': int(prev[0]),
                                'afp_adicional': int(prev[1]),
                                'afp_ahorro': int(prev[5]),
                                'isapre_nombre': str(salud).strip(),
                                'isapre_valor': int(prev[2]),
                                'isapre_adicional': int(prev[3]),
                                'impuesto_unico': int(prev[4]),
                                'provision_impuesto': int(prev[10]),
                                'apv_ahorro': int(prev[9]),
                                'seguro_invalidez': int(prev[7])
                            })
                except Exception as error9:
                    return jsonify({'msg': error9}), 400
                finally:
                    if cursor9:
                        cursor9.close()
        finalLiquidacion.append(
            {'dataliquidacion': dataliquidacion, 'haberes': haberes, 'deberes': deberes, 'previosionOtros': previsionotros, 'previsionDipreca': previsiondipreca, 'totales': totales,
             'observaciones': observa})
        return finalLiquidacion

    def llenardocumento(data):
        for dl in data:
            tracernumber = dl['dataliquidacion'][0]['tracernumber']
            pdfliq.set_font('Arial', '', 8)
            if censura == 1:
                pdfliq.set_xy(15, 42)
                pdfliq.cell(35, 5, str(clppesos(dl['dataliquidacion'][0]['rut'])).strip() + "-" + str(dl['dataliquidacion'][0]['rut_digito_verificador']).strip(), 0, 0, 'L')
            pdfliq.set_xy(40, 42)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['grado']).strip(), 0, 0, 'L')
            pdfliq.set_xy(75, 42)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['nombre']).strip(), 0, 0, 'L')
            pdfliq.set_xy(60, 52)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['reparticion']).strip(), 0, 0, 'L')
            pdfliq.set_xy(110, 52)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['dotacion']).strip(), 0, 0, 'L')
            pdfliq.set_xy(18, 52)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['ge']).strip(), 0, 0, 'L')
            pdfliq.set_xy(26, 52)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['gs']).strip(), 0, 0, 'L')
            pdfliq.set_xy(34, 52)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['tr']).strip(), 0, 0, 'L')
            pdfliq.set_xy(42, 52)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['cf']).strip(), 0, 0, 'L')
            pdfliq.set_xy(50, 52)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['ss']).strip(), 0, 0, 'L')
            pdfliq.set_xy(140, 42)
            pdfliq.cell(35, 5, str(dl['dataliquidacion'][0]['tipo_sueldo_descripcion']).strip(), 0, 0, 'L')

            contarhaberes = 0
            saltolinea = 3
            numbase = 60
            for elementoshaberes in dl['haberes']:
                contarhaberes += 1
            codigoqr = qrcodecarabineros(data)
            pdfliq.image(codigoqr, 180, 10, 25, 25, 'png')
            # Despues de mostrar el codigo Qr en el documento lo elimino para no usar espacio en el servidor.
            os.remove(codigoqr)

            # Creado codigo de Barras
            codigobarras = codigobarrascarabineros(data)
            # pdfliq.set_xy(50,309)
            pdfliq.image(codigobarras, 45, 309, 130, 15, 'png')
            # Despues de mostrar el codigo de barras en el documento lo elimino para no usar espacio en el servidor.
            os.remove(codigobarras)

    def informaciongeneral():
        y = 277
        cont = aux = 0
        data = [{'codigo': 'I', 'descripcion': 'Remuneracion Imponible.'}, {'codigo': 'T', 'descripcion': 'Remuneracion Tributable.'}, {'codigo': 'Z', 'descripcion': 'Remuneracion Afecta a Zona.'},
                {'codigo': 'GE', 'descripcion': 'Grado de Empleo (Grado jerarquico que ostenta).'}, {'codigo': 'GS', 'descripcion': 'Grado de Sueldo (Grado Mayor Sueldo que posee).'},
                {'codigo': 'TR', 'descripcion': 'Trienios con que cuenta.'}, {'codigo': 'CF', 'descripcion': 'Cargas Familiares reconocidas.'},
                {'codigo': 'SS', 'descripcion': 'Sobresueldo (Especialidad que posee).'}, {'codigo': 'F.TERMINO', 'descripcion': 'Fecha termino de descuento.'},
                {'codigo': 'TOTAL HABERES', 'descripcion': 'Suma total de remuneraciones(detalle de haberes).'},
                {'codigo': 'TOTAL DESCUENTOS', 'descripcion': 'Suma Descuentos Legales + Descuentos Institucionales.'},
                {'codigo': 'TOTAL IMPONIBLE', 'descripcion': 'Suma total de Remuneraciones Imponibles (Todas las con Letra I).'},
                {'codigo': 'TOTAL AFECTO A ZONA', 'descripcion': 'Suma total de Remuneraciones Imponibles (Todas las con Letra Z).'},
                {'codigo': 'TOTAL AFECTO A IMPUESTO', 'descripcion': 'Suma total de Remuneraciones Tributable (Todas las con Letra T).'},
                {'codigo': 'ALCANCE LIQUIDO', 'descripcion': 'Total haberes - Total descuentos.'}]

        for cod in data:
            if cont <= 8:
                pdfliq.set_font('Arial', 'B', 6)
                pdfliq.set_xy(18, y)
                pdfliq.cell(15, 5, cod['codigo'], 0, 0, 'L')
                pdfliq.set_font('Arial', '', 6)
                pdfliq.set_xy(44, y)
                pdfliq.cell(15, 5, cod['descripcion'], 0, 0, 'L')
            else:
                if aux == 0:
                    aux = 1
                    y = 277
                pdfliq.set_font('Arial', 'B', 6)
                pdfliq.set_xy(108, y)
                pdfliq.cell(15, 5, cod['codigo'], 0, 0, 'L')
                pdfliq.set_font('Arial', '', 6)
                pdfliq.set_xy(139, y)
                pdfliq.cell(15, 5, cod['descripcion'], 0, 0, 'L')
            cont += 1
            y += 3

    def observaciones(data):
        cont = 1
        pdfliq.set_font('Arial', '', 5)
        for observa in data:
            if observa['observaciones']:
                for obs in observa['observaciones']:
                    # if obs['tipo'] == 'S':
                    pdfliq.set_xy(18, 252 + (cont * 3))
                    pdfliq.cell(170, 3, obs['obs'], 0, 0, 'L')
                    cont += 1

    def haberes(data):
        y = 1
        base = 63
        pdfliq.set_font('Arial', '', 6)
        for h in data:
            if h['haberes']:
                for haber in h['haberes']:
                    pdfliq.set_xy(18, base + (y * 3))
                    pdfliq.cell(5, 3, str(haber['prop']).strip(), 0, 0, 'R')
                    pdfliq.set_xy(28, base + (y * 3))
                    pdfliq.cell(30, 3, str(haber['descripcion']).strip(), 0, 0, 'L')
                    pdfliq.set_xy(70, base + (y * 3))
                    pdfliq.cell(15, 3, str(clppesos(haber['monto'])).strip(), 0, 0, 'R')
                    y += 1

    def deberes(data):
        y = 1
        base = 63
        if censura == 1:
            pdfliq.set_font('Arial', '', 6)
            for h in data:
                if h['deberes']:
                    for deber in h['deberes']:
                        pdfliq.set_xy(91, base + (y * 3))
                        pdfliq.cell(5, 3, str(deber['descripcion']).strip(), 0, 0, 'L')
                        pdfliq.set_xy(125, base + (y * 3))
                        pdfliq.cell(30, 3, str(deber['fechatermino']).strip(), 0, 0, 'R')
                        pdfliq.set_xy(160, base + (y * 3))
                        pdfliq.cell(15, 3, str(deber['origen']).strip(), 0, 0, 'L')
                        pdfliq.set_xy(188, base + (y * 3))
                        pdfliq.cell(15, 3, str(clppesos(deber['monto'])).strip(), 0, 0, 'R')
                        y += 1

    def totales(data):
        for tt in data:
            if tt['totales']:
                pdfliq.set_font('Arial', '', 6)
                for total in tt['totales']:
                    if total['totalimponible']:
                        pdfliq.set_xy(18, 212)
                        pdfliq.cell(22, 3, 'TOTAL IMPONIBLE', 0, 0, 'L')
                        pdfliq.set_xy(67, 211)
                        pdfliq.cell(22, 5, str(clppesos(total['totalimponible'])).strip(), 0, 0, 'R')
                    if total['totalimpuestos']:
                        pdfliq.set_xy(18, 216)
                        pdfliq.cell(22, 3, 'TOTAL AFECTO IMPUESTO', 0, 0, 'L')
                        pdfliq.set_xy(67, 215)
                        pdfliq.cell(22, 5, str(clppesos(total['totalimpuestos'])).strip(), 0, 0, 'R')
                    if total['totalzona']:
                        pdfliq.set_xy(18, 220)
                        pdfliq.cell(22, 3, 'TOTAL AFECTO ZONA', 0, 0, 'L')
                        pdfliq.set_xy(67, 219)
                        pdfliq.cell(22, 5, str(clppesos(total['totalzona'])).strip(), 0, 0, 'R')
                    if total['totalhaber']:
                        pdfliq.set_xy(18, 224)
                        pdfliq.cell(22, 3, 'TOTAL HABERES', 0, 0, 'L')
                        pdfliq.set_xy(67, 223)
                        pdfliq.cell(22, 5, str(clppesos(total['totalhaber'])).strip(), 0, 0, 'R')
                    # if total['totalliquido']:
                    if censura == 1:
                        pdfliq.set_font('Arial', 'B', 8)
                        pdfliq.set_xy(93, 244)
                        pdfliq.cell(22, 3, 'ALCANCE LIQUIDO', 0, 0, 'L')
                        pdfliq.set_xy(180, 243)
                        pdfliq.cell(22, 5, str(clppesos(total['totalliquido'])).strip(), 0, 0, 'R')
                        if total['totaldescuentos']:
                            pdfliq.set_font('Arial', '', 6)
                            pdfliq.set_xy(18, 232)
                            pdfliq.cell(22, 3, 'DESCUENTOS PARTICULARES', 0, 0, 'L')
                            pdfliq.set_xy(67, 231)
                            pdfliq.cell(22, 5, str(clppesos(total['totaldescuentos'])).strip(), 0, 0, 'R')
                        # if total['totalliquido']:
                        pdfliq.set_font('Arial', 'B', 8)
                        pdfliq.set_xy(30, 248)
                        pdfliq.cell(22, 3, str(numero_a_letras(total['totalliquido'])).strip() + " PESOS.-", 0, 0, 'L')

    def descuentostotales(data):
        global afpporcentaje
        for totalesdescuentos in data:
            y = 212
            if totalesdescuentos['previsionDipreca']:
                for dipreca in totalesdescuentos['previsionDipreca']:
                    pdfliq.set_font('Arial', '', 6)
                    if dipreca['fondo_hoscar']:
                        # FONDO PARA HOSCAR
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "FONDO PARA HOSCAR", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "(1,5%)", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(dipreca['fondo_hoscar'])), 0, 0, "R")
                        y += 4
                    if dipreca['fondo_hospital_dipreca']:
                        # FONDO HOSPITAL DIPRECA
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "FONDO HOSPITAL DIPRECA", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "(1.0%)", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(dipreca['fondo_hospital_dipreca'])), 0, 0, "R")
                        y += 4
                    if dipreca['fondo_desahucio']:
                        # FONDO DESAHUCIO
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "FONDO DESAHUCIO", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "(6.0%)", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(dipreca['fondo_desahucio'])), 0, 0, "R")
                        y += 4
                    if dipreca['fondo_retiro_dipreca']:
                        # FONDO RETIRO DIPRECA
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "FONDO RETIRO DIPRECA", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "(8.5%)", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(dipreca['fondo_retiro_dipreca'])), 0, 0, "R")
                        y += 4
                    if dipreca['fondo_rev_pension']:
                        # FONDO REV. PENSIONES
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "FONDO REV. PENSIONES", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "(1.0%)", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(dipreca['fondo_rev_pension'])), 0, 0, "R")
                        y += 4
                    if dipreca['impuesto_unico']:
                        # IMPUESTO UNICO
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "IMPUESTO UNICO", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(dipreca['impuesto_unico'])), 0, 0, "R")
                        y += 4
                    if dipreca['provision_impuesto']:
                        # PROVISION IMPUESTO
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "PROVISION IMPUESTO", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(dipreca['provision_impuesto'])), 0, 0, "R")
                        y += 4

            if totalesdescuentos['previosionOtros']:
                ## print('entro prevision otros')
                if totalesdescuentos['dataliquidacion']:
                    for info in totalesdescuentos['dataliquidacion']:
                        afpporcentaje = info['porcentaje']

                for prevision in totalesdescuentos['previosionOtros']:
                    y = 212
                    pdfliq.set_font('Arial', '', 6)
                    if prevision['afp_nombre']:
                        # AFP
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "AFP " + str(prevision['afp_nombre']).strip(), 0, 0, "L")
                        if afpporcentaje:
                            pdfliq.set_xy(150, y)
                            pdfliq.cell(10, 3, str(afpporcentaje).strip() + "%", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['afp_valor'])), 0, 0, "R")
                        y += 4
                    if prevision['afp_adicional'] != 0:
                        # AFP ADICIONAL
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "AFP ADICIONAL ", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['afp_adicional'])), 0, 0, "R")
                        y += 4
                    if prevision['isapre_valor'] != 0:
                        # ISAPRE
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "ISAPRE " + str(prevision['isapre_nombre']).strip(), 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['isapre_valor'])), 0, 0, "R")
                        y += 4
                    if prevision['isapre_adicional'] != 0:
                        # ISAPRE ADICIONAL
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "ISAPRE " + str(prevision['isapre_nombre']).strip() + " ADICIONAL", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['isapre_adicional'])), 0, 0, "R")
                        y += 4
                    if prevision['impuesto_unico'] != 0:
                        # IMPUESTO UNICO
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "IMPUESTO UNICO", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['impuesto_unico'])), 0, 0, "R")
                        y += 4
                    if prevision['provision_impuesto'] != 0:
                        # PROVISION IMPUESTO
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "PROVISION IMPUESTO", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['provision_impuesto'])), 0, 0, "R")
                        y += 4
                    if prevision['afp_ahorro'] != 0:
                        # AFP AHORRO
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "AFP AHORRO", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['afp_ahorro'])), 0, 0, "R")
                        y += 4
                    if prevision['apv_ahorro'] != 0:
                        # APV AHORRO
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "APV AHORRO", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['apv_ahorro'])), 0, 0, "R")
                        y += 4
                    if prevision['seguro_invalidez'] != 0:
                        # SEGURO INVALIDEZ
                        pdfliq.set_xy(93, y)
                        pdfliq.cell(10, 3, "SEGURO INVALIDEZ", 0, 0, "L")
                        pdfliq.set_xy(150, y)
                        pdfliq.cell(10, 3, "", 0, 0, "L")
                        pdfliq.set_xy(192, y)
                        pdfliq.cell(10, 3, str(clppesos(prevision['seguro_invalidez'])), 0, 0, "R")
                        y += 4

                    descuentoslegales = int(prevision['afp_valor']) + int(prevision['afp_adicional']) + int(prevision['isapre_valor']) + int(prevision['isapre_adicional']) + int(
                        prevision['impuesto_unico']) + int(prevision['provision_impuesto']) + int(prevision['afp_ahorro']) + int(prevision['apv_ahorro'])
                if descuentoslegales:
                    pdfliq.set_font('Arial', '', 6)
                    pdfliq.set_xy(18, 228)
                    pdfliq.cell(22, 3, 'DESCUENTOS LEGALES', 0, 0, 'L')
                    pdfliq.set_xy(67, 227)
                    pdfliq.cell(22, 5, str(clppesos(descuentoslegales)).strip(), 0, 0, 'R')

    token = validar_token()
    data = token.json

    rut = str(rut).strip()
    fechaDesde = str(fecha_desde).strip()  # YYYYmm
    fechaHasta = str(fecha_hasta).strip()  # YYYYmm
    dateDesde = datetime.date(datetime.strptime(fechaDesde, '%Y-%m'))
    dateHasta = datetime.date(datetime.strptime(fechaHasta, '%Y-%m'))
    pdfliq = FPDF(orientation='P', unit='mm', format=(216, 330))
    while dateDesde <= dateHasta:
        contratos = []
        fecha_mes = str(dateDesde).replace('-', '').strip()[:-2]
        dateDesde = dateDesde + relativedelta(months=1)

        for contrato in listar_contratos(rut, fecha_mes):
            id_tipo_funcionario = str(contrato[0]).strip()
            id_tipo_detalle = str(contrato[1]).strip()
            imponible = int(contrato[2])
            reparticion = str(contrato[3]).strip()
            unidad = str(contrato[4]).strip()
            alcance_liquido = int(contrato[5])
            # contratos.append({
            #    'id_tipo_funcionario': id_tipo_funcionario,
            #    'id_tipo_detalle': id_tipo_detalle,
            #    'imponible': imponible,
            #    'reparticion': reparticion,
            #    'unidad': unidad,
            #    'alcance_liquido': alcance_liquido
            # })
            arraycontrato = []
            # print(fecha_mes, contrato)

            try:
                conn = conectorbd()
                cursor = conn.cursor()
                cursor.execute(
                    "EXEC BD_REMUNE.dbo.sp_consultar_LiqBilletaje_2 " + str(rut).strip() + ", " + str(fecha_mes).strip() + ",'" + str(id_tipo_funcionario).strip() + "','" + str(
                        id_tipo_detalle).strip() + "'")
                billetaje = cursor.fetchall()
                if len(billetaje) > 0:
                    for b in billetaje:
                        # Indica la cantidad de contratos
                        arraycontrato.append(b[0])

                        match str(b[0]).strip():
                            case 'P':
                                verificarcontrato = "EXEC BD_REMUNE.dbo.sp_consultar_cabliqLiqui " + str(rut).strip() + ", " + str(fecha_mes).strip() + ",'" + str(
                                    id_tipo_funcionario).strip() + "',"                                                                                                                                                                     "'" + str(
                                    id_tipo_detalle).strip() + "'"
                            case 'S':
                                verificarcontrato = "EXEC BD_REMUNE.dbo.sp_consultar_cabliqSeg " + str(rut).strip() + ", " + str(fecha_mes).strip() + ",'" + str(
                                    id_tipo_funcionario).strip() + "','" + str(
                                    id_tipo_detalle).strip() + "'"
                            case 'R':
                                verificarcontrato = "EXEC BD_REMUNE.dbo.sp_consultar_cabliqReno " + str(rut).strip() + ", " + str(fecha_mes).strip() + ",'" + str(
                                    id_tipo_funcionario).strip() + "','" + str(
                                    id_tipo_detalle).strip() + "'"
                            case 'MP':
                                verificarcontrato = "EXEC BD_REMUNE.dbo.sp_consultar_cabliqManual " + str(rut).strip() + ", " + str(fecha_mes).strip() + ",'" + str(
                                    id_tipo_funcionario).strip() + "','" + str(
                                    id_tipo_detalle).strip() + "', 'P'"
                            case 'MS':
                                verificarcontrato = "EXEC BD_REMUNE.dbo.sp_consultar_cabliqManual " + str(rut).strip() + ", " + str(fecha_mes).strip() + ",'" + str(
                                    id_tipo_funcionario).strip() + "','" + str(
                                    id_tipo_detalle).strip() + "', 'S'"
                            case 'MR':
                                verificarcontrato = "EXEC BD_REMUNE.dbo.sp_consultar_cabliqManual " + str(rut).strip() + ", " + str(fecha_mes).strip() + ",'" + str(
                                    id_tipo_funcionario).strip() + "','" + str(
                                    id_tipo_detalle).strip() + "', 'R'"

                else:
                    return jsonify({'msg': 'No existe liquidacion para la fecha consultada.'}), 404
            except Exception as error:
                return jsonify({'msg': error}), 400
            finally:
                if cursor:
                    cursor.close()

            try:
                conn = conectorbd()
                cursor = conn.cursor()
                cursor.execute(verificarcontrato)
                infocontrato = cursor.fetchone()
                if infocontrato:
                    # return jsonify({'infocontrato': infocontrato})
                    rut_c = infocontrato[0]
                    dv_c = infocontrato[1]
                    codigo_c = infocontrato[2]
                    nombre_c = infocontrato[3]
                    fechaingreso_c = infocontrato[4]
                    fechaingresoformato_c = infocontrato[5]
                    ge_c = infocontrato[6]
                    gs_c = infocontrato[7]
                    tr_c = infocontrato[8]
                    cf_c = infocontrato[9]
                    ssn_c = infocontrato[10]
                    ss_c = infocontrato[11]
                    prevision_c = infocontrato[12]
                    previsionporcentaje_c = infocontrato[13]
                    dotacion_c = infocontrato[14]
                    salud_c = infocontrato[15]
                    tiposueldo_c = infocontrato[16]
                    tiposueldodescripcion_c = infocontrato[17]
                    tracernumber_c = infocontrato[18]
                    grado_c = infocontrato[19]
                    reparticion_c = infocontrato[20]
                    porcentaje_c = infocontrato[21]
                    unidad_c = infocontrato[22]
                    # seguro_c = infocontrato[23]
                    if str(rut_c).strip() == '':
                        return jsonify({'msg': 'No existe informacion del funcionario consultado. (revise tipo funcionario)'}), 403
                else:
                    return jsonify({'msg': 'No es posible obtener informacion de contrato.'}), 403
            except Exception as error:
                return jsonify({'msg': error}), 400
            finally:
                if cursor:
                    cursor.close()
            # =========================================================================================================================================================
            # problemas con funcionarios que tienen otra unidad contable.
            try:
                # validar reparticion funcionario
                # datatoken = validar_token()

                # for d1 in datatoken['datos']:
                #    login_rut = str(d1['id_rut']).strip()
                #    login_clave = str(d1['dt_clave']).strip()
                #    login_ucf = str(d1['dt_glosa'])
                #    login_sitio = 'LIQ'
                #    login_opcion = '00'
                #    login_ip = str(request.args.get('ip')).strip()
                #    login_pagina = 'liquidacion'
                #    login_bbdd = 'bd_remune'
                #    login_tabla = 'ta_liquidacion_' + fecha_mes
                #    login_operacion = 'C'
                #    login_texto_original = 'CONSULTA LIQUIDACION FUNCIONARIO '
                #    login_texto_nuevo = ''
                #    login_rut_mando = str(d1['id_rut']).strip()

                # movimientos(login_rut, login_clave, login_ucf, login_sitio, login_opcion, login_ip, login_pagina, login_bbdd, login_tabla, login_operacion, login_texto_original,
                # login_texto_nuevo,
                #            login_rut_mando)

                for r in data['datos4']:
                    reparticiondesde = '000000000000' if str(r['dt_multi_dotacion']).strip() == 'S' else str(r['dt_reparticion_desde']).strip()
                    reparticionhasta = '999999999999' if str(r['dt_multi_dotacion']).strip() == 'S' else str(r['dt_reparticion_hasta']).strip()
                    reparticioncentra = str(r['dt_reparticion_centra']).strip()
                    multidotacion = str(r['dt_multi_dotacion']).strip()
                    altomando = str(r['dt_acceso_altomando']).strip()
                    superusuario = str(r['dt_super_usuario']).strip()
            except Exception as error:
                return jsonify({'msg': error}), 400
            # =========================================================================================================================================================
            try:
                # consulta privilegios alto mando
                conn = conectorbd()
                cursor = conn.cursor()
                cursor.execute("EXEC BD_PERFIL.dbo.sp_consultar_mando " + str(rut).strip())
                altomando2 = cursor.fetchone()
                if altomando2 is not None:
                    for a in altomando2:
                        rutalto = a[0]
                        nombrealto = a[1]
                        cargoalto = a[2]

                    if str(rutalto).strip() == str(rut).strip() and altomando == 'N':
                        return jsonify({'msg': 'no tiene privilegios alto mando.'}), 404

            except Exception as error:
                return jsonify({'msg': error}), 400
            finally:
                if cursor:
                    cursor.close()

            try:
                numeropaginas = 0
                arreglo1 = [{'P': 'N', 'R': 'N', 'S': 'N', 'MP': 'N', 'MS': 'N', 'MR': 'N'}]
                anno = fecha_mes[:-2]
                mes = messtring(int(fecha_mes[-2:])).upper()

                for a in arreglo1:
                    for ac in arraycontrato:

                        if a[ac]:
                            a[ac] = 'S'
                            numeropaginas += 1
                # pdfliq = FPDF(orientation='P', unit='mm', format=(216, 330))
                if numeropaginas > 0:

                    if str(arreglo1[0]['P']).strip() == 'S':
                        # print("Entra a primera linea -------------------------------------------------------")
                        contarpaginaP = 1
                        totalpaginas = detallehaberes(rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)

                        while contarpaginaP <= totalpaginas:

                            # if numeropaginas == 1:
                            #    if totalpaginas > 1:
                            #       paginatotal = 1
                            # else:
                            #   paginatotal = 0
                            # if totalpaginas == 2:
                            #    pdfopagina = totalpaginas
                            #    pdfopag = 2
                            # cabecera('TRACERNUMER')
                            pdfliq.add_page()

                            datosliquidacion = crearliquidacion('Liqui', rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)
                            for dl in datosliquidacion:
                                tracernumber = dl['dataliquidacion'][0]['tracernumber']

                            # anno = fecha_mes[:-2]
                            # mes = messtring(int(fecha_mes[-2:])).upper()
                            # Crear PDF con datos
                            cabecera('LIQUIDACION DE REMUNERACIONES', tracernumber, mes, anno)
                            rayado(contarpaginaP, totalpaginas)
                            llenardocumento(datosliquidacion)
                            haberes(datosliquidacion)
                            deberes(datosliquidacion)
                            totales(datosliquidacion)
                            descuentostotales(datosliquidacion)
                            informaciongeneral()
                            observaciones(datosliquidacion)

                            contarpaginaP += 1

                    if str(arreglo1[0]['S']).strip() == 'S':
                        # print("Entra a segunda linea -------------------------------------------------------------")
                        contarpaginaR = 1
                        totalpaginas = detallehaberes(rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)

                        while contarpaginaR <= totalpaginas:
                            pdfliq.add_page()

                            # Creando documento PDF
                            datosliquidacion = crearliquidacion('Seg', rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)

                            for dl in datosliquidacion:
                                tracernumber = dl['dataliquidacion'][0]['tracernumber']

                            cabecera('DIFERENCIAS MESES ANTERIORES N', tracernumber, mes, anno)
                            rayado(contarpaginaR, totalpaginas)
                            llenardocumento(datosliquidacion)
                            haberes(datosliquidacion)
                            deberes(datosliquidacion)
                            totales(datosliquidacion)
                            descuentostotales(datosliquidacion)
                            informaciongeneral()
                            observaciones(datosliquidacion)

                            contarpaginaR += 1

                    if str(arreglo1[0]['R']).strip() == 'S':
                        # print("Entra a reno -----------------------------------------------------------------")
                        contarpaginaR = 1
                        totalpaginas = detallehaberes(rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)

                        while contarpaginaR <= totalpaginas:
                            pdfliq.add_page()

                            # Creando documento PDF
                            datosliquidacion = crearliquidacion('Reno', rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)
                            for dl in datosliquidacion:
                                tracernumber = dl['dataliquidacion'][0]['tracernumber']

                            cabecera('DIFERENCIAS AÑOS ANTERIORES N', tracernumber, mes, anno)
                            rayado(contarpaginaR, totalpaginas)
                            llenardocumento(datosliquidacion)
                            haberes(datosliquidacion)
                            deberes(datosliquidacion)
                            totales(datosliquidacion)
                            descuentostotales(datosliquidacion)
                            informaciongeneral()
                            observaciones(datosliquidacion)

                            contarpaginaR += 1

                    if str(arreglo1[0]['MP']).strip() == 'S':
                        # print("Entra a MANUAL PRIMERA ------------------------------------------------------")
                        contarpaginaMP = 1
                        totalpaginas = detallehaberes(rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)

                        while contarpaginaMP <= totalpaginas:
                            pdfliq.add_page()

                            # Creando documento PDF
                            datosliquidacion = crearliquidacion('ManualP', rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)
                            for dl in datosliquidacion:
                                tracernumber = dl['dataliquidacion'][0]['tracernumber']

                            cabecera('PAGOS MANUALES N', tracernumber, mes, anno)
                            rayado(contarpaginaMP, totalpaginas)
                            contarpaginaMP += 1

                    if str(arreglo1[0]['MS']).strip() == 'S':
                        # print("Entra a MANUAL SEGUNDA ------------------------------------------------------------")
                        contarpaginaMS = 1
                        totalpaginas = detallehaberes(rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)

                        while contarpaginaMS <= totalpaginas:
                            pdfliq.add_page()

                            # Creando documento PDF
                            datosliquidacion = crearliquidacion('ManualS', rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)
                            for dl in datosliquidacion:
                                tracernumber = dl['dataliquidacion'][0]['tracernumber']

                            cabecera('PAGOS MANUALES DIF. MESES ANT. N', tracernumber, mes, anno)
                            rayado(contarpaginaMS, totalpaginas)
                            contarpaginaMS += 1

                    if str(arreglo1[0]['MR']).strip() == 'S':
                        # print("Entra a MANUAL RENO ---------------------------------------------------------------")
                        contarpaginaMR = 1
                        totalpaginas = detallehaberes(rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)

                        while contarpaginaMR <= totalpaginas:
                            pdfliq.add_page()

                            # Creando documento PDF
                            datosliquidacion = crearliquidacion('ManualR', rut, fecha_mes, id_tipo_funcionario, id_tipo_detalle)
                            for dl in datosliquidacion:
                                tracernumber = dl['dataliquidacion'][0]['tracernumber']
                            # anno = fecha_mes[:-2]
                            # mes = messtring(int(fecha_mes[-2:])).upper()

                            cabecera('PAGOS MANUALES DIF. AÑOS ANT. N', tracernumber, mes, anno)
                            rayado(contarpaginaMR, totalpaginas)
                            contarpaginaMR += 1

                    ## aca tengo que terminar el recorrido del ciclo para poner mas liquidaciones.

                    # response = make_response(pdfliq.output(dest='S').encode("latin-1"))
                    # response.headers.set('Content-Disposition', 'inline', filename=rut + '.pdf')
                    # response.headers.set('Content-Type', 'application/pdf')
                    # return response

                else:
                    return jsonify({'msg': 'no existe liquidacion'}), 404

            except Exception as error:
                return jsonify({'msg': error}), 400

    pdfliq.close()
    # response = make_response(pdfliq.output(dest='S').encode("latin-1"))
    # response.headers.set('Content-Disposition', 'inline', filename=rut + '.pdf')
    # response.headers.set('Content-Type', 'application/pdf')
    return pdfliq


def clppesos(valor: int):
    dinero = '{:,}'.format(valor).replace(',', '.')
    # montopesos = str(valor).replace('.',',')
    return dinero


def tipofuncionario(idtipo):
    match idtipo:
        case 'U':
            return 'Uniformado'
        case 'I':
            return 'Civil'
        case 'P':
            return 'Profesor'
        case 'J':
            return 'Jornal'
        case 'M':
            return 'Medico'
        case _:
            return ''


def tipodetallecivil(iddetalle):
    match iddetalle:
        case 'C':
            return 'CPR'
        case 'C2':
            return 'CPR 2'
        case 'P':
            return 'Planta'
        case _:
            return ''


def tipodetallemedico(iddetalle):
    match iddetalle:
        case 'A':
            return 'AP28'
        case 'C':
            return 'CPR'
        case 'P':
            return 'Planta'
        case _:
            return ''


def validar_token():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    # return jsonify(logged_in_as=current_user), 200
    return jsonify(current_user)


def detallehaberes(rut, fecha, tf, df):
    try:
        conn = conectorbd()
        cursor = conn.cursor()
        cursor.execute("EXEC BD_REMUNE.dbo.sp_consultar_DetLiqLiqui " + str(rut).strip() + ", " + str(fecha).strip() + ",'" + str(tf).strip() + "','" + str(df).strip() + "'")
        detallehaberess = cursor.fetchall()
        lhab = ldesc = tdesc2 = 0
        op = 1
        for deta in detallehaberess:
            tipodet = str(deta[0]).strip()
            if tipodet == 'H':
                lhab += 1
                nfil = lhab
            if tipodet == 'D':
                ldesc += 1
                nfil = ldesc
            if nfil >= 51:
                op = 2
        return op
    except Exception as error:
        return jsonify({'msg': error}), 400
    finally:
        if cursor:
            cursor.close()


def messtring(idmes):
    match idmes:
        case 1:
            return 'Enero'
        case 2:
            return 'Febrero'
        case 3:
            return 'Marzo'
        case 4:
            return 'Abril'
        case 5:
            return 'Mayo'
        case 6:
            return 'Junio'
        case 7:
            return 'Julio'
        case 8:
            return 'Agosto'
        case 9:
            return 'Septiembre'
        case 10:
            return 'Octubre'
        case 11:
            return 'Noviembre'
        case 12:
            return 'Diciembre'
        case _:
            return ''


def listar_contratos(rut, fecha):
    try:
        conn = conectorbd()
        cursor = conn.cursor()
        cursor.execute("EXEC BD_REMUNE.dbo.sp_listar_contratos " + rut + ", " + fecha)
        contratos = cursor.fetchall()
        cursor.close()
        return contratos
    except Exception as error:
        return error
