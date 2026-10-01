from io import BytesIO
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Announcement


class ResidentDashboardAnnouncementTests(TestCase):
	def test_staff_dashboard_links_to_announcement_management(self):
		staff = User.objects.create_user(username='staff-dashboard', password='test-password', is_staff=True)
		self.client.force_login(staff)

		response = self.client.get(reverse('analytics_dashboard'))

		self.assertContains(response, reverse('admin_announcement_list'))
		self.assertContains(response, 'News &amp; Announcements')

	def test_resident_cannot_access_announcement_management(self):
		resident = User.objects.create_user(username='resident-user', password='test-password')
		self.client.force_login(resident)

		response = self.client.get(reverse('admin_announcement_list'))

		self.assertEqual(response.status_code, 302)

	def test_dashboard_shows_published_announcements_in_news_section(self):
		resident = User.objects.create_user(username='news-resident', password='test-password')
		self.client.force_login(resident)
		Announcement.objects.create(
			title='Neighborhood clean-up',
			content='Join the community clean-up this weekend.',
			announcement_type='news',
			is_published=True,
		)
		Announcement.objects.create(
			title='Draft notice',
			content='This draft should not appear.',
			is_published=False,
		)

		response = self.client.get(reverse('resident_dashboard'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'News &amp; Announcements')
		self.assertContains(response, 'Neighborhood clean-up')
		self.assertNotContains(response, 'Draft notice')

	def test_staff_can_publish_scheduled_announcement_with_image_for_residents(self):
		staff = User.objects.create_user(username='city-staff', password='test-password', is_staff=True)
		resident = User.objects.create_user(username='resident-news', password='test-password')
		image_buffer = BytesIO()
		Image.new('RGB', (2, 2), color='green').save(image_buffer, format='PNG')
		image_bytes = image_buffer.getvalue()

		with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
			self.client.force_login(staff)
			response = self.client.post(reverse('admin_announcement_list'), {
				'title': 'Town hall meeting',
				'announcement_type': 'schedule',
				'content': 'Residents are invited to the town hall.',
				'event_date': '2026-10-18T14:30',
				'is_published': 'on',
				'image': SimpleUploadedFile('town-hall.png', image_bytes, content_type='image/png'),
			})

			self.assertRedirects(response, reverse('admin_announcement_list'))
			announcement = Announcement.objects.get(title='Town hall meeting')
			self.assertEqual(announcement.announcement_type, 'schedule')
			self.assertTrue(announcement.is_published)
			self.assertIsNotNone(announcement.event_date)
			self.assertTrue(announcement.image.name.startswith('announcement_images/'))

			self.client.force_login(resident)
			response = self.client.get(reverse('resident_dashboard'))

			self.assertContains(response, 'Town hall meeting')
			self.assertContains(response, announcement.image.url)
			self.assertContains(response, 'Oct 18, 2026')
