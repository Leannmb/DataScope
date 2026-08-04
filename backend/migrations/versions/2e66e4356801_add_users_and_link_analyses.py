"""add users and link analyses

Revision ID: 2e66e4356801
Revises: 696cf2d050f1
Create Date: 2026-08-01 20:45:44.495641
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e66e4356801"
down_revision: Union[str, Sequence[str], None] = "696cf2d050f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create users and associate existing analyses with a legacy user."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True,
    )

    # Primero se permite NULL porque ya existen análisis.
    op.add_column(
        "analysis",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    connection = op.get_bind()

    legacy_user_id = connection.execute(
        sa.text(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (
                'Legacy User',
                'legacy@datascope.local',
                'ACCOUNT_NOT_LOGINABLE'
            )
            RETURNING id
            """
        )
    ).scalar_one()

    # Asociamos los análisis anteriores al usuario provisional.
    connection.execute(
        sa.text(
            """
            UPDATE analysis
            SET user_id = :legacy_user_id
            WHERE user_id IS NULL
            """
        ),
        {"legacy_user_id": legacy_user_id},
    )

    # Ahora ya podemos exigir que todos los análisis tengan usuario.
    op.alter_column(
        "analysis",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.create_foreign_key(
        "fk_analysis_user_id_users",
        "analysis",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Remove the user relationship and users table."""

    op.drop_constraint(
        "fk_analysis_user_id_users",
        "analysis",
        type_="foreignkey",
    )

    op.drop_column("analysis", "user_id")

    op.drop_index(
        op.f("ix_users_email"),
        table_name="users",
    )

    op.drop_table("users")