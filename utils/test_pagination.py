from unittest import TestCase
from utils.pagnation import make_pagination_range


class PagnationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_firts_range_is_static_if_current_page_is_less_than_half(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_sure_middle_ranges_are_corretct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=17,
        )['pagination']
        self.assertEqual([16, 17, 18, 19], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
