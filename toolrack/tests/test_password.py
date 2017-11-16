from unittest import TestCase

from ..password import generate_password, PasswordProfile, DEFAULT_CHARS


class GeneratePasswordTests(TestCase):

    def test_generate_password(self):
        """generate_password creates a random pasword of the default length."""
        password = generate_password()
        self.assertEqual(len(password), 10)
        for char in password:
            self.assertIn(char, DEFAULT_CHARS)

    def test_generate_password_with_chars(self):
        """The chars to use for generating the password can be specified."""
        self.assertEqual(generate_password(chars='a'), 'a' * 10)

    def test_generate_password_with_length(self):
        """The password length can be specified."""
        password = generate_password(length=4)
        self.assertEqual(len(password), 4)


class PasswordProfileTests(TestCase):

    def test_generate(self):
        """PasswordProfile generates a password with the given set of chars."""
        profile = PasswordProfile('a')
        self.assertEqual(profile.generate(), 'a' * 10)

    def test_generate_length(self):
        """The password length can be specified."""
        profile = PasswordProfile('abcd')
        password = profile.generate(length=4)
        self.assertEqual(len(password), 4)

    def test_chars(self):
        """PasswordProfile.chars returns the set of chars to use."""
        profile = PasswordProfile('abcd')
        self.assertCountEqual(profile.chars, 'abcd')

    def test_definition(self):
        """Characters definitions are expanded."""
        profile = PasswordProfile('{num}')
        self.assertCountEqual(profile.chars, '0123456789')

    def test_generate_definition(self):
        """Character in the definition are used to generate passwords."""
        profile = PasswordProfile('{num}')
        for char in profile.generate():
            self.assertIn(char, '0123456789')
