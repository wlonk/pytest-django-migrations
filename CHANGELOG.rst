=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

v0.4.2
------

Changed
~~~~~~~

* (Hopefully) actually fix dependencies.

v0.4.1
------

Changed
~~~~~~~

* (Hopefully) fix dependencies.

v0.4.0
------

Changed
~~~~~~~

* Change API to be more Pytest-y.

v0.3.0
------

Changed
~~~~~~~

* Update versions and package metadata

v0.2.1
------

Changed
~~~~~~~

* Fix the Readme.

v0.2.0
------

Changed
~~~~~~~

* Complete API redesign: now there's a utility you can call that will
  migrate the database back and forth to specified states, returning the
  ``apps`` object to use to extract pseudo-models. Also a decorator that
  you can wrap the whole thing with to handle cleanup.

v0.1.0
------

Added
~~~~~

* Initial API design, with a decorator that sets up the database state,
  and returns a decorator that you then apply to tests after the
  migration.
