from app.core.security import hash_password, verify_password


def test_password_hashing_uses_bcrypt():
    hashed = hash_password("password123")

    assert hashed != "password123"
    assert hashed.startswith("$2")
    assert verify_password("password123", hashed)
    assert not verify_password("wrong-password", hashed)
