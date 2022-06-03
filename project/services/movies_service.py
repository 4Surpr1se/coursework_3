from project.container import ITEMS_PER_PAGE
from project.dao.movie import MovieDAO


class MoviesService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, filters):
        if filters.get("page") is not None and filters.get("status") == "new":
            movies = self.dao.get_by_filters(user_offset=int(filters.get("page"))*ITEMS_PER_PAGE,
                                             user_limit=ITEMS_PER_PAGE
                                             )
        elif filters.get("page") is not None:
            movies = self.dao.get_all(user_offset=int(filters.get("page"))*ITEMS_PER_PAGE,
                                      user_limit=ITEMS_PER_PAGE
                                      )
        elif filters.get("status") is not None:
            movies = self.dao.get_by_filters()
        else:
            movies = self.dao.get_all()
        return movies
