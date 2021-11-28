"""add users table

Revision ID: fb93c0543677
Revises: 79f1eaeeb15d
Create Date: 2021-11-28 14:12:35.165553

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "fb93c0543677"
down_revision = "79f1eaeeb15d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        # different way of setting id as primary key
        sa.PrimaryKeyConstraint("id"),
        # no duplicate emails
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
