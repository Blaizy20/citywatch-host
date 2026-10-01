import re

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import OTPChallenge, Profile


@override_settings(
	EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
	PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'],
)
class EmailOTPFlowTests(TestCase):
	def registration_data(self):
		return {
			'username': 'resident-otp',
			'email': 'resident@example.com',
			'password': 'River!Stone427',
			'confirm_password': 'River!Stone427',
			'first_name': 'Resident',
			'last_name': 'One',
			'mobile': '09123456789',
			'barangay': 'Poblacion',
			'age': '24',
			'sex': 'Female',
			'address': '1 Example Street',
		}

	def otp_from_latest_email(self):
		match = re.search(r'\b(\d{6})\b', mail.outbox[-1].body)
		self.assertIsNotNone(match)
		return match.group(1)

	def begin_registration(self):
		response = self.client.post(
			reverse('register'),
			self.registration_data(),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.json()['success'])
		self.assertEqual(response.json()['redirect'], reverse('verify_email'))
		self.assertEqual(mail.outbox[-1].to, ['resident@example.com'])
		return OTPChallenge.objects.get(purpose='registration')

	def test_registration_creates_account_only_after_email_otp(self):
		challenge = self.begin_registration()
		self.assertFalse(User.objects.filter(username='resident-otp').exists())
		self.assertNotIn(self.otp_from_latest_email(), challenge.code_hash)

		response = self.client.post(reverse('verify_email'), {'code': self.otp_from_latest_email()})

		self.assertRedirects(response, reverse('login'))
		user = User.objects.get(username='resident-otp')
		self.assertTrue(user.is_active)
		self.assertTrue(user.check_password('River!Stone427'))
		self.assertEqual(Profile.objects.get(user=user).barangay, 'Poblacion')
		self.assertFalse(OTPChallenge.objects.filter(pk=challenge.pk).exists())

	def test_registration_wrong_code_does_not_create_account(self):
		self.begin_registration()
		correct_code = self.otp_from_latest_email()
		wrong_code = f'{(int(correct_code) + 1) % 1_000_000:06d}'

		response = self.client.post(reverse('verify_email'), {'code': wrong_code})

		self.assertContains(response, 'incorrect, expired')
		self.assertFalse(User.objects.filter(username='resident-otp').exists())
		self.assertEqual(OTPChallenge.objects.get(purpose='registration').attempts, 1)

	def test_registration_locks_code_after_five_wrong_attempts(self):
		self.begin_registration()
		correct_code = self.otp_from_latest_email()
		wrong_code = f'{(int(correct_code) + 1) % 1_000_000:06d}'
		for _ in range(5):
			self.client.post(reverse('verify_email'), {'code': wrong_code})

		self.client.post(reverse('verify_email'), {'code': correct_code})

		self.assertFalse(User.objects.filter(username='resident-otp').exists())
		self.assertEqual(OTPChallenge.objects.get(purpose='registration').attempts, 5)

	def test_registration_rejects_duplicate_email(self):
		User.objects.create_user(
			username='existingresident',
			email='resident@example.com',
			password='Strong!Pass123',
		)

		response = self.client.post(
			reverse('register'),
			{
				**self.registration_data(),
				'email': 'resident@example.com',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)

		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.json()['success'])
		self.assertIn('already in use', response.json()['error'].lower())

	def test_registration_rejects_common_password_without_leaking_reason(self):
		response = self.client.post(
			reverse('register'),
			{
				**self.registration_data(),
				'password': 'password',
				'confirm_password': 'password',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)

		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.json()['success'])
		self.assertEqual(response.json()['error'], 'Please choose a stronger password.')
		self.assertNotIn('too common', response.json()['error'].lower())

	def test_registration_otp_ui_uses_resend_label_during_cooldown(self):
		self.begin_registration()

		response = self.client.get(reverse('verify_email'))

		self.assertContains(response, 'Send again OTP')
		self.assertNotContains(response, 'Wait a minute')

	def test_registration_email_body_contains_clear_verification_instructions(self):
		self.begin_registration()

		self.assertIn('verification code', mail.outbox[-1].body.lower())
		self.assertIn('expires in 10 minutes', mail.outbox[-1].body.lower())
		self.assertIn('CityWatch', mail.outbox[-1].subject)

	def test_password_reset_updates_password_after_valid_otp(self):
		user = User.objects.create_user(
			username='resetresident',
			email='reset@example.com',
			password='Old!Password875',
		)
		response = self.client.post(reverse('password_reset'), {
			'action': 'request_code',
			'email': user.email,
		})
		self.assertContains(response, 'Check your email')
		self.assertEqual(mail.outbox[-1].to, [user.email])

		response = self.client.post(reverse('password_reset'), {
			'action': 'reset_password',
			'code': self.otp_from_latest_email(),
			'new_password': 'New!Password875',
			'confirm_password': 'New!Password875',
		})

		self.assertRedirects(response, reverse('login'))
		user.refresh_from_db()
		self.assertTrue(user.check_password('New!Password875'))
		self.assertFalse(user.check_password('Old!Password875'))
		self.assertFalse(OTPChallenge.objects.filter(purpose='password_reset').exists())

	def test_password_reset_does_not_change_password_for_wrong_code(self):
		user = User.objects.create_user(
			username='resetresident',
			email='reset@example.com',
			password='Old!Password875',
		)
		self.client.post(reverse('password_reset'), {
			'action': 'request_code',
			'email': user.email,
		})

		response = self.client.post(reverse('password_reset'), {
			'action': 'reset_password',
			'code': '000000',
			'new_password': 'New!Password875',
			'confirm_password': 'New!Password875',
		})

		self.assertContains(response, 'incorrect, expired')
		user.refresh_from_db()
		self.assertTrue(user.check_password('Old!Password875'))

	def test_password_reset_keeps_original_code_during_resend_cooldown(self):
		user = User.objects.create_user(
			username='resetresident',
			email='reset@example.com',
			password='Old!Password875',
		)
		self.client.post(reverse('password_reset'), {
			'action': 'request_code',
			'email': user.email,
		})
		original_code = self.otp_from_latest_email()

		response = self.client.post(reverse('password_reset'), {
			'action': 'request_code',
			'email': user.email,
		})
		self.assertContains(response, 'Please wait a minute')

		response = self.client.post(reverse('password_reset'), {
			'action': 'reset_password',
			'code': original_code,
			'new_password': 'New!Password875',
			'confirm_password': 'New!Password875',
		})

		self.assertRedirects(response, reverse('login'))
		user.refresh_from_db()
		self.assertTrue(user.check_password('New!Password875'))
