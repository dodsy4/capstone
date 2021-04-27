"""Initial migration.

Revision ID: 23bbc60852fa
Revises: 
Create Date: 2021-04-19 13:39:16.442720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23bbc60852fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('c',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=120), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('reg_num', sa.String(length=120), nullable=True),
    sa.Column('address1', sa.String(length=120), nullable=True),
    sa.Column('city1', sa.String(length=120), nullable=True),
    sa.Column('county1', sa.String(length=120), nullable=True),
    sa.Column('postcode1', sa.String(length=120), nullable=True),
    sa.Column('address2', sa.String(length=120), nullable=True),
    sa.Column('city2', sa.String(length=120), nullable=True),
    sa.Column('county2', sa.String(length=120), nullable=True),
    sa.Column('postcode2', sa.String(length=120), nullable=True),
    sa.Column('address3', sa.String(length=120), nullable=True),
    sa.Column('city3', sa.String(length=120), nullable=True),
    sa.Column('county3', sa.String(length=120), nullable=True),
    sa.Column('postcode3', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('linkedin_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('m',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('waste_stream', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('county', sa.String(length=120), nullable=True),
    sa.Column('postcode', sa.String(length=120), nullable=True),
    sa.Column('condition', sa.String(length=120), nullable=True),
    sa.Column('dimensions', sa.String(length=120), nullable=True),
    sa.Column('image_link1', sa.String(length=120), nullable=True),
    sa.Column('image_link2', sa.String(length=120), nullable=True),
    sa.Column('image_link3', sa.String(length=120), nullable=True),
    sa.Column('longitude', sa.Float(precision=5), nullable=True),
    sa.Column('latitude', sa.Float(precision=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('output',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('material', sa.String(length=120), nullable=True),
    sa.Column('amount', sa.String(length=120), nullable=True),
    sa.Column('unit', sa.String(length=120), nullable=True),
    sa.Column('site_address', sa.String(length=120), nullable=True),
    sa.Column('traditional_address', sa.String(length=120), nullable=True),
    sa.Column('divert_address', sa.String(length=120), nullable=True),
    sa.Column('traditional_cost', sa.String(length=120), nullable=True),
    sa.Column('divert_cost', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('r',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mat_id', sa.Integer(), nullable=False),
    sa.Column('e_id', sa.String(length=120), nullable=False),
    sa.Column('message', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('r')
    op.drop_table('output')
    op.drop_table('m')
    op.drop_table('c')
    # ### end Alembic commands ###