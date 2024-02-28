"""Rename columns for word_use_patterns

Revision ID: a17ab2e17507
Revises: 82ee3a122b06
Create Date: 2024-02-28 17:55:14.313964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a17ab2e17507'
down_revision: Union[str, None] = '82ee3a122b06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('word_use_pattern', sa.Column('japanese', sa.String(), nullable=True))
    op.add_column('word_use_pattern', sa.Column('english', sa.String(), nullable=True))
    op.drop_column('word_use_pattern', 'example_japanese')
    op.drop_column('word_use_pattern', 'example_english')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('word_use_pattern', sa.Column('example_english', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('word_use_pattern', sa.Column('example_japanese', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('word_use_pattern', 'english')
    op.drop_column('word_use_pattern', 'japanese')
    # ### end Alembic commands ###