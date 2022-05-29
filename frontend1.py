import streamlit as st
import pandas as pd
import hashlib
import pickle
import requests
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def main():
	st.title("Welcome to Rendezvous")
	menu = ["Home","Login","SignUp"]
	choice = st.selectbox("Menu",menu)
	if choice == "Home":
		st.subheader("Home")
		st.image('home.jpg')
	elif choice == "Login":
		st.subheader("Login Section")
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)
			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Logged In as {}".format(username))

				def fetch_poster(movie_id):
					url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
						movie_id)
					data = requests.get(url)
					data = data.json()
					poster_path = data['poster_path']
					full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
					return full_path

				def recommend(obj):
					ind = movies[movies['title'] == obj].index[0]
					distances = sorted(list(enumerate(similarity[ind])), reverse=True, key=lambda x: x[1])
					recommended_movie_names = []
					recommended_movie_posters = []
					for i in distances[1:6]:
						# fetch the movie poster
						movie_id = movies.iloc[i[0]].movie_id
						recommended_movie_posters.append(fetch_poster(movie_id))
						recommended_movie_names.append(movies.iloc[i[0]].title)

					return recommended_movie_names, recommended_movie_posters

				st.header('Movie Recommender System')
				st.image('HeaderImg.jpg')
				movies = pickle.load(open('movie_list.pkl', 'rb'))
				similarity = pickle.load(open('similarity.pkl', 'rb'))

				movie_list = movies['title'].values
				selected_movie = st.selectbox(
					"Type or select a movie from the dropdown",
					movie_list
				)

				if st.button('Show Recommendation'):
					recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
					col1, col2, col3, col4, col5 = st.columns(5)
					with col1:
						st.text(recommended_movie_names[0])
						st.image(recommended_movie_posters[0])
					with col2:
						st.text(recommended_movie_names[1])
						st.image(recommended_movie_posters[1])

					with col3:
						st.text(recommended_movie_names[2])
						st.image(recommended_movie_posters[2])
					with col4:
						st.text(recommended_movie_names[3])
						st.image(recommended_movie_posters[3])
					with col5:
						st.text(recommended_movie_names[4])
						st.image(recommended_movie_posters[4])


			else:
				st.warning("Incorrect Username/Password")
	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
if __name__ == '__main__':
	main()