"""add last olumns to posts

Revision ID: cdaebafb53c6
Revises: 3741c140bb61
Create Date: 2021-11-28 14:28:16.081212

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cdaebafb53c6"
down_revision = "3741c140bb61"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
