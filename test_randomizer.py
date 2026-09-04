import unittest

import randomizer


class RandomizerTests(unittest.TestCase):
    def test_deck_has_78_unique_cards(self):
        self.assertEqual(len(randomizer.DECK), 78)
        self.assertEqual(len(set(randomizer.DECK)), 78)

    def test_tarot_draw_has_no_duplicates(self):
        result = randomizer.draw_tarot(24)
        cards = result["cards"]
        self.assertEqual(len(cards), 24)
        self.assertEqual(len({card["full_name"] for card in cards}), 24)
        self.assertTrue(all(card["orientation"] in {"正", "逆"} for card in cards))

    def test_each_question_draw_is_independent_shape(self):
        payload = randomizer.package([
            randomizer.make_result("tarot", 5),
            randomizer.make_result("tarot", 5),
            randomizer.make_result("tarot", 6),
        ])
        self.assertEqual([r["tarot"]["count"] for r in payload["results"]], [5, 5, 6])
        for result in payload["results"]:
            cards = result["tarot"]["cards"]
            self.assertEqual(len(cards), len({card["full_name"] for card in cards}))

    def test_plum_contract(self):
        for _ in range(100):
            result = randomizer.cast_plum()
            self.assertRegex(result["a"], r"^\d{3}$")
            self.assertRegex(result["b"], r"^\d{3}$")
            self.assertIn(result["upper_trigram"], set(randomizer.TRIGRAM.values()))
            self.assertIn(result["lower_trigram"], set(randomizer.TRIGRAM.values()))
            self.assertIn(result["hexagram"], set(randomizer.HEXAGRAM.values()))
            self.assertGreaterEqual(result["moving_line"], 1)
            self.assertLessEqual(result["moving_line"], 6)

    def test_all_hexagram_pairs_are_covered(self):
        pairs = {
            upper + lower
            for upper in set(randomizer.TRIGRAM.values())
            for lower in set(randomizer.TRIGRAM.values())
        }
        self.assertEqual(set(randomizer.HEXAGRAM), pairs)

    def test_invalid_tarot_count_rejected(self):
        with self.assertRaises(ValueError):
            randomizer.draw_tarot(0)
        with self.assertRaises(ValueError):
            randomizer.draw_tarot(25)


if __name__ == "__main__":
    unittest.main()
