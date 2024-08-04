import unittest
from movie_dataset import MovieDataset

class TestMovieDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = MovieDataset('movies_metadata.csv')

    def test_unique_movies_count(self):
        self.assertGreater(self.dataset.get_unique_movies_count(), 0)

    def test_average_rating(self):
        self.assertGreaterEqual(self.dataset.get_average_rating(), 0)

    def test_top_rated_movies(self):
        top_movies = self.dataset.get_top_rated_movies()
        self.assertEqual(len(top_movies), 5)
        self.assertTrue((top_movies['vote_average'].diff().dropna() <= 0).all())

    def test_movies_per_year(self):
        movies_per_year = self.dataset.get_movies_per_year()
        self.assertGreaterEqual(len(movies_per_year), 1)

    def test_movies_per_genre(self):
        movies_per_genre = self.dataset.get_movies_per_genre()
        self.assertGreaterEqual(len(movies_per_genre), 1)

if __name__ == '__main__':
    unittest.main()

    "python -m unittest discover -s tests"