"""Add Geo model mixin columns

Revision ID: 46ba80c4f57b
Revises: 57f4d36e0adf
Create Date: 2014-03-24 00:25:02.206829

"""

# revision identifiers, used by Alembic.
revision = '46ba80c4f57b'
down_revision = '57f4d36e0adf'

from alembic import op
import sqlalchemy as sa
from app import models, db

def upgrade():
    Decimal = sa.Numeric(precision=9, scale=6)
    if db.engine.dialect.name == 'sqlite':
        Decimal = sa.Float()

    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('club', sa.Column('address', sa.UnicodeText(), nullable=False, server_default=''))
    op.add_column('club', sa.Column('city', sa.Unicode(length=50), nullable=False, server_default=''))
    op.add_column('club', sa.Column('country_code', models.UnicodeTextChoices, nullable=False, server_default=''))
    op.add_column('club', sa.Column('latitude', Decimal, nullable=True))
    op.add_column('club', sa.Column('longitude', Decimal, nullable=True))
    op.add_column('club', sa.Column('postal_code', sa.Unicode(length=50), nullable=False, server_default=''))
    op.add_column('club', sa.Column('region', sa.Unicode(length=50), nullable=False, server_default=''))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('club', 'region')
    op.drop_column('club', 'postal_code')
    op.drop_column('club', 'longitude')
    op.drop_column('club', 'latitude')
    op.drop_column('club', 'country_code')
    op.drop_column('club', 'city')
    op.drop_column('club', 'address')
    ### end Alembic commands ###