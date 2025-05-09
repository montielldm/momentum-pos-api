"""Associating Headsquarter and Company models

Revision ID: f84efe0a645d
Revises: 8e169181439d
Create Date: 2025-04-18 18:14:30.221171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f84efe0a645d'
down_revision: Union[str, None] = '8e169181439d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('headsquarters', sa.Column('company_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'headsquarters', 'companies', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'headsquarters', type_='foreignkey')
    op.drop_column('headsquarters', 'company_id')
    # ### end Alembic commands ###
