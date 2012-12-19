#! /usr/bin/python
import cairo

from dance import Dance

def font_extents(context):
    ascent, descent, height, max_x_advance, max_y_advance = context.font_extents()
    return locals()

def text_extents(context, text):
    x_bearing, y_bearing, width, height, x_advance, y_advance = context.text_extents(text)
    return locals()

class DanceCard:
    def __init__ (self, dance):
        self.clear()
        self.set_dance (dance)

    def clear (self):
        self.sectionsof8 = [""] * 8
        self.sectionsof4 = [""] * 4
        self.notesof8 = [""] * 8
        self.notesof4 = [""] * 4
        self.dance = None

    def set_dance (self, dance):
        self.dance = dance
        beats = 0
        for figure in dance.sequence:
            text = figure.get_text()
            count = figure.get_count()
            note = figure.get_note()

            if count < 0:
                count = -count
                if beats % 8 >= 6:
                    beats = (beats + 2) / 8 * 8
                count = count - beats % count
            else:
                rounding = 2
                if count > 2:
                    rounding = 4
                if count > 4:
                    rounding = 8
                if count > 8:
                    rounding = 16
    
                if (beats + count / 2) / rounding != beats / rounding:
                    beats = (beats + count) / rounding * rounding

            if count + beats % 8 > 10:
                if self.sectionsof4[beats / 16]:
                    self.sectionsof4[beats / 16] = self.sectionsof4[beats / 16] + ("; " + text)
                else:
                    self.sectionsof4[beats / 16] = text
                self.notesof4[beats / 16] = note
            else:
                if self.sectionsof8[beats / 8]:
                    self.sectionsof8[beats / 8] = self.sectionsof8[beats / 8] + ("; " + text)
                else:
                    self.sectionsof8[beats / 8] = text
                self.notesof8[beats / 8] = note
            beats = beats + count

    def write_to_context(self, context, width, height, margin):

        # draw lines to the margins on either side.  Negative margin will make the lines shorter.
        context.save()
        context.translate(-margin, 0)
        context.scale(width + 2 * margin, height)
        context.set_line_width(1.0 / 32 / 10) # 32nd of an inch at 7.5 * 10.
        context.move_to(0, 3.0 / 9)
        context.rel_line_to(1, 0)
        context.move_to(0, 5.0 / 9)
        context.rel_line_to(1, 0)
        context.move_to(0, 7.0 / 9)
        context.rel_line_to(1, 0)
        context.stroke()
        context.restore()

        context.save()

        # scale to 9 units high since that's how we divide a card.
        context.scale(height / 9.0, height / 9.0)
        width = width * 9.0 / height
        height = 9.0

        # We want to know how tall our font is, so we approximate a multiplier using this function.
        context.set_font_size(1)
        multiplier = 1 / font_extents(context)['height']

        self.font_size = 0
        def set_font_size(font_size):
            if self.font_size == font_size:
                return
            context.set_font_size(font_size * multiplier)


        def output_text (text, font_size, x, y, width, right_align = False):
            set_font_size(font_size)
            min_font_size = font_size / 100.0

            my_extents = text_extents(context, text)
            while (my_extents['x_advance'] > width):
                font_size = font_size * .75
                set_font_size(font_size)
                my_extents = text_extents(context, text)
                if font_size < min_font_size:
                    return 0
            if right_align:
                context.move_to(x + width - my_extents['x_advance'], y)
            else:
                context.move_to(x, y)
            context.show_text(text)
            return my_extents['x_advance']
        
        set_font_size(.5)
        extents = font_extents(context)
        output_text(self.dance.title, .5, 0, extents['ascent'], width * .75)
        output_text(self.dance.author, .5, 0, .5 + extents['ascent'], width * .75)
        output_text(self.dance.formation, .5, width * .75, extents['ascent'], width * .25, right_align=True)

#        context.move_to(width - text_extents(context, self.formation)["x_advance"], extents['ascent'])
#        context.show_text(self.formation)

        set_font_size(.75)

        max_advance = 0
        for i in xrange(1, 9):
            text = "%d" % (i,)
            advance = text_extents(context, text)['x_advance']
            if advance > max_advance:
                max_advance = advance
        right_edge = max_advance
        left_edge = right_edge + text_extents(context, " ")['x_advance']

        def write_number(num):
            text = "%d" % (num,)
            my_extents = text_extents(context, text)
            context.move_to(right_edge - my_extents['x_advance'], num + .5 - my_extents['height'] / 2 - my_extents['y_bearing'])
            context.show_text(text)
        for i in xrange(1, 9):
            write_number(i)

        def write_text(num, text, note):
            set_font_size(.75)
            number_text = "%d" % (num,)
            number_extents = text_extents(context, number_text)
            x = left_edge
            y = num + .5 - number_extents['height'] / 2 - number_extents['y_bearing']
            if note:
                text_width = output_text (text, .75, x, y, (width - x) * .75)
                context.save()
                context.set_source_rgb(.3, .3, .3)
                x = x + text_width + text_extents(context, " ")['x_advance']
                output_text (note, .75, x, y, width - x, right_align = True)
                context.restore()
                self.font_size = 0
                return width
            else:
                text_width = output_text (text, .75, x, y, width - x)
                return text_width


        def write_section_text(num, text, note, offset = 0):
            set_font_size(1.5)
            my_extents = text_extents(context, text)
            y = 1 + num * 2 + 1 - my_extents['height'] / 2 - my_extents['y_bearing']
            x = left_edge + offset
            if note:
                text_width = output_text (text, 1.5, x, y, (width - x) * .75)
                context.save()
                context.set_source_rgb(.3, .3, .3)
                x = x + text_width + text_extents(context, " ")['x_advance']
                output_text (note, 1.5, x, y, width - x, right_align = True)
                context.restore()
                self.font_size = 0
            else:
                text_width = output_text (text, 1.5, x, y, width - x)

        for i in xrange(4):
            if self.sectionsof4[i]:
                if self.sectionsof8[i * 2]:
                    text_width = write_text(2 * i     + 1, self.sectionsof8[2 * i    ] + "; ", "")
                    write_section_text(i, self.sectionsof4[i], self.notesof4[i], offset=text_width)
                else:
                    write_section_text(i, self.sectionsof4[i], self.notesof4[i])
                write_text(2 * i + 1 + 1, self.sectionsof8[2 * i + 1], self.notesof8[2 * i + 1])
            else:
                write_text(2 * i     + 1, self.sectionsof8[2 * i    ], self.notesof8[2 * i    ])
                write_text(2 * i + 1 + 1, self.sectionsof8[2 * i + 1], self.notesof8[2 * i + 1])

        context.restore()

def print_dances (dances, filename):

    surface = cairo.PDFSurface(filename, 8.5 * 72, 11 * 72)
    context = cairo.Context (surface)
    context.select_font_face("serif")

    for dance in dances:
        context.save()
        context.scale(72, 72)
        context.translate(.5, .5)
        DanceCard(dance).write_to_context(context, 7.5, 10.0, .5)
        context.restore()

        context.show_page()

    surface.finish()

def print_dance (dance, filename):

    surface = cairo.PDFSurface(filename, 8.5 * 72, 11 * 72)
    context = cairo.Context (surface)
    context.select_font_face("serif")

    context.save()
    context.scale(72, 72)
    context.translate(.5, .5)
    DanceCard(dance).write_to_context(context, 7.5, 10.0, .5)
    context.restore()

    context.show_page()

    surface.finish()

import sys
if len(sys.argv) > 2:
    dances = []
    for filename in sys.argv[1:]:
        print filename
        dance = Dance()
        dance.parse(filename)
        dances.append(dance)
        print_dances(dances, "dances.pdf")

else:
    filename = sys.argv[1]
    dance = Dance()
    dance.parse(filename)
#    for figure in dance.sequence:
#        print figure.get_text()
    parts = filename.rsplit(".", 1)
    filename = parts[0] + ".pdf"
    print_dance(dance, filename)
