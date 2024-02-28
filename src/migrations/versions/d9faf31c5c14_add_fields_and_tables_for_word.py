"""Add fields and tables for word

Revision ID: d9faf31c5c14
Revises: b540f19995fa
Create Date: 2024-02-28 12:16:13.561396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9faf31c5c14'
down_revision: Union[str, None] = 'b540f19995fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('words', sa.Column('symbols', sa.String(), nullable=True))
    op.add_column('words', sa.Column('reading', sa.String(), nullable=True))
    op.add_column('words', sa.Column('reading_audio_filename', sa.String(), nullable=True))
    op.drop_column('words', 'meaning')
    op.drop_column('words', 'word')
    op.drop_column('words', 'mnemonic')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('words', sa.Column('mnemonic', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('words', sa.Column('word', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('words', sa.Column('meaning', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('words', 'reading_audio_filename')
    op.drop_column('words', 'reading')
    op.drop_column('words', 'symbols')
    # ### end Alembic commands ###