from datetime import datetime
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.services.pdf_charts import histogram_to_png
from app.services.pdf_conclusions import build_conclusions
from app.services.pdf_cover import build_cover


def format_statistic(
    value: float | int | None,
) -> str:
    """Formatea una estadística para mostrarla en el informe."""

    if value is None:
        return "No disponible"

    if isinstance(value, float):
        return f"{value:.2f}"

    return str(value)


def format_file_size(
    size_bytes: int,
) -> str:
    """Convierte el tamaño del archivo a una unidad legible."""

    if size_bytes < 1024:
        return f"{size_bytes} B"

    size_kb = size_bytes / 1024

    if size_kb < 1024:
        return f"{size_kb:.2f} KB"

    size_mb = size_kb / 1024

    return f"{size_mb:.2f} MB"


def draw_footer(
    canvas,
    document,
) -> None:
    """Dibuja el pie de página del informe."""

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        9,
    )

    canvas.setFillColor(
        colors.HexColor("#64748B")
    )

    generated_at = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    canvas.drawString(
        1.5 * cm,
        0.8 * cm,
        (
            "Generado por DataScope · "
            f"{generated_at}"
        ),
    )

    canvas.drawRightString(
        A4[0] - 1.5 * cm,
        0.8 * cm,
        f"Página {document.page}",
    )

    canvas.restoreState()


def build_pdf_report(
    analysis: dict[str, Any],
) -> BytesIO:
    """Genera un informe PDF con los resultados del análisis."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.7 * cm,
        title=(
            "Informe DataScope - "
            f"{analysis['filename']}"
        ),
        author="DataScope",
    )

    styles = getSampleStyleSheet()

    subtitle_style = ParagraphStyle(
        name="DataScopeSubtitle",
        parent=styles["Heading2"],
        fontSize=15,
        leading=19,
        spaceBefore=14,
        spaceAfter=10,
        textColor=colors.HexColor("#0F172A"),
    )

    chart_title_style = ParagraphStyle(
        name="DataScopeChartTitle",
        parent=styles["Heading3"],
        fontSize=12,
        leading=16,
        spaceBefore=8,
        spaceAfter=8,
        textColor=colors.HexColor("#0F172A"),
    )

    story: list[Any] = []

    # Portada
    story.extend(
        build_cover(analysis)
    )

    # Resumen general
    story.append(
        Paragraph(
            "Resumen general",
            subtitle_style,
        )
    )

    summary_data = [
        [
            "Métrica",
            "Valor",
        ],
        [
            "Filas",
            str(analysis["rows"]),
        ],
        [
            "Columnas",
            str(analysis["columns"]),
        ],
        [
            "Duplicados",
            str(analysis["duplicates"]),
        ],
        [
            "Valores nulos",
            f"{analysis['missing_percentage']} %",
        ],
        [
            "Tamaño del archivo",
            format_file_size(
                analysis["size_bytes"]
            ),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            8 * cm,
            8 * cm,
        ],
        repeatRows=1,
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2563EB"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#F8FAFC"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(summary_table)
    story.append(
        Spacer(
            1,
            12,
        )
    )

    # Columnas
    story.append(
        Paragraph(
            "Columnas",
            subtitle_style,
        )
    )

    columns_data = [
        [
            "Nombre",
            "Tipo",
            "Valores nulos",
        ]
    ]

    for column in analysis["column_types"]:
        column_name = column["name"]

        columns_data.append(
            [
                column_name,
                column["type"],
                str(
                    analysis["missing_values"].get(
                        column_name,
                        0,
                    )
                ),
            ]
        )

    columns_table = Table(
        columns_data,
        colWidths=[
            7 * cm,
            4.5 * cm,
            4.5 * cm,
        ],
        repeatRows=1,
    )

    columns_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2563EB"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F8FAFC"),
                    ],
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(columns_table)

    # Estadísticas numéricas
    numeric_statistics = analysis.get(
        "numeric_statistics",
        [],
    )

    if numeric_statistics:
        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                "Estadísticas numéricas",
                subtitle_style,
            )
        )

        statistics_data = [
            [
                "Columna",
                "Válidos",
                "Únicos",
                "Media",
                "Mediana",
                "Desv.",
                "Mín.",
                "Q1",
                "Q3",
                "Máx.",
            ]
        ]

        for statistics in numeric_statistics:
            statistics_data.append(
                [
                    statistics["name"],
                    str(statistics["count"]),
                    str(statistics["unique"]),
                    format_statistic(
                        statistics["mean"]
                    ),
                    format_statistic(
                        statistics["median"]
                    ),
                    format_statistic(
                        statistics["std"]
                    ),
                    format_statistic(
                        statistics["min"]
                    ),
                    format_statistic(
                        statistics["q1"]
                    ),
                    format_statistic(
                        statistics["q3"]
                    ),
                    format_statistic(
                        statistics["max"]
                    ),
                ]
            )

        statistics_table = Table(
            statistics_data,
            repeatRows=1,
            colWidths=[
                2.8 * cm,
                1.4 * cm,
                1.4 * cm,
                1.5 * cm,
                1.6 * cm,
                1.5 * cm,
                1.3 * cm,
                1.2 * cm,
                1.2 * cm,
                1.3 * cm,
            ],
        )

        statistics_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#2563EB"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#CBD5E1"),
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#F8FAFC"),
                        ],
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (-1, -1),
                        "RIGHT",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(statistics_table)

    # Histogramas
    numeric_histograms = analysis.get(
        "numeric_histograms",
        [],
    )

    if numeric_histograms:
        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                "Distribuciones numéricas",
                subtitle_style,
            )
        )

        for index, histogram in enumerate(
            numeric_histograms
        ):
            story.append(
                Paragraph(
                    str(histogram["name"]),
                    chart_title_style,
                )
            )

            chart_buffer = histogram_to_png(
                histogram
            )

            chart_image = Image(
                chart_buffer,
                width=16 * cm,
                height=8 * cm,
            )

            story.append(chart_image)

            if index < len(numeric_histograms) - 1:
                story.append(
                    Spacer(
                        1,
                        14,
                    )
                )

    # Conclusiones automáticas
    story.extend(
        build_conclusions(analysis)
    )

    document.build(
        story,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer,
    )

    buffer.seek(0)

    return buffer