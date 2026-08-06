from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle


def build_cover(
    analysis: dict[str, Any],
) -> list[Any]:
    """Construye la portada del informe PDF."""

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=12,
    )

    report_style = ParagraphStyle(
        name="CoverReport",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=24,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=8,
    )

    description_style = ParagraphStyle(
        name="CoverDescription",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=30,
    )

    label_style = ParagraphStyle(
        name="CoverLabel",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=6,
    )

    filename_style = ParagraphStyle(
        name="CoverFilename",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=17,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=24,
    )

    generated_style = ParagraphStyle(
        name="CoverGenerated",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=22,
    )

    numeric_columns = len(
        analysis.get(
            "numeric_statistics",
            [],
        )
    )

    generated_at = datetime.now().strftime(
        "%d/%m/%Y · %H:%M"
    )

    summary_data = [
        ["Métrica", "Valor"],
        ["Filas", str(analysis["rows"])],
        ["Columnas", str(analysis["columns"])],
        ["Columnas numéricas", str(numeric_columns)],
        ["Duplicados", str(analysis["duplicates"])],
        [
            "Valores nulos",
            f"{analysis['missing_percentage']} %",
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            8 * cm,
            5 * cm,
        ],
        hAlign="CENTER",
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
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#F8FAFC"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "RIGHT",
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

    return [
        Spacer(1, 1.2 * cm),
        Paragraph(
            "DataScope",
            title_style,
        ),
        Paragraph(
            "Data Analysis Report",
            report_style,
        ),
        Paragraph(
            "Análisis automático de conjuntos de datos",
            description_style,
        ),
        Paragraph(
            "Dataset analizado",
            label_style,
        ),
        Paragraph(
            str(analysis["filename"]),
            filename_style,
        ),
        Paragraph(
            (
                "Informe generado automáticamente por DataScope"
                f"<br/>{generated_at}"
            ),
            generated_style,
        ),
        summary_table,
        PageBreak(),
    ]