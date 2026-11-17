"""init

Revision ID: 5f8069ffb50f
Revises: 
Create Date: 2026-11-13 13:45:06.332490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5f8069ffb50f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # The books table was originally created by SQLModel.metadata.create_all()
    # before Alembic was set up, so create it here for fresh databases.
    op.create_table('books',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('author', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('publisher', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('published_date', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('page_count', sa.Integer(), nullable=False),
    sa.Column('language', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('user',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('uid')
    )
    op.create_unique_constraint('books_uid_key', 'books', ['uid'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user')
    op.drop_table('books')
