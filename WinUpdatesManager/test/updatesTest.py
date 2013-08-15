import unittest
import os
import datetime
import core.updates


class TestSequenceFunctions(unittest.TestCase):

    def test_Updates(self):

        updates = core.updates.Updates()

        self.assertEqual(0, len(updates))
        self.assertRaises(IndexError, updates.__getitem__, -1)
        self.assertRaises(IndexError, updates.__getitem__, 0)
        self.assertRaises(IndexError, updates.__getitem__, 1)

        for update in updates:
            self.fail('Actually there are no updates!')

        updates.addUpdate('Some' + os.sep + 'Path', 123,
                'Win32', '80x86', 'English', datetime.datetime(1970, 1, 1))
        updates.addUpdate('Some' + os.sep + 'Path', 123,
                'Win32', '80x86', 'English', datetime.datetime(1970, 1, 1))
        updates.addUpdate('Some' + os.sep + 'Path2', 456,
                'Win64', 'x86-64', 'Russian', datetime.datetime(2008, 12, 11))
        updates.addUpdate('Some' + os.sep + 'Path2', 456,
                'Win64', 'x86-64', 'Russian', datetime.datetime(2008, 12, 11))

        self.assertEqual(2, len(updates))
        self.assertRaises(IndexError, updates.__getitem__, -1)
        try:
            self.assertEqual(updates.__getitem__(0)['Type'], '80x86')
            self.assertEqual(updates.__getitem__(1)['Language'], 'Russian')
        except:
            self.fail('Actually there are present updates!')
        self.assertRaises(IndexError, updates.__getitem__, 3)

        versions = ['Win64', 'Win32']
        for update, version in zip(updates, versions):
            self.assertEqual(version, update['Version'])

        versions = ['Win32', 'Win64']
        for i in range(0, 2):
            self.assertEqual(updates[i]['Version'], versions[i])

        self.assertEqual('Win32', updates[0]['Version'])
        self.assertEqual('Win64', updates[1]['Version'])

    def test_Versions(self):

        versions = core.updates.Versions()

        path = os.sep + 'midle' + os.sep + 'of' + os.sep + 'nowhere' + os.sep
        self.assertEqual({'UNKNOWN VERSION': path}, versions.getVersion(path))
        self.assertEqual(versions.Win2k,
                        versions.getVersion(os.sep + 'Windows2000' + os.sep))

        self.assertEqual(os.sep + os.sep, versions.getPathKey(''))
        self.assertTrue(os.sep + 'Windows2000' + os.sep ==
                         versions.getPathKey(versions.Win2k) or
                        os.sep + 'WINDOWS2000' + os.sep ==
                         versions.getPathKey(versions.Win2k))

    def test_Types(self):

        types = core.updates.Types()

        path = os.sep + 'midle' + os.sep + 'of' + os.sep + 'nowhere' + os.sep
        self.assertEqual({'UNKNOWN TYPE': path}, types.getType(path))
        self.assertEqual(types.x86,
                        types.getType(os.sep + 'x86' + os.sep))

        self.assertEqual(os.sep + os.sep, types.getPathKey(''))
        self.assertTrue(os.sep + 'x86' + os.sep ==
                         types.getPathKey(types.x86) or
                         os.sep + 'X86' + os.sep ==
                         types.getPathKey(types.x86))

    def test_Languages(self):

        languages = core.updates.Languages()

        path = os.sep + 'midle' + os.sep + 'of' + os.sep + 'nowhere' + os.sep
        self.assertEqual({'UNKNOWN LANGUAGE': path},
                            languages.getLanguage(path))
        self.assertEqual(languages.Neutral,
                        languages.getLanguage(os.sep + 'NEU' + os.sep))

        self.assertEqual(os.sep + os.sep, languages.getPathKey(''))
        self.assertTrue(os.sep + 'NEU' + os.sep ==
                         languages.getPathKey(languages.Neutral) or
                         os.sep + 'Neutral' + os.sep ==
                         languages.getPathKey(languages.Neutral))

    #TODO: test_getItemByPath(self):
    #TODO: test_getKeyPathByValue(self):
    #TODO: test_unknownSubstance(self):
    #TODO: test_toPathStyle(self):

    def test_getKB(self):

        files = [os.sep + 'dotNetFW_4.X' + os.sep +
                'dotNetFx40_Full_x86_x64.exe']
        correctKBs = [-1]

        for KB, updateFile in zip(correctKBs, files):
            self.assertEqual(KB, core.updates.getKB(updateFile))

    def test_getUpdatesFromPackage(self):

        paths = ['E:' + os.sep + '1212' + os.sep + '2761465' + os.sep +
            'WindowsServer2003' + os.sep + 'X64' + os.sep + 'ENU' +
            os.sep + 'IE7-WINDOWSSERVER2003.WINDOWSXP-KB2761465-X64-ENU.EXE',
           'E:' + os.sep + '1212' + os.sep + '2761465' + os.sep +
           'WindowsServer2003' + os.sep + 'X64' + os.sep + 'ENU' + os.sep +
           'IE7-WINDOWSSERVER2003.WINDOWSXP-KB2761465-X64-ENU.EXE']
        date = datetime.datetime(2012, 12, 1)
        updates = core.updates.getUpdatesFromPackage(paths, date)

        self.assertEqual(1, len(updates))

        kbs = [2761465]
        versions = [core.updates.Versions().Win2k3]
        types = ['x64']
        languages = ['English']

        for i in range(0, len(updates)):
            self.assertEqual(paths[i], updates[i]['Path'])
            self.assertEqual(kbs[i], updates[i]['KB'])
            self.assertEqual(versions[i], updates[i]['Version'])
            self.assertEqual(types[i], updates[i]['Type'])
            self.assertEqual(languages[i], updates[i]['Language'])
            self.assertEqual(date, updates[i]['Date'])

    def test_getKBsFromReport(self):

        report = ('Definition Update for Windows Defender - KB2267602' +
                ' (Definition 1.155.758.0)' +
                '' +
                'Download size: 78.7 MB' +
                '' +
                'Update type: Important' +
                '' +
                'Install this update to revise the definition files that' +
                ' are used to detect viruses, spyware, and other potentially' +
                ' unwanted software. Once you have installed this item,' +
                ' it cannot be removed.' +
                '' +
                'More information: ' +
                'http://www.microsoft.com/athome/security/spyware/software' +
                '/about/overview.mspx' +
                '' +
                'Help and Support: ' +
                'http://go.microsoft.com/fwlink/?LinkId=52661' +
                '' +
                '' +
                '' +
                'Microsoft Visual Studio 2010 Service Pack 1' +
                '' +
                'Download size: 368.7 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Important' +
                '' +
                'This download installs Visual Studio 2010 Service Pack 1' +
                ' (SP1). This service pack release addresses issues that' +
                ' were found through a combination of customer and partner' +
                ' feedback, as well as internal testing. These service packs' +
                ' offer Visual Studio users improvements in responsiveness' +
                ' and stability, as well as completes some high-impact' +
                ' scenarios requested by customers.' +
                '' +
                'More information: ' +
                'http://go.microsoft.com/fwlink/?linkid=210715' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Security Update for Internet Explorer Flash Player for' +
                ' Windows 8.1 Preview for x64-based Systems (KB2857645)' +
                '' +
                'Download size: 9.7 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Important' +
                '' +
                'This update addresses the vulnerability discussed in' +
                ' Microsoft Security Advisory (KB2857645). Security issues' +
                ' have been identified that could allow an attacker to' +
                ' compromise a computer running Internet Explorer Flash' +
                ' Player for Windows 8.1 Preview and gain control over it.' +
                ' You can help protect your computer by installing this' +
                ' update from Microsoft. After you install this item,' +
                ' you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://go.microsoft.com/fwlink/?LinkId=264959' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Security Update for Microsoft Visual C++ 2008' +
                ' Service Pack 1 Redistributable Package (KB2538243)' +
                '' +
                'Download size: 4.3 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Important' +
                '' +
                'A security issue has been identified leading to' +
                ' MFC application vulnerability in DLL planting due' +
                ' to MFC not specifying the full path to' +
                ' system/localization DLLs.' +
                '  You can protect your computer by installing' +
                ' this update from Microsoft.  After you install this item,' +
                ' you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://go.microsoft.com/fwlink/?LinkId=216803' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Security Update for Microsoft' +
                ' Visual Studio 2010 (KB2542054)' +
                '' +
                'Download size: 264.4 MB' +
                '' +
                'You may need to restart your computer for' +
                ' this update to take effect.' +
                '' +
                'Update type: Important' +
                '' +
                'A security issue has been identified leading to' +
                ' MFC application vulnerability in DLL planting due' +
                ' to MFC not specifying the full path to' +
                ' system/localization DLLs.  You can protect' +
                ' your computer by installing this update from Microsoft.' +
                '  After you install this item, you may have' +
                ' to restart your computer.' +
                '' +
                'More information: ' +
                'http://go.microsoft.com/fwlink/?LinkId=216926' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Microsoft Visual Studio 2012 (KB2781514)' +
                '' +
                'Download size: 1.1 MB' +
                '' +
                'You may need to restart your computer for' +
                ' this update to take effect.' +
                '' +
                'Update type: Important' +
                '' +
                'Users of Visual Studio may lose the ability' +
                ' to open or create C++ or JavaScript files' +
                ' or projects after the .NET Framework 4.5 is updated.' +
                ' This fix corrects the flaw in Visual Studio.' +
                '' +
                'More information: ' +
                'http://go.microsoft.com/fwlink/?LinkID=272586' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2863147)' +
                '' +
                'Download size: 247 KB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install' +
                ' this item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2863147' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2863204)' +
                '' +
                'Download size: 9.3 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2863204' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2863221)' +
                '' +
                'Download size: 917 KB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Important' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install' +
                ' this item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2863221' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2863312)' +
                '' +
                'Download size: 2.0 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Important' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2863312' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2863532)' +
                '' +
                'Download size: 1.7 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Important' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2863532' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2863721)' +
                '' +
                'Download size: 345 KB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2863721' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2863723)' +
                '' +
                'Download size: 2.2 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2863723' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2863846)' +
                '' +
                'Download size: 15.6 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2863846' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2864806)' +
                '' +
                'Download size: 15.6 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2864806' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2864808)' +
                '' +
                'Download size: 6.9 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2864808' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2865946)' +
                '' +
                'Download size: 569 KB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2865946' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2866512)' +
                '' +
                'Download size: 3.2 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2866512' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2866518)' +
                '' +
                'Download size: 15.7 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2866518' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2866537)' +
                '' +
                'Download size: 425 KB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2866537' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2866763)' +
                '' +
                'Download size: 704 KB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2866763' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2867624)' +
                '' +
                'Download size: 268 KB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2867624' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2868208)' +
                '' +
                'Download size: 7.2 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2868208' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2870257)' +
                '' +
                'Download size: 85 KB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2870257' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2871052)' +
                '' +
                'Download size: 1.2 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2871052' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com' +
                '' +
                '' +
                '' +
                'Update for Windows 8.1 Preview for x64-based Systems' +
                ' (KB2871055)' +
                '' +
                'Download size: 15.6 MB' +
                '' +
                'You may need to restart your computer for this update' +
                ' to take effect.' +
                '' +
                'Update type: Recommended' +
                '' +
                'Install this update to resolve issues in Windows.' +
                ' For a complete listing of the issues that are included' +
                ' in this update, see the associated Microsoft Knowledge' +
                ' Base article for more information. After you install this' +
                ' item, you may have to restart your computer.' +
                '' +
                'More information: ' +
                'http://support.microsoft.com/kb/2871055' +
                '' +
                'Help and Support: ' +
                'http://support.microsoft.com')

        kbsCorrect = [2267602, 2857645, 2538243, 2542054,
                      2781514, 2863147, 2863204, 2863221,
                      2863312, 2863532, 2863721, 2863723,
                      2863846, 2864806, 2864808, 2865946,
                      2866512, 2866518, 2866537, 2866763,
                      2867624, 2868208, 2870257, 2871052,
                      2871055]
        kbs = core.updates.getKBsFromReport(report)
        self.assertEqual(kbsCorrect, kbs)


if __name__ == '__main__':

    unittest.main()
