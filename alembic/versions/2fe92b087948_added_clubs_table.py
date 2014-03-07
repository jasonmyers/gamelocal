"""Added clubs table

Revision ID: 2fe92b087948
Revises: None
Create Date: 2014-03-07 11:40:04.174791

"""

# revision identifiers, used by Alembic.
revision = '2fe92b087948'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clubs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clubs')
    ### end Alembic commands ###
