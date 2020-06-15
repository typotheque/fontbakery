# ------------------------------------------
# WIP Profile
# CURRENTLY IN AN EARLY EXPERIMENTATION PHASE
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

# At this point we already have a importable profile
# It needs some checks though, to be useful.

# profile_imports can be used to mix other profiles
# into this profile. We are only using two profiles
# for this example, containing checks for the accordingly
# named tables

# -------------------------------------------------------

# profile_imports = [
#     ['fontbakery.profiles', ['universal']]
# ]

# -------------------------------------------------------

# putting this at the top of the file
# can give a guick overview:
expected_check_ids = (
    'com.typotheque/examples/hello',
    'com.typotheque/examples/ttf_has_glyphs'
)

# Now we picked some checks from other profiles, but
# what about defining checks ourselves.


# We use `check` as a decorator to wrap an ordinary python
# function into an instance of FontBakeryCheck to prepare
# and mark it as a check.
# A check id is mandatory and must be globally and timely
# unique. See "Naming Things: check-ids" below.
@check(id='com.typotheque/examples/hello')
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




# conditions are used for the dependency injection as arguments
# and to decide if a check will be skipped
@condition
# ttFont is a condition built into FontProfile
# it returns an instance of fontTools.TTLib.TTFont
def is_ttf(ttFont):
   return 'glyf' in ttFont
   
@check(
    id='com.typotheque/examples/ttf_has_glyphs',
    # this check will be skipped if the font is not a ttf
    conditions=["is_ttf"]
)
# this also runs once per font in fonts, but its called with
# the ttFont instance
def has_ttf_glyphs(ttFont):
  """ It's bad when there are no glyphs in the TTF."""
  # savely use the "glyf" table, because of conditions="is_ttf"
  # we know it's available
  if not len(ttFont['glyf'].glyphs):
    return FAIL, "There are no glyphs in this TTF."
  return PASS, "Some gLyphs are in this TTF."


# this must be at the end of the module,
# after all checks were added:
profile.test_expected_checks(expected_check_ids, exclusive=True)
