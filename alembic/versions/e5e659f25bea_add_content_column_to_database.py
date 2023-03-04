"""add content column to database

Revision ID: e5e659f25bea
Revises: 5e03644e77a1
Create Date: 2023-03-04 14:41:45.963938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5e659f25bea'
down_revision = '5e03644e77a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
