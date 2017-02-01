from pbpgraphsapi import graph_data_generators
import unittest


class TestInitDataset(unittest.TestCase):
    def test_init_dataset_player_name(self):
        result = {"label": "Goran Dragic", "data": [{"x": "00:00", "y": 0, "label": "Start of game"}], "fill": False}
        self.assertDictEqual(graph_data_generators._init_dataset_json('Goran Dragic'), result)

    def test_init_dataset_team_name(self):
        result = {"label": "Phoenix Suns", "data": [{"x": "00:00", "y": 0, "label": "Start of game"}], "fill": False}
        self.assertDictEqual(graph_data_generators._init_dataset_json('Phoenix Suns (team)'), result)

    def test_init_dataset_shared_last_name(self):
        result = {"label": "George Hill", "data": [{"x": "00:00", "y": 0, "label": "Start of game"}], "fill": False}
        self.assertDictEqual(graph_data_generators._init_dataset_json('sharedlastGeorge Hill'), result)
