import pytest
from sqlalchemy.orm import configure_mappers

import app.models  # noqa: F401


def test_all_model_relationships_configure():
    try:
        configure_mappers()
    except Exception as exc:
        pytest.fail(
            f"SQLAlchemy model relationship configuration failed:\n\n"
            f"{type(exc).__name__}: {exc}"
        )