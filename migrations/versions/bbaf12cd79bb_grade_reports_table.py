"""Grade reports table

Revision ID: bbaf12cd79bb
Revises: e28ecd5fad34
Create Date: 2018-08-16 23:58:11.766329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbaf12cd79bb'
down_revision = 'e28ecd5fad34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grade_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(length=100), nullable=True),
    sa.Column('session_course', sa.String(length=20), nullable=True),
    sa.Column('date_report', sa.DateTime(), nullable=True),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('tests_names', sa.String(length=500), nullable=True),
    sa.Column('a_grade', sa.String(length=500), nullable=True),
    sa.Column('b_grade', sa.String(length=500), nullable=True),
    sa.Column('c_grade', sa.String(length=500), nullable=True),
    sa.Column('f_grade', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_grade_report_date_creation'), 'grade_report', ['date_creation'], unique=False)
    op.create_index(op.f('ix_grade_report_date_report'), 'grade_report', ['date_report'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_grade_report_date_report'), table_name='grade_report')
    op.drop_index(op.f('ix_grade_report_date_creation'), table_name='grade_report')
    op.drop_table('grade_report')
    # ### end Alembic commands ###
