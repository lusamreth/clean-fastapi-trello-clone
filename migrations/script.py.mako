"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    op.drop_constraint("board_ibfk_1", "board", type_="foreignkey")
    op.drop_constraint("card_ibfk_1", "card", type_="foreignkey")
    op.drop_constraint("todo_ibfk_1", "todo", type_="foreignkey")
    op.drop_constraint("task_ibfk_1", "task", type_="foreignkey")

    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
