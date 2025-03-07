===========
giturlparse
===========

Parse & rewrite git urls (supports GitHub, Bitbucket, FriendCode, Assembla, Gitlab ...)

This is a fork of giturlparse.py with updated parsers.

Original project can be found at https://github.com/FriendCode/giturlparse.py

************
Installing
************

::

    pip install giturlparse

******************
Examples
******************

Exposed attributes
==================

* ``platform``: platform codename
* ``host``: server hostname
* ``resource``: same as ``host``
* ``port``: URL port (only if explicitly defined in URL)
* ``protocol``: URL protocol (git, ssh, http/https)
* ``protocols``: list of protocols explicitly defined in URL
* ``user``: repository user
* ``owner``: repository owner (user or organization)
* ``repo``: repository name
* ``name``: same as ``repo``
* ``groups``: list of groups - gitlab only
* ``path``: path to file or directory (includes the branch name) - gitlab / github only
* ``path_raw``: raw path starting from the repo name (might include platform keyword) - gitlab / github only
* ``branch``: branch name (when parseable) - gitlab / github only

Parse
==================

::

    from giturlparse import parse

    p = parse('git@bitbucket.org:AaronO/some-repo.git')

    p.host, p.owner, p.repo

    # => ('bitbucket.org', 'AaronO', 'some-repo')


Rewrite
==================

::

    from giturlparse import parse

    url = 'git@github.com:Org/Private-repo.git'

    p = parse(url)

    p.url2ssh, p.url2https, p.url2git, p.url2http
    # => ('git@github.com:Org/Private-repo.git', 'https://github.com/Org/Private-repo.git', 'git://github.com/Org/Private-repo.git', None)

URLS
==================

Alternative URLs for same repo::

    from giturlparse import parse

    url = 'git@github.com:Org/Private-repo.git'

    parse(url).urls
    # => {
    #     'ssh': 'git@github.com:Org/Private-repo.git',
    #     'https': 'https://github.com/Org/Private-repo.git',
    #     'git': 'git://github.com/Org/Private-repo.git'
    # }

Validate
==================

::

    from giturlparse import parse, validate

    url = 'git@github.com:Org/Private-repo.git'

    parse(url).valid
    # => True

    # Or

    validate(url)
    # => True

Tests
==================

::

    python -munittest

License
==================

Apache v2 (Check out LICENSE file)
