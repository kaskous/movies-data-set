import pandas as pd
import logging
from typing import List

class MovieDataset:
    def __init__(self, csv_file: str):
        """
        Initialize the MovieDataset with a CSV file.

        :param csv_file: Path to the CSV file containing movie data.
        """
        self.csv_file = csv_file
        self.df = None
        self.load_data()

    def load_data(self):
        """
        Load the dataset from a CSV file into a pandas DataFrame.
        """
        try:
            self.df = pd.read_csv(self.csv_file)
            logging.info("Data loaded successfully from %s", self.csv_file)
        except FileNotFoundError:
            logging.error("File %s not found.", self.csv_file)
            raise
        except Exception as e:
            logging.error("Error loading data: %s", e)
            raise

    def get_unique_movies_count(self) -> int:
        """
        Return the number of unique movies in the dataset.

        :return: Number of unique movie titles.
        """
        return self.df['title'].nunique()

    def get_average_rating(self) -> float:
        """
        Return the average rating of all movies.

        :return: Average rating as a float.
        """
        return self.df['vote_average'].mean()

    def get_top_rated_movies(self, top_n: int = 5) -> pd.DataFrame:
        """
        Return the top N highest rated movies.

        :param top_n: Number of top rated movies to return. Default is 5.
        :return: DataFrame containing the top N highest rated movies.
        """
        return self.df[['id','title', 'vote_average']].sort_values(by='vote_average', ascending=False).head(top_n)

    def get_movies_per_year(self) -> pd.Series:
        """
        Return the number of movies released each year.

        :return: Series with years as index and number of movies as values.
        """
        self.df['release_year'] = pd.to_datetime(self.df['release_date'], errors='coerce').dt.year
        return self.df['release_year'].value_counts().sort_index()

    def get_movies_per_genre(self) -> pd.Series:
        """
        Return the number of movies in each genre.

        :return: Series with genres as index and number of movies as values.
        """
        self.df['genres'] = self.df['genres'].apply(eval)  # Convert string representation of list of dicts to actual list of dicts
        genres_exploded = self.df.explode('genres')
        genres_exploded['genre'] = genres_exploded['genres'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
        return genres_exploded['genre'].value_counts()

    def save_to_json(self, json_file: str):
        """
        Save the dataset to a JSON file.

        :param json_file: Path to the JSON file where the data will be saved.
        """
        self.df.to_json(json_file, orient='records', lines=True)
        logging.info("Data saved to %s", json_file)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dataset = MovieDataset('movies_metadata.csv')
    print(f"Number of unique movies: {dataset.get_unique_movies_count()}")
    print(f"Average rating of all movies: {dataset.get_average_rating()}")
    print("Top 5 highest rated movies:")
    print(dataset.get_top_rated_movies())
    print("Number of movies released each year:")
    print(dataset.get_movies_per_year())
    print("Number of movies in each genre:")
    print(dataset.get_movies_per_genre())
    dataset.save_to_json('movies_metadata.json')
