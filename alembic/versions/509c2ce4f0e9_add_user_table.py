"""add user table

Revision ID: 509c2ce4f0e9
Revises: e5e659f25bea
Create Date: 2023-03-04 14:53:54.963685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '509c2ce4f0e9'
down_revision = 'e5e659f25bea'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()')),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')
            )


def downgrade() -> None:
    op.drop_table('users')
    pass
