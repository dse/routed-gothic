#!/usr/bin/env fontforge
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(sys.argv[0]) + '/../lib')
sys.path.append(os.environ['HOME'] + '/git/dse.d/fontforge-utilities/lib')

import ffutils
import fontforge
import psMat
import math
import unicodedata
import types
import math
import re

wrapper  = ffutils.FontWrapper()
fontData = ffutils.getFontData()

ITALIC_ANGLE_DEG       = ffutils.getCoalesce(fontData, 'italicAngleDeg')
GENERATE_HALF_ITALIC   = ffutils.getCoalesce(fontData, 'generateHalfItalic', False)
GENERATE_ITALIC        = ffutils.getCoalesce(fontData, 'generateItalic', False)
CONDENSED_SCALE_X      = ffutils.getCoalesce(fontData, 'condensedScaleX')
CONDENSED_WIDE_SCALE_X = ffutils.getCoalesce(fontData, 'condensedWideScaleX')

fontSlants = []
fontSlants.append({ 'deg': 0, 'name': '' })
if ITALIC_ANGLE_DEG != None:
    if GENERATE_HALF_ITALIC:
        fontSlants.append({ 'deg': ITALIC_ANGLE_DEG / 2, 'name': 'Half Italic', 'familyNameSuffix': 'Half Italic' })
    if GENERATE_ITALIC:
        fontSlants.append({ 'deg': ITALIC_ANGLE_DEG, 'name': 'Italic' })

# separate family names for condensed variants.  don't
# remember why.
fontStretches = []
fontStretches.append({ 'scale': 1, 'name': '' })
if CONDENSED_SCALE_X != None:
    fontStretches.append({ 'scale': CONDENSED_SCALE_X, 'name': 'Narrow', 'familyNameSuffix': 'Narrow' })
if CONDENSED_WIDE_SCALE_X != None:
    fontStretches.append({ 'scale': CONDENSED_WIDE_SCALE_X, 'name': 'Wide', 'familyNameSuffix': 'Wide' })

print("this is generate-fonts.py")
for fontSlant in (fontSlants):
    for fontStretch in (fontStretches):
        familyNameSuffix = ""
        if 'familyNameSuffix' in fontStretch:
            familyNameSuffix = familyNameSuffix + " " + fontStretch['familyNameSuffix']
        if 'familyNameSuffix' in fontSlant:
            familyNameSuffix = familyNameSuffix + " " + fontSlant['familyNameSuffix']
        wrapper.generate(
            fontName         = "RoutedGothic",
            familyName       = "Routed Gothic",
            weightName       = "Regular",
            italicDeg        = fontSlant['deg'],
            italicName       = fontSlant['name'],
            condensedScale   = fontStretch['scale'],
            condensedName    = fontStretch['name'],
            familyNameSuffix = familyNameSuffix,
        )
