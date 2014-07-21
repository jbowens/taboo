"""empty message

Revision ID: 4a1acda8df3
Revises: 2b576574e73b
Create Date: 2014-07-20 21:23:04.588053

"""

# revision identifiers, used by Alembic.
revision = '4a1acda8df3'
down_revision = '2b576574e73b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('aid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('passwordhash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('aid'),
    sa.UniqueConstraint('username')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admins')
    ### end Alembic commands ###