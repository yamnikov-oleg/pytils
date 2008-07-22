# -*- coding: utf-8 -*-
# pytils - simple processing for russian strings
# Copyright (C) 2006-2008  Yury Yurevich
#
# http://www.pyobject.ru/projects/pytils/
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
"""
Unit-tests for pytils.typo
"""

import unittest
from pytils import typo

def cb_testrule(x):
    return x

class HelpersTestCase(unittest.TestCase):
    """
    Test case for pytils.typo helpers
    """
    def testGetRuleByName(self):
        """
        unit-test for pytils.typo._get_rule_by_name
        """
        self.assert_(
            callable(
                typo._get_rule_by_name('testrule')
        ))
        self.assertEquals(
            'rl_testrule',
            typo._get_rule_by_name('testrule').__name__
        )
    
    def testResolveRule(self):
        """
        unit-test for pytils.typo._resolve_rule
        """
        self.assert_(
            callable(
                typo._resolve_rule_name('testrule')[1]
        ))
        self.assert_(
            callable(
                typo._resolve_rule_name(cb_testrule)[1]
        ))
        self.assertEquals(
            'testrule',
            typo._resolve_rule_name('testrule')[0]
        )
        self.assertEquals(
            'cb_testrule',
            typo._resolve_rule_name(cb_testrule)[0]
        )

    def testResolveRuleWithForcedName(self):
        """
        unit-test for pytils.typo._resolve_rule with forced_name arg
        """
        self.assert_(
            callable(typo._resolve_rule_name('testrule', 'newrule')[1]
        ))
        self.assert_(
            callable(typo._resolve_rule_name(cb_testrule, 'newrule')[1]
        ))
        self.assertEquals(
            'newrule', 
            typo._resolve_rule_name('testrule', 'newrule')[0]
        )
        self.assertEquals(
            'newrule',
            typo._resolve_rule_name(cb_testrule, 'newrule')[0]
        )

class TypographyApplierTestCase(unittest.TestCase):
    """
    Test case for typography rule applier pytils.typo.Typography
    """
    def testExpandEmptyArgs(self):
        self.assertEquals(
            {},
            typo.Typography().rules
        )
        self.assertEquals(
            [],
            typo.Typography().rules_names
        )
    
    def testExpandSimpleStrArgs(self):
        self.assertEquals(
            {'testrule': typo.rl_testrule}, 
            typo.Typography('testrule').rules
        )
        self.assertEquals(
            ['testrule'],
            typo.Typography('testrule').rules_names
        )
    
    def testExpandDictStrArgs(self):
        self.assertEquals(
            {
                'testrule': typo.rl_testrule, 
                'newrule':  typo.rl_testrule
            },
            typo.Typography('testrule', {'newrule': 'testrule'}).rules
        )
        self.assertEquals(
            ['testrule', 'newrule'],
            typo.Typography('testrule', {'newrule': 'testrule'}).rules_names
        )

    def testExpandSimpleCallableArgs(self):
        self.assertEquals(
            {'cb_testrule': cb_testrule},
            typo.Typography(cb_testrule).rules
        )
        self.assertEquals(
            ['cb_testrule'],
            typo.Typography(cb_testrule).rules_names
        )
    
    def testExpandDictCallableArgs(self):
        self.assertEquals(
            {
                'cb_testrule': cb_testrule,
                'newrule': cb_testrule
            }, 
            typo.Typography(cb_testrule, {'newrule': cb_testrule}).rules
        )
        self.assertEquals(
            ['cb_testrule', 'newrule'],
            typo.Typography(cb_testrule, {'newrule': cb_testrule}).rules_names
        )

    def testExpandMixedArgs(self):
        self.assertEquals(
            {
                'cb_testrule': cb_testrule,
                'newrule': typo.rl_testrule
            },
            typo.Typography(cb_testrule, newrule='testrule').rules
        )
        self.assertEquals(
            ['cb_testrule', 'newrule'],
            typo.Typography(cb_testrule, newrule='testrule').rules_names
        )
        self.assertEquals(
            {
                'cb_testrule': cb_testrule,
                'testrule': typo.rl_testrule
            },
            typo.Typography(cb_testrule, 'testrule').rules
        )
        self.assertEquals(
            ['cb_testrule', 'testrule'],
            typo.Typography(cb_testrule, 'testrule').rules_names
        )

    def testRecommendedArgsStyle(self):
        lambdarule = lambda x: x
        self.assertEquals(
            {
                'cb_testrule': cb_testrule,
                'testrule': typo.rl_testrule,
                'newrule': lambdarule
            },
            typo.Typography([cb_testrule], ['testrule'], {'newrule': lambdarule}).rules
        )
        self.assertEquals(
            ['cb_testrule', 'testrule', 'newrule'],
            typo.Typography([cb_testrule], ['testrule'], {'newrule': lambdarule}).rules_names
        )

class RulesTestCase(unittest.TestCase):
    def testCleanspaces(self):
        self.assertEquals(
            u"Точка, точка, запятая, вышла рожица кривая.",
            typo._get_rule_by_name('cleanspaces')(
                u" Точка ,точка , запятая, вышла рожица  кривая . "
            ))
        self.assertEquals(
            u"Точка, точка,\nзапятая,\nвышла рожица кривая.",
            typo._get_rule_by_name('cleanspaces')(
                u" Точка ,точка , \nзапятая,\n вышла рожица  кривая . "
            ))

if __name__ == '__main__':
    unittest.main()
