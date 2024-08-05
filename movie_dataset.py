import pandas as pd
import logging
from typing import Dict, List
from movie import Movie


class MovieDataset:
    def __init__(self, file_path: str):
        """
        Initialize the MovieDataset with a CSV file.

        :param file_path: Path to the CSV file containing movie data.
        """
        self.file_path = file_path
        self.df = self.load_data()

    def load_data(self) -> pd.DataFrame:
        """
        Load data from the CSV file.

        :return: DataFrame containing movie data.
        """
        logging.info(f"Loading data from {self.file_path}")
        try:
            df = pd.read_csv(self.file_path)
            logging.info("Data loaded successfully")
            return df
        except FileNotFoundError:
            logging.error(f"File {self.file_path} not found.")
            raise

    def _row_to_movie(self, row: pd.Series) -> Movie:
        """
        Convert a row from the DataFrame to a Movie object.

        :param row: A row of the DataFrame.
        :return: A Movie object.
        """
        return Movie(
            title=str(row["title"]),
            release_date=str(row["release_date"]),
            vote_average=float(row["vote_average"]),
            genres=self._parse_genres(str(row["genres"])),
            overview=str(row["overview"]),
        )

    def _parse_genres(self, genres_str: str) -> List[str]:
        """
        Parse the genres string into a list of genre names.

        :param genres_str: A string representation of the genres.
        :return: A list of genre names.
        """
        genres_list = eval(genres_str)
        return (
            [genre["name"] for genre in genres_list]
            if isinstance(genres_list, list)
            else []
        )
    
    def get_average_rating(self) -> float:
        """
        Return the average rating of all movies.

        :return: Average rating as a float.
        """
        return self.df["vote_average"].mean()

    def get_unique_movies_count(self) -> int:
        """
        Return the number of unique movies in the dataset.

        :return: Number of unique movie titles.
        """
        return self.df["title"].nunique()

    def get_top_rated_movies(self, top_n: int = 5) -> List[Movie]:
        """
        Return the top N highest rated movies.

        :param top_n: Number of top rated movies to return. Default is 5.
        :return: A list of top N highest rated Movie objects.
        """
        sorted_df = self.df[["title", "vote_average"]].sort_values(
            by="vote_average", ascending=False
        )
        top_rated_df = sorted_df.head(top_n)
        merged_df = top_rated_df.merge(self.df, on=["title", "vote_average"])
        top_rated_movies = [self._row_to_movie(row) for _, row in merged_df.iterrows()]
        return top_rated_movies

    def get_movies_per_year(self) -> Dict[int, int]:
        """
        Return the number of movies released each year.

        :return: Dictionary with years as keys and number of movies as values.
        """
        self.df["release_year"] = pd.to_datetime(
            self.df["release_date"], errors="coerce"
        ).dt.year
        self.df = self.df.dropna(subset=["release_year"])
        self.df["release_year"] = self.df["release_year"].astype(int)
        movies_per_year = self.df["release_year"].value_counts().sort_index()
        return movies_per_year.to_dict()

    def get_movies_per_genre(self) -> Dict[str, int]:
        """
        Return the number of movies in each genre.

        :return: Dictionary with genres as keys and number of movies as values.
        """
        self.df["genres"] = self.df["genres"].apply(
            eval
        )  # Convert string representation of list of dicts to actual list of dicts
        genres_exploded_df = self.df.explode("genres")
        genres_exploded_df["genre"] = genres_exploded_df["genres"].apply(
            lambda x: x["name"] if isinstance(x, dict) else None
        )
        movies_per_genre_series = genres_exploded_df["genre"].value_counts()
        movies_per_genre_dict = movies_per_genre_series.to_dict()
        return movies_per_genre_dict

    def save_to_json(self, output_file: str):
        """
        Save the dataset to a JSON file.

        :param output_file: Path to the output JSON file.
        """
        self.df.to_json(output_file, orient="records", lines=True)
        logging.info(f"Data saved to {output_file}")
