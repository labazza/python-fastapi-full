"""create posts table

Revision ID: 915f99c3c942
Revises: 
Create Date: 2021-11-28 12:17:24.057075

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "915f99c3c942"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # just some columns for example
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
