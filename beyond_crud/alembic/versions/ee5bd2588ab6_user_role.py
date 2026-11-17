"""user role

Revision ID: ee5bd2588ab6
Revises: 5f8069ffb50f
Create Date: 2026-11-16 15:43:42.842903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ee5bd2588ab6'
down_revision: Union[str, Sequence[str], None] = '5f8069ffb50f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # server_default lets this run on a table that already has rows.
    op.add_column('user', sa.Column('role', sa.VARCHAR(), nullable=False, server_default='user'))
    op.create_unique_constraint('user_uid_key', 'user', ['uid'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('user_uid_key', 'user', type_='unique')
    op.drop_column('user', 'role')
