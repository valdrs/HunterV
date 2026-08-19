"""add subdomain uniqueness constraint

Revision ID: ab1b1419441f
Revises: 71827d48a883
Create Date: 2026-08-19 10:13:53.709008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab1b1419441f'
down_revision: Union[str, Sequence[str], None] = '71827d48a883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("subdomains", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            "uq_subdomain_target_hostname",
            ["target_id", "hostname"],
        )


def downgrade() -> None:
    with op.batch_alter_table("subdomains", schema=None) as batch_op:
        batch_op.drop_constraint(
            "uq_subdomain_target_hostname",
            type_="unique",
        )