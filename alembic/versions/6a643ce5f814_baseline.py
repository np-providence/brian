"""baseline

Revision ID: 6a643ce5f814
Revises: 
Create Date: 2020-01-08 23:26:57.682701

"""
from alembic import op
import sqlalchemy as sa
from datetime import date, datetime


# revision identifiers, used by Alembic.
revision = '6a643ce5f814'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Attendee',
        sa.Column('id', sa.BIGINT, primary_key = True),
        sa.Column('email', sa.String, unique = True),
        sa.Column('course', sa.String),
        sa.Column('year', sa.String),
        sa.Column('gender', sa.String),
        sa.Column('passHash', sa.String()),
        sa.Column('status', sa.Boolean),
    )
    op.create_table(
        'User',
        sa.Column('id', sa.BIGINT, primary_key = True),
        sa.Column('email', sa.String, unique = True),
        sa.Column('name', sa.String),
        sa.Column('passHash', sa.String()),
        sa.Column('isAdmin', sa.Boolean),
    )
    op.create_table(
        'Features',
        sa.Column('id', sa.BIGINT, primary_key = True),
        sa.Column('attendee_id', sa.String, unique = True),
        sa.Column('eventowner_id', sa.String),
        sa.Column('feat', sa.ARRAY(sa.String)),
        sa.Column('dateTimeRecorded', sa.DateTime, default=datetime.utcnow),
    )
    op.create_table(
        'Camera',
        sa.Column('macaddress', sa.BIGINT, primary_key = True),
        sa.Column('location', sa.String),
    )

    pass


def downgrade():
    op.drop_table('Attendee')
    op.drop_table('User')
    op.drop_table('Camera')
    op.drop_table('Features')
    pass
