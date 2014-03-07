"""Added game type column to clubs table

Revision ID: 2d2525b773e
Revises: 2fe92b087948
Create Date: 2014-03-07 14:10:43.691612

"""

# revision identifiers, used by Alembic.
revision = '2d2525b773e'
down_revision = '2fe92b087948'

from alembic import op
import sqlalchemy as sa

from app.models import UnicodeChoices


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('game', UnicodeChoices(length=50), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'game')
    ### end Alembic commands ###