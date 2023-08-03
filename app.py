import streamlit as st
from main import TMDbConnection


def app():
    st.title("MOVIE FINDER APPICATION")
    
    tmdb_conn = TMDbConnection(connection_name="tmdb_api")
    
    
    st.markdown("Enter movie genres name")
    st.markdown("Developed by Sumit Dey")
    
    movie_list = tmdb_conn._get_genre_list("8c86b08b6e2eceefdebe6bafc3ecea99","https://api.themoviedb.org/3")
    
    movie = st.selectbox("Enter a movie name from the below list",[", ".join(sublist)for sublist in movie_list])
    genre_input = []
    if st.button("Get Movie"):
        genre_input = movie.split(',')
        data = tmdb_conn.query(genre_input)     
        l = len(data)
        col_count = 5
        num_rows = (l + col_count - 1) // col_count
        for row in range(num_rows):
            cols = st.columns(col_count)
            for col in cols:
                index = row * col_count + cols.index(col)
                if index < l:
                    movie = data[index]
                    title = movie.get("title", "N/A")
                    poster_path = movie.get("poster_url", "N/A")
                    col.text(title)
                    col.image(poster_path)
                else:
                    break
    else:
        st.title("TOP MOVIES OVER THE YEAR")
        data = tmdb_conn.query(genre_input)
        movies_data = data.get("data","N/A")
        l = len(movies_data)
        col_count = 5
        num_rows = (l + col_count - 1) // col_count
        for row in range(num_rows):
            cols = st.columns(col_count)
            for col in cols:
                index = row * col_count + cols.index(col)
                if index < l:
                    movie = movies_data[index]
                    title = movie.get("title", "N/A")
                    poster_path = "http://image.tmdb.org/t/p/w500/" + movie.get("poster", "N/A")
                    col.text(title)
                    col.image(poster_path)
                else:
                    break

            

    




    

if __name__ == "__main__":
    app()