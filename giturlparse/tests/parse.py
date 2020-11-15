# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from giturlparse import parse

# Test data
VALID_PARSE_URLS = (
    # Valid SSH, HTTPS, GIT
    ('SSH', ('git@github.com:Org/Repo.git', {
        'host': 'github.com',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'ssh',
        'github': True,
        'bitbucket': False,
        'assembla': False
    })),
    ('HTTPS', ('https://github.com/Org/Repo.git', {
        'host': 'github.com',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'https',
        'github': True,
        'bitbucket': False,
        'assembla': False
    })),
    ('HTTPS', ('https://github.com/foo-bar/xpwn', {
        'host': 'github.com',
        'user': 'git',
        'owner': 'foo-bar',
        'repo': 'xpwn',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'https',
        'github': True,
    })),
    ('GIT', ('git://github.com/Org/Repo.git', {
        'host': 'github.com',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'git',
        'github': True,
    })),
    ('GIT', ('git://github.com/foo-bar/xpwn', {
        'host': 'github.com',
        'user': 'git',
        'owner': 'foo-bar',
        'repo': 'xpwn',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'git',
        'github': True,
    })),

    # BitBucket
    ('SSH', ('git@bitbucket.org:Org/Repo.git', {
        'host': 'bitbucket.org',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'ssh',
        'platform': 'bitbucket'
    })),

    # Gitlab
    ('SSH', ('git@host.org:9999/Org/Repo.git', {
        'host': 'host.org',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'ssh',
        'platform': 'gitlab'
    })),
    ('SSH', ('git@host.org:9999/Org-hyphen/Repo.git', {
        'host': 'host.org',
        'user': 'git',
        'owner': 'Org-hyphen',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'ssh',
        'platform': 'gitlab'
    })),
    ('SSH', ('git@host.org:Org/Repo.git', {
        'host': 'host.org',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'ssh',
        'platform': 'gitlab'
    })),
    ('SSH', ('ssh://git@host.org:9999/Org/Repo.git', {
        'host': 'host.org',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'ssh',
        'platform': 'gitlab'
    })),
    ('HTTPS', ('https://host.org/Org/Repo.git', {
        'host': 'host.org',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': [],
        'path': '',
        'pathname': '',
        'branch': '',
        'protocol': 'https',
        'platform': 'gitlab'
    })),
    ('HTTPS', ('https://github.com/nephila/giturlparse/blob/master/giturlparse/github.py', {
        'host': 'github.com',
        'user': 'git',
        'owner': 'nephila',
        'repo': 'giturlparse',
        'groups': [],
        'path': 'master/giturlparse/github.py',
        'pathname': '/blob/master/giturlparse/github.py',
        'branch': '',
        'protocol': 'https',
        'platform': 'github'
    })),
    ('HTTPS', ('https://github.com/nephila/giturlparse/tree/feature/py37', {
        'host': 'github.com',
        'user': 'git',
        'owner': 'nephila',
        'repo': 'giturlparse',
        'groups': [],
        'path': '',
        'pathname': '/tree/feature/py37',
        'branch': 'feature/py37',
        'protocol': 'https',
        'platform': 'github'
    })),
    ('HTTPS', ('https://gitlab.com/nephila/giturlparse/blob/master/giturlparse/github.py', {
        'host': 'gitlab.com',
        'user': 'git',
        'owner': 'nephila',
        'repo': 'giturlparse',
        'groups': [],
        'path': 'master/giturlparse/github.py',
        'pathname': '/blob/master/giturlparse/github.py',
        'branch': '',
        'protocol': 'https',
        'platform': 'gitlab'
    })),
    ('HTTPS',
     ('https://gitlab.com/nephila/group2/third-group/giturlparse/blob/master/'
      'giturlparse/platforms/github.py', {
        'host': 'gitlab.com',
        'user': 'git',
        'owner': 'nephila',
        'repo': 'giturlparse',
        'groups': ['group2', 'third-group'],
        'path': 'master/giturlparse/platforms/github.py',
        'pathname': '/blob/master/giturlparse/platforms/github.py',
        'branch': '',
        'protocol': 'https',
        'platform': 'gitlab'
      })),
    ('SSH', ('git@host.org:9999/Org/Group/subGroup/Repo.git/blob/master/giturlparse/github.py', {
        'host': 'host.org',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': ['Group', 'subGroup'],
        'path': 'master/giturlparse/github.py',
        'pathname': '/blob/master/giturlparse/github.py',
        'branch': '',
        'protocol': 'ssh',
        'platform': 'gitlab'
    })),
    ('GIT', ('git://host.org:9999/Org/Group/subGroup/Repo.git/blob/master/giturlparse/github.py', {
        'host': 'host.org',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': ['Group', 'subGroup'],
        'path': 'master/giturlparse/github.py',
        'pathname': '/blob/master/giturlparse/github.py',
        'branch': '',
        'protocol': 'git',
        'platform': 'gitlab'
    })),
    ('GIT', ('git://host.org:9999/Org/Group/subGroup/Repo.git/-/tree/feature/custom-branch', {
        'host': 'host.org',
        'user': 'git',
        'owner': 'Org',
        'repo': 'Repo',
        'groups': ['Group', 'subGroup'],
        'path': '',
        'pathname': '/-/tree/feature/custom-branch',
        'branch': 'feature/custom-branch',
        'protocol': 'git',
        'platform': 'gitlab'
    })),
)

INVALID_PARSE_URLS = (
    ('SSH No Username', '@github.com:Org/Repo.git'),
    ('SSH No Repo', 'git@github.com:Org'),
    ('HTTPS No Repo', 'https://github.com/Org'),
    ('GIT No Repo', 'git://github.com/Org'),
)


# Here's our "unit tests".
class UrlParseTestCase(unittest.TestCase):
    def _test_valid(self, url, expected):
        p = parse(url)
        self.assertTrue(p.valid, "%s is not a valid URL" % url)
        for k, v in expected.items():
            attr_v = getattr(p, k)
            self.assertEqual(
                attr_v, v, "[%s] Property '%s' should be '%s' but is '%s'" % (
                    url, k, v, attr_v
                )
            )

    def testValidUrls(self):
        for test_type, data in VALID_PARSE_URLS:
            self._test_valid(*data)

    def _test_invalid(self, url):
        p = parse(url)
        self.assertFalse(p.valid)

    def testInvalidUrls(self):
        for problem, url in INVALID_PARSE_URLS:
            self._test_invalid(url)


# Test Suite
suite = unittest.TestLoader().loadTestsFromTestCase(UrlParseTestCase)
