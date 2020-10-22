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
        return [
            TestCase(args=['english', 'all', 'brrrrrrrrrrr'], check_function=self.check1),
            TestCase(args=['english', 'korean', 'hello'], check_function=self.check2)
        ]

    def check1(self, reply, attach):
        reply = reply.lower()
        if 'unable' not in reply:
            return CheckResult.wrong('You didn\'t do a test for a nonexistent word.')
        return CheckResult.correct()

    def check2(self, reply, attach):
        if 'support korean' in reply.lower():
            return CheckResult.correct()

        return CheckResult.wrong(
            'You didn\'t correctly write that your program doesn\'t support a particular language.')


if __name__ == '__main__':
    TranslatorTest('translator.translator').run_tests()
