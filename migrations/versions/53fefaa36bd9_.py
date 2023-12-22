"""empty message

Revision ID: 53fefaa36bd9
Revises: 
Create Date: 2023-12-04 22:11:39.056343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "53fefaa36bd9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("board_ibfk_1", "board", type_="foreignkey")
    op.drop_constraint("card_ibfk_1", "card", type_="foreignkey")
    op.drop_constraint("todo_ibfk_1", "todo", type_="foreignkey")
    op.drop_constraint("task_ibfk_1", "task", type_="foreignkey")
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cabinet")
    op.drop_table("task")
    op.drop_table("auth")
    op.drop_table("card")
    op.drop_table("user")
    op.drop_table("board")
    op.drop_table("todo")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "todo",
        sa.Column("todo_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("card_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("created_on", mysql.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(["card_id"], ["card.card_id"], name="todo_ibfk_1"),
        sa.PrimaryKeyConstraint("todo_id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "board",
        sa.Column("board_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("description", mysql.VARCHAR(length=1028), nullable=True),
        sa.Column("topic", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("cabinet_id", mysql.VARCHAR(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["cabinet_id"],
            ["cabinet.cabinet_id"],
            name="board_ibfk_1",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("board_id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "user",
        sa.Column("user_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("username", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("password", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("email", mysql.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "card",
        sa.Column("card_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("title", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("description", mysql.VARCHAR(length=1028), nullable=True),
        sa.Column("board_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("created_on", mysql.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["board.board_id"], name="card_ibfk_1"),
        sa.PrimaryKeyConstraint("card_id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "auth",
        sa.Column("jti", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("user_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("token_value", mysql.VARCHAR(length=1025), nullable=False),
        sa.Column("token_type", mysql.VARCHAR(length=255), nullable=False),
        sa.Column(
            "expire_at",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("jti"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "task",
        sa.Column("task_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("description", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("created_on", mysql.DATETIME(), nullable=False),
        sa.Column("todo_id", mysql.VARCHAR(length=255), nullable=False),
        sa.ForeignKeyConstraint(["todo_id"], ["todo.todo_id"], name="task_ibfk_1"),
        sa.PrimaryKeyConstraint("task_id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "cabinet",
        sa.Column("cabinet_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("author", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("description", mysql.VARCHAR(length=1028), nullable=True),
        sa.Column("created_on", mysql.DATETIME(), nullable=False),
        sa.PrimaryKeyConstraint("cabinet_id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    # ### end Alembic commands ###
