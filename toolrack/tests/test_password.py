from ..password import (
    DEFAULT_CHARS,
    generate_password,
    PasswordProfile,
)


class TestGeneratePassword:
    def test_generate_password(self):
        """generate_password creates a random pasword of the default length."""
        password = generate_password()
        assert len(password) == 10
        for char in password:
            assert char in DEFAULT_CHARS

    def test_generate_password_with_chars(self):
        """The chars to use for generating the password can be specified."""
        assert generate_password(chars="a") == "a" * 10

    def test_generate_password_with_length(self):
        """The password length can be specified."""
        password = generate_password(length=4)
        assert len(password) == 4


class TestPasswordProfile:
    def test_generate(self):
        """PasswordProfile generates a password with the given set of chars."""
        profile = PasswordProfile("a")
        assert profile.generate() == "a" * 10

    def test_generate_length(self):
        """The password length can be specified."""
        profile = PasswordProfile("abcd")
        password = profile.generate(length=4)
        assert len(password) == 4

    def test_chars(self):
        """PasswordProfile.chars returns the set of chars to use."""
        profile = PasswordProfile("abcd")
        assert sorted(profile.chars) == list("abcd")

    def test_definition(self):
        """Characters definitions are expanded."""
        profile = PasswordProfile("{num}")
        assert sorted(profile.chars) == list("0123456789")

    def test_generate_definition(self):
        """Character in the definition are used to generate passwords."""
        profile = PasswordProfile("{num}")
        for char in profile.generate():
            assert char in "0123456789"
