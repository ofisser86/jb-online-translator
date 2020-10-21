from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

import sys
import os

if sys.platform.startswith("win"):
    import _locale

    # pylint: disable=protected-access
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class TranslatorTest(StageTest):
    def generate(self):
        return [TestCase(stdin='3\n0\nhello')]

    def check(self, reply, attach):
        reply = reply.lower()

        if 'arabic translations' not in reply:
            return CheckResult.wrong("There are no \'Arabic translations\' in your output!")
        if 'arabic examples' not in reply:
            return CheckResult.wrong("There are no \'Arabic examples\' in your output!")
        if 'russian translations' not in reply:
            return CheckResult.wrong("There are no \'Russian translations\' in your output!")
        if 'russian examples' not in reply:
            return CheckResult.wrong("There are no \'Russian examples\' in your output!")

        file_name = 'hello.txt'

        if not os.path.exists(file_name):
            return CheckResult.wrong(
                "Looks like you didn't create a file named WORD.txt where WORD is word you want to translate.")

        with open(file_name) as file:
            output = file.read().lower()
            if 'spanish translation' not in output:
                return CheckResult.wrong("There are no \'Spanish translations\' in the output file!")
            if 'spanish example' not in output:
                return CheckResult.wrong("There are no \'Spanish examples\' in the output file!")
            if 'turkish example' not in output:
                return CheckResult.wrong("There are no \'Turkish examples\' in the output file!")

        return CheckResult.correct()


if __name__ == '__main__':
    TranslatorTest('translator.translator').run_tests()
