import pytest

from game.configs import determine_box_number, get_dimensions_from_height


@pytest.mark.parametrize(
    "x, y, expected_output",
    [
        (629, 632, 77),
        (146, 487, 34),
        (489, 357, 39),
    ],
)
def test_determine_box_number(x, y, expected_output):
    base_dimensions = get_dimensions_from_height(1100)
    output = determine_box_number(base_dimensions, x, y)
    assert output == expected_output
