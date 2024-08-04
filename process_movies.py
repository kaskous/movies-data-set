import logging
from movie_dataset import MovieDataset


def main():
    logging.basicConfig(level=logging.INFO)
    dataset = MovieDataset("movies_metadata.csv")

    unique_movies = dataset.get_unique_movies_count()
    top_rated_movies = dataset.get_top_rated_movies()
    movies_per_year = dataset.get_movies_per_year()
    movies_per_genre = dataset.get_movies_per_genre()

    output = (
        f"Number of unique movies: {unique_movies}\n"
        f"Average rating of all movies: {dataset.get_average_rating():.2f}\n"
        f"Top 5 highest rated movies:\n"
        + "\n".join(str(movie) for movie in top_rated_movies)
        + "\n"
        f"Number of movies released each year:\n{movies_per_year}\n"
        f"Number of movies in each genre:\n{movies_per_genre}"
    )

    print(output)
    dataset.save_to_json("movies_metadata.json")


if __name__ == "__main__":
    main()
