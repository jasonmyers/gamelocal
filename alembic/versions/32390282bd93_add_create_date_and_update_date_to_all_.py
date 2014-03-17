"""Add create_date and update_date to all tables

Revision ID: 32390282bd93
Revises: 2d2525b773e
Create Date: 2014-03-17 15:59:26.962150

"""

# revision identifiers, used by Alembic.
revision = '32390282bd93'
down_revision = '2d2525b773e'

from alembic import op
import sqlalchemy as sa

import datetime


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'clubs',
        sa.Column('create_date', sa.DateTime(), nullable=False,
                  server_default=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    )
    op.add_column(
        'clubs',
        sa.Column('update_date', sa.DateTime(), nullable=False,
                  server_default=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'update_date')
    op.drop_column('clubs', 'create_date')
    ### end Alembic commands ###
