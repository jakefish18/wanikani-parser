"""Adding cascade delete for all relationships

Revision ID: 5221d221807b
Revises: d2106f5c7fca
Create Date: 2024-02-11 18:29:03.246011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5221d221807b'
down_revision: Union[str, None] = 'd2106f5c7fca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###