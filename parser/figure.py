
def massage_direction(direction):
    return direction

def massage_target(target):
    if target == "Sh":
        return "Shadow"
    return target

def massage_formation(formation):
    if formation == "ring":
        return "Ring"
    if formation == "wave":
        return "Wave"
    return formation

def massage_distance(distance):
    parts = distance.rsplit(".", 1)
    if len(parts) == 2:
        if parts[0] == "0":
            parts[0] = ""
        if parts[1] == "25":
            return parts[0] + unichr(188)
        if parts[1] == "5":
            return parts[0] + unichr(189)
        if parts[1] == "75":
            return parts[0] + unichr(190)

        if parts[0]:
            parts[0] = parts[0] + " "
        if parts[1] == "125":
            return parts[0] + "1/8"
        if parts[1] == "375":
            return parts[0] + "3/8"
        if parts[1] == "625":
            return parts[0] + "5/8"
        if parts[1] == "875":
            return parts[0] + "7/8"
    return distance

def massage_circle_distance(distance):
    if distance == "4":
        return "once"
    return massage_distance(str(float(distance) / 4.0))

class Figure:

    defaults = {
        "balsw"     : { "target" : "P" },
        "gypsymelt" : { "target" : "P" },
        "givetake"  : { "target" : "M" },
        "circle"    : { "distance" : "4", "direction" : "L" },
        "singprom"  : { "distance" : "4", "direction" : "R" },
        "dsd"       : { "distance" : "1", "target" : "P" },
        "seesaw"    : { "distance" : "1", "target" : "P" },
        "caltwirl"  : { "target" : "P" },
        "boxgnat"   : { "target" : "P" },
        "star"      : { "distance" : "4" },
        "sw"        : { "target" : "P" },
        "ala"       : { "distance" : "1", "target" : "P" },
        "gypsy"     : { "distance" : "1", "target" : "P" },
        "chain"     : { "target" : "W" },
        "rollaway"  : { "who" : "M", "target" : "W" },
        "sqthru"    : { "distance" : "4" },
        "prom"      : { "distance" : "1" },
        }
    def __init__ (self, tag, attrs, count):
        self.tag = tag
        self.attrs = attrs
        self.count = count

    def get_attr(self, attr):
        if self.attrs[attr] is not None:
            return self.attrs[attr]
        try:
            return Figure.defaults[self.tag][attr]
        except:
            return None

    def get_note (self):
        if self.attrs["note"]:
            return self.attrs["note"]
        if self.tag == "hey" and self.attrs["crossings"]:
            return self.attrs["crossings"]
        return ""

    def get_count (self):
        return self.count

    def get_text (self):
        if self.attrs["text"]:
            return self.attrs["text"]

        if self.tag == 'balsw':
            target = self.get_attr ("target")
            target = massage_target (target)
            text = target + "B&S"
        elif self.tag == 'gypsymelt':
            target = self.get_attr ("target")
            target = massage_target (target)
            text = target + " gypsy and sw"
        elif self.tag == 'givetake':
            target = self.get_attr ("target")
            target = massage_target(target)
            if target == "M":
                target = ""
            text = target + "G&T"
        elif self.tag == "circle":
            text = "Cir %s %s" % (massage_direction(self.get_attr("direction")), massage_circle_distance(self.get_attr("distance")))
        elif self.tag == "singprom":
            text = "Single File Prom %s %s" % (massage_direction(self.get_attr("direction")), massage_circle_distance(self.get_attr("distance")))
        elif self.tag == "dsd":
            if self.get_attr("distance") != "1":
                text = "%s DSD %s" % (massage_target(self.get_attr("target")), massage_distance(self.get_attr("distance")))
            else:
                text = "%s DSD" % (massage_target(self.get_attr("target")),)
        elif self.tag == "seesaw":
            if self.get_attr("distance") != "1":
                text = "%s seesaw %s" % (massage_target(self.get_attr("target")), massage_distance(self.get_attr("distance")))
            else:
                text = "%s seesaw" % (massage_target(self.get_attr("target")),)
        elif self.tag == "hey":
            if self.get_attr("crossings") and self.get_attr("distance") is None:
                idistance = len(self.get_attr("crossings").split(","))
                idistance = (idistance + 1) / 2 * 2
            if self.get_attr("distance"):
                idistance = int(self.get_attr("distance"))
            if idistance != 8:
                text = massage_distance(str(idistance / 8.0)) + " Hey"
            else:
                text = "Hey"
        elif self.tag == "lchain":
            text = "W chain"
        elif self.tag == "chain":
            text = "%s chain" % (self.get_attr("target"),)
        elif self.tag == "pet":
            text = "Pet Twirl"
        elif self.tag == "rightleft":
            text = "R&L"
        elif self.tag == "bal":
            if self.get_attr("formation"):
                formation = massage_formation (self.get_attr("formation"))
                text = "%s Bal" % (formation,)
                if self.get_attr("target") in ("R", "L"):
                    text = text + " to the " + self.get_attr("target")
                elif self.get_attr("target") in ("P", "N", "Sh"):
                    text = text + " to your " + self.get_attr("target")
                elif self.get_attr("target"):
                    text = text + " " + self.get_attr("target")
            else:
                if self.get_attr("target"):
                    text = "%s Bal" % (self.get_attr("target"),)
                else:
                    text = "Bal"
        elif self.tag == "slide":
            text = "Slide %s" % (self.get_attr("direction"),)
        elif self.tag == "rollaway":
            text = "Roll Away %s" % (self.get_attr("target"),)
            if self.get_attr("direction"):
                text = text + " to the " + self.get_attr("direction")
        elif self.tag == "passthru":
            text = "Pass Thru"
        elif self.tag == "passacross":
            text = "Pass Thru Across"
        elif self.tag == "pass":
            text = "%s Pass %s sh" % (self.get_attr("target"), self.get_attr("shoulder"),)
        elif self.tag == "xtrail":
            text = "X Trail Thru"
        elif self.tag == "caltwirl":
            text = "%s Cal Twirl" % (self.get_attr("target"),)
        elif self.tag == "boxgnat":
            text = "%s Box The Gnat" % (self.get_attr("target"),)
        elif self.tag == "down":
            text = "Down the Hall"
        elif self.tag == "turn":
            if self.get_attr("as") == "alone":
                text = "Turn alone"
            else:
                text = "Turn as %s" % (self.get_attr("as"),)
        elif self.tag == "return":
            text = "Come Back"
        elif self.tag == "bend":
            text = "Bend the Line"
        elif self.tag == "prom":
            if self.get_attr("distance") != "4":
                text = "%s prom %s" % (self.get_attr("target"), massage_distance(self.get_attr("distance")))
            else:
                text = "%s prom" % (self.get_attr("target"),)
        elif self.tag == "starprom":
            text = "%s Star prom" % (self.get_attr("target"),)
        elif self.tag == "butterfly":
            text = "Butterfly Whirl"
        elif self.tag == "ll":
            text = "LL"
        elif self.tag == "star":
            if self.get_attr("distance") != "4":
                text = "%s Star %s" % (massage_direction(self.get_attr("direction")), massage_circle_distance(self.get_attr("distance")))
            else:
                text = "%s Star" % (massage_direction(self.get_attr("direction")),)
        elif self.tag == "figure":
            text = self.get_attr("text")
        elif self.tag == "sw":
            text = "%s sw" % (massage_target(self.get_attr("target")),)
        elif self.tag == "orbit":
            text = "%s orbit %s %s" % (massage_target(self.get_attr("target")), massage_direction(self.get_attr("direction")), massage_distance(self.get_attr("distance")))
        elif self.tag == "ala":
            text = "%s %s ala %s" % (massage_target(self.get_attr("target")), massage_direction(self.get_attr("direction")), massage_distance(self.get_attr("distance")))
        elif self.tag == "gypsy":
            if self.get_attr("distance") != "1":
                text = "%s %s sh gypsy %s" % (massage_target(self.get_attr("target")), massage_direction(self.get_attr("direction")), massage_distance(self.get_attr("distance")))
            else:
                text = "%s %s sh gypsy" % (massage_target(self.get_attr("target")), massage_direction(self.get_attr("direction")))
        elif self.tag == "passocean":
            text = "Pass to ocean wave"
        elif self.tag == "madrobin":
            text = "Mad robin"
        elif self.tag == "courtesy":
            text = "Courtesy Turn"
        elif self.tag == "sqthru":
            if self.get_attr("distance") != "4":
                text = "Square Thru %s" % (massage_circle_distance(self.get_attr("distance")))
            else:
                text = "Square Thru"
        elif self.tag == "pullby":
            text = "%s pull by %s" % (massage_target(self.get_attr("target")), massage_direction(self.get_attr("direction")))
        elif self.tag == "halfeight":
            text = unichr(189) + " figure eight"
            if self.get_attr("direction"):
                text = text + " " + self.get_attr("direction")
        elif self.tag == "corners":
            text = "Turn contra corners"
        else:
            raise Exception(str ("Unrecognized tag %s" % (self.tag,)))
        if self.get_attr("destination"):
            text = text + " to " + self.get_attr("destination")
        if self.get_attr("who"):
            text = massage_target(self.get_attr("who")) + " " + text
        if self.get_attr("when"):
            text = text + " " + self.get_attr("when")
        if self.get_attr("end"):
            text = text + " end " + self.get_attr("end")

        # overrides
        if self.get_attr("text"):
            text = self.get_attr("text")

        return text

    @classmethod
    def parse(cls, node):
        tag = node.tagName
        attrs = {}
        for attr in ("note", "target", "distance", "direction", "formation", "destination", "crossings", "who", "as", "text", "count", "shoulder", "when", "end"):
            try:
                attrs[attr] = node.attributes[attr].nodeValue
            except:
                attrs[attr] = None

        if tag == 'while':
            count = 0
            children = [] 
            for childNode in node.childNodes:
                if childNode.nodeType == childNode.ELEMENT_NODE:
                    child = Figure.parse(childNode)
                    if child.count > count:
                        count = child.count
                    children.append (child)
            return WhileFigure(children, attrs, count)
        elif tag in ('balsw', 'gypsymelt', 'givetake', 'corners'):
            count = 16
        elif tag in ("dsd", "seesaw", "lchain", "chain", "pet", "rightleft", "prom", "ll", "madrobin", "halfeight"):
            count = 8
        elif tag == "return":
            count = 6
        elif tag in ("slide", "passthru", "passacross", "bend", "courtesy", "pullby", "rollaway"):
            count = 2
        elif tag in ("bal", "pass", "xtrail", "caltwirl", "boxgnat", "down", "starprom", "butterfly", "passocean"):
            count = 4
        elif tag == "turn":
            if attrs["as"] == "alone":
                count = 2
            else:
                count = 4
        elif tag in ("circle", "star", "sqthru", "singprom"):
            distance = attrs["distance"]
            if distance is None:
                distance = "4"
            count = int(float(distance) * 2)
        elif tag == "hey":
            idistance = 4
            if attrs["crossings"] and attrs["distance"] is None:
                idistance = len(attrs["crossings"].split(","))
                idistance = (idistance + 1) / 2 * 2
            if attrs["distance"] is not None:
                idistance = int(attrs["distance"])
            count = idistance * 2
        elif tag == "figure":
            pass
        elif tag == "sw":
            count = -16
        elif tag == "orbit":
            distance = float (attrs["distance"])
            count = int (distance * 4)
        elif tag == "ala" or tag == "gypsy":
            distance = attrs["distance"]
            if distance is None:
                distance = "1"
            distance = float (distance)
            times = int (distance // 1.5)
            distance = distance % 1.5
            if distance <= .125:
                offset = 0
            elif distance <= .375:
                offset = 1
            elif distance <= .625:
                offset = 2
            elif distance <= .875:
                offset = 4
            elif distance <= 1.125:
                offset = 6
            elif distance <= 1.175:
                offset = 7
            elif distance <= 1.625:
                offset = 8
            count = offset + 8 * times
        else:
            raise Exception(str("Unrecognized tag %s" % (tag,)))

        # overrides
        if attrs["count"]:
            count = int(attrs["count"])

        return Figure(tag, attrs, count)

class WhileFigure(Figure):
    def __init__ (self, children, attrs, count):
        self.tag = "while"
        self.children = children
        self.attrs = attrs
        self.count = count

    def get_text(self):
        return ", ".join ([figure.get_text() for figure in self.children])
