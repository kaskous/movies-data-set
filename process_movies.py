from movie_dataset import MovieDataset
import logging

def main():
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

if __name__ == "__main__":
    main()