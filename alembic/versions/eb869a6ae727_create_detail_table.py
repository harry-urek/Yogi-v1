"""create detail table

Revision ID: eb869a6ae727
Revises: 7561294e9a4f
Create Date: 2023-09-16 01:48:35.703518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb869a6ae727'
down_revision: Union[str, None] = '7561294e9a4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('details', sa.Column('id', sa.Integer(), primary_key=True, index=True),
                    op.Column('plant_family', sa.String),
                    op.Column('plant_bio', sa.String),
                    op.Column('plant_descr', sa.String),
                    op.Column('plant_url', sa.String),
                    op.Column('plant_id', sa.String),
                    op.create_foreign_key('plant_detail_fk', source_table="details", referent_table="plants", local_cols=[
                        'plant_id'], remote_cols=['id']))


def downgrade() -> None:
    op.drop_table('details')
