#!/usr/bin/env fontforge
# -*- coding: utf-8 -*-

import fontforge
import psMat
import math
import unicodedata
import types
import math
import os

SOURCE_FILENAME    = "src/routed-gothic-stroke-source.sfd"
DIST_DIRECTORY     = "dist"
DIST_TTF_DIRECTORY = DIST_DIRECTORY + "/ttf"
DIST_SFD_DIRECTORY = DIST_DIRECTORY + "/sfd"
DIST_EOT_DIRECTORY = DIST_DIRECTORY + "/eot"
FONT_FILE_BASENAME = "routed-gothic"

CAP_HEIGHT = 736  # from bottom of lower stroke to top of upper stroke
STROKE_WIDTH = 96 # font is designed for this
AUTO_WIDTH = 144
AUTO_KERN = 144
KERN_CLASS_DIST = 8
SUPERSUBSCRIPT_SCALE = 0.75     # see any drafting literature
SUPERSUBSCRIPT_FRACTION_LINE = CAP_HEIGHT / 2

# from bottom of fraction line stroke to top    of upper stroke of denominator, and
# from top    of fraction line stroke to bottom of lower stroke of numerator
SUPERSUBSCRIPT_FRACTION_LINE_SEPARATION = 96

FRACTION_LINE_BEARING = 48      # left and right bearing
FRACTION_LINE_EXTRA_WIDTH = 96

CODEPOINT_FRACTION_LINE = 0xe000 # a private use area codepoint

CONDENSED_SCALE_X = 0.8         # arbitrary
CONDENSED_WIDE_SCALE_X = 1.25   # arbitrary
ITALIC_ANGLE_DEG = 22.5         # see any drafting literature

DIGIT_NAMES = [
    "ZERO", "ONE", "TWO", "THREE", "FOUR",
    "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"
]

SUPERSCRIPT_DIGIT_CODEPOINTS = [
    ord(unicodedata.lookup("SUPERSCRIPT " + d))
    for d in DIGIT_NAMES
]

SUBSCRIPT_DIGIT_CODEPOINTS = [
    ord(unicodedata.lookup("SUBSCRIPT " + d))
    for d in DIGIT_NAMES
]

VULGAR_FRACTIONS = [
    { 'codepoint': "VULGAR FRACTION ONE QUARTER"    , 'numerator': "SUPERSCRIPT ONE",   'denominator': "SUBSCRIPT FOUR"  },
    { 'codepoint': "VULGAR FRACTION ONE HALF"       , 'numerator': "SUPERSCRIPT ONE",   'denominator': "SUBSCRIPT TWO"   },
    { 'codepoint': "VULGAR FRACTION THREE QUARTERS" , 'numerator': "SUPERSCRIPT THREE", 'denominator': "SUBSCRIPT FOUR"  },
    { 'codepoint': "VULGAR FRACTION ONE THIRD"      , 'numerator': "SUPERSCRIPT ONE",   'denominator': "SUBSCRIPT THREE" },
    { 'codepoint': "VULGAR FRACTION TWO THIRDS"     , 'numerator': "SUPERSCRIPT TWO",   'denominator': "SUBSCRIPT THREE" },
    { 'codepoint': "VULGAR FRACTION ONE FIFTH"      , 'numerator': "SUPERSCRIPT ONE",   'denominator': "SUBSCRIPT FIVE"  },
    { 'codepoint': "VULGAR FRACTION TWO FIFTHS"     , 'numerator': "SUPERSCRIPT TWO",   'denominator': "SUBSCRIPT FIVE"  },
    { 'codepoint': "VULGAR FRACTION THREE FIFTHS"   , 'numerator': "SUPERSCRIPT THREE", 'denominator': "SUBSCRIPT FIVE"  },
    { 'codepoint': "VULGAR FRACTION FOUR FIFTHS"    , 'numerator': "SUPERSCRIPT FOUR",  'denominator': "SUBSCRIPT FIVE"  },
    { 'codepoint': "VULGAR FRACTION ONE SIXTH"      , 'numerator': "SUPERSCRIPT ONE",   'denominator': "SUBSCRIPT SIX"   },
    { 'codepoint': "VULGAR FRACTION FIVE SIXTHS"    , 'numerator': "SUPERSCRIPT FIVE",  'denominator': "SUBSCRIPT SIX"   },
    { 'codepoint': "VULGAR FRACTION ONE SEVENTH"    , 'numerator': 1, 'denominator': 7 },
    { 'codepoint': "VULGAR FRACTION ONE EIGHTH"     , 'numerator': 1, 'denominator': 8 },
    { 'codepoint': "VULGAR FRACTION THREE EIGHTHS"  , 'numerator': 3, 'denominator': 8 },
    { 'codepoint': "VULGAR FRACTION FIVE EIGHTHS"   , 'numerator': 5, 'denominator': 8 },
    { 'codepoint': "VULGAR FRACTION SEVEN EIGHTHS"  , 'numerator': 7, 'denominator': 8 },
]

SUPERSCRIPTS = [
    { 'codepoint': "SUPERSCRIPT ZERO",                 'of': u'0' },
    { 'codepoint': "SUPERSCRIPT ONE",                  'of': u'1' },
    { 'codepoint': "SUPERSCRIPT TWO",                  'of': u'2' },
    { 'codepoint': "SUPERSCRIPT THREE",                'of': u'3' },
    { 'codepoint': "SUPERSCRIPT FOUR",                 'of': u'4' },
    { 'codepoint': "SUPERSCRIPT FIVE",                 'of': u'5' },
    { 'codepoint': "SUPERSCRIPT SIX",                  'of': u'6' },
    { 'codepoint': "SUPERSCRIPT SEVEN",                'of': u'7' },
    { 'codepoint': "SUPERSCRIPT EIGHT",                'of': u'8' },
    { 'codepoint': "SUPERSCRIPT NINE",                 'of': u'9' },
    { 'codepoint': "SUPERSCRIPT PLUS SIGN",            'of': u'+' },
    { 'codepoint': "SUPERSCRIPT MINUS",                'of': "MINUS SIGN" },
    { 'codepoint': "SUPERSCRIPT EQUALS SIGN",          'of': u'=' },
    { 'codepoint': "SUPERSCRIPT LEFT PARENTHESIS",     'of': u'(' },
    { 'codepoint': "SUPERSCRIPT RIGHT PARENTHESIS",    'of': u')' },
    { 'codepoint': "SUPERSCRIPT LATIN SMALL LETTER N", 'of': u'n' },
    { 'codepoint': "SUPERSCRIPT LATIN SMALL LETTER I", 'of': u'i' },
]

SUBSCRIPTS = [
    { 'codepoint': "SUBSCRIPT ZERO",                   'of': u'0' },
    { 'codepoint': "SUBSCRIPT ONE",                    'of': u'1' },
    { 'codepoint': "SUBSCRIPT TWO",                    'of': u'2' },
    { 'codepoint': "SUBSCRIPT THREE",                  'of': u'3' },
    { 'codepoint': "SUBSCRIPT FOUR",                   'of': u'4' },
    { 'codepoint': "SUBSCRIPT FIVE",                   'of': u'5' },
    { 'codepoint': "SUBSCRIPT SIX",                    'of': u'6' },
    { 'codepoint': "SUBSCRIPT SEVEN",                  'of': u'7' },
    { 'codepoint': "SUBSCRIPT EIGHT",                  'of': u'8' },
    { 'codepoint': "SUBSCRIPT NINE",                   'of': u'9' },
    { 'codepoint': "SUBSCRIPT PLUS SIGN",              'of': u'+' },
    { 'codepoint': "SUBSCRIPT MINUS",                  'of': "MINUS SIGN" },
    { 'codepoint': "SUBSCRIPT EQUALS SIGN",            'of': u'=' },
    { 'codepoint': "SUBSCRIPT LEFT PARENTHESIS",       'of': u'(' },
    { 'codepoint': "SUBSCRIPT RIGHT PARENTHESIS",      'of': u')' },
    # { 'codepoint': "LATIN SUBSCRIPT SMALL LETTER N",   'of': u'n' },
]

# U+2090          ₐ     LATIN SUBSCRIPT SMALL LETTER A
# U+2091          ₑ     LATIN SUBSCRIPT SMALL LETTER E
# U+2092          ₒ     LATIN SUBSCRIPT SMALL LETTER O
# U+2093          ₓ     LATIN SUBSCRIPT SMALL LETTER X
# U+2094          ₔ     LATIN SUBSCRIPT SMALL LETTER SCHWA
# U+2095          ₕ     LATIN SUBSCRIPT SMALL LETTER H
# U+2096          ₖ     LATIN SUBSCRIPT SMALL LETTER K
# U+2097          ₗ     LATIN SUBSCRIPT SMALL LETTER L
# U+2098          ₘ     LATIN SUBSCRIPT SMALL LETTER M
# U+209A          ₚ     LATIN SUBSCRIPT SMALL LETTER P
# U+209B          ₛ     LATIN SUBSCRIPT SMALL LETTER S
# U+209C          ₜ     LATIN SUBSCRIPT SMALL LETTER T
# U+2A27          ⨧     PLUS SIGN WITH SUBSCRIPT TWO
# U+2C7C          ⱼ     LATIN SUBSCRIPT SMALL LETTER J

###############################################################################

def supersubscriptCodepoint(foo, superscript = True):
    if isinstance(foo, str) or isinstance(foo, unicode):
        if (len(foo) == 1):
            cp = ord(foo)
        else:
            char = unicodedata.lookup(foo)
            cp = ord(char)
    elif isinstance(foo, int):
        cp = foo
    else:
        raise TypeError("argument to codepoint must be a string or an integer")

    if (cp >= 48 and cp <= 57):
        if superscript:
            return SUPERSCRIPT_DIGIT_CODEPOINTS[cp - 48]
        else:
            return SUBSCRIPT_DIGIT_CODEPOINTS[cp - 48]
    elif (cp >= 0 and cp <= 9):
        if superscript:
            return SUPERSCRIPT_DIGIT_CODEPOINTS[cp]
        else:
            return SUBSCRIPT_DIGIT_CODEPOINTS[cp]
    else:
        return cp

def superscriptCodepoint(foo):
    return supersubscriptCodepoint(foo, True)

def subscriptCodepoint(foo):
    return supersubscriptCodepoint(foo, False)

def codepoint(foo):
    if isinstance(foo, str) or isinstance(foo, unicode):
        if (len(foo) == 1):
            return ord(foo)
        else:
            char = unicodedata.lookup(foo)
            return ord(char)
    elif isinstance(foo, int):
        if foo >= 0 and foo <= 9:
            return foo + 48
        else:
            return foo
    else:
        raise TypeError("argument to codepoint must be a string or an integer")

def intersect(a, b):
    return list(set(a) & set(b))

def anchorPointTransform(anchorPoint, transform):
    x = anchorPoint[2]
    y = anchorPoint[3]
    p = fontforge.point(x, y)
    p = p.transform(transform)
    return (anchorPoint[0],
            anchorPoint[1],
            p.x,
            p.y)

def italicAngleRad(deg):
    return deg * math.pi / 180

def italicSlantRatio(deg):
    return math.tan(italicAngleRad(deg))

def italicSkew(deg):
    return psMat.skew(italicAngleRad(deg))

def italicUnskew(deg):
    return psMat.inverse(italicSkew(deg))

def italicShiftLeft(deg):
    return psMat.translate(-CAP_HEIGHT / 2 * italicSlantRatio(deg), 0)

def italicShiftRight(deg):
    return psMat.inverse(italicShiftLeft(deg))

def italicTransform(deg):
    return psMat.compose(italicSkew(deg), italicShiftLeft(deg))

def italicUntransform(deg):
    return psMat.inverse(italicTransform(deg))

# for referenced characters in italic and half-italic fonts
def referenceTransform(ref, glyph, deg):
    thatglyphname = ref[0]
    thisglyphname = glyph.glyphname
    r = ref[1]

    columnA = "%s's reference to %s:" % (thisglyphname, thatglyphname)
    columnB = str(r)

    ri = psMat.inverse(r)

    result = psMat.identity()
    result = psMat.compose(result, italicShiftRight(deg))
    result = psMat.compose(result, italicUnskew(deg))
    result = psMat.compose(result, r)
    result = psMat.compose(result, italicSkew(deg))
    result = psMat.compose(result, italicShiftLeft(deg))

    return (ref[0], result)

def makeSuperscriptOrSubscript(font, sourceCodepoint, destCodepoint, superscript = True, placementMethod = 3):
    sourceCodepoint = codepoint(sourceCodepoint)
    destCodepoint   = codepoint(destCodepoint)

    # vcenter = amount to raise raw scaled number to make it vertically centered
    # vdiff = amount to raise or lower from vcenter

    if placementMethod == 1:
        vcenter = (1 - SUPERSUBSCRIPT_SCALE) * SUPERSUBSCRIPT_FRACTION_LINE
        vdiff = (SUPERSUBSCRIPT_SCALE * SUPERSUBSCRIPT_FRACTION_LINE
                 + (1 - SUPERSUBSCRIPT_SCALE / 2) * STROKE_WIDTH
                 + SUPERSUBSCRIPT_FRACTION_LINE_SEPARATION)
    if placementMethod == 2:
        vcenter = SUPERSUBSCRIPT_FRACTION_LINE * (1 - SUPERSUBSCRIPT_SCALE)
        vdiff = CAP_HEIGHT / 2
    if placementMethod == 3:
        vcenter = SUPERSUBSCRIPT_FRACTION_LINE * (1 - SUPERSUBSCRIPT_SCALE)
        vdiff = (1 - SUPERSUBSCRIPT_SCALE / 2) * (CAP_HEIGHT - STROKE_WIDTH)

    if superscript:
        vshift = vcenter + vdiff
    else:
        vshift = vcenter - vdiff

    vshiftXform = psMat.translate(0, vshift)

    font.selection.select(sourceCodepoint)
    font.copy()
    font.selection.select(destCodepoint)
    font.paste()

    destGlyph = font.createChar(destCodepoint)
    destGlyph.transform(psMat.scale(SUPERSUBSCRIPT_SCALE))
    destGlyph.transform(vshiftXform)

    additionalbearing = STROKE_WIDTH / 2 * (1 - SUPERSUBSCRIPT_SCALE)

    destGlyph.transform(psMat.translate(additionalbearing, 0))
    destGlyph.width = destGlyph.width + additionalbearing

    print "%s => %d" % (unicodedata.name(unichr(destCodepoint)), destCodepoint)

def makeSuperscript(font, sourceCodepoint, destCodepoint):
    makeSuperscriptOrSubscript(font, sourceCodepoint, destCodepoint, True)

def makeSubscript(font, sourceCodepoint, destCodepoint):
    makeSuperscriptOrSubscript(font, sourceCodepoint, destCodepoint, False)

def makeVulgarFraction(font, superCodepoint, subCodepoint, destCodepoint):
    superCodepoint = codepoint(superCodepoint)
    subCodepoint = codepoint(subCodepoint)
    destCodepoint = codepoint(destCodepoint)

    super = font.createChar(superCodepoint)
    sub   = font.createChar(subCodepoint)
    dest  = font.createChar(destCodepoint)
    dest.clear()

    fractionline = font[CODEPOINT_FRACTION_LINE]

    width = max([
        super.width,
        sub.width,
        fractionline.width
    ])

    dest.addReference(super.glyphname,        psMat.translate((width - super.width       ) / 2, 0))
    dest.addReference(sub.glyphname,          psMat.translate((width - sub.width         ) / 2, 0))
    dest.addReference(fractionline.glyphname, psMat.translate((width - fractionline.width) / 2, 0))
    dest.width = width

def generate(
        italicDeg = 0,
        italicName = "",
        condensedScale = 1,
        condensedName = "",
        autoHint = False,
        manualHints = False,
        autoInstr = False,
        autoKern = False,
        autoWidth = False,
        noRemoveOverlap = False,
        noAddExtrema = False,
        generateSuperAndSubscripts = True,
        generateSuperAndSubscriptsMethod = 3,
        fontName = "RoutedGothic",
        familyName = "Routed Gothic",
        weightName = "Regular",
        familyNameSuffix = "",
        fontFileBasename = FONT_FILE_BASENAME
):

    font = fontforge.open(SOURCE_FILENAME)

    if generateSuperAndSubscripts:

        for ss in SUPERSCRIPTS:
            sscp = codepoint(ss['codepoint'])
            ssof = codepoint(ss['of'])
            makeSuperscript(font, ssof, sscp)

        for ss in SUBSCRIPTS:
            sscp = codepoint(ss['codepoint'])
            ssof = codepoint(ss['of'])
            makeSubscript(font, ssof, sscp)

        superDigitGlyphs = [
            font[cp]
            for cp in SUPERSCRIPT_DIGIT_CODEPOINTS
        ]
        fractionlinewidth = max([g.width for g in superDigitGlyphs]) + FRACTION_LINE_EXTRA_WIDTH

        fractionline = font.createChar(CODEPOINT_FRACTION_LINE)
        pen = fractionline.glyphPen()
        pen.moveTo((STROKE_WIDTH / 2 + FRACTION_LINE_BEARING,
                    SUPERSUBSCRIPT_FRACTION_LINE))
        pen.lineTo((fractionlinewidth - STROKE_WIDTH / 2 - FRACTION_LINE_BEARING,
                    SUPERSUBSCRIPT_FRACTION_LINE))
        pen.endPath()           # leave path open
        pen = None              # finalize
        fractionline.width = fractionlinewidth

        for vf in VULGAR_FRACTIONS:
            numerator   = vf['numerator']
            denominator = vf['denominator']
            fraction    = vf['codepoint']

            numerator   = superscriptCodepoint(numerator)
            denominator = subscriptCodepoint(denominator)
            fraction    = codepoint(fraction)
            makeVulgarFraction(font, numerator, denominator, fraction)

    if autoKern:
        for lookupName in font.gpos_lookups:
            for subtableName in font.getLookupSubtables(lookupName):
                if font.isKerningClass(subtableName):
                    font.removeLookupSubtable(subtableName);

    # condense kerning pairs if needed

    if (condensedScale != 1) and not autoKern:
        for lookupName in font.gpos_lookups:
            for subtableName in font.getLookupSubtables(lookupName):
                if font.isKerningClass(subtableName):
                    kc = font.getKerningClass(subtableName)
                    offsets = kc[2]
                    newOffsets = [o * condensedScale for o in offsets]
                    font.alterKerningClass(subtableName, kc[0], kc[1], newOffsets)

    condensedTransform = psMat.scale(condensedScale, 1)

    if condensedScale != 1:
        font.selection.all()
        font.transform(condensedTransform)

    for glyph in font.glyphs():
        if manualHints:
            glyph.manualHints = True
        else:
            glyph.manualHints = False
        if italicDeg:
            width = glyph.width
            for name in glyph.layers:
                layer = glyph.layers[name]
                layer.transform(italicTransform(italicDeg))
                glyph.layers[name] = layer
                glyph.width = width
            glyph.anchorPoints = [
                anchorPointTransform(p, italicTransform(italicDeg))
                for p in glyph.anchorPoints
            ]

        glyph.round()
        glyph.stroke("circular", STROKE_WIDTH, "round", "round")
        if not noRemoveOverlap:
            glyph.removeOverlap()
        if not noAddExtrema:
            glyph.addExtrema()

    if autoWidth:
        font.autoWidth(AUTO_WIDTH, -1024, 1024)

    # call build() on glyphs that reference two glyphs if anchor
    # points would be used
    for glyph in font.glyphs():
        built = False
        if len(glyph.references) == 2:
            glyphname1 = glyph.references[0][0]
            glyphname2 = glyph.references[1][0]
            g1 = font[glyphname1]
            g2 = font[glyphname2]
            g1BaseAps = tuple([ap[0] for ap in g1.anchorPoints if ap[1] == "base"])
            g1MarkAps = tuple([ap[0] for ap in g1.anchorPoints if ap[1] == "mark"])
            g2BaseAps = tuple([ap[0] for ap in g2.anchorPoints if ap[1] == "base"])
            g2MarkAps = tuple([ap[0] for ap in g2.anchorPoints if ap[1] == "mark"])
            i1 = intersect(g1BaseAps, g2MarkAps)
            i2 = intersect(g2BaseAps, g1MarkAps)
            if len(i1) or len(i2):
                glyph.build()
                built = True
        if not built:
            if italicDeg:
                glyph.references = [
                    referenceTransform(r, glyph, italicDeg)
                    for r in glyph.references
                ]

    for glyph in font.glyphs():
        if autoHint:
            glyph.autoHint()
        if autoInstr:
            glyph.autoInstr()

    font.strokedfont = False

    if autoKern:
        font.selection.all()
        font.addLookup("autoKern", "gpos_pair", (), (("liga",(("latn",("dflt")),)),))
        font.addKerningClass("autoKern", "autoKern", 288, 16, False, True)

    font.fontname    = fontName
    font.familyname  = familyName
    font.fullname    = familyName
    font.weight      = weightName
    font.italicangle = italicDeg
    basename         = fontFileBasename

    familyNameSuffix = re.sub(r'^\s+', '', familyNameSuffix)
    familyNameSuffix = re.sub(r'\s+$', '', familyNameSuffix)

    if condensedScale != 1:
        # separate family names for condensed variants.  don't
        # remember why.
        font.familyname  = font.familyname + " " + condensedName.replace("-", " ")

        font.fontname    = font.fontname   +       condensedName.replace("-", "").replace(" ", "")
        font.fullname    = font.fullname   + " " + condensedName.replace("-", " ")

        basename         = basename        + "-" + condensedName.lower().replace(" ", "-")

    if italicDeg:
        font.fontname    = font.fontname   + "-" + italicName.replace(" ", "-")
        font.fullname    = font.fullname   + " " + italicName.replace("-", " ")

        basename         = basename        + "-" + italicName.lower().replace(" ", "-")

        font.italicangle = -ITALIC_ANGLE_DEG

    if familyNameSuffix != "":
        font.familyname  = font.familyname + " " + familyNameSuffix

    sfdFilename = DIST_SFD_DIRECTORY + "/" + basename + ".sfd"
    ttfFilename = DIST_TTF_DIRECTORY + "/" + basename + ".ttf"

    sfdDir = os.path.dirname(sfdFilename)
    ttfDir = os.path.dirname(ttfFilename)
    if not os.path.exists(sfdDir):
        print "makedirs " + sfdDir
        os.makedirs(sfdDir)
    if not os.path.exists(ttfDir):
        print "makedirs " + ttfDir
        os.makedirs(ttfDir)

    print "Saving " + sfdFilename + " ..."
    font.save(sfdFilename)
    print "Saving " + ttfFilename + " ..."
    font.generate(ttfFilename, flags=("no-hints", "omit-instructions"))

    font.close()

italicTypes = [
    { 'deg': 0,                    'name': '',            'appendToFontFamilyName': False },
    { 'deg': ITALIC_ANGLE_DEG / 2, 'name': 'Half Italic', 'appendToFontFamilyName': False },
    { 'deg': ITALIC_ANGLE_DEG,     'name': 'Italic',      'appendToFontFamilyName': False }
]

condensedTypes = [
    { 'scale': 1,                      'name': '',       'appendToFontFamilyName': False },
    { 'scale': CONDENSED_SCALE_X,      'name': 'Narrow', 'appendToFontFamilyName': False },
    { 'scale': CONDENSED_WIDE_SCALE_X, 'name': 'Wide',   'appendToFontFamilyName': False }
]

for italic in (italicTypes):
    for condensed in (condensedTypes):
        familyNameSuffix = ""
        if 'appendToFontFamilyName' in italic and italic['appendToFontFamilyName']:
            familyNameSuffix = familyNameSuffix + " " + italic['name']
        if 'appendToFontFamilyName' in condensed and condensed['appendToFontFamilyName']:
            familyNameSuffix = familyNameSuffix + " " + condensed['name']
        generate(
            italicDeg        = italic['deg'],
            italicName       = italic['name'],
            condensedScale   = condensed['scale'],
            condensedName    = condensed['name'],
            familyNameSuffix = familyNameSuffix
        )
