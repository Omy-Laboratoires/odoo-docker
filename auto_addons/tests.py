# Copyright 2015 Elico Corp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import unittest
from addons import *


class RepoTest(unittest.TestCase):

    def test_check_is_url(self):
        remote_url = 'connector'
        self.repo = Repo(remote_url)
        self.assertTrue(self.repo._is_url('https://github.com'))
        self.assertTrue(self.repo._is_url('http://github.com'))
        self.assertFalse(self.repo._is_url('ttps://github.com'))

    def test_parse_oca_repo(self):
        remote_url = 'connector'
        self.repo = Repo(remote_url)
        self.repo._parse_org_repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.folder, 'connector')

    def test_parse_organization_and_repo(self):
        remote_url = 'OCA/connector'
        self.repo = Repo(remote_url)
        self.repo._parse_org_repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.folder, 'connector')

    def test_parse_url(self):
        remote_url = 'https://github.com/OCA/connector'
        self.repo = Repo(remote_url)
        self.repo._parse_url(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.folder, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')

    def test_path(self):
        remote_url = 'connector'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.path, '%sconnector' % (EXTRA_ADDONS_PATH, ))

    def test_repo_oca_repo(self):
        remote_url = 'connector'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'connector')
        self.assertEqual(self.repo.branch, None)
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, '%sconnector' % (EXTRA_ADDONS_PATH, ))

    def test_repo_organization_and_repo(self):
        remote_url = 'OCA/connector'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'connector')
        self.assertEqual(self.repo.branch, None)
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, f'{EXTRA_ADDONS_PATH}connector')

    def test_repo_url(self):
        remote_url = 'https://github.com/OCA/connector'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'connector')
        self.assertEqual(self.repo.branch, None)
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, f'{EXTRA_ADDONS_PATH}connector')

    def test_repo_oca_repo_and_branch(self):
        remote_url = 'connector 8.0'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'connector')
        self.assertEqual(self.repo.branch, '8.0')
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, f'{EXTRA_ADDONS_PATH}connector')

    def test_repo_organization_and_repo_and_branch(self):
        remote_url = 'OCA/connector 8.0'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'connector')
        self.assertEqual(self.repo.branch, '8.0')
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, f'{EXTRA_ADDONS_PATH}connector')

    def test_repo_url_and_branch(self):
        remote_url = 'https://github.com/OCA/connector 8.0'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'connector')
        self.assertEqual(self.repo.branch, '8.0')
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, f'{EXTRA_ADDONS_PATH}connector')

    def test_repo_rename_and_url(self):
        remote_url = 'connector_rename https://github.com/OCA/connector'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'connector_rename')
        self.assertEqual(self.repo.branch, None)
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, f'{EXTRA_ADDONS_PATH}connector_rename')

    def test_repo_rename_and_url_and_branch(self):
        remote_url = 'connector_rename https://github.com/OCA/connector 8.0'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'connector_rename')
        self.assertEqual(self.repo.branch, '8.0')
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'connector')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, f'{EXTRA_ADDONS_PATH}connector_rename')

    def test_repo_rename_and_url_and_branch_new(self):
        remote_url = 'account-financial-reporting https://github.com/OCA/account-financial-reporting 8.0'
        self.repo = Repo(remote_url)
        self.assertEqual(self.repo.remote_url, remote_url)
        self.assertEqual(self.repo.folder, 'account-financial-reporting')
        self.assertEqual(self.repo.branch, '8.0')
        self.assertEqual(self.repo.organization, DEFAULT_ORGANIZATION)
        self.assertEqual(self.repo.repository, 'account-financial-reporting')
        self.assertEqual(self.repo.netloc, 'github.com')
        self.assertEqual(self.repo.path, f'{EXTRA_ADDONS_PATH}account-financial-reporting')

    def test_download_cmd(self):
        repo = Repo('Elico-Corp/odoo')
        self.assertEqual(
            'git clone https://github.com/Elico-Corp/odoo.git /opt/odoo/additional_addons/odoo',
            repo.download_cmd)

    def test_download_cmd_with_branch(self):
        repo = Repo('Elico-Corp/odoo 8.0')
        self.assertEqual(
            'git clone -b 8.0 https://github.com/Elico-Corp/odoo.git /opt/odoo/additional_addons/odoo',
            repo.download_cmd
        )


if __name__ == '__main__':
    unittest.main()
