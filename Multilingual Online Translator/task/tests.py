from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

import sys
if sys.platform.startswith("win"):
    import _locale
    # pylint: disable=protected-access
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class TranslatorTest(StageTest):
    def generate(self):
        return [TestCase(stdin='3\n4\nhello')]

    def check(self, reply, attach):
        reply = reply.lower()
        if not ('arabic' in reply and 'turkish' in reply
                and 'spanish translations' in reply and 'hola' in reply):
            return CheckResult.wrong('Try to print out all the languages that your translator can translate.')

        return CheckResult.correct()


if __name__ == '__main__':
    TranslatorTest('translator.translator').run_tests()
