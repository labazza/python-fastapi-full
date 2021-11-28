"""add content column posts table

Revision ID: 79f1eaeeb15d
Revises: 915f99c3c942
Create Date: 2021-11-28 14:04:46.412343

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "79f1eaeeb15d"
down_revision = "915f99c3c942"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
