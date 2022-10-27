from unittest.mock import MagicMock

import pytest

from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_1 = Movie(id=1, title="Бриллиантовая рука",
                    description="В приморском портовом городе действует банда жуликов под предводительством некоего Шефа.",
                    trailer="https://www.youtube.com/watch?v=_MYPtgu4TV4", year=1969, rating=8.3)
    movie_2 = Movie(id=2, title="Жестокий романс",
                    description="Действие разворачивается на берегу Волги в вымышленном провинциальном городке Бряхимове в 1877—1878 годах.",
                    trailer="https://www.youtube.com/watch?v=A7tjUDUQVcY", year=1984, rating=8.0)
    movie_3 = Movie(id=3, title="Кин-дза-дза!",
                    description="Примерный семьянин и живущий своей работой прораб Владимир Николаевич, и грузинский паренек-студент Гедеван волею судьбы попадают на далекую планету Плюк, что находится в созвездии Кин-дза-дза.",
                    trailer="https://www.youtube.com/watch?v=3XdnlaKQke8", year=1986, rating=8.0)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) == 3
        assert movies[0].title == "Бриллиантовая рука"
        assert movies[1].title == "Жестокий романс"
        assert movies[2].title == "Кин-дза-дза!"

    def test_create(self):
        movie_d = {"title": "Мужики!..",
                   "description": "Узнав о том, что умерла его бывшая невеста, шахтер Павел Зубов приезжает в родное село.",
                   "trailer": "https://www.youtube.com/watch?v=qSWJ5vPTsM8", "year": 1982, "rating": 7.6}

        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(4)

    def test_update(self):
        movie_d = {"id": 2, "title": "Жестокий роман"}

        self.movie_service.update(movie_d)
