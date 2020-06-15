# ------------------------------------------
# WIP Profile - basically a "hello world" file

# comments ending with ? are where Stephen Nixon is unsure of their absolute accuracy

# Following instructions & code, with slightly modifications, from
# https://font-bakery.readthedocs.io/en/stable/developer/writing-profiles.html
# ------------------------------------------

# We are going to define checks and conditons
from fontbakery.callable import check, condition
# All possible statuses a check can yield, in order of
# severity. The least severe being DEBUG. The most severe
# status emitted by a check is the end result of that check.
# DEBUG can't be an end result, the least severe status
# allowed as a check is PASS.
from fontbakery.checkrunner import (DEBUG, PASS,
               INFO, SKIP, WARN, FAIL, ERROR)
# Used to inform get_module_profile whether and
# how to create a profile. This
# example will create an instance of `FontsProfile`.
# The comment at the end of the line disables flake8
# and pylint to complain about unused imports.
from fontbakery.fonts_profile import profile_factory # NOQA pylint: disable=unused-import
from fontbakery.checkrunner import Section

# needed to import universal checks
from fontbakery.profiles.universal import UNIVERSAL_PROFILE_CHECKS

# At this point we already have a importable profile
# It needs some checks though, to be useful.

# profile_imports can be used to mix other profiles
# into this profile. We are only using two profiles
# for this example, containing checks for the accordingly
# named tables

# also needed to import universal checks?
profile_imports = ('fontbakery.profiles.universal',)

# seems to be needed to mark this as a profile?
profile = profile_factory(default_section=Section("Typotheque"))

# putting this at the top of the file
# can give a guick overview of checks below:
TYPOTHEQUE_CHECK_IDS = [
    'com.typotheque/check/hello',
]

# the "Expected" check list can concatenate lists of checks in this profile and other imported ones
EXPECTED_CHECK_IDS = \
    UNIVERSAL_PROFILE_CHECKS + \
    TYPOTHEQUE_CHECK_IDS

# Now we picked some checks from other profiles, but
# what about defining checks ourselves.


# We use `check` as a decorator to wrap an ordinary python
# function into an instance of FontBakeryCheck to prepare
# and mark it as a check.
# A check id is mandatory and must be globally and timely
# unique. See "Naming Things: check-ids" below.
@check(id='com.typotheque/check/hello')
# This check will run only once as it has no iterable
# arguments. Since it has no arguments at all and because
# checks should be idempotent (and this one is), there's
# not much sense in having it all. It will run once
# and always yield the same result.
def hello_world():
  """Simple "Hello World" example."""
  # The function name of a check is not very important
  # to create it, only to import it from another module
  # or to call it directly, However, a short line of
  # human readable description is mandatory, preferable
  # via the docstring of the check.
  
  # A status of a check can be `return`ed or `yield`ed
  # depending on the nature of the check, `return`
  # can only return just one status while `yield`
  # makes a generator out of it and it can produce
  # many statuses.
  # A status also always must be a tuple of (Status, Message)
  # For `Message` a string is OK, but for unit testing
  # it turned out that an instance of `fontbakery.message.Message`
  # can be very useful. It can additionally provide
  # a status code, better suited to figure out the exact
  # check result.
  yield PASS, 'Hello World'


# necessary to register checks that are imported from other profiles (e.g. universal checks)
profile.auto_register(globals())

# this must be at the end of the module,
# after all checks were added:
profile.test_expected_checks(EXPECTED_CHECK_IDS, exclusive=True)
