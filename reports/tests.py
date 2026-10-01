from io import BytesIO
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from .forms import AnnouncementForm, ReportForm
from .models import Announcement


class ResidentDashboardAnnouncementTests(TestCase):
	def test_report_category_choices_have_no_blank_and_include_pets(self):
		choices = list(ReportForm().fields['category'].choices)
		values = [value for value, _ in choices]

		self.assertNotIn('', values)
		self.assertIn('pets', values)

	def test_announcement_detail_shows_full_content_and_does_not_show_drafts(self):
		resident = User.objects.create_user(username='reader-resident', password='test-password')
		self.client.force_login(resident)
		full_content = 'A detailed community update. ' * 18
		announcement = Announcement.objects.create(
			title='Full story',
			content=full_content,
			is_published=True,
		)
		draft = Announcement.objects.create(title='Private draft', content='Draft text', is_published=False)

		response = self.client.get(reverse('announcement_detail', args=[announcement.pk]))

		self.assertContains(response, full_content)
		self.assertContains(response, 'id="announcement-detail-content"')
		self.assertEqual(self.client.get(reverse('announcement_detail', args=[draft.pk])).status_code, 404)

	def test_staff_can_edit_announcement_and_preserve_publish_date(self):
		staff = User.objects.create_user(username='announcement-editor', password='test-password', is_staff=True)
		announcement = Announcement.objects.create(
			title='Original title',
			content='Original content',
			announcement_type='news',
			is_published=True,
			date_published=timezone.now(),
			is_featured=True,
		)
		published_at = announcement.date_published
		self.client.force_login(staff)

		response = self.client.post(reverse('admin_announcement_edit', args=[announcement.pk]), {
			'title': 'Updated title',
			'announcement_type': 'advisory',
			'content': 'Updated full advisory text.',
			'is_published': 'on',
			'is_featured': 'on',
		})

		self.assertRedirects(response, reverse('admin_announcement_list'))
		announcement.refresh_from_db()
		self.assertEqual(announcement.title, 'Updated title')
		self.assertEqual(announcement.content, 'Updated full advisory text.')
		self.assertEqual(announcement.date_published, published_at)
		self.assertTrue(announcement.is_featured)

	def test_staff_can_delete_announcement_with_post_only(self):
		staff = User.objects.create_user(username='announcement-deleter', password='test-password', is_staff=True)
		announcement = Announcement.objects.create(title='Remove me', content='Old update')
		self.client.force_login(staff)

		self.assertEqual(self.client.get(reverse('admin_announcement_delete', args=[announcement.pk])).status_code, 405)
		response = self.client.post(reverse('admin_announcement_delete', args=[announcement.pk]))

		self.assertRedirects(response, reverse('admin_announcement_list'))
		self.assertFalse(Announcement.objects.filter(pk=announcement.pk).exists())

	def test_resident_announcement_surfaces_render_dialog_triggers_and_close_control(self):
		resident = User.objects.create_user(username='dialog-reader', password='test-password')
		self.client.force_login(resident)
		announcement = Announcement.objects.create(
			title='Read this update',
			content='A full story for the dialog.',
			is_published=True,
		)
		detail_url = reverse('announcement_detail', args=[announcement.pk])

		for page_url in (reverse('announcements'), reverse('resident_dashboard')):
			response = self.client.get(page_url)
			self.assertContains(response, 'id="resident-announcement-dialog"')
			self.assertContains(response, 'id="close-announcement-dialog"')
			self.assertContains(response, f'data-announcement-dialog href="{detail_url}"')

	def test_featured_announcement_appears_as_hero_and_is_removed_from_regular_list(self):
		resident = User.objects.create_user(username='featured-reader', password='test-password')
		self.client.force_login(resident)
		featured = Announcement.objects.create(
			title='Featured town event',
			content='Join the community this Saturday.',
			is_published=True,
			is_featured=True,
		)
		regular = Announcement.objects.create(title='Regular update', content='Read this update.', is_published=True)

		response = self.client.get(reverse('announcements'))

		self.assertContains(response, 'Featured town event')
		self.assertContains(response, reverse('announcement_detail', args=[featured.pk]))
		self.assertContains(response, 'Regular update')
		self.assertEqual(list(response.context['announcements']), [regular])

		response = self.client.get(reverse('resident_dashboard'))
		self.assertContains(response, 'Featured town event')
		self.assertContains(response, reverse('announcement_detail', args=[featured.pk]))

	def test_staff_featured_update_publishes_and_replaces_previous_feature(self):
		staff = User.objects.create_user(username='featured-staff', password='test-password', is_staff=True)
		old_featured = Announcement.objects.create(title='Old feature', content='Old', is_published=True, is_featured=True)
		self.client.force_login(staff)

		response = self.client.post(reverse('admin_announcement_list'), {
			'title': 'New feature',
			'announcement_type': 'event',
			'content': 'New featured event.',
			'is_featured': 'on',
		})

		self.assertRedirects(response, reverse('admin_announcement_list'))
		old_featured.refresh_from_db()
		new_featured = Announcement.objects.get(title='New feature')
		self.assertFalse(old_featured.is_featured)
		self.assertTrue(new_featured.is_featured)
		self.assertTrue(new_featured.is_published)

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
