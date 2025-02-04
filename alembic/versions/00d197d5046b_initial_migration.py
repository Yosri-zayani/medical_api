"""Initial Migration

Revision ID: 00d197d5046b
Revises: 
Create Date: 2024-12-22 22:42:27.255714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00d197d5046b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medical_departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medical_departments_id'), 'medical_departments', ['id'], unique=False)
    op.create_index(op.f('ix_medical_departments_name'), 'medical_departments', ['name'], unique=True)
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.DateTime(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('medical_history', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patients_email'), 'patients', ['email'], unique=True)
    op.create_index(op.f('ix_patients_id'), 'patients', ['id'], unique=False)
    op.create_index(op.f('ix_patients_name'), 'patients', ['name'], unique=False)
    op.create_table('research_papers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('authors', sa.String(), nullable=True),
    sa.Column('publication_date', sa.DateTime(), nullable=True),
    sa.Column('abstract', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_research_papers_id'), 'research_papers', ['id'], unique=False)
    op.create_index(op.f('ix_research_papers_title'), 'research_papers', ['title'], unique=False)
    op.create_table('medical_specialties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['medical_departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medical_specialties_id'), 'medical_specialties', ['id'], unique=False)
    op.create_index(op.f('ix_medical_specialties_name'), 'medical_specialties', ['name'], unique=True)
    op.create_table('doctors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('specialty_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['specialty_id'], ['medical_specialties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_doctors_email'), 'doctors', ['email'], unique=True)
    op.create_index(op.f('ix_doctors_id'), 'doctors', ['id'], unique=False)
    op.create_index(op.f('ix_doctors_name'), 'doctors', ['name'], unique=False)
    op.create_table('medical_services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('specialty_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['specialty_id'], ['medical_specialties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medical_services_id'), 'medical_services', ['id'], unique=False)
    op.create_index(op.f('ix_medical_services_name'), 'medical_services', ['name'], unique=False)
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('appointment_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('scheduled', 'completed', 'cancelled', name='appointment_status'), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['medical_services.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appointments_id'), 'appointments', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_appointments_id'), table_name='appointments')
    op.drop_table('appointments')
    op.drop_index(op.f('ix_medical_services_name'), table_name='medical_services')
    op.drop_index(op.f('ix_medical_services_id'), table_name='medical_services')
    op.drop_table('medical_services')
    op.drop_index(op.f('ix_doctors_name'), table_name='doctors')
    op.drop_index(op.f('ix_doctors_id'), table_name='doctors')
    op.drop_index(op.f('ix_doctors_email'), table_name='doctors')
    op.drop_table('doctors')
    op.drop_index(op.f('ix_medical_specialties_name'), table_name='medical_specialties')
    op.drop_index(op.f('ix_medical_specialties_id'), table_name='medical_specialties')
    op.drop_table('medical_specialties')
    op.drop_index(op.f('ix_research_papers_title'), table_name='research_papers')
    op.drop_index(op.f('ix_research_papers_id'), table_name='research_papers')
    op.drop_table('research_papers')
    op.drop_index(op.f('ix_patients_name'), table_name='patients')
    op.drop_index(op.f('ix_patients_id'), table_name='patients')
    op.drop_index(op.f('ix_patients_email'), table_name='patients')
    op.drop_table('patients')
    op.drop_index(op.f('ix_medical_departments_name'), table_name='medical_departments')
    op.drop_index(op.f('ix_medical_departments_id'), table_name='medical_departments')
    op.drop_table('medical_departments')
    # ### end Alembic commands ###
