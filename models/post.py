import sqlalchemy as sa
from main import metadata

posts = sa.Table(
    "posts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(150), nullable=False, unique=True),
    sa.Column("content", sa.String(150), nullable=False),
    sa.Column(
        "published_at", sa.DateTime, server_default=sa.func.now(), nullable=True
    ),
    sa.Column("published", sa.Boolean, server_default=False),
)
