from dataclasses import dataclass


@dataclass
class Movie:
    title: str
    release_date: str
    vote_average: float
    genres: list
    overview: str

    def __str__(self):
        return f"Title: {self.title}, Release Date: {self.release_date}, Rating: {self.vote_average}, Genres: {', '.join(self.genres)}, Overview: {self.overview}"
