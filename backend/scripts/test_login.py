import requests

LOGIN_URL = "http://localhost:8000/api/v1/auth/login"

payload = {
    "email": "user@example.com",
    "password": "stringst",
}


with requests.Session() as session:
    response = session.post(
        LOGIN_URL,
        json=payload,
    )

    print("=" * 60)
    print("STATUS")
    print("=" * 60)
    print(response.status_code)

    print("\n" + "=" * 60)
    print("RESPONSE BODY")
    print("=" * 60)
    print(response.text)

    print("\n" + "=" * 60)
    print("RESPONSE HEADERS")
    print("=" * 60)

    for key, value in response.headers.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 60)
    print("SET-COOKIE")
    print("=" * 60)
    print(response.headers.get("set-cookie"))

    print("\n" + "=" * 60)
    print("REFRESH TOKEN FROM COOKIE JAR")
    print("=" * 60)

    refresh_token = session.cookies.get("refresh_token")

    print(refresh_token)

    if refresh_token:
        print("\nRefresh token FOUND.")
    else:
        print("\nRefresh token NOT FOUND.")
