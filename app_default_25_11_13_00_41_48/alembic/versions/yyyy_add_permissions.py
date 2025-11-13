"""Add permissions column to roles table

Revision ID: yyyy
Revises: xxxx
Create Date: 2024-06-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "yyyy"
down_revision = "xxxx"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("roles", sa.Column("permissions", postgresql.JSONB, nullable=False, server_default="{}"))
    # Optional: Update existing roles with default permissions
    op.execute("UPDATE roles SET permissions = '{}'::jsonb WHERE permissions IS NULL")


def downgrade():
    op.drop_column("roles", "permissions")
