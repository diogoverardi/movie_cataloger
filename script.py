import os
import json
import re
import urllib
from pprint import pprint

main_direcorty_absolute_path = "/Users/diogoverardi/Movies/uncatalogued_movies" 

def rename_main_folders(folders_list):
	
	for folder_name in folders_list:
		movie_release_date 		= detected_movie_release_date(folder_name)
		original_movie_name 	= folder_name 
		formatted_movie_name 	= format_movie_name(original_movie_name, movie_release_date)
		movie_director 			= get_movie_director(formatted_movie_name, movie_release_date)
				
		print "Original Movie Name: %s" 	% original_movie_name
		print "Formatted Movie Name: %s"    % formatted_movie_name   
		print "Release Date: %s" 		 	% movie_release_date
		print "Movie Director: %s" 		 	% movie_director
		print "New Title: %s - %s (%s)"     % (formatted_movie_name, movie_release_date, movie_director)


def format_movie_name(movie_name, release_year):
	
	# split the folder name in two parts and get the one before the release year
	movie_name_pieces = movie_name.split(release_year)[0]
	
	# s
	formatted_name = movie_name_pieces.replace("."," ").strip()
	
	return formatted_name
		
		
def detected_movie_release_date(movie_name):
	
	movie_name_pieces = movie_name.split('.')	
	
	for piece in movie_name_pieces:
		if len(piece) == 4 and re.match('.*([1-2][0-9]{3})', piece):
			return piece
	
	return null		


def get_movie_director(movie_name, movie_year):

	url 	= 'http://www.omdbapi.com/'
	api_id 	= 'tt3896198'
	api_key = '7ff45fea'
	
	params_formatted = urllib.urlencode({
		'i': 		api_id,
		'apikey': 	api_key,
		't': 		movie_name,
		'y': 		movie_year,
	})
	
	full_url = url + '?' + params_formatted
	
	response 	= urllib.urlopen(full_url)
	data 		= json.loads(response.read())

	return data['Director']


for y in os.walk(main_direcorty_absolute_path):
	rename_main_folders(y[1])
	print("\n")
	break
	
	
	