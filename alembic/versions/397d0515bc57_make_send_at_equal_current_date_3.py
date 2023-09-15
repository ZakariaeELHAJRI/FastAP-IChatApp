"""make send_at equal current date 3

Revision ID: 397d0515bc57
Revises: 9e4e576dd0b3
Create Date: 2023-08-26 00:55:12.278696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '397d0515bc57'
down_revision: Union[str, None] = '9e4e576dd0b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Alter the column type
    op.alter_column('message', 'send_at', existing_type=sa.DateTime(), type_=sa.DateTime(timezone=True), nullable=False)
    
def downgrade() -> None:
    # Revert the column type if needed
    op.alter_column('message', 'send_at', existing_type=sa.DateTime(timezone=True), type_=sa.DateTime(), nullable=False)
