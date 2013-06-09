# -*- coding: utf-8 -*-

from lxml import etree
from mingus.core import notes, chords, mt_exceptions

import logging

class MusicXMLReader(object):
    def __init__(self, filename, part=0):
        self.__notes_depot = []

        logging.debug("Parsing file %s" % filename)

        try:
            if isinstance(filename, basestring):
                with open(filename) as fp:
                    t = etree.parse(fp)
            else:
                t = etree.parse(filename)
        except (IOError, etree.XMLSyntaxError):
            logging.error("Error reading file %s" % filename)
            return None

        parts = etree.ETXPath("//part")(t)

        logging.debug("Found %s parts in the file, reading part #%s" % (len(parts), part))

        if part > len(parts) - 1:
            logging.error("Part %s not available" % part)
            return None

        for m in etree.ETXPath(".//measure")(parts[part]):
            logging.debug("Reading measure %s" % m.attrib.get("number"))

            for chunk in etree.ETXPath(".//note|harmony|direction")(m):
            # for chunk in etree.ETXPath(".//direction")(m):
                if chunk.tag == "note":
                    note = self.__parse_note(chunk)
                    if note:
                        self.__notes_depot.append(note)
                elif chunk.tag == "direction":
                    chord = self.__try_to_parse_label(chunk)

                    if chord:
                        self.__dump_chord(chord)

                elif chunk.tag == "harmony":
                    self.__dump_chord(self.__parse_harmony(chunk))

    def __dump_chord(self, chord):
        if self.__notes_depot:
            logging.info("Notes in melody are: %s" % (", ".join(self.__notes_depot)))

        self.__notes_depot = []

        if chord:
            try:
                chord_tones = chords.from_shorthand(chord)
                logging.info("\nChord is %s" % chord)
                logging.info("Chord tones are: %s" % (", ".join(chord_tones)))
            except mt_exceptions.FormatError:
                logging.error("Error parsing chord symbol %s" % chord)

    def __calc_alteration(self, alter):
        if alter:
            alter = int(alter[0].text)
            return ("#" if alter > 0 else "b") * abs(alter)

        return ""

    def __parse_note(self, note):
        step = etree.ETXPath("./pitch/step")(note)
        alter = etree.ETXPath("./pitch/alter")(note)

        n = ""

        if step:
            n = step[0].text

            n += self.__calc_alteration(alter)

        if n:
            return notes.remove_redundant_accidentals(n)

    def __unify_chord(self, label):
        if u"(" not in label:
            label = label.rstrip(u")")

        if u")" not in label:
            label = label.lstrip("u(")

        label = label.replace(u"7sus4", u"sus47")
        label = label.replace(u"m(7)", u"mM7")

        return label

    def __parse_harmony(self, chord):
        step = etree.ETXPath("./root/root-step")(chord)
        kind = etree.ETXPath("./kind")(chord)
        alter = etree.ETXPath("./root/root-alter")(chord)
        bass = etree.ETXPath("./bass/bass-step")(chord)
        bass_alter = etree.ETXPath("./bass/bass-alter")(chord)

        c = ""

        if step:
            c = step[0].text

            c += self.__calc_alteration(alter)

            if kind:
                kind = kind[0].get("text")
                if kind.startswith("o"):
                    kind = "dim" + kind[1:]

                c += kind

            if bass:
                c += "/" + bass[0].text
                c += self.__calc_alteration(bass_alter)

        return self.__unify_chord(c)

    def __try_to_parse_label(self, label):
        words = etree.ETXPath("./direction-type/words")(label)

        if words and words[0].get("default-y") == "100":
            label = self.__unify_chord(words[0].text)

            return label


if __name__ == "__main__":
    import sys
    import codecs
    logging.basicConfig(level=logging.INFO)

    # Printing to stdout in utf-8
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    
    MusicXMLReader("samples/musescore/L03.xml")
    # print(parse_music_xml("samples/musescore/L04.xml"))
