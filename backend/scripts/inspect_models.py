from __future__ import annotations

import inspect

from sqlalchemy.orm import RelationshipProperty

from app.db.base import Base
import app.models  # noqa: F401


def get_models():
    return sorted(
        {
            mapper.class_
            for mapper in Base.registry.mappers
            if inspect.isclass(mapper.class_)
        },
        key=lambda model: model.__name__,
    )


def main():
    models = get_models()

    print(f"TOTAL MODELS: {len(models)}")

    for model in models:
        table = model.__table__

        print(f"\n## {model.__name__} | table={table.name}")

        # Columns + Foreign Keys
        print("COLUMNS:")
        for column in table.columns:
            flags = []

            if column.primary_key:
                flags.append("PK")

            if not column.nullable:
                flags.append("NOT NULL")

            if column.unique:
                flags.append("UNIQUE")

            flag_text = f" [{', '.join(flags)}]" if flags else ""

            print(
                f"  {column.name}: "
                f"{column.type}{flag_text}"
            )

            for fk in column.foreign_keys:
                print(
                    f"    FK -> {fk.target_fullname}"
                )

        # Relationships
        print("RELATIONSHIPS:")

        relationships = []

        for name, attribute in vars(model).items():
            if isinstance(attribute, RelationshipProperty):
                relationships.append((name, attribute))

        if not relationships:
            print("  -")
        else:
            for name, rel in relationships:
                try:
                    target = rel.argument
                except Exception:
                    target = "?"

                try:
                    back_populates = rel.back_populates
                except Exception:
                    back_populates = "?"

                try:
                    backref = rel.backref
                except Exception:
                    backref = "?"

                try:
                    secondary = (
                        rel.secondary.name
                        if rel.secondary is not None
                        else None
                    )
                except Exception:
                    secondary = "?"

                details = [
                    f"target={target}",
                    f"back_populates={back_populates}",
                ]

                if backref:
                    details.append(f"backref={backref}")

                if secondary:
                    details.append(f"secondary={secondary}")

                print(
                    f"  {name}: "
                    + ", ".join(details)
                )

        # Constraints
        uniques = []
        checks = []

        for constraint in table.constraints:
            name = type(constraint).__name__

            if name == "UniqueConstraint":
                uniques.append(
                    ", ".join(
                        column.name
                        for column in constraint.columns
                    )
                )

            elif name == "CheckConstraint":
                checks.append(str(constraint.sqltext))

        if uniques:
            print("UNIQUE:")
            for unique in uniques:
                print(f"  ({unique})")

        if checks:
            print("CHECK:")
            for check in checks:
                print(f"  {check}")


if __name__ == "__main__":
    main()