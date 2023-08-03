# Streamlit Hackathon -- Movie Finder App

This Streamlit app allows you to explore top movies based on genres using The Movie Database (TMDb) API.

## Installation

1. Clone this repository to your local machine.

```bash
git clone https://github.com/your_username/top-movie-over-the-year.git
```

2. open terminal and type the below command

```python
pipenv install
```

3. run the application

```
streamlit run app.py
```

## Usage

1. Upon running the Streamlit app, you will see a list of movie genres in the dropdown menu. Select a movie genre from the list.

2. Click on the "Get Movie" button to view the top movies for the selected genre. Each movie will be displayed along with its title and poster image.

3. If you wish to explore another genre, you can simply select a different genre from the dropdown menu and repeat the steps above.

4. Find the live [project link](https://mfcustomconnection.streamlit.app/)

## Notes

- The app uses The Movie Database (TMDb) API to fetch movie data based on selected genres. The movie data includes movie titles and poster images.

- The app uses a custom TMDbConnection class to interact with the TMDb API. The connection details are provided in the main.py file

## Developed By

- This app was developed by Sumit Dey, as a submission for the **Streamlit Connections Hackathon**.
  Connect with the author on [Github](https://github.com/Tripletesumit/).
