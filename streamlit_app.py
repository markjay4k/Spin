from red import Database
import streamlit as st


def display_images_in_grid(image_urls):
    cols = st.columns(5)
    for index, url in enumerate(image_urls):
        with cols[index % 5]:  
            st.image(url)


def cover_urls(genre):
    db = Database()
    movies = db.get_movies_by_genre(genre=genre)
    urls = []
    for movie in movies:
        try:
            urls.append(movie['full-size cover url'])
        except KeyError as error:
            print(movie['title'])
    return urls


def main():
    image_urls = cover_urls('horror')
    st.title('horror movies')
    display_images_in_grid(image_urls)


if __name__ == "__main__":
    main()
