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

# from ShortSegmentPen import *

# needed to import universal checks
from fontbakery.profiles.universal import UNIVERSAL_PROFILE_CHECKS

# At this point we already have a importable profile
# It needs some checks though, to be useful.

# profile_imports can be used to mix other profiles
# into this profile. We are only using two profiles
# for this example, containing checks for the accordingly
# named tables

# also needed to import universal checks?
# profile_imports = ('fontbakery.profiles.universal',)

# seems to be needed to mark this as a profile?
profile = profile_factory(default_section=Section("Typotheque"))

# putting this at the top of the file
# can give a guick overview of checks below:
TYPOTHEQUE_CHECK_IDS = [
    'com.typotheque/check/short-segments--otf_ttf',
]

# the "Expected" check list can concatenate lists of checks in this profile and other imported ones
EXPECTED_CHECK_IDS = \
    TYPOTHEQUE_CHECK_IDS
    # UNIVERSAL_PROFILE_CHECKS + \

@check(id='com.typotheque/check/short-segments--otf_ttf')

def short_segments_otf_ttf(ttFont):
  """Report short segments in an OTF or TTF."""

  # TODO: print results in a more-readable way
  # TODO: decompose components and remove overlap before checking

  from fontTools.pens.basePen import BasePen
  from fontbakery.utils import ShortSegmentPen
  import pprint

  pp = pprint.PrettyPrinter(indent=4)

  results= {}

  glyphset = ttFont.getGlyphSet()

  # set for minimum segment length, in units out of 1000 UPM
  tooSmall = 2
  # derive minSize for segment
  minSize = ttFont['head'].unitsPerEm * (tooSmall / 1000)

  for glyphName in glyphset.keys():
    try:
      glyph = glyphset[glyphName]
      pen = ShortSegmentPen(glyph, minSize)
      glyph.draw(pen)
      result = pen.shortSegments
      if len(result) > 0:
        results[glyphName] = result

    # TODO: find why some glyphs have a TypeError: '_TTGlyphGlyf' object is not subscriptable (it is probably due to non-decomposed components)
    except TypeError:
      continue

  if len(results.keys()) > 0:
      yield WARN, f"Font has glyphs with segments shorter than {minSize}"
      for result in results.keys():

          #TODO: is this the best way to print a list of issues?
          yield INFO, f"{result}: {results[result]}"


# necessary to register checks that are imported from other profiles (e.g. universal checks)
profile.auto_register(globals())

# this must be at the end of the module,
# after all checks were added:
profile.test_expected_checks(EXPECTED_CHECK_IDS, exclusive=True)


