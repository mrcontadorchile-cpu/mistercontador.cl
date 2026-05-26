#!/usr/bin/env python3
"""Genera PDFs de material contable educativo para mistercontador.cl"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                 Spacer, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Paleta Mister Contador
GOLD   = colors.HexColor('#F5C200')
BLACK  = colors.HexColor('#0a0a0a')
DARK   = colors.HexColor('#1a1a1a')
GRAY   = colors.HexColor('#555555')
LGRAY  = colors.HexColor('#eeeeee')
WHITE  = colors.white

OUT = os.path.dirname(os.path.abspath(__file__))

def base_doc(filename, title):
    path = os.path.join(OUT, filename)
    doc = SimpleDocTemplate(path, pagesize=letter,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm,
                            title=title, author='Mister Contador')
    return doc

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = letter
    # Header bar
    canvas.setFillColor(GOLD)
    canvas.rect(0, h - 1.5*cm, w, 1.5*cm, fill=1, stroke=0)
    canvas.setFillColor(BLACK)
    canvas.setFont('Helvetica-Bold', 11)
    canvas.drawString(2*cm, h - 1.1*cm, 'MISTER CONTADOR')
    canvas.setFont('Helvetica', 9)
    canvas.drawRightString(w - 2*cm, h - 1.1*cm, 'mistercontador.cl')
    # Footer
    canvas.setFillColor(LGRAY)
    canvas.rect(0, 0, w, 1*cm, fill=1, stroke=0)
    canvas.setFillColor(GRAY)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(2*cm, 0.35*cm, 'Herramienta educativa gratuita — mistercontador.cl/herramientas/guia-cuentas-contables/')
    canvas.drawRightString(w - 2*cm, 0.35*cm, f'Pág. {doc.page}')
    canvas.restoreState()

def styles():
    ss = getSampleStyleSheet()
    title = ParagraphStyle('MCtitle', parent=ss['Title'],
                           fontSize=22, textColor=BLACK, spaceAfter=6,
                           fontName='Helvetica-Bold', alignment=TA_LEFT)
    sub   = ParagraphStyle('MCsub', parent=ss['Normal'],
                           fontSize=10, textColor=GRAY, spaceAfter=12,
                           fontName='Helvetica')
    h2    = ParagraphStyle('MCh2', parent=ss['Heading2'],
                           fontSize=13, textColor=BLACK, spaceBefore=14,
                           spaceAfter=6, fontName='Helvetica-Bold')
    body  = ParagraphStyle('MCbody', parent=ss['Normal'],
                           fontSize=9, textColor=colors.HexColor('#333333'),
                           spaceAfter=6, fontName='Helvetica', leading=13)
    note  = ParagraphStyle('MCnote', parent=ss['Normal'],
                           fontSize=8, textColor=GRAY,
                           fontName='Helvetica-Oblique', leading=11)
    return title, sub, h2, body, note

# ─────────────────────────────────────────────────────────────────────────────
# 1. LIBRO DIARIO
# ─────────────────────────────────────────────────────────────────────────────
def make_libro_diario():
    doc = base_doc('libro-diario.pdf', 'Libro Diario — Mister Contador')
    title_s, sub_s, h2_s, body_s, note_s = styles()
    story = []

    story.append(Paragraph('LIBRO DIARIO', title_s))
    story.append(Paragraph('Formato para registrar cronológicamente las operaciones contables de tu empresa.', sub_s))
    story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceAfter=10))

    # Instrucciones
    story.append(Paragraph('¿Cómo usarlo?', h2_s))
    instrucciones = [
        '1. Registra cada operación en orden cronológico, de la más antigua a la más reciente.',
        '2. Cada operación debe tener al menos una cuenta en el DEBE y una en el HABER.',
        '3. El total del DEBE siempre debe ser igual al total del HABER (partida doble).',
        '4. Usa la columna "Glosa" para describir brevemente qué pasó.',
        '5. Numera cada asiento de forma correlativa.',
    ]
    for i in instrucciones:
        story.append(Paragraph(i, body_s))

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('Empresa: ________________________________  RUT: _____________________  Período: _______________', body_s))
    story.append(Spacer(1, 0.3*cm))

    # Tabla principal — 20 filas vacías
    header = ['N°', 'Fecha', 'Cuenta', 'Glosa / Descripción', 'Debe ($)', 'Haber ($)']
    data = [header]
    for i in range(1, 21):
        data.append([str(i), '', '', '', '', ''])
    # Fila totales
    data.append(['', '', '', 'TOTALES', '___________', '___________'])

    col_w = [1.2*cm, 2.2*cm, 3.8*cm, 6.2*cm, 2.8*cm, 2.8*cm]
    tbl = Table(data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), GOLD),
        ('TEXTCOLOR',    (0,0), (-1,0), BLACK),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0), 9),
        ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
        ('ALIGN',        (3,1), (3,-1), 'LEFT'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, LGRAY]),
        ('BACKGROUND',   (0,-1), (-1,-1), colors.HexColor('#f0f0f0')),
        ('FONTNAME',     (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('GRID',         (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('BOX',          (0,0), (-1,-1), 1, GOLD),
        ('ROWHEIGHT',    (0,1), (-1,-2), 0.7*cm),
        ('ROWHEIGHT',    (0,0), (-1,0), 0.65*cm),
        ('FONTSIZE',     (0,1), (-1,-1), 8),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
    ]))
    story.append(tbl)

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('⚡ Recuerda: Debe = Haber en cada asiento. Si no cuadra, revisa las cuentas utilizadas.', note_s))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Firma responsable: _________________________________  Fecha de cierre: ________________', body_s))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print('✓ libro-diario.pdf')

# ─────────────────────────────────────────────────────────────────────────────
# 2. LIBRO MAYOR
# ─────────────────────────────────────────────────────────────────────────────
def make_libro_mayor():
    doc = base_doc('libro-mayor.pdf', 'Libro Mayor — Mister Contador')
    title_s, sub_s, h2_s, body_s, note_s = styles()
    story = []

    story.append(Paragraph('LIBRO MAYOR', title_s))
    story.append(Paragraph('Formato para resumir los movimientos de cada cuenta y calcular su saldo.', sub_s))
    story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceAfter=10))

    story.append(Paragraph('¿Cómo usarlo?', h2_s))
    instrucciones = [
        '1. Crea una hoja (tarjeta T) por cada cuenta que uses en tu contabilidad.',
        '2. Anota en el DEBE los aumentos de activos y gastos; en el HABER los aumentos de pasivo, patrimonio e ingresos.',
        '3. Al final del período, suma el DEBE y el HABER por separado.',
        '4. El Saldo es la diferencia: si el DEBE es mayor → Saldo Deudor; si el HABER es mayor → Saldo Acreedor.',
        '5. Transfiere los saldos al Balance de Comprobación.',
    ]
    for i in instrucciones:
        story.append(Paragraph(i, body_s))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Empresa: ________________________________  Período: _______________', body_s))
    story.append(Spacer(1, 0.4*cm))

    # Genera 4 tarjetas T por página
    cuentas_ejemplo = ['Caja', 'Banco', 'Clientes', 'Proveedores',
                       'Ventas', 'Costo de Ventas', 'Sueldos', 'Capital']

    for idx, cuenta in enumerate(cuentas_ejemplo):
        story.append(Paragraph(f'Cuenta: {cuenta}', h2_s))

        header = ['Fecha', 'Glosa', 'N° Asiento', 'DEBE ($)', 'HABER ($)', 'Saldo ($)']
        data = [header]
        for _ in range(8):
            data.append(['', '', '', '', '', ''])
        data.append(['', 'TOTALES', '', '___________', '___________', '___________'])
        data.append(['', 'Tipo de Saldo:', '', 'Deudor □', 'Acreedor □', ''])

        col_w = [2*cm, 5.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]
        tbl = Table(data, colWidths=col_w, repeatRows=1)
        tbl.setStyle(TableStyle([
            ('BACKGROUND',   (0,0), (-1,0), GOLD),
            ('TEXTCOLOR',    (0,0), (-1,0), BLACK),
            ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',     (0,0), (-1,0), 8),
            ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
            ('ALIGN',        (1,1), (1,-1), 'LEFT'),
            ('ROWBACKGROUNDS', (0,1), (-1,-3), [WHITE, LGRAY]),
            ('BACKGROUND',   (0,-2), (-1,-1), colors.HexColor('#f0f0f0')),
            ('FONTNAME',     (0,-2), (-1,-1), 'Helvetica-Bold'),
            ('GRID',         (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
            ('BOX',          (0,0), (-1,-1), 1, GOLD),
            ('ROWHEIGHT',    (0,1), (-1,-3), 0.65*cm),
            ('FONTSIZE',     (0,1), (-1,-1), 8),
            ('TOPPADDING',   (0,0), (-1,-1), 3),
            ('BOTTOMPADDING',(0,0), (-1,-1), 3),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph('⚡ El saldo de cada cuenta del Libro Mayor alimenta el Balance de Comprobación y el Balance General.', note_s))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print('✓ libro-mayor.pdf')

# ─────────────────────────────────────────────────────────────────────────────
# 3. PLAN DE CUENTAS BÁSICO
# ─────────────────────────────────────────────────────────────────────────────
def make_plan_cuentas():
    doc = base_doc('plan-cuentas-basico.pdf', 'Plan de Cuentas Básico — Mister Contador')
    title_s, sub_s, h2_s, body_s, note_s = styles()
    story = []

    story.append(Paragraph('PLAN DE CUENTAS BÁSICO PARA PYMES', title_s))
    story.append(Paragraph('Listado ordenado de cuentas contables para una PyME chilena. Adapta los nombres a tu rubro y giro.', sub_s))
    story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceAfter=10))

    story.append(Paragraph('Empresa: ________________________________  RUT: _____________________  Giro: _______________', body_s))
    story.append(Spacer(1, 0.3*cm))

    cuentas = [
        # (código, nombre, tipo, descripción)
        ('1', 'ACTIVO', 'header', ''),
        ('1.1', 'Activo Corriente', 'subheader', ''),
        ('1.1.01', 'Caja', 'Activo', 'Efectivo físico disponible en el local.'),
        ('1.1.02', 'Banco', 'Activo', 'Saldo en cuenta corriente o vista.'),
        ('1.1.03', 'Clientes', 'Activo', 'Deudas de clientes por ventas a crédito.'),
        ('1.1.04', 'Inventario / Mercadería', 'Activo', 'Productos disponibles para la venta.'),
        ('1.1.05', 'IVA Crédito Fiscal', 'Activo', 'IVA de compras recuperable.'),
        ('1.1.06', 'PPM por recuperar', 'Activo', 'Pagos provisionales acumulados.'),
        ('1.1.07', 'Documentos por cobrar', 'Activo', 'Pagarés o letras a favor de la empresa.'),
        ('1.1.08', 'Anticipo a proveedores', 'Activo', 'Pagos adelantados a proveedores.'),
        ('1.2', 'Activo No Corriente', 'subheader', ''),
        ('1.2.01', 'Maquinaria y Equipos', 'Activo', 'Equipos usados en la operación.'),
        ('1.2.02', 'Vehículos', 'Activo', 'Medios de transporte de la empresa.'),
        ('1.2.03', 'Muebles y Útiles', 'Activo', 'Mobiliario y equipamiento.'),
        ('1.2.04', 'Depreciación acumulada', 'Activo', 'Desgaste acumulado de activos fijos (saldo acreedor).'),
        ('1.2.05', 'Depósitos en garantía', 'Activo', 'Garantías entregadas por contratos.'),
        ('2', 'PASIVO', 'header', ''),
        ('2.1', 'Pasivo Corriente', 'subheader', ''),
        ('2.1.01', 'Proveedores', 'Pasivo', 'Deudas por compras a crédito.'),
        ('2.1.02', 'IVA Débito Fiscal', 'Pasivo', 'IVA cobrado en ventas, adeudado al SII.'),
        ('2.1.03', 'PPM por pagar', 'Pasivo', 'Pago provisional mensual declarado.'),
        ('2.1.04', 'Impuesto a la renta por pagar', 'Pasivo', 'Impuesto de 1ª categoría del ejercicio.'),
        ('2.1.05', 'Remuneraciones por pagar', 'Pasivo', 'Sueldos devengados aún no pagados.'),
        ('2.1.06', 'AFP por pagar', 'Pasivo', 'Cotizaciones previsionales retenidas.'),
        ('2.1.07', 'Salud por pagar', 'Pasivo', 'Cotizaciones de salud retenidas.'),
        ('2.1.08', 'Documentos por pagar', 'Pasivo', 'Pagarés o letras firmadas a terceros.'),
        ('2.2', 'Pasivo No Corriente', 'subheader', ''),
        ('2.2.01', 'Préstamos bancarios L/P', 'Pasivo', 'Créditos bancarios a más de 12 meses.'),
        ('2.2.02', 'Leasing', 'Pasivo', 'Deuda por arrendamiento financiero.'),
        ('3', 'PATRIMONIO', 'header', ''),
        ('3.1.01', 'Capital', 'Patrimonio', 'Aportes de los dueños a la empresa.'),
        ('3.1.02', 'Utilidades acumuladas', 'Patrimonio', 'Ganancias anteriores retenidas.'),
        ('3.1.03', 'Pérdidas acumuladas', 'Patrimonio', 'Pérdidas anteriores no cubiertas.'),
        ('3.1.04', 'Resultado del ejercicio', 'Patrimonio', 'Ganancia o pérdida del período actual.'),
        ('3.1.05', 'Reservas', 'Patrimonio', 'Utilidades reservadas con fines específicos.'),
        ('4', 'INGRESOS', 'header', ''),
        ('4.1.01', 'Ventas', 'Ingreso', 'Ingresos por venta de productos del giro.'),
        ('4.1.02', 'Ingresos por servicios', 'Ingreso', 'Ingresos por prestación de servicios.'),
        ('4.1.03', 'Otros ingresos operacionales', 'Ingreso', 'Ingresos relacionados al giro, no directos.'),
        ('4.2.01', 'Ingresos no operacionales', 'Ingreso', 'Intereses, venta de activos u otros.'),
        ('5', 'GASTOS', 'header', ''),
        ('5.1.01', 'Costo de ventas', 'Gasto', 'Costo de la mercadería o servicio vendido.'),
        ('5.1.02', 'Sueldos y salarios', 'Gasto', 'Remuneraciones brutas del personal.'),
        ('5.1.03', 'Cotizaciones patronales', 'Gasto', 'SIS, AFP empleador, mutual.'),
        ('5.1.04', 'Arriendo', 'Gasto', 'Pago por uso del local u oficina.'),
        ('5.1.05', 'Servicios básicos', 'Gasto', 'Agua, luz, gas, internet, teléfono.'),
        ('5.1.06', 'Publicidad y marketing', 'Gasto', 'Gastos en promoción y difusión.'),
        ('5.1.07', 'Honorarios externos', 'Gasto', 'Contadores, asesores, diseñadores.'),
        ('5.1.08', 'Depreciación del período', 'Gasto', 'Desgaste de activos fijos del período.'),
        ('5.1.09', 'Seguros', 'Gasto', 'Primas de seguros del negocio.'),
        ('5.1.10', 'Intereses financieros', 'Gasto', 'Intereses de créditos o leasing.'),
        ('5.1.11', 'Gastos de representación', 'Gasto', 'Gastos relacionados a clientes o reuniones.'),
        ('5.1.12', 'Materiales y suministros', 'Gasto', 'Insumos y materiales de operación.'),
        ('5.1.13', 'Gastos varios', 'Gasto', 'Otros gastos menores de operación.'),
    ]

    TYPE_COLORS = {
        'Activo':    colors.HexColor('#FFF9E0'),
        'Pasivo':    colors.HexColor('#FFF0F0'),
        'Patrimonio':colors.HexColor('#F0FFF4'),
        'Ingreso':   colors.HexColor('#EFF6FF'),
        'Gasto':     colors.HexColor('#F7F7F7'),
    }
    TYPE_TEXT = {
        'Activo':    colors.HexColor('#B8860B'),
        'Pasivo':    colors.HexColor('#CC0000'),
        'Patrimonio':colors.HexColor('#15803D'),
        'Ingreso':   colors.HexColor('#1D4ED8'),
        'Gasto':     colors.HexColor('#555555'),
    }

    data = [['Código', 'Nombre de la Cuenta', 'Tipo', 'Descripción / Uso']]
    row_styles = []
    row_num = 1

    for cod, nombre, tipo, desc in cuentas:
        if tipo == 'header':
            data.append([cod, nombre, '', ''])
            row_styles.append(('header', row_num))
        elif tipo == 'subheader':
            data.append([cod, nombre, '', ''])
            row_styles.append(('subheader', row_num))
        else:
            data.append([cod, nombre, tipo, desc])
            row_styles.append(('data', row_num, tipo))
        row_num += 1

    col_w = [2.2*cm, 5.5*cm, 2.5*cm, 7*cm]
    tbl = Table(data, colWidths=col_w, repeatRows=1)

    base_style = [
        ('FONTNAME',  (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',  (0,0), (-1,0), 9),
        ('BACKGROUND',(0,0), (-1,0), GOLD),
        ('TEXTCOLOR', (0,0), (-1,0), BLACK),
        ('ALIGN',     (0,0), (-1,-1), 'LEFT'),
        ('VALIGN',    (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',      (0,0), (-1,-1), 0.3, colors.HexColor('#dddddd')),
        ('BOX',       (0,0), (-1,-1), 1, GOLD),
        ('TOPPADDING',(0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
        ('FONTSIZE',  (0,1), (-1,-1), 8),
    ]

    for rs in row_styles:
        r = rs[1]
        if rs[0] == 'header':
            base_style += [
                ('BACKGROUND', (0,r), (-1,r), BLACK),
                ('TEXTCOLOR',  (0,r), (-1,r), GOLD),
                ('FONTNAME',   (0,r), (-1,r), 'Helvetica-Bold'),
                ('FONTSIZE',   (0,r), (-1,r), 10),
                ('SPAN',       (0,r), (-1,r)),
            ]
        elif rs[0] == 'subheader':
            base_style += [
                ('BACKGROUND', (0,r), (-1,r), colors.HexColor('#333333')),
                ('TEXTCOLOR',  (0,r), (-1,r), WHITE),
                ('FONTNAME',   (0,r), (-1,r), 'Helvetica-Bold'),
                ('LEFTPADDING',(0,r), (-1,r), 16),
                ('SPAN',       (0,r), (-1,r)),
            ]
        else:
            tipo = rs[2]
            if tipo in TYPE_COLORS:
                base_style += [('BACKGROUND', (0,r), (-1,r), TYPE_COLORS[tipo])]
                base_style += [('TEXTCOLOR',  (2,r), (2,r), TYPE_TEXT[tipo])]
                base_style += [('FONTNAME',   (2,r), (2,r), 'Helvetica-Bold')]

    tbl.setStyle(TableStyle(base_style))
    story.append(tbl)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('⚡ Este plan de cuentas es una base orientativa. Adáptalo al rubro y tamaño de tu empresa. Tu contador puede ayudarte a estructurarlo correctamente para tu declaración de impuestos.', note_s))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print('✓ plan-cuentas-basico.pdf')

# ─────────────────────────────────────────────────────────────────────────────
# 4. EJERCICIO PRÁCTICO RESUELTO
# ─────────────────────────────────────────────────────────────────────────────
def make_ejercicio():
    doc = base_doc('ejercicio-contable-resuelto.pdf', 'Ejercicio Contable Resuelto — Mister Contador')
    title_s, sub_s, h2_s, body_s, note_s = styles()
    story = []

    story.append(Paragraph('EJERCICIO CONTABLE RESUELTO', title_s))
    story.append(Paragraph('Caso práctico: Tienda de ropa "La Moda" — Primer mes de operación.', sub_s))
    story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceAfter=8))

    story.append(Paragraph('CONTEXTO', h2_s))
    story.append(Paragraph(
        'La Moda es una tienda de ropa recién constituida como SpA. La dueña, Claudia, '
        'aporta $5.000.000 como capital inicial. Durante el primer mes registra las '
        'siguientes operaciones:', body_s))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('OPERACIONES DEL MES', h2_s))

    ops = [
        ['N°', 'Fecha', 'Descripción'],
        ['1', '01/03', 'Claudia aporta $5.000.000 como capital inicial. Deposita en la cuenta bancaria de la empresa.'],
        ['2', '03/03', 'Compra mercadería (ropa) por $2.000.000 + IVA al contado. Pago con transferencia.'],
        ['3', '10/03', 'Vende ropa por $1.500.000 + IVA. El cliente paga en efectivo.'],
        ['4', '15/03', 'Paga arriendo del local: $300.000 (exento de IVA). Con cheque.'],
        ['5', '20/03', 'Vende ropa por $800.000 + IVA a crédito (cliente le debe el dinero).'],
        ['6', '25/03', 'Paga sueldos del mes: $600.000 bruto. AFP y salud descuentos del trabajador: $120.000.'],
        ['7', '28/03', 'El cliente de la operación 5 paga lo que debía. Transferencia recibida.'],
        ['8', '31/03', 'Declara F29: IVA DF $437.000 − IVA CF $380.000 = Pago neto SII $57.000.'],
    ]
    col_w = [1*cm, 1.8*cm, 14.2*cm]
    tbl = Table(ops, colWidths=col_w)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), GOLD),
        ('TEXTCOLOR',    (0,0), (-1,0), BLACK),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0), 9),
        ('FONTSIZE',     (0,1), (-1,-1), 8),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE, LGRAY]),
        ('GRID',         (0,0), (-1,-1), 0.3, colors.HexColor('#cccccc')),
        ('BOX',          (0,0), (-1,-1), 1, GOLD),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('ALIGN',        (0,0), (1,-1), 'CENTER'),
    ]))
    story.append(tbl)

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('SOLUCIÓN — LIBRO DIARIO', h2_s))
    story.append(Paragraph('(IVA = 19% | IVA CF compra: $380.000 | IVA DF venta 1: $285.000 | IVA DF venta 2: $152.000)', note_s))
    story.append(Spacer(1, 0.2*cm))

    asientos = [
        ['N°', 'Cuenta', 'Tipo', 'Debe ($)', 'Haber ($)', 'Glosa'],
        ['1', 'Banco', 'Activo ↑', '5.000.000', '', 'Aporte de capital inicial'],
        ['',  'Capital', 'Patrimonio ↑', '', '5.000.000', ''],
        ['2', 'Inventario', 'Activo ↑', '2.000.000', '', 'Compra mercadería contado'],
        ['',  'IVA Crédito Fiscal', 'Activo ↑', '380.000', '', ''],
        ['',  'Banco', 'Activo ↓', '', '2.380.000', ''],
        ['3', 'Caja', 'Activo ↑', '1.785.000', '', 'Venta efectivo + IVA'],
        ['',  'Ventas', 'Ingreso ↑', '', '1.500.000', ''],
        ['',  'IVA Débito Fiscal', 'Pasivo ↑', '', '285.000', ''],
        ['4', 'Gasto Arriendo', 'Gasto ↑', '300.000', '', 'Arriendo local marzo'],
        ['',  'Banco', 'Activo ↓', '', '300.000', ''],
        ['5', 'Clientes', 'Activo ↑', '952.000', '', 'Venta a crédito + IVA'],
        ['',  'Ventas', 'Ingreso ↑', '', '800.000', ''],
        ['',  'IVA Débito Fiscal', 'Pasivo ↑', '', '152.000', ''],
        ['6', 'Gasto Sueldos', 'Gasto ↑', '600.000', '', 'Sueldos brutos marzo'],
        ['',  'AFP por pagar', 'Pasivo ↑', '', '80.000', ''],
        ['',  'Salud por pagar', 'Pasivo ↑', '', '40.000', ''],
        ['',  'Banco', 'Activo ↓', '', '480.000', ''],
        ['7', 'Banco', 'Activo ↑', '952.000', '', 'Cobro cliente op. 5'],
        ['',  'Clientes', 'Activo ↓', '', '952.000', ''],
        ['8', 'IVA Débito Fiscal', 'Pasivo ↓', '437.000', '', 'Declaración F29 — pago neto'],
        ['',  'IVA Crédito Fiscal', 'Activo ↓', '', '380.000', ''],
        ['',  'Banco', 'Activo ↓', '', '57.000', ''],
    ]
    col_w2 = [0.7*cm, 3.8*cm, 2.5*cm, 2.5*cm, 2.5*cm, 5*cm]
    tbl2 = Table(asientos, colWidths=col_w2, repeatRows=1)
    tbl2.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), GOLD),
        ('TEXTCOLOR',    (0,0), (-1,0), BLACK),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0), 8),
        ('FONTSIZE',     (0,1), (-1,-1), 7.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE, LGRAY]),
        ('GRID',         (0,0), (-1,-1), 0.3, colors.HexColor('#cccccc')),
        ('BOX',          (0,0), (-1,-1), 1, GOLD),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN',        (3,0), (4,-1), 'RIGHT'),
        ('ALIGN',        (0,0), (0,-1), 'CENTER'),
        ('TOPPADDING',   (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0), (-1,-1), 3),
    ]))
    story.append(tbl2)

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('RESULTADO DEL MES', h2_s))
    resumen = [
        ['Concepto', 'Monto ($)'],
        ['Total Ingresos (Ventas)', '2.300.000'],
        ['Total Gastos', '900.000'],
        ['Utilidad del período', '1.400.000'],
        ['IVA neto pagado al SII', '57.000'],
        ['Saldo en Banco al cierre', '3.720.000'],
    ]
    col_w3 = [10*cm, 3*cm]
    tbl3 = Table(resumen, colWidths=col_w3)
    tbl3.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), GOLD),
        ('TEXTCOLOR',    (0,0), (-1,0), BLACK),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 9),
        ('BACKGROUND',   (0,-1), (-1,-1), colors.HexColor('#F0FFF4')),
        ('FONTNAME',     (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR',    (1,-1), (1,-1), colors.HexColor('#15803D')),
        ('ROWBACKGROUNDS',(0,1),(-1,-2), [WHITE, LGRAY]),
        ('GRID',         (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('BOX',          (0,0), (-1,-1), 1, GOLD),
        ('ALIGN',        (1,0), (1,-1), 'RIGHT'),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
    ]))
    story.append(tbl3)
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('⚡ Consejo de Mister Contador: practica haciendo el Libro Mayor de cada cuenta de este ejercicio. Toma cada cuenta (Banco, Ventas, etc.) y suma sus movimientos para verificar los saldos finales.', note_s))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print('✓ ejercicio-contable-resuelto.pdf')

if __name__ == '__main__':
    make_libro_diario()
    make_libro_mayor()
    make_plan_cuentas()
    make_ejercicio()
    print('\n¡Todos los PDFs generados!')
