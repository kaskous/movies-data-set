import unittest
import os
from movie_dataset import (
    MovieDataset,
    Movie,
)

class TestMovieDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = MovieDataset("movies_metadata.csv")

    def test_load_data(self):
        self.assertFalse(
            self.dataset.df.empty, "DataFrame should not be empty after loading data"
        )

    def test_unique_movies_count(self):
        self.assertGreater(
            self.dataset.get_unique_movies_count(),
            0,
            "There should be at least one unique movie",
        )

    def test_average_rating(self):
        self.assertGreaterEqual(
            self.dataset.get_average_rating(),
            0,
            "Average rating should be non-negative",
        )

    def test_top_rated_movies(self):
        top_movies = self.dataset.get_top_rated_movies()
        self.assertEqual(
            len(top_movies), 5, "There should be exactly 5 top rated movies"
        )

    def test_movies_per_year(self):
        movies_per_year = self.dataset.get_movies_per_year()
        self.assertIsInstance(movies_per_year, dict, "The result should be a dictionary")
        self.assertGreaterEqual(
            len(movies_per_year),
            1,
            "There should be movies released in at least one year",
        )
        for year, count in movies_per_year.items():
            self.assertIsInstance(year, int, "Year should be an integer")
            self.assertIsInstance(count, int, "Movie count should be an integer")

    def test_movies_per_genre(self):
        movies_per_genre = self.dataset.get_movies_per_genre()
        self.assertIsInstance(movies_per_genre, dict, "The result should be a dictionary")
        self.assertGreaterEqual(
            len(movies_per_genre), 1, "There should be at least one genre with movies"
        )
        for genre, count in movies_per_genre.items():
            self.assertIsInstance(genre, str, "Genre should be a string")
            self.assertIsInstance(count, int, "Movie count should be an integer")

    def test_movie_parsing(self):
        first_movie = self.dataset._row_to_movie(self.dataset.df.iloc[0])
        self.assertIsInstance(
            first_movie, Movie, "Parsed movie should be an instance of Movie"
        )
        self.assertIsInstance(first_movie.title, str, "Movie title should be a string")
        self.assertIsInstance(
            first_movie.release_date, str, "Movie release date should be a string"
        )
        self.assertIsInstance(
            first_movie.vote_average, float, "Movie vote average should be a float"
        )
        self.assertIsInstance(first_movie.genres, list, "Movie genres should be a list")
        self.assertIsInstance(
            first_movie.overview, str, "Movie overview should be a string"
        )

    def test_save_to_json(self):
        output_file = "test_movies_metadata.json"
        self.dataset.save_to_json(output_file)
        self.assertTrue(os.path.exists(output_file), "JSON file should be created")
        os.remove(output_file)


if __name__ == "__main__":
    unittest.main()
