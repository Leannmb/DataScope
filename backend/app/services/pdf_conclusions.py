from typing import Any

from reportlab.lib import colors
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Spacer,
)


def build_conclusions(
    analysis: dict[str, Any],
) -> list[Any]:
    """Construye conclusiones automáticas a partir del análisis."""

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="ConclusionsTitle",
        parent=styles["Heading2"],
        fontSize=17,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=16,
    )

    item_style = ParagraphStyle(
        name="ConclusionItem",
        parent=styles["BodyText"],
        fontSize=11,
        leading=17,
        leftIndent=14,
        bulletIndent=0,
        spaceAfter=10,
        textColor=colors.HexColor("#334155"),
    )

    rows = analysis["rows"]
    columns = analysis["columns"]
    duplicates = analysis["duplicates"]

    numeric_statistics = analysis.get(
        "numeric_statistics",
        [],
    )

    numeric_columns = len(
        numeric_statistics
    )

    if rows == 1:
        rows_text = "1 fila"
    else:
        rows_text = f"{rows} filas"

    if columns == 1:
        columns_text = "1 columna"
    else:
        columns_text = f"{columns} columnas"

    if duplicates == 0:
        duplicate_text = (
            "No se detectaron registros duplicados."
        )
    elif duplicates == 1:
        duplicate_text = (
            "Se detectó 1 registro duplicado."
        )
    else:
        duplicate_text = (
            f"Se detectaron {duplicates} "
            "registros duplicados."
        )

    if numeric_columns == 0:
        numeric_text = (
            "El dataset no contiene columnas numéricas."
        )
    elif numeric_columns == 1:
        numeric_text = (
            "Se analizó 1 columna numérica."
        )
    else:
        numeric_text = (
            f"Se analizaron {numeric_columns} "
            "columnas numéricas."
        )

    conclusions: list[str] = [
        (
            f"El dataset contiene {rows_text} "
            f"y {columns_text}."
        ),
        duplicate_text,
        (
            "El porcentaje global de valores nulos es del "
            f"{analysis['missing_percentage']} %."
        ),
        numeric_text,
        (
            "El tamaño del archivo es de "
            f"{analysis['size_bytes']} bytes."
        ),
    ]

    valid_deviations = [
        statistics
        for statistics in numeric_statistics
        if statistics.get("std") is not None
    ]

    if valid_deviations:
        highest_dispersion = max(
            valid_deviations,
            key=lambda statistics: statistics["std"],
        )

        conclusions.append(
            (
                f'La columna "{highest_dispersion["name"]}" '
                "presenta la mayor desviación típica "
                f'({highest_dispersion["std"]}).'
            )
        )

    content: list[Any] = [
        PageBreak(),
        Paragraph(
            "Conclusiones automáticas",
            title_style,
        ),
        Spacer(1, 6),
    ]

    for conclusion in conclusions:
        content.append(
            Paragraph(
                conclusion,
                item_style,
                bulletText="•",
            )
        )

    return content