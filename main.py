import streamlit as st
import requests
from streamlit.connections import ExperimentalBaseConnection

class TMDbConnection(ExperimentalBaseConnection[requests.Session]):

    def __init__(self, connection_name: str, **kwargs):
        super().__init__(connection_name, **kwargs)
        self._resource = self._connect()
    def _connect(self) -> requests.Session:
        return requests.Session()

    def cursor(self):
        return self._resource
    def query(self,genres, ttl: int = 3600):
        def _get_genre_names(api_key, base_url, genre_ids):
            # Fetch genre names
            url = f"{base_url}/genre/movie/list"
            params = {
                "api_key": api_key,
                "language": "en-US"
            }

            response = self._resource.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                genre_data = data.get("genres", [])
                genre_names = [genre.get("name", "N/A") for genre in genre_data if genre.get("id") in genre_ids]
                return genre_names
            else:
                return ["N/A"]
        

        # fetch movie_data in accordence to genre.
        def _get_movies_data(api_key, base_url,genres):

            movies_data = []
            processed_ids = set()

            for genre in genres:
                page = 1
                while True:
                    url = f"{base_url}/discover/movie"
                    params = {
                        "api_key": api_key,
                        "language": "en-US",
                        "with_genres": genre,
                        # "sort_by": "popularity.desc",
                        "page": page
                    }

                    response = self._resource.get(url, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        results = data.get("results", [])
                        if not results:  # Check if results list is empty
                            print(f"No data received for genre {genre}")
                            continue
                        for movie in results:

                            movie_id = movie.get("id")
                            # print(movie.get('title'))
                            if movie_id not in processed_ids:
                                movie_name = movie.get("title")
                                poster_path = movie.get("poster_path")
                                if movie_name and poster_path:
                                    poster_url = f"http://image.tmdb.org/t/p/w500/{poster_path}"
                                    movies_data.append({"title": movie_name, "poster_url": poster_url})
                                    processed_ids.add(movie_id)
                        total_pages = 5
                        # print(total_pages)
                        if page >= total_pages:
                            break
                        else:
                            page += 1
                else:
                    print(f"Error fetching data for genre {genre}: {response.status_code}")
            return movies_data
        api_key = "8c86b08b6e2eceefdebe6bafc3ecea99"
        base_url = "https://api.themoviedb.org/3"
        # Fetch top-rated movies
        if not genres:
            url = f"{base_url}/movie/top_rated"
            params = {
                "api_key": api_key,
                "language": "en-US",
                "page": 1
            }

            response = self._resource.get(url, params=params)
            
            all_data = []
            if response.status_code == 200:
                data = response.json()
                movies = data.get("results", [])
                

                if not movies:
                    st.warning("No movies found.")
                    return

                for movie in movies[:50]:
                    temp_data = {}
                    movie_title = movie.get("title", "N/A")
                    genre_ids = movie.get("genre_ids", [])
                    genre_names = _get_genre_names(api_key, base_url, genre_ids)
                    temp_data["title"] = movie_title
                    temp_data["poster"] = movie.get("poster_path","N/A")
                    temp_data["genre"] = genre_names
                    all_data.append(temp_data)
                    # st.write(f"{movie_title} - {', '.join(genre_names)}")
                # print(all_data)
                return {"data":all_data}
        else:
            return _get_movies_data(api_key=api_key,base_url=base_url,genres=genres)
    
    def _get_genre_list(self,api_key, base_url) -> list:
            url = f"{base_url}/movie/top_rated"
            param = {
                "api_key": api_key,
                "language":"en-US",
                "page":1
            }
            response1 = self._resource.get(url, params=param)
            url = f"{base_url}/genre/movie/list"
            params = {
                "api_key": api_key,
                "language": "en-US"
            }
            response2 = self._resource.get(url, params=param)
            
            
            genre_list = []
            if(response1.status_code == 200 and response2.status_code == 200):
                data1 = response1.json()
                data2 = response2.json()
                movies = data1.get("results",[])

                for movie in movies:
                    genre_ids = movie.get("genre_ids",[])
                    genre_data = data2.get("genres", [])
                    genre_names = [genre.get("name", "N/A") for genre in genre_data if genre.get("id") in genre_ids]
                    if genre_names not in genre_list:
                        genre_list.append(genre_names)
            # return the movie list
            return genre_list
        



