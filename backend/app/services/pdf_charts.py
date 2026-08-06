from io import BytesIO

import matplotlib.pyplot as plt


def histogram_to_png(
    histogram: dict,
) -> BytesIO:
    fig, ax = plt.subplots(
        figsize=(7, 3.5)
    )

    ax.bar(
        histogram["labels"],
        histogram["counts"],
    )

    ax.set_title(histogram["name"])

    ax.set_ylabel("Frecuencia")

    plt.xticks(
        rotation=45,
        ha="right",
        fontsize=8,
    )

    plt.tight_layout()

    image = BytesIO()

    plt.savefig(
        image,
        format="png",
        dpi=180,
    )

    plt.close(fig)

    image.seek(0)

    return image