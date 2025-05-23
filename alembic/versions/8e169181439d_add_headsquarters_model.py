"""Add Headsquarters model

Revision ID: 8e169181439d
Revises: 57a10bfed4c6
Create Date: 2025-04-18 17:52:12.728623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e169181439d'
down_revision: Union[str, None] = '57a10bfed4c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('headsquarters',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=500), nullable=False),
    sa.Column('phone', sa.String(length=60), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'CLOSE', name='statusheadsquarters'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('headsquarter_id', sa.UUID(), nullable=False))
    op.drop_constraint('users_company_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'headsquarters', ['headsquarter_id'], ['id'])
    op.drop_column('users', 'company_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('company_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_foreign_key('users_company_id_fkey', 'users', 'companies', ['company_id'], ['id'])
    op.drop_column('users', 'headsquarter_id')
    op.drop_table('headsquarters')
    # ### end Alembic commands ###
