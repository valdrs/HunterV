"""add subdomain timestamps

Revision ID: 1e1b64c1fb54
Revises: ab1b1419441f
Create Date: 2026-08-19 13:10:16.716069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e1b64c1fb54'
down_revision: Union[str, Sequence[str], None] = 'ab1b1419441f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("subdomains", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "first_seen",
                sa.DateTime(timezone=True),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )

        batch_op.add_column(
            sa.Column(
                "last_seen",
                sa.DateTime(timezone=True),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("subdomains", schema=None) as batch_op:
        batch_op.drop_column("last_seen")
        batch_op.drop_column("first_seen")