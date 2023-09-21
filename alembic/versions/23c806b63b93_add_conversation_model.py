"""Add Conversation model

Revision ID: 23c806b63b93
Revises: f8c2f8a76120
Create Date: 2023-09-16 15:34:49.247625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '23c806b63b93'
down_revision: Union[str, None] = 'f8c2f8a76120'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'conversation' table
    op.create_table(
        'conversation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user1_id', sa.Integer(), nullable=False),
        sa.Column('user2_id', sa.Integer(), nullable=False),
        # Add other columns for Conversation model here
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user1_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['user2_id'], ['user.id'], ),
        sa.UniqueConstraint('user1_id', 'user2_id', name='_user_user_uc'),
    )

def downgrade():
    # Drop the 'conversation' table
    op.drop_table('conversation')
