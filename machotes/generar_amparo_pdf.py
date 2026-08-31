"""
Generador del PDF: machote de demanda de amparo indirecto (tramitacion sumaria/urgente)
para persona extrana a juicio que acredita interes juridico con contrato privado
traslativo de dominio con firmas ratificadas ante notario (documento de fecha cierta),
y que reclama la restitucion del inmueble y/o la devolucion del dinero pagado.

Base: Contradiccion de tesis 173/2006-PS, Primera Sala de la SCJN.

Uso:
    pip install reportlab
    python generar_amparo_pdf.py
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    PageBreak, KeepTogether, HRFlowable, Table, TableStyle,
)

OUT = "AMPARO-INDIRECTO-VIA-SUMARIA-DEVOLUCION-DINERO.pdf"

SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SERIF_I = "Times-Italic"

S = {
    "portada_kicker": ParagraphStyle(
        "pk", fontName=SERIF_B, fontSize=10, leading=14, alignment=TA_CENTER,
        textColor=colors.HexColor("#7a5c1e"), spaceAfter=10,
    ),
    "portada_title": ParagraphStyle(
        "pt", fontName=SERIF_B, fontSize=20, leading=25, alignment=TA_CENTER,
        spaceAfter=8,
    ),
    "portada_sub": ParagraphStyle(
        "ps", fontName=SERIF_I, fontSize=11.5, leading=16, alignment=TA_CENTER,
        textColor=colors.HexColor("#333333"), spaceAfter=14,
    ),
    "h1": ParagraphStyle(
        "h1", fontName=SERIF_B, fontSize=13, leading=17, alignment=TA_JUSTIFY,
        spaceBefore=16, spaceAfter=8, textColor=colors.HexColor("#1a1a1a"),
    ),
    "h2": ParagraphStyle(
        "h2", fontName=SERIF_B, fontSize=11, leading=15, alignment=TA_JUSTIFY,
        spaceBefore=11, spaceAfter=5,
    ),
    "body": ParagraphStyle(
        "body", fontName=SERIF, fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY,
        spaceAfter=7, firstLineIndent=0,
    ),
    "body_i": ParagraphStyle(
        "bodyi", fontName=SERIF, fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY,
        spaceAfter=7, leftIndent=16,
    ),
    "quote": ParagraphStyle(
        "quote", fontName=SERIF_I, fontSize=9.8, leading=14, alignment=TA_JUSTIFY,
        leftIndent=22, rightIndent=10, spaceBefore=4, spaceAfter=9,
        textColor=colors.HexColor("#2b2b2b"),
    ),
    "center_b": ParagraphStyle(
        "cb", fontName=SERIF_B, fontSize=11, leading=15, alignment=TA_CENTER,
        spaceBefore=8, spaceAfter=8,
    ),
    "right": ParagraphStyle(
        "r", fontName=SERIF, fontSize=10.5, leading=15, alignment=TA_RIGHT,
        spaceAfter=6,
    ),
    "note": ParagraphStyle(
        "note", fontName=SERIF, fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY,
        leftIndent=10, rightIndent=10, spaceAfter=6,
        textColor=colors.HexColor("#5a3c00"),
    ),
    "small": ParagraphStyle(
        "small", fontName=SERIF, fontSize=9, leading=12.5, alignment=TA_JUSTIFY,
        spaceAfter=5, textColor=colors.HexColor("#444444"),
    ),
    "firma": ParagraphStyle(
        "firma", fontName=SERIF_B, fontSize=10.5, leading=15, alignment=TA_CENTER,
        spaceAfter=3,
    ),
}


def rule(color="#b9a26a", width=0.9, sb=2, sa=8):
    return HRFlowable(width="100%", thickness=width, color=colors.HexColor(color),
                      spaceBefore=sb, spaceAfter=sa)


def callout(title, text):
    """Caja de nota tecnica / advertencia."""
    inner = [
        Paragraph("<b>%s</b>" % title, S["note"]),
        Paragraph(text, S["note"]),
    ]
    t = Table([[inner]], colWidths=[16.4 * cm])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#c8ab63")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbf6e7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 8)])


def checklist(rows, col1="Documento / anexo", col2="Objeto probatorio"):
    data = [[Paragraph("<b>%s</b>" % col1, S["small"]),
             Paragraph("<b>%s</b>" % col2, S["small"])]]
    for a, b in rows:
        data.append([Paragraph(a, S["small"]), Paragraph(b, S["small"])])
    t = Table(data, colWidths=[7.2 * cm, 9.2 * cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#efe9d8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(SERIF, 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(2.3 * cm, 1.35 * cm,
                      "Machote de amparo indirecto - CT 173/2006-PS (fecha cierta) - "
                      "formato editable de uso profesional")
    canvas.drawRightString(letter[0] - 2.3 * cm, 1.35 * cm, "Pag. %d" % doc.page)
    canvas.setStrokeColor(colors.HexColor("#cccccc"))
    canvas.setLineWidth(0.4)
    canvas.line(2.3 * cm, 1.75 * cm, letter[0] - 2.3 * cm, 1.75 * cm)
    canvas.restoreState()


def build(story):
    doc = BaseDocTemplate(
        OUT, pagesize=letter,
        leftMargin=2.3 * cm, rightMargin=2.3 * cm,
        topMargin=2.2 * cm, bottomMargin=2.3 * cm,
        title="Machote - Demanda de amparo indirecto (via sumaria): fecha cierta "
              "y devolucion del dinero pagado",
        author="Machote profesional",
        subject="Amparo indirecto - persona extrana a juicio - CT 173/2006-PS",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])
    doc.build(story)



# ---------------------------------------------------------------------------
# CONTENIDO
# ---------------------------------------------------------------------------

story = []
P = lambda t, k="body": story.append(Paragraph(t, S[k]))
SP = lambda h=6: story.append(Spacer(1, h))

# ============================== PORTADA ====================================
SP(28)
P("MACHOTE PROFESIONAL &nbsp;|&nbsp; FORMATO EDITABLE", "portada_kicker")
story.append(rule())
SP(6)
P("DEMANDA DE AMPARO INDIRECTO", "portada_title")
P("(promovida por persona extra&ntilde;a a juicio, con solicitud de suspensi&oacute;n y "
  "de tramitaci&oacute;n sumaria y urgente)", "portada_sub")
story.append(rule())
SP(10)
P("MATERIA: restituci&oacute;n del inmueble y <b>devoluci&oacute;n de las cantidades "
  "de dinero pagadas</b>, acreditando el inter&eacute;s jur&iacute;dico con un contrato "
  "privado traslativo de dominio cuyas firmas fueron ratificadas ante notario "
  "p&uacute;blico (documento de fecha cierta).", "center_b")
SP(14)

P("<b>Base jurisprudencial rectora</b>", "h2")
P("Contradicci&oacute;n de tesis <b>173/2006-PS</b>, resuelta por la Primera Sala de la "
  "Suprema Corte de Justicia de la Naci&oacute;n entre los criterios de los Tribunales "
  "Colegiados Primero, Segundo y Tercero, todos en Materia Civil del Sexto Circuito "
  "(Novena &Eacute;poca, <i>Semanario Judicial de la Federaci&oacute;n y su Gaceta</i>, "
  "Tomo XXVI, septiembre de 2007, p&aacute;gina 191; registro digital de la ejecutoria: "
  "20357), de la que deriv&oacute; la jurisprudencia de rubro: <b>&ldquo;INTER&Eacute;S "
  "JUR&Iacute;DICO EN EL AMPARO. PUEDE ACREDITARSE CON EL CONTRATO PRIVADO TRASLATIVO DE "
  "DOMINIO CUYAS FIRMAS SE RATIFICAN ANTE NOTARIO, PORQUE ES UN DOCUMENTO DE FECHA CIERTA "
  "(LEGISLACI&Oacute;N DEL ESTADO DE PUEBLA)&rdquo;</b>.")
P("<b>Criterios complementarios:</b> 1a./J. 46/99 (ineficacia del contrato privado de "
  "fecha incierta); 1a./J. 44/2005 (basta la presentaci&oacute;n ante notario y la "
  "certificaci&oacute;n de firmas para la fecha cierta); 1a./J. 33/2003 (fecha cierta por "
  "muerte de uno de los firmantes); y la ejecutoria de la contradicci&oacute;n de tesis "
  "14/2004-PS (no se requiere protocolizaci&oacute;n).")
SP(10)
P("<b>Foro previsto:</b> Juzgados de Distrito en Materia Civil en la Ciudad de "
  "M&eacute;xico. &nbsp;<b>Versi&oacute;n:</b> 1.0 &mdash; 10 de agosto de 2026.", "small")
SP(14)

story.append(callout(
    "AVISO INDISPENSABLE",
    "Este documento es un <b>formato base (machote)</b> de tr&aacute;mite forense. "
    "No constituye asesor&iacute;a jur&iacute;dica para un caso concreto ni sustituye la "
    "intervenci&oacute;n de un abogado con c&eacute;dula profesional, quien debe adaptarlo "
    "a los hechos reales, verificar el <b>texto vigente</b> de todos los preceptos citados y "
    "confirmar la <b>vigencia y aplicabilidad</b> de cada tesis en el Sistema de Consulta de "
    "la SCJN (sjf2.scjn.gob.mx) antes de presentarlo. Los campos entre corchetes "
    "<b>[ ]</b> son obligatoriamente sustituibles. La jurisprudencia rectora se emiti&oacute; "
    "respecto de la legislaci&oacute;n del Estado de Puebla: en la Ciudad de M&eacute;xico se "
    "invoca por identidad de raz&oacute;n y se refuerza con la normativa local que se cita en "
    "el Anexo A."))

story.append(PageBreak())

# ======================= NOTA TECNICA: LA "VIA SUMARIA" =====================
P("NOTA T&Eacute;CNICA PRELIMINAR: QU&Eacute; SIGNIFICA AQU&Iacute; &ldquo;V&Iacute;A "
  "SUMARIA&rdquo;", "h1")
story.append(rule())
P("La Ley de Amparo <b>no contempla una &ldquo;v&iacute;a sumaria&rdquo;</b> como carril "
  "procesal aut&oacute;nomo: sus dos v&iacute;as son el amparo <b>indirecto</b> (ante Juez de "
  "Distrito) y el <b>directo</b> (ante Tribunal Colegiado). Por ello, en este machote la "
  "expresi&oacute;n &ldquo;v&iacute;a sumaria&rdquo; se traduce en el <b>tr&aacute;mite "
  "abreviado, urgente y preferente del amparo indirecto</b>, que se construye con cuatro "
  "herramientas que van expresamente solicitadas en el cuerpo del escrito:")
P("<b>1. Suspensi&oacute;n provisional de plano o de inmediato</b> (art&iacute;culos 125 a "
  "129, 138, 139, 147 y 148 de la Ley de Amparo), para detener el remate, la "
  "adjudicaci&oacute;n, la escrituraci&oacute;n, la entrega material del inmueble y la "
  "entrega de fondos al ejecutante <i>antes</i> de que el da&ntilde;o se consume.", "body_i")
P("<b>2. Habilitaci&oacute;n de d&iacute;as y horas inh&aacute;biles</b> (art&iacute;culo 20 "
  "de la Ley de Amparo), cuando la diligencia est&eacute; se&ntilde;alada en fecha "
  "inminente.", "body_i")
P("<b>3. Petici&oacute;n de tr&aacute;mite preferente</b> y de que la audiencia "
  "constitucional se celebre en el plazo m&aacute;s breve legalmente posible, sin "
  "diferimientos innecesarios.", "body_i")
P("<b>4. Ofrecimiento anticipado y completo de la prueba documental</b>, para que el "
  "asunto quede en estado de resoluci&oacute;n en la primera audiencia.", "body_i")
story.append(callout(
    "SI LO QUE SE BUSCA ES &Uacute;NICAMENTE COBRAR DINERO A UN PARTICULAR",
    "El amparo <b>no</b> es la v&iacute;a para condenar a un particular (por ejemplo, al "
    "vendedor) a devolver el precio. El amparo s&oacute;lo puede: (i) restituir al quejoso en "
    "el goce del derecho violado por la <b>autoridad</b>; (ii) ordenar a la autoridad la "
    "devoluci&oacute;n de cantidades que ella retiene o que se enteraron por virtud del acto "
    "reclamado; y (iii) abrir la puerta al <b>cumplimiento sustituto</b> (art&iacute;culos 204 "
    "y 205 de la Ley de Amparo) cuando la restituci&oacute;n material sea imposible. Para "
    "recuperar el precio frente al vendedor la v&iacute;a es la <b>civil ordinaria</b> "
    "(rescisi&oacute;n, nulidad, evicci&oacute;n y saneamiento &mdash;art&iacute;culos 2119 a "
    "2141 del C&oacute;digo Civil para el Distrito Federal&mdash;, o da&ntilde;os y "
    "perjuicios), o la <b>terceria excluyente de dominio</b> dentro del juicio de origen. "
    "El Anexo D contiene la variante para ese escenario."))

P("GU&Iacute;A R&Aacute;PIDA DE LLENADO", "h1")
story.append(rule())
P("Sustituya cada campo entre corchetes y elimine los que no apliquen. El machote "
  "est&aacute; escrito para el siguiente <b>supuesto tipo</b>, que es el que resolvi&oacute; "
  "la contradicci&oacute;n de tesis 173/2006-PS:", "small")
story.append(checklist([
    ("[NOMBRE DEL QUEJOSO]", "Persona que compr&oacute; el inmueble por contrato privado."),
    ("[NOMBRE DEL VENDEDOR / DEUDOR]", "Quien apareci&oacute; como demandado en el juicio de "
                                       "origen y como titular registral."),
    ("[NOMBRE DEL EJECUTANTE]", "Actor del juicio de origen (acreedor); ser&aacute; tercero "
                                "interesado."),
    ("[JUZGADO RESPONSABLE]", "&Oacute;rgano jurisdiccional que orden&oacute; el embargo, el "
                              "remate o la entrega."),
    ("[EXPEDIENTE __/20__]", "N&uacute;mero del juicio de origen."),
    ("[FECHA DEL CONTRATO]", "Fecha de celebraci&oacute;n del contrato privado."),
    ("[FECHA DE RATIFICACI&Oacute;N]", "Fecha de la certificaci&oacute;n notarial: es la que "
                                       "otorga la <b>fecha cierta</b>."),
    ("[MONTO PAGADO]", "Precio y dem&aacute;s cantidades cuya devoluci&oacute;n se reclama."),
    ("[FECHA DEL EMBARGO / REMATE]", "Debe ser <b>posterior</b> a la ratificaci&oacute;n "
                                     "notarial; ah&iacute; est&aacute; la clave del caso."),
], col1="Campo", col2="Contenido"))
SP(8)
story.append(callout(
    "REGLA DE ORO DEL CASO",
    "El &eacute;xito depende de una sola comparaci&oacute;n de fechas: la "
    "<b>ratificaci&oacute;n notarial de firmas debe ser anterior</b> al embargo, gravamen o "
    "acto de privaci&oacute;n. Si es posterior, el amparo est&aacute; perdido (as&iacute; se "
    "resolvi&oacute; en el amparo en revisi&oacute;n 128/2006). Verifique tambi&eacute;n que "
    "la certificaci&oacute;n notarial no adolezca de los vicios que se&ntilde;ala el Anexo C."))

story.append(PageBreak())


# ==================== CUERPO DE LA DEMANDA: PROEMIO ========================
P("CUERPO DE LA DEMANDA", "portada_kicker")
story.append(rule())
SP(6)

P("<b>QUEJOSO:</b> [NOMBRE COMPLETO DEL QUEJOSO]<br/>"
  "<b>ACTOS RECLAMADOS:</b> embargo, remate, adjudicaci&oacute;n, entrega del inmueble y "
  "aplicaci&oacute;n de cantidades<br/>"
  "<b>ASUNTO:</b> Se promueve juicio de amparo indirecto como persona extra&ntilde;a a "
  "juicio; se solicita la suspensi&oacute;n provisional y definitiva y tr&aacute;mite "
  "urgente<br/>"
  "<b>ESCRITO INICIAL DE DEMANDA</b>", "right")
SP(12)

P("C. JUEZ DE DISTRITO EN MATERIA CIVIL EN LA CIUDAD DE M&Eacute;XICO<br/>"
  "EN TURNO. &nbsp;P R E S E N T E.", "center_b")
SP(8)

P("[NOMBRE COMPLETO DEL QUEJOSO], por mi propio derecho, se&ntilde;alando como domicilio "
  "para o&iacute;r y recibir toda clase de notificaciones y documentos el ubicado en "
  "[CALLE, N&Uacute;MERO, COLONIA, ALCALD&Iacute;A, C.P., CIUDAD DE M&Eacute;XICO], "
  "autorizando para los mismos efectos, as&iacute; como para imponerse de autos, ofrecer y "
  "rendir pruebas, alegar, interponer recursos y con las m&aacute;s amplias facultades que "
  "concede el art&iacute;culo 12 de la Ley de Amparo, a los licenciados en derecho "
  "[NOMBRE DEL ABOGADO 1, c&eacute;dula profesional n&uacute;mero ____] y [NOMBRE DEL "
  "ABOGADO 2, c&eacute;dula profesional n&uacute;mero ____]; y autorizando en "
  "t&eacute;rminos del p&aacute;rrafo segundo del propio precepto a [NOMBRE] solamente "
  "para o&iacute;r notificaciones e imponerse de autos; asimismo, manifestando mi "
  "conformidad para recibir notificaciones por v&iacute;a electr&oacute;nica a trav&eacute;s "
  "de la Firma Electr&oacute;nica del Poder Judicial de la Federaci&oacute;n, con la "
  "cuenta [CORREO / FIREL / e.firma]; ante Usted comparezco y respetuosamente expongo:")
P("Que por medio del presente escrito, con fundamento en los art&iacute;culos 1&ordm;, "
  "14, 16, 17 y 107, fracciones I, VII y XVI, de la Constituci&oacute;n Pol&iacute;tica de "
  "los Estados Unidos Mexicanos; 1&ordm;, fracci&oacute;n I, 2&ordm;, 5&ordm;, "
  "fracci&oacute;n I, 6&ordm;, 17, 18, 33, fracci&oacute;n IV, 35, 37, 107, fracciones IV "
  "y VI, 108, 119, 125 a 129, 138, 139, 147 y 148 de la Ley de Amparo, vengo a "
  "<b>demandar el amparo y protecci&oacute;n de la Justicia Federal</b>, en mi calidad de "
  "<b>persona extra&ntilde;a al juicio</b> de origen, en contra de los actos de autoridad "
  "que m&aacute;s adelante precisar&eacute;, para lo cual, en cumplimiento del "
  "art&iacute;culo 108 de la Ley de Amparo, manifiesto:")

# ------------------------- I y II: PARTES -----------------------------------
P("I. NOMBRE Y DOMICILIO DEL QUEJOSO", "h1")
P("[NOMBRE COMPLETO DEL QUEJOSO], con domicilio para o&iacute;r y recibir notificaciones el "
  "se&ntilde;alado en el proemio de este escrito. Comparezco por mi propio derecho y no por "
  "conducto de representante alguno.")

P("II. NOMBRE Y DOMICILIO DE LOS TERCEROS INTERESADOS", "h1")
P("Con fundamento en el art&iacute;culo 5&ordm;, fracci&oacute;n III, incisos a) y b), de "
  "la Ley de Amparo, tienen ese car&aacute;cter:", "small")
P("<b>a)</b> [NOMBRE DEL EJECUTANTE / ACTOR EN EL JUICIO DE ORIGEN], con domicilio en "
  "[DOMICILIO SE&Ntilde;ALADO EN EL EXPEDIENTE __/20__ DEL JUZGADO RESPONSABLE].", "body_i")
P("<b>b)</b> [NOMBRE DEL VENDEDOR / DEMANDADO EN EL JUICIO DE ORIGEN], con domicilio en "
  "[DOMICILIO].", "body_i")
P("<b>c)</b> [NOMBRE DEL POSTOR O ADJUDICATARIO, si ya hubo remate], con domicilio en "
  "[DOMICILIO].", "body_i")
P("<b>d)</b> [Instituci&oacute;n de cr&eacute;dito, acreedor hipotecario o cesionario de "
  "derechos, si existe], con domicilio en [DOMICILIO].", "body_i")
P("Bajo protesta de decir verdad manifiesto que los domicilios anteriores son los que "
  "obran en el expediente de origen y que desconozco cualquier otro; para el caso de "
  "ignorancia o inexactitud, solicito que se requiera a la autoridad responsable su "
  "informe, en t&eacute;rminos del art&iacute;culo 27 de la Ley de Amparo.", "small")

# ------------------------- III: AUTORIDADES ---------------------------------
P("III. AUTORIDADES RESPONSABLES", "h1")
P("<b>1. Ordenadora:</b> C. Juez [__] de lo [Civil / Mercantil / Familiar] del Tribunal "
  "Superior de Justicia de la Ciudad de M&eacute;xico, en los autos del juicio "
  "[ejecutivo mercantil / especial hipotecario / ordinario civil / de alimentos] "
  "n&uacute;mero de expediente [__/20__], promovido por [EJECUTANTE] en contra de "
  "[VENDEDOR].", "body_i")
P("<b>2. Ejecutora:</b> C. Actuario y/o Secretario Actuario adscrito al juzgado "
  "se&ntilde;alado, o cualquier servidor p&uacute;blico que materialmente ejecute los actos "
  "reclamados.", "body_i")
P("<b>3.</b> C. Director del Registro P&uacute;blico de la Propiedad y de Comercio de la "
  "Ciudad de M&eacute;xico, por cuanto hace a la inscripci&oacute;n del embargo, del "
  "gravamen y/o de la adjudicaci&oacute;n derivada del remate.", "body_i")
P("<b>4.</b> [En su caso] C. Tesorer&iacute;a de la Ciudad de M&eacute;xico y/o Consejer&iacute;a "
  "Jur&iacute;dica, por cuanto hace a las cantidades enteradas o retenidas con motivo de los "
  "actos reclamados.", "body_i")

# ------------------------- IV: ACTOS RECLAMADOS -----------------------------
P("IV. NORMA GENERAL, ACTO U OMISI&Oacute;N QUE SE RECLAMA", "h1")
P("Se reclama de las autoridades se&ntilde;aladas, en el &aacute;mbito de sus respectivas "
  "competencias:")
P("<b>a)</b> <b>El auto de exequendo y la diligencia de embargo</b> de fecha [FECHA], "
  "trabada sobre el inmueble ubicado en [DESCRIPCI&Oacute;N E IDENTIFICACI&Oacute;N "
  "REGISTRAL DEL INMUEBLE: calle, n&uacute;mero, colonia, alcald&iacute;a, folio real "
  "n&uacute;mero ____], as&iacute; como su inscripci&oacute;n registral.", "body_i")
P("<b>b)</b> <b>El proveido que orden&oacute; sacar a remate</b> dicho inmueble, la "
  "convocatoria y los edictos correspondientes, la audiencia de remate de [FECHA] y la "
  "<b>resoluci&oacute;n que aprueba el remate y ordena la adjudicaci&oacute;n</b>, el "
  "otorgamiento de la escritura y la <b>entrega material</b> del bien.", "body_i")
P("<b>c)</b> <b>La orden de aplicaci&oacute;n y entrega al ejecutante del producto del "
  "remate</b>, as&iacute; como de cualquier cantidad depositada, retenida o enterada con "
  "motivo de la ejecuci&oacute;n, incluidas las que el suscrito hubo de pagar en "
  "t&eacute;rminos del hecho [__] de esta demanda.", "body_i")
P("<b>d)</b> <b>La omisi&oacute;n de llamarme a juicio</b> y de otorgarme la garant&iacute;a "
  "de audiencia, no obstante que desde el [FECHA DE RATIFICACI&Oacute;N NOTARIAL] soy el "
  "propietario del inmueble embargado, y todas las consecuencias de hecho y de derecho "
  "de los actos anteriores.", "body_i")
story.append(callout(
    "AJUSTE OBLIGATORIO",
    "Se&ntilde;ale como acto reclamado destacado <b>el &uacute;ltimo eslab&oacute;n de la "
    "cadena de ejecuci&oacute;n que a&uacute;n no se ha consumado</b> (por ejemplo, la "
    "resoluci&oacute;n que aprueba el remate y ordena la entrega). Si la adjudicaci&oacute;n "
    "ya se inscribi&oacute; a favor de un tercero registral de buena fe, conserve la "
    "reclamaci&oacute;n y refuerce el <b>Cuarto concepto de violaci&oacute;n</b> y el "
    "cap&iacute;tulo de efectos, pues ah&iacute; radicar&aacute; la pretensi&oacute;n de "
    "devoluci&oacute;n del dinero por v&iacute;a de cumplimiento sustituto."))

# ------------------------- V: HECHOS ---------------------------------------
P("V. HECHOS Y ANTECEDENTES (bajo protesta de decir verdad)", "h1")
P("Bajo protesta de decir verdad, manifiesto que los hechos y abstenciones que constituyen "
  "los antecedentes de los actos reclamados y fundan los conceptos de violaci&oacute;n son "
  "los siguientes:", "small")
P("<b>1. Adquisici&oacute;n del inmueble.</b> El [FECHA DEL CONTRATO], el suscrito "
  "celebr&oacute; con [NOMBRE DEL VENDEDOR] un <b>contrato privado de compraventa</b> "
  "respecto del inmueble ubicado en [UBICACI&Oacute;N], identificado con el folio real "
  "[____] del Registro P&uacute;blico de la Propiedad y de Comercio de la Ciudad de "
  "M&eacute;xico, por un precio total de <b>$[MONTO] ([CANTIDAD] pesos moneda "
  "nacional)</b>.", "body_i")
P("<b>2. Pago del precio.</b> El precio fue pagado &iacute;ntegramente por el suscrito en "
  "[una sola exhibici&oacute;n / [__] parcialidades], mediante [transferencias "
  "electr&oacute;nicas SPEI de fechas ____, cheques n&uacute;mero ____ librados a cargo de "
  "____, efectivo con recibo de fecha ____], como se acredita con los comprobantes que se "
  "anexan y con el recibo finiquito de [FECHA]. Adicionalmente erogu&eacute; "
  "<b>$[MONTO]</b> por concepto de [impuesto sobre adquisici&oacute;n de inmuebles, "
  "derechos registrales, honorarios, aval&uacute;o, mejoras &uacute;tiles y necesarias], "
  "seg&uacute;n los comprobantes que igualmente se acompa&ntilde;an.", "body_i")
P("<b>3. Ratificaci&oacute;n de firmas ante notario: la fecha cierta.</b> El "
  "<b>[FECHA DE RATIFICACI&Oacute;N]</b> ambos contratantes comparecimos personalmente ante "
  "el licenciado [NOMBRE], titular de la Notar&iacute;a P&uacute;blica n&uacute;mero [__] "
  "de la Ciudad de M&eacute;xico, quien <b>certific&oacute; la ratificaci&oacute;n del "
  "contenido del contrato y la autenticidad de nuestras firmas</b>, hizo constar nuestra "
  "comparecencia, identidad y capacidad, y autoriz&oacute; la certificaci&oacute;n con su "
  "firma y sello. <b>Es esta fecha la que otorga fecha cierta al documento</b>.", "body_i")
P("<b>4. Posesi&oacute;n y publicidad de hecho.</b> Desde el [FECHA] he tenido la "
  "posesi&oacute;n material, p&uacute;blica, pac&iacute;fica, continua y a t&iacute;tulo de "
  "propietario del inmueble, pagando el impuesto predial y los derechos por suministro de "
  "agua a mi nombre, como se acredita con las boletas que se anexan.", "body_i")
P("<b>5. El juicio de origen, ajeno al suscrito.</b> Con posterioridad a la fecha cierta "
  "antes se&ntilde;alada, esto es, el [FECHA DE PRESENTACI&Oacute;N DE LA DEMANDA DE "
  "ORIGEN], [EJECUTANTE] demand&oacute; a [VENDEDOR] en la v&iacute;a [__], ante el "
  "juzgado responsable, expediente [__/20__], reclamando prestaciones de car&aacute;cter "
  "<b>personal</b> [pago de pesos derivado de t&iacute;tulo de cr&eacute;dito / "
  "cumplimiento de contrato / alimentos]. <b>Jam&aacute;s fui parte, ni fui llamado, "
  "emplazado, o&iacute;do ni vencido en ese juicio</b>, ni tuve conocimiento de su "
  "existencia mientras se tramit&oacute;.", "body_i")
P("<b>6. El embargo sobre bien ajeno.</b> El [FECHA DEL EMBARGO] &mdash;esto es, "
  "<b>[__] d&iacute;as / meses / a&ntilde;os despu&eacute;s</b> de la ratificaci&oacute;n "
  "notarial de mi contrato&mdash; se trab&oacute; embargo sobre el inmueble de mi "
  "propiedad, por la sola circunstancia de que en el Registro P&uacute;blico "
  "a&uacute;n apareciera inscrito a nombre de mi vendedor.", "body_i")
P("<b>7. Remate, adjudicaci&oacute;n y aplicaci&oacute;n de fondos.</b> [Describa: "
  "convocatoria de ____, audiencia de remate de ____, postura legal de $____, "
  "resoluci&oacute;n de ____ que aprob&oacute; el remate y adjudic&oacute; a ____, orden de "
  "escrituraci&oacute;n y de entrega, y orden de entregar al ejecutante el producto del "
  "remate por $____]. [En su caso: adem&aacute;s, para intentar evitar la "
  "desposesi&oacute;n, el suscrito hubo de exhibir la cantidad de $____ mediante billete de "
  "dep&oacute;sito n&uacute;mero ____, que la responsable retiene o aplic&oacute;].", "body_i")
P("<b>8. Conocimiento de los actos reclamados.</b> Tuve conocimiento completo y exacto de "
  "los actos reclamados el <b>[FECHA]</b>, con motivo de [la diligencia actuarial de "
  "notificaci&oacute;n practicada en el inmueble / el certificado de gravamen expedido el "
  "____ / la publicaci&oacute;n de edictos / la solicitud de inscripci&oacute;n de mi "
  "t&iacute;tulo, negada mediante nota de ____], por lo que la presente demanda se "
  "promueve dentro del plazo de <b>quince d&iacute;as</b> que establece el "
  "art&iacute;culo 17 de la Ley de Amparo, computado conforme al art&iacute;culo 18 del "
  "mismo ordenamiento.", "body_i")
P("<b>9. Inexistencia de consentimiento y de recurso id&oacute;neo.</b> No he consentido "
  "expresa ni t&aacute;citamente los actos reclamados, ni tengo a mi alcance recurso "
  "ordinario que los pueda revocar, nulificar o modificar con la misma amplitud y efectos "
  "restitutorios que el juicio de amparo, precisamente por mi condici&oacute;n de persona "
  "extra&ntilde;a al juicio de origen.", "body_i")

story.append(PageBreak())


# ------------------ VI: DERECHOS Y PRECEPTOS VIOLADOS ----------------------
P("VI. DERECHOS HUMANOS Y PRECEPTOS CONSTITUCIONALES VIOLADOS", "h1")
P("Art&iacute;culos <b>1&ordm;, 14 (segundo p&aacute;rrafo), 16 (primer p&aacute;rrafo), "
  "17 y 27</b> de la Constituci&oacute;n Pol&iacute;tica de los Estados Unidos Mexicanos, "
  "en relaci&oacute;n con los art&iacute;culos <b>8.1, 21 y 25</b> de la Convenci&oacute;n "
  "Americana sobre Derechos Humanos y <b>14 del Pacto Internacional de Derechos Civiles y "
  "Pol&iacute;ticos</b>, que consagran los derechos de <b>audiencia y debido proceso</b>, "
  "<b>legalidad y seguridad jur&iacute;dica</b>, <b>tutela judicial efectiva</b> y "
  "<b>propiedad privada</b>.")

# ------------------ COMPETENCIA, OPORTUNIDAD, PROCEDENCIA -------------------
P("VII. COMPETENCIA, OPORTUNIDAD Y PROCEDENCIA DE LA V&Iacute;A", "h1")
P("<b>A. Competencia.</b> Ese Juzgado de Distrito es competente en t&eacute;rminos de los "
  "art&iacute;culos 33, fracci&oacute;n IV, 35 y 37 de la Ley de Amparo, pues los actos "
  "reclamados deben tener ejecuci&oacute;n y se ejecutan materialmente en la Ciudad de "
  "M&eacute;xico, donde se ubica el inmueble.")
P("<b>B. Oportunidad.</b> La demanda se presenta dentro del plazo de quince d&iacute;as "
  "previsto en el art&iacute;culo 17 de la Ley de Amparo, contado a partir del "
  "d&iacute;a siguiente a aquel en que tuve conocimiento completo y exacto de los actos "
  "reclamados, seg&uacute;n el hecho 8, y en t&eacute;rminos del art&iacute;culo 18 del "
  "mismo ordenamiento.")
P("<b>C. Procedencia del amparo indirecto.</b> Los actos reclamados son actos de tribunales "
  "judiciales <b>ejecutados fuera de juicio o despu&eacute;s de concluido</b> y, en todo "
  "caso, actos <b>dentro de juicio que afectan a una persona extra&ntilde;a</b> a &eacute;l, "
  "cuya ejecuci&oacute;n es de <b>imposible reparaci&oacute;n</b>, pues privan de la "
  "propiedad y posesi&oacute;n de un inmueble; de ah&iacute; que se surtan las hip&oacute;tesis "
  "de las fracciones <b>IV y VI del art&iacute;culo 107</b> de la Ley de Amparo.")
P("<b>D. Inaplicabilidad del principio de definitividad.</b> El principio de definitividad "
  "no rige respecto de quien es <b>persona extra&ntilde;a al juicio</b> de origen, pues no "
  "estando llamado a &eacute;l carece de legitimaci&oacute;n para agotar los recursos "
  "ordinarios que la ley procesal reserva a las partes; conclusi&oacute;n que se corrobora "
  "con el hecho de que la terceria excluyente de dominio es un medio de defensa "
  "<b>optativo</b> y no un recurso que deba agotarse forzosamente antes del amparo. Se "
  "invoca el criterio reiterado del Poder Judicial de la Federaci&oacute;n en el sentido de "
  "que el tercero extra&ntilde;o puede optar entre la terceria y el juicio de garantias "
  "[insertar aqu&iacute; la tesis vigente que se localice en el Sistema de Consulta de la "
  "SCJN].")
P("<b>E. No se trata de actos consumados de modo irreparable.</b> Aun en el supuesto de que "
  "el remate se hubiere consumado, los actos reclamados <b>no son irreparables</b> en el "
  "sentido de la fracci&oacute;n XVI del art&iacute;culo 61 de la Ley de Amparo, pues sus "
  "efectos son jur&iacute;dicamente reversibles mediante la insubsistencia de las "
  "actuaciones y la cancelaci&oacute;n de las inscripciones registrales, y, en el extremo, "
  "econ&oacute;micamente reparables por la v&iacute;a del <b>cumplimiento sustituto</b> que "
  "prev&eacute;n los art&iacute;culos 204 y 205 de la Ley de Amparo. Confundir la "
  "dificultad de la restituci&oacute;n con la imposibilidad de reparaci&oacute;n "
  "equivaldr&iacute;a a premiar la celeridad de la ejecuci&oacute;n inconstitucional y a "
  "vaciar de contenido el art&iacute;culo 17 constitucional.")

# ------------------ EL NUCLEO: INTERES JURIDICO ----------------------------
P("VIII. ACREDITAMIENTO DEL INTER&Eacute;S JUR&Iacute;DICO: EL CONTRATO PRIVADO RATIFICADO "
  "ANTE NOTARIO ES DOCUMENTO DE FECHA CIERTA", "h1")
story.append(rule())
P("Este cap&iacute;tulo constituye el eje del asunto, porque la &uacute;nica causal de "
  "improcedencia que suele oponerse en casos como el presente es la prevista en la "
  "fracci&oacute;n XII del art&iacute;culo 61 de la Ley de Amparo, por supuesta falta de "
  "inter&eacute;s jur&iacute;dico. Tal objeci&oacute;n es jur&iacute;dicamente insostenible, "
  "por las razones siguientes.")

P("1. Qu&eacute; debe acreditarse", "h2")
P("Conforme al principio de instancia de parte agraviada, el inter&eacute;s "
  "jur&iacute;dico corresponde al titular del derecho afectado y debe acreditarse de manera "
  "<b>fehaciente</b>, sin inferirse de presunciones. Ostent&aacute;ndome como propietario, "
  "debo demostrar el dominio sobre la cosa <b>con un documento id&oacute;neo</b>, esto es, "
  "con un documento que por sus caracter&iacute;sticas objetivas sea <b>de fecha "
  "cierta</b>, pues s&oacute;lo as&iacute; puede el juzgador determinar si el reclamo que "
  "sobre el bien realizan terceros deriva de actos anteriores o posteriores a la "
  "adquisici&oacute;n.")

P("2. Cu&aacute;ndo un documento privado es de fecha cierta", "h2")
P("La Primera Sala de la Suprema Corte de Justicia de la Naci&oacute;n, al resolver la "
  "<b>contradicci&oacute;n de tesis 173/2006-PS</b>, sistematiz&oacute; que un documento "
  "privado adquiere fecha cierta en cualquiera de los siguientes supuestos: <b>(i)</b> desde "
  "su inscripci&oacute;n en el Registro P&uacute;blico; <b>(ii)</b> si se otorga en escritura "
  "p&uacute;blica, desde la fecha de su otorgamiento; <b>(iii)</b> desde la muerte de "
  "cualquiera de los firmantes; y <b>(iv)</b> <b>desde el momento en que el documento se "
  "entrega o presenta a un funcionario en raz&oacute;n de su oficio</b>. Este &uacute;ltimo "
  "supuesto es el que se actualiza en la especie.")

P("3. La ratificaci&oacute;n de firmas ante notario colma ese cuarto supuesto", "h2")
P("La propia Primera Sala resolvi&oacute; expresamente que <b>la ratificaci&oacute;n de "
  "firmas ante notario s&iacute; otorga fecha cierta</b> al contrato privado traslativo de "
  "dominio y que ese documento <b>s&iacute; acredita el inter&eacute;s jur&iacute;dico en el "
  "amparo</b>, sin que sea necesario que el contrato se haya celebrado ante el notario ni "
  "que &eacute;ste lo haya redactado o protocolizado, conforme al criterio de rubro:")
P("&ldquo;INTER&Eacute;S JUR&Iacute;DICO EN EL AMPARO. PUEDE ACREDITARSE CON EL CONTRATO "
  "PRIVADO TRASLATIVO DE DOMINIO CUYAS FIRMAS SE RATIFICAN ANTE NOTARIO, PORQUE ES UN "
  "DOCUMENTO DE FECHA CIERTA (LEGISLACI&Oacute;N DEL ESTADO DE PUEBLA)&rdquo;, del que se "
  "desprenden cuatro definiciones vinculantes: <b>a)</b> entre las funciones notariales "
  "est&aacute; expedir las certificaciones que legalmente procedan; <b>b)</b> la "
  "certificaci&oacute;n de la ratificaci&oacute;n de firmas otorga la certeza de que "
  "<b>al menos en esa fecha ya se hab&iacute;a celebrado el acto traslativo de dominio</b>, "
  "evitando el riesgo de fraude contra acreedores; <b>c)</b> mientras no se declare "
  "judicialmente su falsedad, esa certificaci&oacute;n <b>convierte al documento privado en "
  "documento p&uacute;blico con valor probatorio pleno</b> en cuanto a la ratificaci&oacute;n "
  "de las firmas; y <b>d)</b> por ello constituye <b>prueba suficiente</b> para acreditar "
  "que la propiedad se transmiti&oacute; <b>antes</b> del embargo, y por tanto el "
  "inter&eacute;s jur&iacute;dico para pedir la protecci&oacute;n constitucional.", "quote")
P("La misma Sala hab&iacute;a establecido, al resolver la contradicci&oacute;n de tesis "
  "<b>14/2004-PS</b>, que basta la presentaci&oacute;n del documento ante el notario y la "
  "certificaci&oacute;n de las firmas, porque su intervenci&oacute;n atiende a la "
  "<b>materialidad del acto a trav&eacute;s de su fecha</b> y no a las formalidades del "
  "mismo, de modo que <b>no deben exigirse mayores formalidades a la fe p&uacute;blica</b> "
  "del funcionario en ejercicio de sus funciones.")

P("4. Aplicaci&oacute;n al caso concreto", "h2")
P("En la especie, el contrato privado de compraventa de [FECHA DEL CONTRATO] fue ratificado "
  "en cuanto a su contenido y firmas ante el notario p&uacute;blico n&uacute;mero [__] de "
  "la Ciudad de M&eacute;xico el <b>[FECHA DE RATIFICACI&Oacute;N]</b>, quien hizo constar "
  "la comparecencia, identidad y capacidad de los contratantes y autoriz&oacute; la "
  "certificaci&oacute;n con su firma y sello. Por consiguiente, <b>desde esa fecha</b> el "
  "documento es de fecha cierta y prueba plenamente que el inmueble ya hab&iacute;a salido "
  "del patrimonio de [VENDEDOR] e ingresado al m&iacute;o. Y como el embargo se trab&oacute; "
  "el <b>[FECHA DEL EMBARGO]</b>, es decir, con <b>posterioridad</b>, resulta incontrovertible "
  "que el acto reclamado recay&oacute; sobre un <b>bien ajeno al deudor</b> y afect&oacute; "
  "mi esfera jur&iacute;dica.")
P("Debe subrayarse que la jurisprudencia rectora fue emitida al interpretar la "
  "legislaci&oacute;n del Estado de Puebla; sin embargo, se invoca por <b>identidad de "
  "raz&oacute;n</b>, porque la <i>ratio decidendi</i> descansa en la naturaleza de la fe "
  "p&uacute;blica notarial y en la instituci&oacute;n de la fecha cierta, extra&iacute;da "
  "por analog&iacute;a del precepto que en la Ciudad de M&eacute;xico corresponde al "
  "<b>art&iacute;culo 2034, fracci&oacute;n III, del C&oacute;digo Civil para el Distrito "
  "Federal</b>, de contenido sustancialmente id&eacute;ntico al art&iacute;culo 1687 del "
  "C&oacute;digo Civil poblano que analiz&oacute; la Primera Sala. A ello se suma que el "
  "<b>art&iacute;culo 3005, fracci&oacute;n III</b>, del propio C&oacute;digo Civil local "
  "reconoce expresamente la registrabilidad de los <b>documentos privados</b> cuando al "
  "calce conste que el notario se cercior&oacute; de la autenticidad de las firmas y de la "
  "voluntad de las partes, lo que confirma que el legislador local atribuye a esa "
  "certificaci&oacute;n plena eficacia frente a terceros.")
P("Finalmente, la circunstancia de que mi t&iacute;tulo no se hubiere inscrito no destruye "
  "el inter&eacute;s jur&iacute;dico: la inscripci&oacute;n registral en el sistema "
  "mexicano es <b>declarativa y no constitutiva</b> de derechos, pues la traslaci&oacute;n "
  "de dominio opera por el acuerdo de las partes sobre la cosa y el precio "
  "(art&iacute;culos 2248 y 2249 del C&oacute;digo Civil para el Distrito Federal), y en el "
  "juicio de amparo la propiedad no se decide en definitiva, sino <b>de manera presuntiva</b> "
  "y para el solo efecto de determinar si el acto reclamado irrumpi&oacute; "
  "inconstitucionalmente en la esfera jur&iacute;dica del quejoso.")

story.append(PageBreak())


# ------------------ IX: CONCEPTOS DE VIOLACION ------------------------------
P("IX. CONCEPTOS DE VIOLACI&Oacute;N", "h1")
story.append(rule())

P("PRIMERO. Violaci&oacute;n a la garant&iacute;a de audiencia (art&iacute;culo 14, "
  "segundo p&aacute;rrafo, constitucional): se me priv&oacute; de la propiedad sin haber "
  "sido o&iacute;do ni vencido en juicio.", "h2")
P("El segundo p&aacute;rrafo del art&iacute;culo 14 constitucional prohibe privar a persona "
  "alguna de sus propiedades y posesiones sino mediante juicio seguido ante los tribunales "
  "previamente establecidos, en el que se cumplan las formalidades esenciales del "
  "procedimiento. La primera y m&aacute;s elemental de esas formalidades es la "
  "<b>notificaci&oacute;n del inicio del procedimiento</b> a quien puede resultar afectado.")
P("En el caso, los actos reclamados producen el efecto de privarme del inmueble de mi "
  "propiedad &mdash;acreditada con documento de fecha cierta anterior al embargo&mdash; "
  "dentro de un procedimiento en el que <b>nunca fui llamado</b>, en el que no se me "
  "notific&oacute; nada, en el que no pude ofrecer pruebas ni alegar y en el que no se "
  "dict&oacute; resoluci&oacute;n alguna en mi contra. La responsable no pod&iacute;a "
  "ignorar que el bien era ajeno al deudor: bastaba constatar la posesi&oacute;n del "
  "suscrito al momento de la diligencia, o requerir la exhibici&oacute;n del t&iacute;tulo "
  "de propiedad.")
P("La afectaci&oacute;n es de la mayor entidad, pues no se limita a la posesi&oacute;n: se "
  "extiende al <b>precio que pagu&eacute;</b>, que resultar&iacute;a perdido sin causa "
  "jur&iacute;dica alguna si se consuma el remate. La privaci&oacute;n de un inmueble sin "
  "audiencia y sin restituci&oacute;n del valor entregado configura una "
  "<b>confiscaci&oacute;n de facto</b>, incompatible con los art&iacute;culos 14 y 22 "
  "constitucionales y con el art&iacute;culo 21 de la Convenci&oacute;n Americana sobre "
  "Derechos Humanos, que prohibe privar a persona alguna de sus bienes sino mediante el "
  "pago de indemnizaci&oacute;n justa y con apego a la ley.")

P("SEGUNDO. Violaci&oacute;n a los principios de legalidad y seguridad jur&iacute;dica "
  "(art&iacute;culo 16 constitucional): es ilegal el embargo trabado en bienes que ya "
  "hab&iacute;an salido del patrimonio del deudor.", "h2")
P("El embargo, por definici&oacute;n, debe recaer <b>en bienes del deudor</b>. La "
  "responsable orden&oacute; y ejecut&oacute; el aseguramiento de un bien que, al momento de "
  "la diligencia, ya no formaba parte del patrimonio del demandado, sino del m&iacute;o, "
  "seg&uacute;n documento de fecha cierta preexistente. El acto carece, por tanto, de la "
  "debida fundamentaci&oacute;n y motivaci&oacute;n, pues parte de una premisa "
  "f&aacute;ctica falsa: la pertenencia del bien al ejecutado.")
P("Tampoco puede oponerse la falta de inscripci&oacute;n de mi t&iacute;tulo, porque el "
  "ejecutante es un <b>acreedor a t&iacute;tulo personal</b>: no ostenta derecho real "
  "alguno, ni poder directo e inmediato sobre la cosa, de modo que no puede prevalerse de "
  "la omisi&oacute;n registral para hacer efectivo su cr&eacute;dito sobre un bien ajeno. "
  "En este sentido, la Tercera Sala de la Suprema Corte de Justicia de la Naci&oacute;n "
  "sostuvo la jurisprudencia de rubro <b>&ldquo;EMBARGO, ES ILEGAL EL TRABADO EN BIENES "
  "SALIDOS DEL DOMINIO DEL DEUDOR, AUN CUANDO NO SE ENCUENTREN INSCRITOS EN EL REGISTRO "
  "P&Uacute;BLICO DE LA PROPIEDAD A NOMBRE DEL NUEVO ADQUIRENTE&rdquo;</b>, criterio "
  "expresamente recogido por los Tribunales Colegiados contendientes en la "
  "contradicci&oacute;n de tesis 173/2006-PS.")
P("[<b>Variante para acreedor con derecho real inscrito:</b> si el ejecutante es acreedor "
  "hipotecario cuya garant&iacute;a se inscribi&oacute; <b>antes</b> de mi "
  "adquisici&oacute;n, se reformula este concepto para reclamar &uacute;nicamente la "
  "omisi&oacute;n de llamarme al juicio en mi calidad de adquirente y la "
  "aplicaci&oacute;n del excedente del producto del remate, as&iacute; como la "
  "devoluci&oacute;n de las cantidades que pagu&eacute; y que la responsable retiene.]", "small")

P("TERCERO. Violaci&oacute;n al derecho a la tutela judicial efectiva y desconocimiento de "
  "la jurisprudencia obligatoria de la Primera Sala (art&iacute;culos 17 constitucional y "
  "217 de la Ley de Amparo).", "h2")
P("Si al resolver este juicio se desestimara mi inter&eacute;s jur&iacute;dico bajo el "
  "argumento de que el contrato debi&oacute; celebrarse o redactarse ante notario, o de que "
  "debi&oacute; protocolizarse o inscribirse, se reeditar&iacute;a exactamente el criterio "
  "que la Primera Sala de la Suprema Corte de Justicia de la Naci&oacute;n "
  "<b>declar&oacute; superado</b> al resolver la contradicci&oacute;n de tesis 173/2006-PS, "
  "con lo que se desatender&iacute;a jurisprudencia obligatoria en t&eacute;rminos del "
  "art&iacute;culo 217 de la Ley de Amparo y se me negar&iacute;a el acceso efectivo a la "
  "justicia constitucional. Con ese proceder se generar&iacute;a, adem&aacute;s, la "
  "paradoja de dejar sin protecci&oacute;n al adquirente diligente que acudi&oacute; ante "
  "un fedatario, para beneficiar a un acreedor personal ajeno al bien.")

P("CUARTO. Efectos restitutorios y devoluci&oacute;n de las cantidades pagadas: el "
  "cumplimiento sustituto (art&iacute;culos 77, 204 y 205 de la Ley de Amparo).", "h2")
P("Conforme al art&iacute;culo 77, fracci&oacute;n I, de la Ley de Amparo, la sentencia que "
  "concede el amparo contra actos positivos debe <b>restituir al quejoso en el pleno goce "
  "del derecho violado, restableciendo las cosas al estado que guardaban antes de la "
  "violaci&oacute;n</b>; y el propio precepto obliga al juzgador a precisar en el "
  "&uacute;ltimo considerando <b>los efectos concretos</b> del amparo y las medidas que las "
  "autoridades deban adoptar para asegurar su plena eficacia. De ah&iacute; que en este caso "
  "los efectos deban comprender, de manera <b>subsidiaria y escalonada</b>:")
P("<b>a) Restituci&oacute;n en especie (pretensi&oacute;n principal).</b> Dejar "
  "insubsistente todo lo actuado a partir de la diligencia de embargo por cuanto hace al "
  "inmueble de mi propiedad; levantar el embargo; declarar la nulidad del remate y de la "
  "adjudicaci&oacute;n; ordenar la cancelaci&oacute;n de las inscripciones registrales "
  "correspondientes; y restituirme en la posesi&oacute;n material del bien.", "body_i")
P("<b>b) Devoluci&oacute;n de las cantidades que la autoridad retiene o aplic&oacute; "
  "(pretensi&oacute;n directa).</b> Toda cantidad que el suscrito hubo de exhibir, depositar "
  "o enterar con motivo de los actos reclamados &mdash;billetes de dep&oacute;sito, "
  "garant&iacute;as, gastos de ejecuci&oacute;n, derechos registrales, contribuciones por la "
  "adjudicaci&oacute;n&mdash; carece de causa jur&iacute;dica si el acto que la origin&oacute; "
  "es inconstitucional; por tanto, su devoluci&oacute;n <b>con los rendimientos generados</b> "
  "no es una condena civil, sino un efecto natural y necesario de la restituci&oacute;n que "
  "ordena el art&iacute;culo 77, fracci&oacute;n I, de la Ley de Amparo. Retenerlas "
  "constituir&iacute;a un nuevo acto de privaci&oacute;n sin juicio.", "body_i")
P("<b>c) Cumplimiento sustituto (pretensi&oacute;n subsidiaria).</b> Si al momento de dictar "
  "sentencia, o durante la etapa de cumplimiento, resultara <b>materialmente imposible o "
  "desproporcionadamente gravoso</b> restituir las cosas al estado anterior &mdash;por "
  "ejemplo, si el inmueble ya fue adjudicado, escriturado e inscrito a favor de un tercero "
  "registral de buena fe&mdash;, desde ahora, con fundamento en los art&iacute;culos <b>204, "
  "fracci&oacute;n II, y 205</b> de la Ley de Amparo, <b>solicito expresamente el "
  "cumplimiento sustituto</b> mediante el pago de los da&ntilde;os y perjuicios "
  "ocasionados, cuya base de cuantificaci&oacute;n m&iacute;nima, plenamente demostrable en "
  "el incidente respectivo, se integra por: <b>(i)</b> el precio efectivamente pagado, "
  "esto es, $[MONTO], acreditado con el contrato de fecha cierta y los comprobantes de pago; "
  "<b>(ii)</b> los gastos, contribuciones, honorarios y derechos erogados con motivo de la "
  "adquisici&oacute;n, por $[MONTO]; <b>(iii)</b> el valor de las mejoras &uacute;tiles y "
  "necesarias, por $[MONTO]; <b>(iv)</b> la <b>actualizaci&oacute;n</b> de dichas "
  "cantidades conforme al &Iacute;ndice Nacional de Precios al Consumidor desde la fecha de "
  "cada erogaci&oacute;n; y <b>(v)</b> los <b>intereses legales</b> correspondientes. "
  "Subsidiariamente, y para el caso de que resultare mayor, el <b>valor comercial actual</b> "
  "del inmueble seg&uacute;n aval&uacute;o practicado por instituci&oacute;n autorizada.", "body_i")
P("No obsta que el cumplimiento sustituto se resuelva ordinariamente en la etapa de "
  "ejecuci&oacute;n, pues su solicitud expresa desde la demanda cumple una doble "
  "funci&oacute;n procesal: fija la pretensi&oacute;n econ&oacute;mica del quejoso para "
  "evitar que se le tenga por no formulada, y permite al juzgador precisar los efectos del "
  "amparo con la amplitud que exige el art&iacute;culo 77 de la Ley de Amparo. Se solicita, "
  "por ello, que en el &uacute;ltimo considerando de la sentencia se <b>reserve "
  "expresamente</b> el derecho del suscrito a promover el incidente correspondiente.")
story.append(callout(
    "PRECISI&Oacute;N T&Eacute;CNICA QUE EVITA UN DESECHAMIENTO",
    "No plantee la devoluci&oacute;n del dinero como <b>prestaci&oacute;n</b> reclamada al "
    "vendedor o al ejecutante: el amparo no condena a particulares al pago de prestaciones "
    "civiles. Pl&aacute;ntelo, como aqu&iacute;, en dos planos: (i) como <b>efecto "
    "restitutorio</b> frente a la autoridad que retiene o aplic&oacute; el dinero, y "
    "(ii) como <b>cumplimiento sustituto</b> para el caso de imposibilidad material de "
    "restituir el inmueble. La acci&oacute;n civil contra el vendedor (evicci&oacute;n y "
    "saneamiento, arts. 2119 a 2141 del C&oacute;digo Civil para el Distrito Federal) se "
    "reserva y se ejerce por separado: v&eacute;ase el Anexo D."))

# ------------------ X: SUSPENSION ------------------------------------------
P("X. SOLICITUD DE SUSPENSI&Oacute;N PROVISIONAL Y DEFINITIVA", "h1")
P("Con fundamento en los art&iacute;culos 125, 126, 128, 129, 138, 139, 147 y 148 de la Ley "
  "de Amparo, solicito que se conceda la <b>suspensi&oacute;n provisional de inmediato</b> "
  "y, en su oportunidad, la <b>definitiva</b>, para el efecto de que las cosas se mantengan "
  "en el estado que actualmente guardan y <b>no se ejecuten</b>: la audiencia de remate "
  "se&ntilde;alada para el [FECHA Y HORA]; la aprobaci&oacute;n del remate; la "
  "adjudicaci&oacute;n; el otorgamiento de la escritura; la <b>entrega material y "
  "desposesi&oacute;n</b> del inmueble; la inscripci&oacute;n de la adjudicaci&oacute;n en "
  "el Registro P&uacute;blico; ni la <b>entrega, aplicaci&oacute;n o disposici&oacute;n de "
  "los fondos</b> producto del remate o depositados con motivo de la ejecuci&oacute;n.")
P("Se satisfacen los requisitos del art&iacute;culo 128 de la Ley de Amparo: <b>a)</b> la "
  "medida es solicitada por el quejoso; y <b>b)</b> no se sigue perjuicio al inter&eacute;s "
  "social ni se contravienen disposiciones de orden p&uacute;blico, pues la sociedad no "
  "est&aacute; interesada en que se remate un inmueble ajeno al deudor, sino precisamente en "
  "lo contrario. Por el contrario, de ejecutarse los actos reclamados se causar&iacute;an "
  "da&ntilde;os de <b>dif&iacute;cil reparaci&oacute;n</b>, al perder el suscrito la "
  "propiedad, la posesi&oacute;n y el dinero pagado, mientras que la suspensi&oacute;n "
  "&uacute;nicamente posterga temporalmente el cobro de un cr&eacute;dito personal que "
  "podr&aacute; hacerse efectivo sobre otros bienes del deudor. Realizada la "
  "<b>ponderaci&oacute;n</b> que ordena el art&iacute;culo 138 de la Ley de Amparo, la "
  "apariencia del buen derecho es palmaria, pues descansa en un documento de fecha cierta y "
  "en jurisprudencia obligatoria de la Primera Sala de la Suprema Corte.")
P("En t&eacute;rminos del art&iacute;culo 132 de la Ley de Amparo, manifiesto mi "
  "disposici&oacute;n a exhibir la <b>garant&iacute;a</b> que ese Juzgado fije para "
  "responder de los da&ntilde;os y perjuicios que la medida pudiera ocasionar al tercero "
  "interesado, solicitando que su monto se determine considerando que el suscrito "
  "<b>conserva la posesi&oacute;n</b> del inmueble y que no existe riesgo de deterioro ni de "
  "insolvencia.")
P("Asimismo, con fundamento en el <b>art&iacute;culo 20</b> de la Ley de Amparo, y dado que "
  "la diligencia de [remate / entrega] est&aacute; se&ntilde;alada para el [FECHA Y HORA], "
  "solicito la <b>habilitaci&oacute;n de d&iacute;as y horas inh&aacute;biles</b> para "
  "proveer sobre la suspensi&oacute;n y para practicar las notificaciones respectivas, "
  "as&iacute; como que el acuerdo se comunique a las responsables por la v&iacute;a "
  "<b>m&aacute;s expedita</b> (oficio v&iacute;a electr&oacute;nica, fax o "
  "tel&eacute;grafo), en t&eacute;rminos del art&iacute;culo 23 del mismo ordenamiento.")

story.append(PageBreak())


# ------------------ XI: TRAMITE SUMARIO / URGENTE ---------------------------
P("XI. SOLICITUD DE TR&Aacute;MITE SUMARIO, URGENTE Y PREFERENTE", "h1")
P("Con el objeto de que este juicio se resuelva en el plazo m&aacute;s breve legalmente "
  "posible, respetuosamente solicito:")
P("<b>1.</b> Que se provea sobre la suspensi&oacute;n <b>el mismo d&iacute;a</b> de la "
  "presentaci&oacute;n de la demanda, habilitando d&iacute;as y horas inh&aacute;biles "
  "(art&iacute;culo 20 de la Ley de Amparo).", "body_i")
P("<b>2.</b> Que los informes justificados se requieran con el apercibimiento del "
  "art&iacute;culo 117, &uacute;ltimo p&aacute;rrafo, y 260, fracci&oacute;n III, de la Ley "
  "de Amparo, y que se ordene a la responsable remitir <b>copia certificada completa</b> del "
  "expediente de origen.", "body_i")
P("<b>3.</b> Que la audiencia constitucional se se&ntilde;ale en el plazo m&aacute;s breve "
  "posible y que <b>no se difiera</b>, habida cuenta de que la totalidad de las pruebas del "
  "suscrito son documentales que se exhiben desde este escrito, por lo que el asunto "
  "quedar&aacute; en estado de resoluci&oacute;n sin necesidad de dilaci&oacute;n "
  "probatoria alguna.", "body_i")
P("<b>4.</b> Que se acuerde el <b>tratamiento preferente</b> del expediente, dada la "
  "naturaleza de los actos reclamados, que tienden a la privaci&oacute;n definitiva de la "
  "propiedad y de la vivienda del suscrito.", "body_i")

# ------------------ XII: PRUEBAS -------------------------------------------
P("XII. PRUEBAS", "h1")
P("Con fundamento en los art&iacute;culos 75, 119 y 121 de la Ley de Amparo, ofrezco desde "
  "este momento las siguientes pruebas, que se relacionan con todos y cada uno de los hechos "
  "y conceptos de violaci&oacute;n:", "small")
story.append(checklist([
    ("<b>1. Documental privada de fecha cierta.</b> Original y copia certificada del "
     "contrato privado de compraventa de [FECHA], <b>con la certificaci&oacute;n de "
     "ratificaci&oacute;n de firmas</b> del notario p&uacute;blico n&uacute;mero [__] de "
     "[FECHA].",
     "Prueba <b>esencial</b>: acredita la fecha cierta, la traslaci&oacute;n de dominio "
     "anterior al embargo y el inter&eacute;s jur&iacute;dico. Reviselo contra el Anexo C."),
    ("<b>2. Comprobantes de pago del precio.</b> Recibos, finiquito, comprobantes de "
     "transferencia SPEI, estados de cuenta y copias de cheques.",
     "Acredita el <b>monto pagado</b>, base de la devoluci&oacute;n y del cumplimiento "
     "sustituto."),
    ("<b>3. Comprobantes de gastos y contribuciones.</b> Impuesto sobre adquisici&oacute;n de "
     "inmuebles, derechos registrales, honorarios, aval&uacute;o, facturas de mejoras.",
     "Integra los da&ntilde;os y perjuicios cuantificables."),
    ("<b>4. Documental p&uacute;blica.</b> Copia certificada de la totalidad del expediente "
     "[__/20__] del juzgado responsable, que se solicita requerir a la autoridad.",
     "Acredita que el suscrito no fue parte ni fue llamado, y las fechas del embargo y del "
     "remate."),
    ("<b>5. Certificado de existencia o inexistencia de gravamen</b> y constancia de folio "
     "real expedidos por el Registro P&uacute;blico de la Propiedad y de Comercio.",
     "Acredita el estado registral y la fecha de inscripci&oacute;n del embargo."),
    ("<b>6. Documental p&uacute;blica.</b> Informe del notario p&uacute;blico n&uacute;mero "
     "[__] sobre la autenticidad de la certificaci&oacute;n, firma y sello, que se solicita "
     "requerir.",
     "Blinda la certificaci&oacute;n frente a objeciones de falsedad."),
    ("<b>7. Boletas de predial y de derechos por suministro de agua</b> a nombre del quejoso, "
     "y comprobantes de servicios.",
     "Acredita posesi&oacute;n a t&iacute;tulo de propietario y publicidad de hecho."),
    ("<b>8. Inspecci&oacute;n judicial</b> en el inmueble [en su caso].",
     "Acredita la posesi&oacute;n material actual del quejoso."),
    ("<b>9. Presuncional</b> legal y humana e <b>instrumental</b> de actuaciones.",
     "En todo lo que favorezca al quejoso."),
], col1="Prueba", col2="Objeto"))
SP(6)
P("Solicito que las documentales se tengan por desahogadas por su propia y especial "
  "naturaleza, y que se me devuelvan los originales previo cotejo, dej&aacute;ndose copia "
  "certificada en autos.", "small")

# ------------------ XIII: PETITORIOS --------------------------------------
P("XIII. PUNTOS PETITORIOS", "h1")
P("Por lo expuesto y fundado, de Usted C. Juez de Distrito atentamente pido:", "small")
P("<b>PRIMERO.</b> Tenerme por presentado en los t&eacute;rminos de este escrito, "
  "<b>admitir a tr&aacute;mite</b> la demanda de amparo indirecto, reconocer mi "
  "personalidad y la calidad de <b>persona extra&ntilde;a al juicio</b> de origen, y tener "
  "por se&ntilde;alado el domicilio y por autorizados a los profesionistas indicados.")
P("<b>SEGUNDO.</b> Conceder la <b>suspensi&oacute;n provisional de inmediato</b> en los "
  "t&eacute;rminos solicitados en el cap&iacute;tulo X, habilitando d&iacute;as y horas "
  "inh&aacute;biles y ordenando su comunicaci&oacute;n por la v&iacute;a m&aacute;s "
  "expedita; y, previa vista y celebraci&oacute;n de la audiencia incidental, conceder la "
  "<b>suspensi&oacute;n definitiva</b>.")
P("<b>TERCERO.</b> Requerir a las autoridades responsables sus <b>informes justificados</b> "
  "con el apercibimiento legal correspondiente, orden&aacute;ndoles remitir copia "
  "certificada completa del expediente de origen; dar vista a los terceros interesados y al "
  "Agente del Ministerio P&uacute;blico de la Federaci&oacute;n adscrito.")
P("<b>CUARTO.</b> Admitir y tener por desahogadas las <b>pruebas</b> ofrecidas, "
  "acordar el <b>tr&aacute;mite preferente</b> solicitado y se&ntilde;alar la audiencia "
  "constitucional en el plazo m&aacute;s breve legalmente posible.")
P("<b>QUINTO.</b> En su oportunidad, <b>conceder el amparo y protecci&oacute;n de la "
  "Justicia Federal</b> y, en el &uacute;ltimo considerando de la sentencia, precisar como "
  "efectos, conforme al art&iacute;culo 77 de la Ley de Amparo: <b>(i)</b> dejar "
  "insubsistente todo lo actuado en el juicio de origen por cuanto hace al inmueble "
  "propiedad del suscrito, a partir de la diligencia de embargo de [FECHA]; <b>(ii)</b> "
  "levantar el embargo y ordenar la cancelaci&oacute;n de las inscripciones registrales "
  "respectivas; <b>(iii)</b> dejar sin efectos el remate, la adjudicaci&oacute;n, la "
  "escrituraci&oacute;n y la orden de entrega, restituyendo al suscrito en la "
  "posesi&oacute;n del bien; y <b>(iv)</b> ordenar la <b>devoluci&oacute;n al suscrito de "
  "todas las cantidades</b> que con motivo de los actos reclamados fueron depositadas, "
  "retenidas, aplicadas o enteradas, con sus rendimientos y debidamente actualizadas.")
P("<b>SEXTO.</b> Para el caso de que la restituci&oacute;n en especie resulte material o "
  "jur&iacute;dicamente imposible o desproporcionadamente gravosa, <b>reservar "
  "expresamente</b> el derecho del suscrito a solicitar el <b>cumplimiento sustituto</b> "
  "previsto en los art&iacute;culos 204, fracci&oacute;n II, y 205 de la Ley de Amparo, "
  "mediante el pago de los da&ntilde;os y perjuicios integrados por el precio pagado, "
  "gastos, contribuciones, mejoras, actualizaci&oacute;n conforme al &Iacute;ndice Nacional "
  "de Precios al Consumidor e intereses legales, en los t&eacute;rminos del cuarto concepto "
  "de violaci&oacute;n.")
P("<b>S&Eacute;PTIMO.</b> Tener por hecha la manifestaci&oacute;n de voluntad para recibir "
  "notificaciones por v&iacute;a electr&oacute;nica y ordenar la devoluci&oacute;n de los "
  "documentos originales previo cotejo y certificaci&oacute;n.")
SP(10)
P("<b>PROTESTO LO NECESARIO</b>", "center_b")
P("Ciudad de M&eacute;xico, a [__] de [MES] de [A&Ntilde;O].", "center_b")
SP(26)
story.append(rule(color="#333333", width=0.6, sa=4))
P("[NOMBRE COMPLETO DEL QUEJOSO]", "firma")
P("Quejoso", "small")
SP(18)
story.append(rule(color="#333333", width=0.6, sa=4))
P("LIC. [NOMBRE DEL ABOGADO]", "firma")
P("Autorizado en t&eacute;rminos del art&iacute;culo 12 de la Ley de Amparo &mdash; "
  "C&eacute;dula profesional n&uacute;mero [______]", "small")

story.append(PageBreak())


# ============================== ANEXO A ====================================
P("ANEXO A &mdash; CAT&Aacute;LOGO DE FUNDAMENTOS PARA INVOCAR", "h1")
story.append(rule())
story.append(callout(
    "VERIFICACI&Oacute;N OBLIGATORIA ANTES DE PRESENTAR",
    "Todas las tesis de este cat&aacute;logo provienen de la ejecutoria de la "
    "contradicci&oacute;n de tesis 173/2006-PS o son citadas en ella. Aun as&iacute;, "
    "<b>confirme su vigencia</b> (no interrupci&oacute;n, no superaci&oacute;n, no "
    "sustituci&oacute;n) en el Sistema de Consulta del Semanario Judicial de la "
    "Federaci&oacute;n (sjf2.scjn.gob.mx) y coteje el <b>texto vigente</b> de cada precepto, "
    "pues varios criterios son de la Novena &Eacute;poca y se emitieron bajo la Ley de "
    "Amparo abrogada."))
P("A.1 Jurisprudencia y tesis", "h2")
story.append(checklist([
    ("Contradicci&oacute;n de tesis <b>173/2006-PS</b>, Primera Sala. Novena &Eacute;poca, "
     "SJF y su Gaceta, Tomo XXVI, sept. 2007, p. 191 (registro digital de la ejecutoria: "
     "20357).",
     "Criterio <b>rectora</b>: el contrato privado traslativo de dominio cuyas firmas se "
     "ratifican ante notario es documento de <b>fecha cierta</b> y acredita el "
     "inter&eacute;s jur&iacute;dico en el amparo. Fue emitida respecto de la "
     "legislaci&oacute;n de Puebla: inv&oacute;quela por identidad de raz&oacute;n."),
    ("<b>1a./J. 46/99</b> &mdash; &ldquo;INTER&Eacute;S JUR&Iacute;DICO EN EL AMPARO, "
     "INEFICACIA DEL CONTRATO PRIVADO DE COMPRAVENTA DE FECHA INCIERTA, PARA "
     "ACREDITARLO&rdquo;. Tomo X, dic. 1999, p. 78.",
     "Define los supuestos de fecha cierta. &Uacute;sela <b>a favor</b>: su lectura "
     "correcta, fijada en la CT 173/2006-PS, incluye la presentaci&oacute;n del documento "
     "ante funcionario en raz&oacute;n de su oficio."),
    ("<b>1a./J. 44/2005</b> &mdash; &ldquo;DOCUMENTO PRIVADO DE FECHA CIERTA. PARA "
     "CONSIDERARLO COMO TAL ES SUFICIENTE QUE SE PRESENTE ANTE NOTARIO P&Uacute;BLICO Y QUE "
     "&Eacute;STE CERTIFIQUE LAS FIRMAS PLASMADAS EN &Eacute;L&rdquo;. Tomo XXI, jun. 2005, "
     "p. 77.",
     "Derivada de la CT 14/2004-PS: <b>no se requiere protocolizaci&oacute;n</b>. Cita "
     "central del cap&iacute;tulo VIII."),
    ("<b>1a./J. 33/2003</b> &mdash; fecha cierta por <b>muerte</b> de uno de los firmantes. "
     "Tomo XVIII, jul. 2003, p. 122.",
     "Alternativa si el vendedor falleci&oacute; antes del acto reclamado. Sostiene "
     "adem&aacute;s que en amparo la propiedad se examina de manera <b>presuntiva</b>."),
    ("<b>VI.2o.C.288 C</b> &mdash; &ldquo;COMPRAVENTA, CONTRATO PRIVADO DE. ES DE FECHA "
     "CIERTA SI SE RATIFICA ANTE FEDATARIO P&Uacute;BLICO O FUNCIONARIO AUTORIZADO, AUNQUE "
     "NO SE HAYA CELEBRADO ANTE &Eacute;STE&rdquo;. Tomo XVII, mar. 2003, p. 1702.",
     "Criterio que <b>prevaleci&oacute;</b> en la contradicci&oacute;n. &Uacute;til como "
     "refuerzo argumentativo."),
    ("Jurisprudencia 242 (Tercera Sala) &mdash; &ldquo;EMBARGO, ES ILEGAL EL TRABADO EN "
     "BIENES SALIDOS DEL DOMINIO DEL DEUDOR, AUN CUANDO NO SE ENCUENTREN INSCRITOS... A "
     "NOMBRE DEL NUEVO ADQUIRENTE&rdquo;. Ap&eacute;ndice 1917-1995, T. IV, p. 165.",
     "Columna vertebral del <b>segundo</b> concepto de violaci&oacute;n."),
    ("Jurisprudencia 150 (Tercera Sala) &mdash; &ldquo;COMPRAVENTA DE INMUEBLES. FALTA DE "
     "ESCRITURA P&Uacute;BLICA ANTE NOTARIO&rdquo;. Ap&eacute;ndice 1917-2000, T. IV, "
     "pp. 123-124.",
     "La escritura p&uacute;blica <b>no es solemnidad</b>: su falta no anula el contrato ni "
     "impide que surta efectos."),
    ("<b>2a./J. 16/94</b> &mdash; &ldquo;INTER&Eacute;S JUR&Iacute;DICO, AFECTACI&Oacute;N "
     "DEL. DEBE PROBARSE FEHACIENTEMENTE&rdquo;.",
     "La invocar&aacute; la contraparte. Neutral&iacute;cela: el documento de fecha cierta "
     "<b>es</b> prueba fehaciente, no presunci&oacute;n."),
    ("<b>2a./J. 21/98</b> &mdash; las <b>copias fotost&aacute;ticas simples</b>, por s&iacute; "
     "solas, no acreditan el inter&eacute;s jur&iacute;dico.",
     "Advertencia pr&aacute;ctica: exhiba <b>original o copia certificada</b>, nunca copia "
     "simple."),
], col1="Criterio", col2="Uso estrat&eacute;gico"))

P("A.2 Preceptos legales", "h2")
story.append(checklist([
    ("<b>Constituci&oacute;n:</b> 1&ordm;, 14 (2&ordm; p&aacute;rrafo), 16, 17, 22, 27, 103 y "
     "107, fracciones I, VII y XVI.",
     "Audiencia, legalidad, tutela judicial, prohibici&oacute;n de confiscaci&oacute;n, "
     "propiedad y bases del amparo."),
    ("<b>Ley de Amparo:</b> 1&ordm;, 2&ordm;, 5&ordm;, 6&ordm;, 12, 17, 18, 20, 23, 27, 33 "
     "fr. IV, 35, 37, 61 (fr. XII, XVI, XVIII y XX), 75, 77, 79, 107 (fr. IV y VI), 108, "
     "117, 119, 121, 125-129, 132, 138, 139, 147, 148, 204, 205 y 217.",
     "Estructura de la demanda, procedencia, suspensi&oacute;n, efectos de la sentencia y "
     "<b>cumplimiento sustituto</b>."),
    ("<b>Tratados:</b> 8.1, 21 y 25 de la Convenci&oacute;n Americana sobre Derechos "
     "Humanos; 14 del Pacto Internacional de Derechos Civiles y Pol&iacute;ticos.",
     "Debido proceso, propiedad privada y protecci&oacute;n judicial; control de "
     "convencionalidad."),
    ("<b>C&oacute;digo Civil para el Distrito Federal:</b> 2034 fr. III (fecha cierta), "
     "2248 y 2249 (perfeccionamiento de la venta), 2320 y 2321 (forma), 3005 fr. III "
     "(registrabilidad del documento privado certificado por notario), 3007 (efectos frente "
     "a terceros), 2119 a 2141 (evicci&oacute;n y saneamiento), 1882 y 1883 (pago de lo "
     "indebido y enriquecimiento ileg&iacute;timo).",
     "Sustituye a los art&iacute;culos poblanos citados en la ejecutoria (1687, 2121, 2122, "
     "2182, 2988, 2989, 2997). <b>Coteje el texto vigente.</b>"),
    ("<b>Ley del Notariado de la Ciudad de M&eacute;xico:</b> preceptos que regulan la fe "
     "p&uacute;blica notarial y los <b>cotejos y certificaciones de firmas</b> "
     "[insertar numerales del texto vigente].",
     "Equivalente local de los art&iacute;culos 14, 123, 136, 137 y 138 de la Ley del "
     "Notariado de Puebla que analiz&oacute; la Primera Sala."),
    ("<b>C&oacute;digo de Procedimientos Civiles aplicable</b> en la Ciudad de M&eacute;xico "
     "(o el C&oacute;digo Nacional de Procedimientos Civiles y Familiares, seg&uacute;n la "
     "etapa de implementaci&oacute;n vigente): documentos p&uacute;blicos y su valor "
     "probatorio pleno; terceria excluyente de dominio.",
     "<b>Verifique</b> qu&eacute; ordenamiento rige a la fecha de presentaci&oacute;n y el "
     "r&eacute;gimen transitorio aplicable al juicio de origen."),
], col1="Ordenamiento", col2="Materia"))

story.append(PageBreak())

# ============================== ANEXO B ====================================
P("ANEXO B &mdash; CUANTIFICACI&Oacute;N DEL DINERO CUYA DEVOLUCI&Oacute;N SE RECLAMA", "h1")
story.append(rule())
P("Llene esta tabla y repl&iacute;quela en el cuarto concepto de violaci&oacute;n y en el "
  "punto petitorio sexto. Cada renglon debe tener respaldo documental; sin comprobante, el "
  "concepto no es cuantificable en el incidente de cumplimiento sustituto.", "small")
story.append(checklist([
    ("Precio pagado por el inmueble", "$[______] &mdash; Comprobante: [contrato, recibos, "
     "SPEI, cheques]"),
    ("Impuesto sobre adquisici&oacute;n de inmuebles", "$[______] &mdash; Comprobante: "
     "[declaraci&oacute;n y pago]"),
    ("Derechos registrales y certificaciones", "$[______] &mdash; Comprobante: [recibos]"),
    ("Honorarios notariales y aval&uacute;o", "$[______] &mdash; Comprobante: [facturas]"),
    ("Mejoras &uacute;tiles y necesarias", "$[______] &mdash; Comprobante: [facturas, "
     "peritaje]"),
    ("Cantidades exhibidas o retenidas en el juicio de origen", "$[______] &mdash; "
     "Comprobante: [billete de dep&oacute;sito n&uacute;m. ____]"),
    ("<b>Subtotal hist&oacute;rico</b>", "<b>$[______]</b>"),
    ("Actualizaci&oacute;n conforme al INPC", "Desde la fecha de cada erogaci&oacute;n hasta "
     "el pago"),
    ("Intereses legales", "Conforme al ordenamiento aplicable, desde el requerimiento"),
    ("<b>Pretensi&oacute;n subsidiaria</b>", "<b>Valor comercial actual</b> del inmueble "
     "seg&uacute;n aval&uacute;o de instituci&oacute;n autorizada, si resultare mayor"),
], col1="Concepto", col2="Monto y respaldo"))

# ============================== ANEXO C ====================================
P("ANEXO C &mdash; ERRORES FATALES A REVISAR EN LA CERTIFICACI&Oacute;N NOTARIAL", "h1")
story.append(rule())
P("La contradicci&oacute;n 173/2006-PS confirm&oacute; que la ratificaci&oacute;n ante "
  "notario otorga fecha cierta, <b>pero</b> los criterios del Tercer Tribunal Colegiado que "
  "participaron en ella demuestran que una certificaci&oacute;n <b>defectuosa</b> destruye "
  "el caso. Revise cada punto <b>antes</b> de presentar la demanda:", "small")
story.append(checklist([
    ("La certificaci&oacute;n no hace constar la <b>capacidad</b> de los comparecientes.",
     "Caso resuelto en el amparo en revisi&oacute;n <b>301/2004</b>: se sobreseyo por esa "
     "omisi&oacute;n. Solicite al notario una certificaci&oacute;n complementaria o "
     "aclaratoria."),
    ("Falta la <b>identidad</b> de los firmantes, la frase <b>&ldquo;ante m&iacute;&rdquo;</b>, "
     "la firma o el <b>sello</b> del notario.",
     "Requisitos formales exigidos por la ley del notariado. Su ausencia hace ineficaz la "
     "certificaci&oacute;n."),
    ("La <b>firma del notario es ap&oacute;crifa</b> o el fedatario la desconoce.",
     "Caso del amparo en revisi&oacute;n <b>264/2004</b>. Obtenga <b>informe previo</b> del "
     "notario que reconozca firma y sello, y ofr&eacute;zcalo como prueba."),
    ("La fecha de la certificaci&oacute;n es <b>anterior</b> a la fecha del contrato "
     "(imposibilidad l&oacute;gica).",
     "Caso del amparo en revisi&oacute;n <b>325/2004</b>: certificaci&oacute;n declarada "
     "inveros&iacute;mil. Coteje fechas d&iacute;a por d&iacute;a."),
    ("La ratificaci&oacute;n es <b>posterior</b> al embargo, gravamen o inscripci&oacute;n.",
     "Caso del amparo en revisi&oacute;n <b>128/2006</b>: el amparo se pierde. Reoriente la "
     "estrategia a la v&iacute;a civil (Anexo D)."),
    ("Se exhibe <b>copia simple</b> del contrato o de la certificaci&oacute;n.",
     "Insuficiente conforme a la jurisprudencia 2a./J. 21/98. Exhiba original o copia "
     "certificada."),
    ("El vendedor <b>no era propietario</b> al momento de la venta.",
     "Situaci&oacute;n detectada en el amparo en revisi&oacute;n 439/2002. Acredite la "
     "cadena de t&iacute;tulos con el folio real."),
    ("El contrato se &ldquo;celebr&oacute;&rdquo; ante un <b>Juez</b> u otro funcionario sin "
     "facultades para dar fe de actos traslativos.",
     "Caso del amparo directo <b>41/2006</b>: no otorga fecha cierta. Solo funcionarios "
     "competentes en raz&oacute;n de su oficio."),
], col1="Vicio a detectar", col2="Precedente y remedio"))

story.append(PageBreak())

# ============================== ANEXO D ====================================
P("ANEXO D &mdash; VARIANTE: RECUPERACI&Oacute;N DEL DINERO POR LA V&Iacute;A ORDINARIA", "h1")
story.append(rule())
P("Cuando la ratificaci&oacute;n notarial es <b>posterior</b> al embargo, cuando el amparo se "
  "sobresee, o cuando el objetivo real es &uacute;nicamente <b>recuperar el precio pagado al "
  "vendedor</b>, el amparo no es la v&iacute;a. Estas son las acciones id&oacute;neas, que "
  "conviene reservar expresamente en el escrito de amparo:")
P("<b>1. Terceria excluyente de dominio</b> dentro del juicio de origen.", "h2")
P("Se promueve ante el mismo juez de la ejecuci&oacute;n, antes de que se otorgue la "
  "escritura al adjudicatario o se entregue el bien. Su objeto es liberar el inmueble del "
  "embargo acreditando el dominio con el mismo documento de fecha cierta. Es <b>optativa</b> "
  "frente al amparo y puede ejercerse aun despu&eacute;s de un sobreseimiento.")
P("<b>2. Acci&oacute;n de evicci&oacute;n y saneamiento contra el vendedor</b> "
  "(art&iacute;culos 2119 a 2141 del C&oacute;digo Civil para el Distrito Federal).", "h2")
P("Es la v&iacute;a natural para <b>recuperar el dinero</b>. Si el comprador es privado del "
  "bien por sentencia o remate derivado de una causa anterior a la venta, el vendedor "
  "responde de la evicci&oacute;n y debe restituir: <b>(i)</b> el precio pagado; "
  "<b>(ii)</b> los gastos del contrato; <b>(iii)</b> los gastos del juicio; <b>(iv)</b> las "
  "mejoras &uacute;tiles y necesarias; y <b>(v)</b> el valor de las mejoras "
  "voluptuarias y los da&ntilde;os, si obr&oacute; de mala fe. Prestaciones que deben "
  "reclamarse <b>expresamente y por separado</b> en la demanda civil.")
P("<b>Prestaciones tipo:</b> a) la declaraci&oacute;n judicial de que el demandado "
  "incumpli&oacute; su obligaci&oacute;n de garantizar la posesi&oacute;n pac&iacute;fica y "
  "&uacute;til del inmueble; b) el pago de $[MONTO] por concepto de precio pagado; c) el "
  "pago de $[MONTO] por gastos, contribuciones y mejoras; d) el pago de da&ntilde;os y "
  "perjuicios; e) intereses legales y actualizaci&oacute;n; y f) gastos y costas.", "small")
P("<b>3. Nulidad del remate o de la adjudicaci&oacute;n</b> en la v&iacute;a ordinaria "
  "civil, y <b>enriquecimiento ileg&iacute;timo o pago de lo indebido</b> "
  "(art&iacute;culos 1882 y 1883 del C&oacute;digo Civil para el Distrito Federal) contra "
  "quien recibi&oacute; el dinero sin causa.", "h2")
P("<b>4. Sobre la &ldquo;v&iacute;a sumaria&rdquo; local.</b>", "h2")
P("Si lo que se busca es un juicio civil r&aacute;pido para el cobro, verifique cu&aacute;l "
  "es la v&iacute;a abreviada vigente en la Ciudad de M&eacute;xico a la fecha de "
  "presentaci&oacute;n &mdash;juicio oral civil, juicio ejecutivo civil o el procedimiento "
  "que corresponda conforme al <b>C&oacute;digo Nacional de Procedimientos Civiles y "
  "Familiares</b> y su r&eacute;gimen de implementaci&oacute;n&mdash;, as&iacute; como la "
  "cuant&iacute;a y la competencia. La denominaci&oacute;n &ldquo;v&iacute;a sumaria&rdquo; "
  "no es uniforme y su eleccion err&oacute;nea genera improcedencia de la v&iacute;a.")
SP(10)
story.append(callout(
    "CIERRE",
    "Este machote est&aacute; construido sobre la <i>ratio decidendi</i> de la "
    "contradicci&oacute;n de tesis 173/2006-PS: <b>la fe p&uacute;blica notarial que "
    "certifica una ratificaci&oacute;n de firmas fija la fecha del acto traslativo de "
    "dominio y, con ello, abre la puerta del juicio de amparo al adquirente</b>. Todo el "
    "&eacute;xito procesal depende de dos elementos materiales: una certificaci&oacute;n "
    "notarial impecable y una fecha anterior al acto de privaci&oacute;n. Lo dem&aacute;s es "
    "argumentaci&oacute;n."))

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    build(story)
    print("PDF generado: %s" % OUT)
