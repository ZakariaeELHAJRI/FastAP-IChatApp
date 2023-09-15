"""make send_at equal current date 2

Revision ID: 9e4e576dd0b3
Revises: a46785dcede8
Create Date: 2023-08-26 00:54:03.382693

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9e4e576dd0b3'
down_revision: Union[str, None] = 'a46785dcede8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Alter the column type
    op.alter_column('message', 'send_at', existing_type=sa.DateTime(), type_=sa.DateTime(timezone=True), nullable=False)
    
def downgrade() -> None:
    # Revert the column type if needed
    op.alter_column('message', 'send_at', existing_type=sa.DateTime(timezone=True), type_=sa.DateTime(), nullable=False)
