import unittest
import datetime
import inspectReport
import core.updates


class TestSequenceFunctions(unittest.TestCase):

    def test_convertUifListIntoUpdates(self):

        items = []
        items.append({'Language': 'Neutral',
                      'Type': 'x64',
                      'KB': 2795944,
                      'Date': 'ISODate(\'2013-02-12T00:00:00Z\')',
                      'Version': 'Windows 8',
                      'Path': '\\2795944\\Windows8\\NEU\\x64' +
                      '\\Windows8-RT-KB2795944-x64.msu'})
        self.assertEqual(1, len(inspectReport.convertUifListIntoUpdates(items)))

    def test_items2KBs(self):

        items = [{'KB': 1}, {'KB': 2}, {'KB': 3},
                 {'KB': 4}, {'KB': 5}, {'KB': 6}]
        refKbList = [1, 2, 3, 4, 5, 6]
        kbList = inspectReport.items2KBs(items)

        self.assertEqual(refKbList, kbList)

    def test_getListDiff(self):

        KBs = [2900986, 2898785, 2267602, 2907997, 2742614, 2737084, 2789649,
               2833958, 2840632, 2861702, 2727528, 2757638, 2770660, 2781197,
               2785220, 2803821, 2807986, 2813430, 2829254, 2829361, 2830290,
               2835361, 2835364, 2839894, 2845187, 2847311, 2849470, 2862152,
               2862330, 2862335, 2862966, 2863725, 2864058, 2864202, 2868038,
               2868623, 2868626, 2868725, 2871690, 2875783, 2876331, 2884256,
               2887069, 2892074, 2893294, 2893984, 2750149, 2805222, 2805227,
               2779444, 2768703, 2769034, 2769165, 2772501, 2777294, 2795944,
               2798162, 2800033, 2802618, 2805966, 2808679, 2811660, 2822241,
               2836988, 2845533, 2856373, 2869628, 2871389, 2871777, 2877213,
               2882780, 2885699, 2891804, 2893519, 2904266, 2913152, 890830]

        founded = [2750149, 2795944, 2768703, 2777294, 2772501, 2769165,
                   2769034, 2737084, 2779444, 2907997, 2898785, 2893984,
                   2893294, 2892074, 2887069, 2871690, 2785220, 2757638,
                   2742614, 2789649, 2807986, 2781197, 2781197, 2830290,
                   2829361, 2829254, 2839894, 2845187, 2835364, 2835361,
                   2803821, 2868623, 2849470, 2840632, 2884256, 2868038,
                   2862335, 2862330, 2847311, 2900986, 2875783, 2868626,
                   2727528, 2770660]

        refDiff = [2913152, 2861702, 2811660, 2891804, 2877213, 2800033,
                   2833958, 2876331, 2871389, 2856373, 2864058, 2864202,
                   2885699, 2813430, 2871777, 2862152, 2904266, 890830,
                   2893519, 2798162, 2805966, 2882780, 2845533, 2822241,
                   2805222, 2808679, 2836988, 2805227, 2863725, 2802618,
                   2267602, 2868725, 2862966, 2869628]

        diff = inspectReport.getListDiff(KBs, founded)

        self.assertEqual(refDiff, diff)

    def test_getData(self):

        updates = [
        {'Date': datetime.date(2014, 7, 8),
         'KB': {'UNKNOWN KB': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight_Developer.exe'},
         'Type': 'x86', 'Language': 'Neutral',
         'Path': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight_Developer.exe',
         'Version': {'UNKNOWN VERSION': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight_Developer.exe'}},
        {'Date': datetime.date(2014, 7, 8),
         'KB': {'UNKNOWN KB': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight_Developer.dmg'},
         'Type': 'x86', 'Language': 'Neutral',
         'Path': '\\2977218\\Windows\\x86\\NEU\\Silverlight_Developer.dmg',
         'Version': {'UNKNOWN VERSION': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight_Developer.dmg'}},
        {'Date': datetime.date(2014, 7, 8),
         'KB': {'UNKNOWN KB': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight.exe'},
         'Type': 'x86', 'Language': 'Neutral',
         'Path': '\\2977218\\Windows\\x86' +
         '\\NEU\\Silverlight.exe',
         'Version': {'UNKNOWN VERSION': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight.exe'}},
        {'Date': datetime.date(2014, 7, 8),
         'KB': {'UNKNOWN KB': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight.dmg'}, 'Type': 'x86', 'Language': 'Neutral',
         'Path': '\\2977218\\Windows\\x86\\NEU\\Silverlight.dmg',
         'Version': {'UNKNOWN VERSION': '\\2977218\\Windows\\x86' +
             '\\NEU\\Silverlight.dmg'}},
        {'Date': datetime.date(2014, 7, 8),
         'KB': {'UNKNOWN KB': '\\2977218\\Windows\\x64' +
             '\\NEU\\Silverlight_x64.exe'}, 'Type': 'x64',
         'Language': 'Neutral',
         'Path': '\\2977218\\Windows\\x64\\NEU\\Silverlight_x64.exe',
         'Version': {'UNKNOWN VERSION': '\\2977218\\Windows\\x64' +
             '\\NEU\\Silverlight_x64.exe'}},
        {'Date': datetime.date(2014, 7, 8),
         'KB': {'UNKNOWN KB': '\\2977218\\Windows\\x64' +
             '\\NEU\\Silverlight_Developer_x64.exe'},
         'Type': 'x64', 'Language': 'Neutral',
         'Path': '\\2977218\\Windows\\x64' +
             '\\NEU\\Silverlight_Developer_x64.exe',
         'Version': {'UNKNOWN VERSION': '\\2977218\\Windows\\x64' +
             '\\NEU\\Silverlight_Developer_x64.exe'}}
        ]

        coreUpdates = core.updates.Updates()
        coreUpdates.addUpdates(updates)
        data = inspectReport.getData(coreUpdates, [2977218], {})
        updates = data.get('Updates')
        self.assertIsNotNone(updates)
        self.assertEqual(6, len(updates))

if __name__ == '__main__':

    unittest.main()
