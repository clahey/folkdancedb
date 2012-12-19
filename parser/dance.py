from xml.dom.minidom import parse
from figure import Figure

def warn (filename, text):
    raise str("%s: %s" % (filename, text))

class Dance:
    def __init__ (self):
        self.clear()

    def clear (self):
        self.sequence = []
        self.author = ""
        self.title = ""
        self.formation = ""

    def parse (self, file_or_dom):
        if type(file_or_dom) in (str, unicode):
            filename = file_or_dom
            dom = parse(file_or_dom)
        else:
            filename = "from dom"
            dom = file_or_dom
        notes = []
        root = dom.documentElement
        for child in root.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                tag = child.tagName
                try:
                    text = child.childNodes[0].data
                except:
                    text = ""
                if tag == "author":
                    if self.author:
                        warn(filename, "Duplicated author tag")
                        return
                    self.author = text
                elif tag == "title":
                    if self.title:
                        warn(filename, "Duplicated title tag")
                        return
                    self.title = text
                elif tag == "formation":
                    if self.formation:
                        warn(filename, "Duplicated formation tag")
                        return
                    self.formation = text
                elif tag == "note":
                    notes.append(text)
                elif tag == "sequence":
                    self.parse_sequence (child)
                elif tag == "dancetype" or tag == "year":
                    pass
                else:
                    warn(filename, "Unrecognized tag %s" % (tag,))
                    return

    def parse_sequence (self, sequenceNode):
        sequence = []
        for childNode in sequenceNode.childNodes:
            if childNode.nodeType == childNode.ELEMENT_NODE:
                sequence.append(Figure.parse(childNode))

        self.sequence = sequence

