"""add foreignkey to posts table

Revision ID: 3741c140bb61
Revises: fb93c0543677
Create Date: 2021-11-28 14:22:07.166758

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3741c140bb61"
down_revision = "fb93c0543677"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
