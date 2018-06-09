'''Generate MusicXML file with simple backing music given chord progressions.
'''

import datetime
import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, tostring as xml_to_string

import music21

class MusicGenerator(object):
    def __init__(self):
        # Set some default configurations.
        self._cfg = {
            'bpm': 94,
            'time_signature': '4/4',
            'chord_list': 'C F G C',
            'style': 'arpeggio',
            'instrument': 'Piano',
        }
        self._xml = None

    def set_cfg(self, cfg):
        self._cfg = cfg
        self._xml = None

    def get_xml(self):
        if not self._xml:
            self._generate_xml()
        return xml_to_string(self._xml, 'utf-8')

    def get_mid(self):
        stream = music21.converter.parseData(self.get_xml(), format='musicxml')
        stream.write('midi', 'output.mid')

    def _generate_xml(self):
        title = self._cfg.get('title', 'Untitled')
        root = Element('score-partwise')
        root.set('version', '3.0')
        identification = SubElement(root, 'identification')
        encoding = SubElement(identification, 'encoding')
        SubElement(encoding, 'software').text = 'BackingMusicGenerator'
        SubElement(encoding, 'encoding-date').text = datetime.datetime.now().strftime('%Y-%m-%d')
        credit = SubElement(root, 'credit')
        SubElement(credit, 'credit-type').text = 'title'
        SubElement(credit, 'credit-words').text = title
        self._add_part(root)
        self._xml = root

    def _add_part(self, root):
        existing_part_cnt = len(root.findall('part'))
        if existing_part_cnt == 0:
            # Add a unique <part-list> element.
            SubElement(root, 'part-list')
        part_list = root.find('part-list')

        new_part_id = 'P{}'.format(existing_part_cnt + 1)  # start at 'P1'
        score_part = SubElement(part_list, 'score-part')
        score_part.set('id', new_part_id)
        part = SubElement(root, 'part')
        part.set('id', new_part_id)
        # <score_part> contains top-level info, <part> contains actual music notes.

        instrument_id = '{}-I1'.format(new_part_id)
        score_instrument = SubElement(score_part, 'score-instrument')
        score_instrument.set('id', instrument_id)
        SubElement(score_instrument, 'instrument-name').text = self._cfg['instrument']

        midi_instrument = SubElement(score_part, 'midi-instrument')
        midi_instrument.set('id', instrument_id)
        SubElement(midi_instrument, 'midi-channel').text = '2'
        SubElement(midi_instrument, 'midi-program').text = '1'

        #--- tmp

        measure_cnt = 0
        NOTES = {'C': 'C,E,G', 'F': 'F,A,C', 'G': 'G,B,D'}
        for chord in self._cfg['chord_list'].split(' '):
            measure_cnt += 1
            measure = SubElement(part, 'measure')
            measure.set('number', str(measure_cnt))
            attributes = SubElement(measure, 'attributes')
            SubElement(attributes, 'divisions').text = '1'
            SubElement(SubElement(attributes, 'key'), 'fifths').text = '0'
            time = SubElement(attributes, 'time')
            SubElement(time, 'beats').text = '4'
            SubElement(time, 'beat-type').text = '4'
            clef = SubElement(attributes, 'clef')
            SubElement(clef, 'sign').text = 'G'
            SubElement(clef, 'line').text = '2'
            SubElement(clef, 'clef-octave-change').text = '-1'
            staff_details = SubElement(attributes, 'staff-details')
            SubElement(staff_details, 'staff-lines').text = '5'
            notes_in_chord = NOTES[chord].split(',')
            self._add_quarter_note(measure, notes_in_chord[0], 2)
            self._add_quarter_note(measure, notes_in_chord[0], 3)
            self._add_quarter_note(measure, notes_in_chord[1], 3)
            self._add_quarter_note(measure, notes_in_chord[2], 3)

    def _add_quarter_note(self, measure, step, octave):
        note = SubElement(measure, 'note')
        pitch = SubElement(note, 'pitch')
        SubElement(pitch, 'step').text = step
        SubElement(pitch, 'octave').text = str(octave)
        SubElement(note, 'duration').text = '1'
        SubElement(note, 'voice').text = '1'
        SubElement(note, 'type').text = 'quarter'
        SubElement(note, 'staff').text = '1'


if __name__ == '__main__':
    gen = MusicGenerator()
    xml_tree = gen.generate_xml(cfg)
    raw_xml_str = xml_to_string(xml_tree, 'utf-8')
    print(xml.dom.minidom.parseString(raw_xml_str).toprettyxml(indent='  '))
    xml_to_midi(raw_xml_str)
