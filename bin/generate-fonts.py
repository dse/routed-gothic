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

DIGIT_NAMES = ["ZERO", "ONE", "TWO", "THREE", "FOUR",
               "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]

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

def supersubscript_codepoint(foo, superscript = True):
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

def superscript_codepoint(foo):
    return supersubscript_codepoint(foo, True)

def subscript_codepoint(foo):
    return supersubscript_codepoint(foo, False)

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

def anchor_point_transform(anchor_point, transform):
    x = anchor_point[2]
    y = anchor_point[3]
    p = fontforge.point(x, y)
    p = p.transform(transform)
    return (anchor_point[0],
            anchor_point[1],
            p.x,
            p.y)

def italic_angle_rad(deg):
    return deg * math.pi / 180

def italic_slant_ratio(deg):
    return math.tan(italic_angle_rad(deg))

def italic_skew(deg):
    return psMat.skew(italic_angle_rad(deg))

def italic_unskew(deg):
    return psMat.inverse(italic_skew(deg))

def italic_shift_left(deg):
    return psMat.translate(-CAP_HEIGHT / 2 * italic_slant_ratio(deg), 0)

def italic_shift_right(deg):
    return psMat.inverse(italic_shift_left(deg))

def italic_transform(deg):
    return psMat.compose(italic_skew(deg), italic_shift_left(deg))

def italic_untransform(deg):
    return psMat.inverse(italic_transform(deg))

# for referenced characters in italic and half-italic fonts
def reference_transform(ref, glyph, deg):
    thatglyphname = ref[0]
    thisglyphname = glyph.glyphname
    r = ref[1]

    column_a = "%s's reference to %s:" % (thisglyphname, thatglyphname)
    column_b = str(r)

    ri = psMat.inverse(r)

    result = psMat.identity()
    result = psMat.compose(result, italic_shift_right(deg))
    result = psMat.compose(result, italic_unskew(deg))
    result = psMat.compose(result, r)
    result = psMat.compose(result, italic_skew(deg))
    result = psMat.compose(result, italic_shift_left(deg))

    return (ref[0], result)

def make_superscript_or_subscript(font, source_codepoint, dest_codepoint, superscript = True, placement_method = 3):
    source_codepoint = codepoint(source_codepoint)
    dest_codepoint   = codepoint(dest_codepoint)

    # vcenter = amount to raise raw scaled number to make it vertically centered
    # vdiff = amount to raise or lower from vcenter

    if placement_method == 1:
        vcenter = (1 - SUPERSUBSCRIPT_SCALE) * SUPERSUBSCRIPT_FRACTION_LINE
        vdiff = SUPERSUBSCRIPT_SCALE * SUPERSUBSCRIPT_FRACTION_LINE + (1 - SUPERSUBSCRIPT_SCALE / 2) * STROKE_WIDTH + SUPERSUBSCRIPT_FRACTION_LINE_SEPARATION
    if placement_method == 2:
        vcenter = SUPERSUBSCRIPT_FRACTION_LINE * (1 - SUPERSUBSCRIPT_SCALE)
        vdiff = CAP_HEIGHT / 2
    if placement_method == 3:
        vcenter = SUPERSUBSCRIPT_FRACTION_LINE * (1 - SUPERSUBSCRIPT_SCALE)
        vdiff = (1 - SUPERSUBSCRIPT_SCALE / 2) * (CAP_HEIGHT - STROKE_WIDTH)

    if superscript:
        vshift = vcenter + vdiff
    else:
        vshift = vcenter - vdiff

    vshift_xform = psMat.translate(0, vshift)

    font.selection.select(source_codepoint)
    font.copy()
    font.selection.select(dest_codepoint)
    font.paste()

    dest_glyph = font.createChar(dest_codepoint)
    dest_glyph.transform(psMat.scale(SUPERSUBSCRIPT_SCALE))
    dest_glyph.transform(vshift_xform)

    additionalbearing = STROKE_WIDTH / 2 * (1 - SUPERSUBSCRIPT_SCALE)    

    dest_glyph.transform(psMat.translate(additionalbearing, 0))
    dest_glyph.width = dest_glyph.width + additionalbearing

    print "%s => %d" % (unicodedata.name(unichr(dest_codepoint)), dest_codepoint)

def make_superscript(font, source_codepoint, dest_codepoint):
    make_superscript_or_subscript(font, source_codepoint, dest_codepoint, True)

def make_subscript(font, source_codepoint, dest_codepoint):
    make_superscript_or_subscript(font, source_codepoint, dest_codepoint, False)

def make_vulgar_fraction(font, super_codepoint, sub_codepoint, dest_codepoint):
    super_codepoint = codepoint(super_codepoint)
    sub_codepoint = codepoint(sub_codepoint)
    dest_codepoint = codepoint(dest_codepoint)
    
    super = font.createChar(super_codepoint)
    sub   = font.createChar(sub_codepoint)
    dest  = font.createChar(dest_codepoint)
    dest.clear()

    fractionline = font[CODEPOINT_FRACTION_LINE]

    width = max([super.width,
                 sub.width,
                 fractionline.width])

    dest.addReference(super.glyphname,        psMat.translate((width - super.width       ) / 2, 0))
    dest.addReference(sub.glyphname,          psMat.translate((width - sub.width         ) / 2, 0))
    dest.addReference(fractionline.glyphname, psMat.translate((width - fractionline.width) / 2, 0))
    dest.width = width

def generate(italic_deg = 0,
             italic_name = "",
             condensed_scale = 1,
             condensed_name = "",
             auto_hint = False,
             manual_hints = False,
             auto_instr = False,
             auto_kern = False,
             auto_width = False,
             no_remove_overlap = False,
             no_add_extrema = False,
             generate_super_and_subscripts = True,
             generate_super_and_subscripts_method = 3,
             font_name = "RoutedGothic",
             family_name = "Routed Gothic",
             weight_name = "Regular",
             font_file_basename = FONT_FILE_BASENAME):

    font = fontforge.open(SOURCE_FILENAME)

    if generate_super_and_subscripts:

        for ss in SUPERSCRIPTS:
            sscp = codepoint(ss['codepoint'])
            ssof = codepoint(ss['of'])
            make_superscript(font, ssof, sscp)

        for ss in SUBSCRIPTS:
            sscp = codepoint(ss['codepoint'])
            ssof = codepoint(ss['of'])
            make_subscript(font, ssof, sscp)

        super_digit_glyphs = [
            font[cp]
            for cp in SUPERSCRIPT_DIGIT_CODEPOINTS
        ]
        fractionlinewidth = max([g.width for g in super_digit_glyphs]) + FRACTION_LINE_EXTRA_WIDTH

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

            numerator   = superscript_codepoint(numerator)
            denominator = subscript_codepoint(denominator)
            fraction    = codepoint(fraction)
            make_vulgar_fraction(font, numerator, denominator, fraction)

    if auto_kern:
        for lookupName in font.gpos_lookups:
            for subtableName in font.getLookupSubtables(lookupName):
                if font.isKerningClass(subtableName):
                    font.removeLookupSubtable(subtableName);

    # condense kerning pairs if needed

    if (condensed_scale != 1) and not auto_kern:
        for lookupName in font.gpos_lookups:
            for subtableName in font.getLookupSubtables(lookupName):
                if font.isKerningClass(subtableName):
                    kc = font.getKerningClass(subtableName)
                    offsets = kc[2]
                    newOffsets = [o * condensed_scale for o in offsets]
                    font.alterKerningClass(subtableName, kc[0], kc[1], newOffsets)

    condensed_transform = psMat.scale(condensed_scale, 1)

    if condensed_scale != 1:
        font.selection.all()
        font.transform(condensed_transform)

    for glyph in font.glyphs():
        if manual_hints:
            glyph.manualHints = True
        else:
            glyph.manualHints = False
        if italic_deg:
            width = glyph.width
            for name in glyph.layers:
                layer = glyph.layers[name]
                layer.transform(italic_transform(italic_deg))
                glyph.layers[name] = layer
                glyph.width = width
            glyph.anchorPoints = [
                anchor_point_transform(p, italic_transform(italic_deg))
                for p in glyph.anchorPoints
            ]

        glyph.round()
        glyph.stroke("circular", STROKE_WIDTH, "round", "round")
        if not no_remove_overlap:
            glyph.removeOverlap()
        if not no_add_extrema:
            glyph.addExtrema()

    if auto_width:
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
            g1_base_aps = tuple([ap[0] for ap in g1.anchorPoints if ap[1] == "base"])
            g1_mark_aps = tuple([ap[0] for ap in g1.anchorPoints if ap[1] == "mark"])
            g2_base_aps = tuple([ap[0] for ap in g2.anchorPoints if ap[1] == "base"])
            g2_mark_aps = tuple([ap[0] for ap in g2.anchorPoints if ap[1] == "mark"])
            i1 = intersect(g1_base_aps, g2_mark_aps)
            i2 = intersect(g2_base_aps, g1_mark_aps)
            if len(i1) or len(i2):
                glyph.build()
                built = True
        if not built:
            if italic_deg:
                glyph.references = [
                    reference_transform(r, glyph, italic_deg)
                    for r in glyph.references
                ]
                
    for glyph in font.glyphs():
        if auto_hint:
            glyph.autoHint()
        if auto_instr:
            glyph.autoInstr()

    font.strokedfont = False

    if auto_kern:
        font.selection.all()
        font.addLookup("autoKern", "gpos_pair", (), (("liga",(("latn",("dflt")),)),))
        font.addKerningClass("autoKern", "autoKern", 288, 16, False, True)

    font.fontname    = font_name
    font.familyname  = family_name
    font.fullname    = family_name
    font.weight      = weight_name
    font.italicangle = italic_deg
    basename         = font_file_basename

    if condensed_scale != 1:
        # separate family names for condensed variants.  don't
        # remember why.
        font.familyname  = font.familyname + " " + condensed_name.replace("-", " ")
        
        font.fontname    = font.fontname   +       condensed_name.replace("-", "").replace(" ", "")
        font.fullname    = font.fullname   + " " + condensed_name.replace("-", " ")

        basename         = basename        + "-" + condensed_name.lower().replace(" ", "-")

    if italic_deg:
        font.fontname    = font.fontname   + "-" + italic_name.replace(" ", "-")
        font.fullname    = font.fullname   + " " + italic_name.replace("-", " ")

        basename         = basename        + "-" + italic_name.lower().replace(" ", "-")
        
        font.italicangle = -ITALIC_ANGLE_DEG

    sfd_filename = DIST_SFD_DIRECTORY + "/" + basename + ".sfd"
    ttf_filename = DIST_TTF_DIRECTORY + "/" + basename + ".ttf"

    sfd_dir = os.path.dirname(sfd_filename)
    ttf_dir = os.path.dirname(ttf_filename)
    if not os.path.exists(sfd_dir):
        print "makedirs " + sfd_dir
        os.makedirs(sfd_dir)
    if not os.path.exists(ttf_dir):
        print "makedirs " + ttf_dir
        os.makedirs(ttf_dir)

    print "Saving " + sfd_filename + " ..."
    font.save(sfd_filename)
    print "Saving " + ttf_filename + " ..."
    font.generate(ttf_filename, flags=("no-hints", "omit-instructions"))

    font.close()

italic_types = [
    { 'deg': 0,                    'name': ''            },
    { 'deg': ITALIC_ANGLE_DEG / 2, 'name': 'Half Italic' },
    { 'deg': ITALIC_ANGLE_DEG,     'name': 'Italic'      }
]

condensed_types = [
    { 'scale': 1,                      'name': ''       },
    { 'scale': CONDENSED_SCALE_X,      'name': 'Narrow' },
    { 'scale': CONDENSED_WIDE_SCALE_X, 'name': 'Wide'   }
]

for italic in (italic_types):
    for condensed in (condensed_types):
        generate(italic_deg      = italic['deg'],
                 italic_name     = italic['name'],
                 condensed_scale = condensed['scale'],
                 condensed_name  = condensed['name'])

