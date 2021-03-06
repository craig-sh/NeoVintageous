from collections import namedtuple

from NeoVintageous.vi.utils import modes

from NeoVintageous.tests import set_text
from NeoVintageous.tests import add_sel
from NeoVintageous.tests import get_sel
from NeoVintageous.tests import first_sel
from NeoVintageous.tests import ViewTest


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected msg')

TESTS = (
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 1}, 'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 1}, 'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 2}, 'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 2}, 'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 3}, 'abc abc abc',         'should join 3 lines'),
    test_data('abc\n    abc\n    abc',                   [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 3}, 'abc abc abc',         'should join 3 lines'),
    test_data('abc\nabc\nabc\nabc\nabc',                 [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 5}, 'abc abc abc abc abc', 'should join 5 lines'),
    test_data('abc\n    abc\n    abc\n    abc\n    abc', [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 5}, 'abc abc abc abc abc', 'should join 5 lines'),
    test_data('abc\n\n',                                 [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 3}, 'abc ',                'should join 3 lines and add one trailing space'),
    test_data('\n\nabc',                                 [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 3}, 'abc',                 'should join 3 lines without adding any spaces'),
    test_data('abc \n    abc  \n  abc',                  [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 3}, 'abc abc  abc',        'should join 3 lines with leading spaces removed but trailing spaces intact'),
    test_data('   abc\nabc   ',                          [[(0, 0), (0, 0)]],                   {'mode': modes.INTERNAL_NORMAL, 'count': 1}, '   abc abc   ',       'should join 2 lines with leading spaces of first line and trailing spaces of last line intact'),
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 1)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 1)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 1)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 1)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\nabc\nabc',                           [[(0, 1), (0, 0)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\n    abc\nabc',                       [[(0, 1), (0, 0)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\nabc\nabc',                           [[(0, 1), (0, 0)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\n    abc\nabc',                       [[(0, 1), (0, 0)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\nabc\nabc',                           [[(0, 0), (1, 1)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\n    abc\nabc',                       [[(0, 0), (1, 1)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\nabc\nabc',                           [[(1, 1), (0, 0)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\n    abc\nabc',                       [[(1, 1), (0, 0)]],                   {'mode': modes.VISUAL},                       'abc abc\nabc',        'should join 2 lines'),
    test_data('abc\nabc\nabc',                           [[(0, 0), (2, 1)]],                   {'mode': modes.VISUAL},                       'abc abc abc',         'should join 3 lines'),
    test_data('abc\n    abc\nabc',                       [[(0, 0), (2, 1)]],                   {'mode': modes.VISUAL},                       'abc abc abc',         'should join 3 lines'),
    test_data('abc\nabc\nabc',                           [[(2, 1), (0, 0)]],                   {'mode': modes.VISUAL},                       'abc abc abc',         'should join 3 lines'),
    test_data('abc\n    abc\nabc',                       [[(2, 1), (0, 0)]],                   {'mode': modes.VISUAL},                       'abc abc abc',         'should join 3 lines'),
    test_data('abc\nabc\nabc',                           [[(0, 0), (1, 1)]],                   {'mode': modes.VISUAL, 'count': 3},           'abc abc\nabc',        'should join 2 lines - count shouldn\'t matter'),
    test_data('abc\n    abc\nabc',                       [[(0, 0), (1, 1)]],                   {'mode': modes.VISUAL, 'count': 3},           'abc abc\nabc',        'should join 2 lines - count shouldn\'t matter'),
    test_data('   abc\nabc   ',                          [[(0, 0), (1, 5)]],                   {'mode': modes.VISUAL},                       '   abc abc   ',       'should join 2 lines with leading spaces of first line and trailing spaces of last line intact'),
    test_data('    abc\n\n\n',                           [[(0, 0), (3, 0)]],                   {'mode': modes.VISUAL_LINE},                  '    abc \n',          'should join 4 lines'),
    test_data('    abc  \n   abc\nabc',                  [[(0, 0), (0, 1)], [(1, 0), (1, 1)]], {'mode': modes.VISUAL_BLOCK},                 '    abc  abc\nabc',   'should join 2 lines'),
)


class Test_vi_big_j(ViewTest):
    def testAll(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.view.sel().clear()

            self.write(data.initial_text)
            for region in data.regions:
                add_sel(self.view, self.R(*region))

            self.view.run_command('_vi_big_j', data.cmd_params)

            actual = self.view.substr(self.R(0, self.view.size()))
            msg = "[{0}] {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)
