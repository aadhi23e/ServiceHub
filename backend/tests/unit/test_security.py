from app.core.security import (
    create_access_token,
    decode_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)


def test_password_hash_is_not_plaintext() -> None:
    password = "StrongPassword123!"

    password_hash = hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2")


def test_password_verification() -> None:
    password = "StrongPassword123!"

    password_hash = hash_password(password)

    assert verify_password(password, password_hash)
    assert not verify_password("WrongPassword!", password_hash)


def test_refresh_token_is_random() -> None:
    first = generate_refresh_token()
    second = generate_refresh_token()

    assert first != second
    assert len(first) > 20


def test_refresh_token_hash_is_deterministic() -> None:
    token = generate_refresh_token()

    first_hash = hash_refresh_token(token)
    second_hash = hash_refresh_token(token)

    assert first_hash == second_hash
    assert first_hash != token


def test_access_token_round_trip() -> None:
    token, expires_in = create_access_token(
        user_id=123,
        role="CUSTOMER",
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "123"
    assert payload["role"] == "CUSTOMER"
    assert payload["type"] == "access"
    assert payload["jti"]
    assert expires_in > 0