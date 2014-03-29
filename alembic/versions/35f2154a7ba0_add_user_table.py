"""Add User table

Revision ID: 35f2154a7ba0
Revises: 511aee157fa9
Create Date: 2014-03-28 22:53:26.886547

"""

# revision identifiers, used by Alembic.
revision = '35f2154a7ba0'
down_revision = '511aee157fa9'

from alembic import op
import sqlalchemy as sa
from app import models

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('address', sa.UnicodeText(), nullable=False),
    sa.Column('city', sa.UnicodeText(), nullable=False),
    sa.Column('region', sa.UnicodeText(), nullable=False),
    sa.Column('postal_code', sa.UnicodeText(), nullable=False),
    sa.Column('country_code', models.UnicodeTextChoices, nullable=False),
    sa.Column('timezone', sa.UnicodeText(), nullable=False),
    sa.Column('latitude', models.DialectNumeric(), nullable=True),
    sa.Column('longitude', models.DialectNumeric(), nullable=True),
    sa.Column('email', sa.UnicodeText(), nullable=False),
    sa.Column('email_confirmed', sa.Boolean(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=False),
    sa.Column('locale', sa.UnicodeText(), nullable=False),
    sa.Column('last_login_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###