from unittest import TestCase

from gs1.compress.utils import *


class TestUtilFunctions(TestCase):
    """Test util functions of the compression package."""
    def test_find_candidates_from_table_opt(self):
        """Test finding candidates from optimization table."""
        exist_list = find_candidates_from_table_opt(["01", "22", "3102"])
        self.assertEqual(exist_list.get('0A'), 4)
        self.assertEqual(len(exist_list), 2)

    def test_find_best_optimization_candidate(self):
        """Test finding the best optimization candidate."""
        candidates_normal = {"0A": 2}
        candidates_abnormal = {'2B': -1}
        self.assertEqual(
            find_best_optimization_candidate(candidates_normal), '0A')
        self.assertEqual(
            find_best_optimization_candidate(candidates_abnormal), '')

    def test_remove_optimized_key_from_ai_list(self):
        """Test removing optimized key from application identifier list."""
        key_list = ['0A']
        candidates = {'s': '0A'}
        candidate_wrong = {'s': 'b'}
        self.assertEqual(
            remove_optimized_key_from_ai_list(key_list, candidate_wrong),
            ['0A'])
        self.assertEqual(
            remove_optimized_key_from_ai_list(key_list, candidates), [])

    def test_separate_id_non_id(self):
        """Test separate a GS1 identifier dict."""
        gs1_dict = {"10": "2010005828", "21": "xyz1234", "01": "09421902960055"}
        result = separate_id_non_id(gs1_dict)
        self.assertEqual(result.get('ID').get('01'), '09421902960055')
        self.assertEqual(result.get('nonID').get('10'), '2010005828')
        self.assertEqual(result.get('nonID').get('21'), 'xyz1234')
