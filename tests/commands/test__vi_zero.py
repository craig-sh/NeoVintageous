from collections import namedtuple

from VintageousPlus.vi.utils import modes

from VintageousPlus.tests import set_text
from VintageousPlus.tests import add_sel
from VintageousPlus.tests import get_sel
from VintageousPlus.tests import first_sel
from VintageousPlus.tests import second_sel
from VintageousPlus.tests import ViewTest


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected actual_func msg')

TESTS = (
    test_data('abc',      [[(0, 2), (0, 2)]], {'mode': modes.NORMAL}, [(0, 0), (0, 0)], first_sel, ''),
    test_data('abc',      [[(0, 2), (0, 2)]], {'mode': modes.INTERNAL_NORMAL}, [(0, 2), (0, 0)], first_sel, ''),
    test_data('abc\nabc', [[(0, 2), (1, 3)]], {'mode': modes.VISUAL},           [(0, 2), (1, 1)], first_sel, ''),
    test_data('abc\nabc', [[(1, 3), (0, 2)]], {'mode': modes.VISUAL},           [(1, 3), (0, 0)], first_sel, ''),

    # TODO: Test multiple sels.
)


class Test__vi_zero(ViewTest):
    def testAll(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.view.sel().clear()

            set_text(self.view, data.initial_text)
            for region in data.regions:
                add_sel(self.view, self.R(*region))

            self.view.run_command('_vi_zero', data.cmd_params)

            msg = "[{0}] {1}".format(i, data.msg)
            actual = data.actual_func(self.view)
            self.assertEqual(self.R(*data.expected), actual, msg)
