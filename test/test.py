import sys
import os
# jenkins exposes the workspace directory through env.
sys.path.append(os.environ['WORKSPACE'])
import pytest


@pytest.mark.parametrize("one, two, exp",[(1,2,3),(2,5,7),(5,4,1)])
def test_add(one, two, exp):
	res = one + two
	assert res == exp

