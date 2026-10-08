"""#02 Page/Chapter API のテスト。

テンプレート版（`test_legacy.py`）と同じ挙動を API 経由でも満たすことを確認する。
"""
import datetime
import io
import json
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from wisme.models import Chapter, Page, SearchedWord
from wisme.tests.test_legacy import make_page, make_verified_user

LIST_URL = reverse('api:page-list')


def detail_url(page_id):
    return reverse('api:page-detail', args=[page_id])


def picture_url(page_id):
    return reverse('api:page-picture', args=[page_id])


def post_json(client, url, payload):
    return client.post(url, data=json.dumps(payload), content_type='application/json')


def patch_json(client, url, payload):
    return client.patch(url, data=json.dumps(payload), content_type='application/json')


def make_png_bytes():
    """multipart アップロード用の最小 PNG を生成する。"""
    buf = io.BytesIO()
    Image.new('RGB', (1, 1), color='red').save(buf, format='PNG')
    buf.seek(0)
    buf.name = 'cover.png'
    return buf


# DoD: 一覧は自分のページのみ返す
class PageListAPITest(TestCase):
    def setUp(self):
        self.user1 = make_verified_user('api-list1@example.com', 'Testpass123!')
        self.user2 = make_verified_user('api-list2@example.com', 'Testpass123!')
        make_page(self.user1, title='user1のページ')
        make_page(self.user2, title='user2のページ')
        self.client.force_login(self.user1)

    def test_returns_only_own_pages(self):
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, 200)
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'user1のページ')

    def test_ordered_by_page_date_desc(self):
        # setUp のページは page_date が今日なので、前後に挟まる日付で並び順を見る
        Page.objects.create(
            owner=self.user1, title='古い', thoughts='',
            page_date=datetime.date(2020, 1, 1),
        )
        Page.objects.create(
            owner=self.user1, title='さらに古い', thoughts='',
            page_date=datetime.date(2010, 1, 1),
        )
        titles = [p['title'] for p in self.client.get(LIST_URL).json()['results']]
        self.assertEqual(titles, ['user1のページ', '古い', 'さらに古い'])

    def test_response_is_paginated(self):
        body = self.client.get(LIST_URL).json()
        self.assertIn('count', body)
        self.assertIn('results', body)


# DoD: 作成（chapters あり/なし）と order の再採番
class PageCreateAPITest(TestCase):
    def setUp(self):
        self.user = make_verified_user('api-create@example.com', 'Testpass123!')
        self.client.force_login(self.user)

    def test_create_with_chapters(self):
        response = post_json(self.client, LIST_URL, {
            'title': 'テスト本',
            'thoughts': '全体の感想',
            'page_date': '2026-04-19',
            'chapters': [
                {'title': '序章', 'content': '始まり'},
                {'title': '終章', 'content': '終わり'},
            ],
        })
        self.assertEqual(response.status_code, 201)
        page = Page.objects.get(owner=self.user, title='テスト本')
        chapters = list(page.chapters.all())
        self.assertEqual([c.order for c in chapters], [0, 1])
        self.assertEqual([c.title for c in chapters], ['序章', '終章'])

    def test_create_without_chapters(self):
        response = post_json(self.client, LIST_URL, {
            'title': '章なし本',
            'page_date': '2026-04-19',
        })
        self.assertEqual(response.status_code, 201)
        page = Page.objects.get(owner=self.user, title='章なし本')
        self.assertEqual(page.chapters.count(), 0)

    def test_owner_is_request_user(self):
        post_json(self.client, LIST_URL, {'title': 'owner確認', 'page_date': '2026-04-19'})
        self.assertEqual(Page.objects.get(title='owner確認').owner, self.user)

    def test_client_supplied_order_is_ignored(self):
        post_json(self.client, LIST_URL, {
            'title': 'order無視',
            'page_date': '2026-04-19',
            'chapters': [
                {'order': 99, 'title': 'A', 'content': ''},
                {'order': 5, 'title': 'B', 'content': ''},
            ],
        })
        page = Page.objects.get(title='order無視')
        self.assertEqual([c.order for c in page.chapters.all()], [0, 1])

    def test_title_is_required(self):
        response = post_json(self.client, LIST_URL, {'page_date': '2026-04-19'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.json())


# DoD: 作成時に未関連の SearchedWord が自動で紐付く
class UnlinkedWordAttachAPITest(TestCase):
    def setUp(self):
        self.user = make_verified_user('api-word@example.com', 'Testpass123!')
        self.other = make_verified_user('api-word-other@example.com', 'Testpass123!')
        self.client.force_login(self.user)

    def test_create_attaches_own_unlinked_words(self):
        word = SearchedWord.objects.create(owner=self.user, word='apple', meaning='りんご')
        post_json(self.client, LIST_URL, {'title': '紐付け確認', 'page_date': '2026-04-19'})
        word.refresh_from_db()
        self.assertEqual(word.note, Page.objects.get(title='紐付け確認'))

    def test_create_does_not_touch_other_users_words(self):
        other_word = SearchedWord.objects.create(owner=self.other, word='banana', meaning='バナナ')
        post_json(self.client, LIST_URL, {'title': '他人の単語', 'page_date': '2026-04-19'})
        other_word.refresh_from_db()
        self.assertIsNone(other_word.note)

    def test_already_linked_word_is_not_moved(self):
        existing = make_page(self.user, title='既存ページ')
        word = SearchedWord.objects.create(owner=self.user, word='cherry', meaning='さくらんぼ', note=existing)
        post_json(self.client, LIST_URL, {'title': '新ページ', 'page_date': '2026-04-19'})
        word.refresh_from_db()
        self.assertEqual(word.note, existing)

    def test_update_attaches_unlinked_words(self):
        page = make_page(self.user, title='更新対象')
        word = SearchedWord.objects.create(owner=self.user, word='durian', meaning='ドリアン')
        patch_json(self.client, detail_url(page.id), {'title': '更新後'})
        word.refresh_from_db()
        self.assertEqual(word.note, page)


# DoD: 詳細は chapters と words を埋め込む
class PageDetailAPITest(TestCase):
    def setUp(self):
        self.user = make_verified_user('api-detail@example.com', 'Testpass123!')
        self.client.force_login(self.user)
        self.page = make_page(self.user, title='詳細ページ')
        Chapter.objects.create(page=self.page, order=0, title='1章', content='a')
        SearchedWord.objects.create(owner=self.user, word='word1', meaning='意味1', note=self.page)

    def test_detail_contains_chapters_and_words(self):
        body = self.client.get(detail_url(self.page.id)).json()
        self.assertEqual(body['title'], '詳細ページ')
        self.assertEqual([c['title'] for c in body['chapters']], ['1章'])
        self.assertEqual([w['word'] for w in body['words']], ['word1'])

    def test_list_does_not_contain_words(self):
        results = self.client.get(LIST_URL).json()['results']
        self.assertNotIn('words', results[0])


# DoD: 更新（章の追加・削除・並び替え）
class PageUpdateAPITest(TestCase):
    def setUp(self):
        self.user = make_verified_user('api-update@example.com', 'Testpass123!')
        self.client.force_login(self.user)
        self.page = make_page(self.user, title='旧タイトル')
        self.c1 = Chapter.objects.create(page=self.page, order=0, title='旧1章', content='旧1')
        self.c2 = Chapter.objects.create(page=self.page, order=1, title='旧2章', content='旧2')

    def test_patch_title_only_keeps_chapters(self):
        response = patch_json(self.client, detail_url(self.page.id), {'title': '新タイトル'})
        self.assertEqual(response.status_code, 200)
        self.page.refresh_from_db()
        self.assertEqual(self.page.title, '新タイトル')
        self.assertEqual(self.page.chapters.count(), 2)

    def test_patch_chapters_replaces_all(self):
        response = patch_json(self.client, detail_url(self.page.id), {
            'chapters': [
                {'title': '更新1章', 'content': '更新1'},
                {'title': '新3章', 'content': '新3'},
            ],
        })
        self.assertEqual(response.status_code, 200)
        chapters = list(self.page.chapters.all())
        self.assertEqual([c.title for c in chapters], ['更新1章', '新3章'])
        self.assertEqual([c.order for c in chapters], [0, 1])

    def test_patch_reorders_chapters(self):
        patch_json(self.client, detail_url(self.page.id), {
            'chapters': [
                {'title': '旧2章', 'content': '旧2'},
                {'title': '旧1章', 'content': '旧1'},
            ],
        })
        self.assertEqual([c.title for c in self.page.chapters.all()], ['旧2章', '旧1章'])

    def test_patch_empty_chapters_deletes_all(self):
        patch_json(self.client, detail_url(self.page.id), {'chapters': []})
        self.assertEqual(self.page.chapters.count(), 0)

    def test_put_updates_page(self):
        response = self.client.put(
            detail_url(self.page.id),
            data=json.dumps({'title': 'PUT後', 'page_date': '2026-04-19'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.page.refresh_from_db()
        self.assertEqual(self.page.title, 'PUT後')


# DoD: 削除
class PageDeleteAPITest(TestCase):
    def setUp(self):
        self.user = make_verified_user('api-delete@example.com', 'Testpass123!')
        self.client.force_login(self.user)
        self.page = make_page(self.user, title='削除対象')
        Chapter.objects.create(page=self.page, order=0, title='章', content='')

    def test_delete_returns_204_and_removes_page(self):
        response = self.client.delete(detail_url(self.page.id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Page.objects.filter(id=self.page.id).exists())

    def test_delete_cascades_to_chapters(self):
        self.client.delete(detail_url(self.page.id))
        self.assertEqual(Chapter.objects.count(), 0)


# DoD: 他人のページには一切アクセスできない／未認証は 403
class PagePermissionAPITest(TestCase):
    def setUp(self):
        self.user1 = make_verified_user('api-perm1@example.com', 'Testpass123!')
        self.user2 = make_verified_user('api-perm2@example.com', 'Testpass123!')
        self.user2_page = make_page(self.user2, title='user2のページ')

    def test_unauthenticated_list_returns_403(self):
        self.assertEqual(self.client.get(LIST_URL).status_code, 403)

    def test_unauthenticated_create_returns_403(self):
        response = post_json(self.client, LIST_URL, {'title': 'x', 'page_date': '2026-04-19'})
        self.assertEqual(response.status_code, 403)

    def test_retrieve_other_users_page_returns_404(self):
        # get_queryset を owner で絞っているため、存在を漏らさず 404 になる
        self.client.force_login(self.user1)
        response = self.client.get(detail_url(self.user2_page.id))
        self.assertEqual(response.status_code, 404)

    def test_patch_other_users_page_returns_404(self):
        self.client.force_login(self.user1)
        response = patch_json(self.client, detail_url(self.user2_page.id), {'title': '乗っ取り'})
        self.assertEqual(response.status_code, 404)
        self.user2_page.refresh_from_db()
        self.assertEqual(self.user2_page.title, 'user2のページ')

    def test_delete_other_users_page_returns_404(self):
        self.client.force_login(self.user1)
        response = self.client.delete(detail_url(self.user2_page.id))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Page.objects.filter(id=self.user2_page.id).exists())

    def test_cannot_override_owner_on_create(self):
        self.client.force_login(self.user1)
        post_json(self.client, LIST_URL, {
            'title': 'owner偽装',
            'page_date': '2026-04-19',
            'owner': self.user2.id,
        })
        self.assertEqual(Page.objects.get(title='owner偽装').owner, self.user1)


# DoD: 表紙画像はページ本体と分けて picture エンドポイントに送る
@override_settings(
    STORAGES={
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    },
    MEDIA_ROOT=tempfile.mkdtemp(),
)
class PagePictureUploadAPITest(TestCase):
    """本番は Cloudinary だが、テストではローカルの FileSystemStorage に差し替える。"""

    def setUp(self):
        self.user = make_verified_user('api-upload@example.com', 'Testpass123!')
        self.other = make_verified_user('api-upload-other@example.com', 'Testpass123!')
        self.client.force_login(self.user)

    def upload(self, page_id):
        # Django テストクライアントの put は multipart を自動生成しないため明示的に組み立てる
        from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
        return self.client.put(
            picture_url(page_id),
            data=encode_multipart(BOUNDARY, {'picture': make_png_bytes()}),
            content_type=MULTIPART_CONTENT,
        )

    def test_create_with_json_then_upload_picture(self):
        response = post_json(self.client, LIST_URL, {
            'title': '画像と章',
            'page_date': '2026-04-19',
            'chapters': [
                {'title': '序章', 'content': '始まり'},
                {'title': '終章', 'content': '終わり'},
            ],
        })
        self.assertEqual(response.status_code, 201)
        page_id = response.json()['id']

        response = self.upload(page_id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['picture'])
        page = Page.objects.get(id=page_id)
        self.assertTrue(page.picture)
        self.assertEqual([c.title for c in page.chapters.all()], ['序章', '終章'])

    def test_replace_picture_deletes_old_file(self):
        page = make_page(self.user, title='差し替え')
        self.upload(page.id)
        page.refresh_from_db()
        old_name = page.picture.name

        self.upload(page.id)
        page.refresh_from_db()
        self.assertNotEqual(page.picture.name, old_name)
        self.assertFalse(page.picture.storage.exists(old_name))

    def test_delete_picture(self):
        page = make_page(self.user, title='画像削除')
        self.upload(page.id)
        page.refresh_from_db()
        name = page.picture.name

        response = self.client.delete(picture_url(page.id))
        self.assertEqual(response.status_code, 204)
        page.refresh_from_db()
        self.assertFalse(page.picture)
        self.assertFalse(page.picture.storage.exists(name))

    def test_upload_without_file_returns_400(self):
        page = make_page(self.user, title='ファイルなし')
        from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
        response = self.client.put(
            picture_url(page.id),
            data=encode_multipart(BOUNDARY, {}),
            content_type=MULTIPART_CONTENT,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('picture', response.json())

    def test_upload_to_other_users_page_returns_404(self):
        other_page = make_page(self.other, title='他人のページ')
        self.assertEqual(self.upload(other_page.id).status_code, 404)
        other_page.refresh_from_db()
        self.assertFalse(other_page.picture)

    def test_multipart_to_page_list_returns_415(self):
        response = self.client.post(LIST_URL, {
            'title': '画像あり',
            'page_date': '2026-04-19',
            'picture': make_png_bytes(),
        })
        self.assertEqual(response.status_code, 415)

    def test_picture_in_json_is_ignored(self):
        response = post_json(self.client, LIST_URL, {
            'title': 'picture無視',
            'page_date': '2026-04-19',
            'picture': 'wisme/picture/fake.png',
        })
        self.assertEqual(response.status_code, 201)
        self.assertFalse(Page.objects.get(title='picture無視').picture)
