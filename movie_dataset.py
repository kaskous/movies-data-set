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
            logging.exception(f"File {self.file_path} not found.")
            raise
        except pd.errors.EmptyDataError:
            logging.exception(f"File {self.file_path} is empty.")
            raise
        except pd.errors.ParserError:
            logging.exception(f"File {self.file_path} could not be parsed.")
            raise
        except Exception as e:
            logging.exception(f"An unexpected error occurred while loading the file: {e}")
            raise

    def _row_to_movie(self, row: pd.Series) -> Movie:
        """
        Convert a row from the DataFrame to a Movie object.

        :param row: A row of the DataFrame.
        :return: A Movie object.
        """
        try:
            movie = Movie(
                title=str(row["title"]),
                release_date=str(row["release_date"]),
                vote_average=float(row["vote_average"]),
                genres=self._parse_genres(str(row["genres"])),
                overview=str(row["overview"]),
            )
            return movie
        except KeyError as e:
            logging.exception(f"Missing key in data row: {e}")
            raise
        except Exception as e:
            logging.exception(f"Error converting row to Movie: {e}")
            raise

    def _parse_genres(self, genres_str: str) -> List[str]:
        """
        Parse the genres string into a list of genre names.

        :param genres_str: A string representation of the genres.
        :return: A list of genre names.
        """
        try:
            genres_list = eval(genres_str)
            parsed_genres = (
                [genre["name"] for genre in genres_list]
                if isinstance(genres_list, list)
                else []
            )
            return parsed_genres
        except (SyntaxError, TypeError) as e:
            logging.exception(f"Error parsing genres string: {e}")
            return []

    def get_average_rating(self) -> float:
        """
        Return the average rating of all movies.

        :return: Average rating as a float.
        """
        try:
            average_rating = self.df["vote_average"].mean()
            return average_rating
        except KeyError as e:
            logging.exception(f"Missing key in data: {e}")
            raise
        except Exception as e:
            logging.exception(f"Error calculating average rating: {e}")
            raise

    def get_unique_movies_count(self) -> int:
        """
        Return the number of unique movies in the dataset.

        :return: Number of unique movie titles.
        """
        try:
            unique_count = self.df["title"].nunique()
            return unique_count
        except KeyError as e:
            logging.exception(f"Missing key in data: {e}")
            raise
        except Exception as e:
            logging.exception(f"Error counting unique movies: {e}")
            raise

    def get_top_rated_movies(self, top_n: int = 5) -> List[Movie]:
        """
        Return the top N highest rated movies.

        :param top_n: Number of top rated movies to return. Default is 5.
        :return: A list of top N highest rated Movie objects.
        """
        try:
            sorted_df = self.df[["title", "vote_average"]].sort_values(
                by="vote_average", ascending=False
            )
            top_rated_df = sorted_df.head(top_n)
            merged_df = top_rated_df.merge(self.df, on=["title", "vote_average"])
            top_rated_movies = [self._row_to_movie(row) for _, row in merged_df.iterrows()]
            logging.info(f"Top {top_n} rated movies retrieved.")
            return top_rated_movies
        except KeyError as e:
            logging.exception(f"Missing key in data: {e}")
            raise
        except Exception as e:
            logging.exception(f"Error retrieving top rated movies: {e}")
            raise

    def get_movies_per_year(self) -> Dict[int, int]:
        """
        Return the number of movies released each year.

        :return: Dictionary with years as keys and number of movies as values.
        """
        try:
            self.df["release_year"] = pd.to_datetime(
                self.df["release_date"], errors="coerce"
            ).dt.year
            self.df = self.df.dropna(subset=["release_year"])
            self.df["release_year"] = self.df["release_year"].astype(int)
            movies_per_year = self.df["release_year"].value_counts().sort_index()
            logging.info("Movies per year calculated.")
            return movies_per_year.to_dict()
        except KeyError as e:
            logging.exception(f"Missing key in data: {e}")
            raise
        except Exception as e:
            logging.exception(f"Error calculating movies per year: {e}")
            raise

    def get_movies_per_genre(self) -> Dict[str, int]:
        """
        Return the number of movies in each genre.

        :return: Dictionary with genres as keys and number of movies as values.
        """
        try:
            self.df["genres"] = self.df["genres"].apply(eval)
            genres_exploded_df = self.df.explode("genres")
            genres_exploded_df["genre"] = genres_exploded_df["genres"].apply(
                lambda x: x["name"] if isinstance(x, dict) else None
            )
            movies_per_genre_series = genres_exploded_df["genre"].value_counts()
            movies_per_genre_dict = movies_per_genre_series.to_dict()
            logging.info("Movies per genre calculated.")
            return movies_per_genre_dict
        except KeyError as e:
            logging.exception(f"Missing key in data: {e}")
            raise
        except Exception as e:
            logging.exception(f"Error calculating movies per genre: {e}")
            raise

    def save_to_json(self, output_file: str):
        """
        Save the dataset to a JSON file.

        :param output_file: Path to the output JSON file.
        """
        try:
            self.df.to_json(output_file, orient="records", lines=True)
            logging.info(f"Data saved to {output_file}")
        except Exception as e:
            logging.exception(f"Error saving data to JSON: {e}")
            raise
