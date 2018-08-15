import os
import json
import re
import urllib
from pprint import pprint

main_direcorty_absolute_path = "/Users/diogoverardi/Movies/uncatalogued_movies/" 

def main():
	main_menu()
#	for y in os.walk(main_direcorty_absolute_path):
#		rename_main_folders(y[1])
#		print("\n")
#		break
		

def rename_main_folders(folders_list):
	
	for folder_name in folders_list:
		
		# check for folders already formatted
		if folder_name.find('.') == -1:
			print "The current folder is already formatted:"
			print "    %s" % folder_name
			continue

		
#		original_movie_name 	= folder_name 
#		movie_release_date 		= detected_movie_release_date(original_movie_name)
#		formatted_movie_name 	= format_movie_name(original_movie_name, movie_release_date)
#		movie_director 			= get_movie_director(formatted_movie_name, movie_release_date)
#		
#		new_folder_name = formatted_movie_name + ' - ' + movie_release_date + ' (' + movie_director + ')'
#				
#		print "Original Movie Name: %s" 	% original_movie_name
#		print "Formatted Movie Name: %s"    % formatted_movie_name   
#		print "Release Date: %s" 		 	% movie_release_date
#		print "Movie Director: %s" 		 	% movie_director
#		print "New Title: %s"               % new_title
#		
#		# go to the movies directory
#		os.chdir(main_direcorty_absolute_path)
#		
#		# rename the folder
#		os.rename(folder_name, new_folder_name)
#
#		pprint(new_title)
#		
#		break
		


def format_movie_name(movie_name, release_year):
	
	# split the folder name in two parts and get the one before the release year
	movie_name_pieces = movie_name.split(release_year)[0]
	
	# replaces all the . with blank spaces, and removes the space from the begginig and ending of the title
	formatted_name = movie_name_pieces.replace("."," ").strip()
	
	return formatted_name
		
		
# returns the year when the movie was released or False		
def detected_movie_release_date(movie_name):
	
	# divides the name on each .
	movie_name_pieces = movie_name.split('.')	
			
	# run trought the array until it finds the year in the title
	date = [piece for piece in movie_name_pieces if len(piece) == 4 and re.match('.*([1-2][0-9]{3})', piece)][0]		
	
	return date if date else False		


# returns the director's name or the error message when it occurs
def get_movie_director(movie_name, movie_year):

	url 	= 'http://www.omdbapi.com/'
	api_id 	= 'tt3896198'
	api_key = '7ff45fea'
	
	# format the URL for the JSON Request 
	params_formatted = urllib.urlencode({
		'i': 		api_id,
		'apikey': 	api_key,
		't': 		movie_name,
		'y': 		movie_year,
	})
	
	# put together the URL
	full_url = url + '?' + params_formatted
	
	# get the response data from the request 
	response 	= urllib.urlopen(full_url)
	data 		= json.loads(response.read())
	
	# returns the Error message if it occurs , otherwise the Director's name
	return data['Error'] if data['Response'] == 'False' else data['Director']
	
	
def main_menu():
	print "------- Welcome to the Movie Cataloger -------"
	print "1 - Rename all my current folders"	
	print "2 - Remove all the .txt files"	
	print "3 - Rename all .mkv files"	
	print "4 - Create genres folders (Drama, Action, Horros.....etc...)"	
	
	option = input("What would you like to do? ") 	
	
	return option
	

if __name__ == '__main__':
	main()
	
	