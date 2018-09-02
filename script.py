import os,json,re,urllib
from pprint import pprint

main_directory_absolute_path 	= ""
extensions_to_delete 			= ['.dat','.txt','.jpg','.jpeg'] 
extensions_to_rename 			= ['.mkv', '.mp4', '.mov'] 
config_file 					= 'config.txt'
		

def rename_main_folders(folders_list):
	
	for folder_name in folders_list:
		
		# check for folders already formatted
		if folder_name.find('.') == -1:
			print "The current folder is already formatted:"
			print "    %s" % folder_name
			continue

		# invalid folde or file
		if folder_name.find('.') == 0:
			continue

		original_movie_name 	= folder_name 
		movie_release_date 		= detected_movie_release_date(original_movie_name)
		formatted_movie_name 	= format_movie_name(original_movie_name, movie_release_date)
		movie_director 			= get_movie_director(formatted_movie_name, movie_release_date).replace(".","").strip()
		
		new_folder_name = formatted_movie_name + ' - ' + movie_release_date + ' (' + movie_director + ')'
				
		print "-------------------------------"		
		print "Original Movie Name: %s" 	% original_movie_name
		print "Formatted Movie Name: %s"    	% formatted_movie_name   
		print "Release Date: %s" 	 	% movie_release_date
		print "Movie Director: %s" 		% movie_director
		print "New Title: %s"       	    	% new_folder_name
		print "-------------------------------"	
		
		# go to the movies directory
		os.chdir(os.path.abspath(main_directory_absolute_path))
		
		# rename the folder
		try:
			os.rename(folder_name, new_folder_name)
		except OSError:
			print("Oops! An error occured when trying to rename the folder")


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
	
	# return 'Unknown' if director's name is unavailable, otherwise the Director's name		
	return 'Unknown' if data['Response'] == 'False' or data['Director'] == 'N/A' else data['Director'] 	
	
	
# make it recursive to go into all sub-directories	
def remove_unnecessary_files(directory, is_sub_directory = False):
	
	parent_directory = os.listdir(directory)

	for file in parent_directory:

		file_absolute_path = directory + '/' + file
			
		# recursive function for going inside the folders and deleting it there
		if os.path.isdir(file_absolute_path) and is_sub_directory == False:
			remove_unnecessary_files(file_absolute_path, True)

		# actually deleting the files
		if file.endswith(tuple(extensions_to_delete)):
			try:
				os.remove(file_absolute_path)
				print "removing (%s)" % file_absolute_path
			except OSError:
				print "Oops! An error occured when trying to delete the file (%s)" % file_absolute_path


def rename_movie_files(directory, folder_name = None, is_sub_directory = False):
	
	parent_directory = os.listdir(directory)

	for file in parent_directory:

		folder_absolute_path = directory + '/' + file
		
		if os.path.isdir(folder_absolute_path) and is_sub_directory == False:
			rename_movie_files(folder_absolute_path, file, True)
		
		# actually renaming the files
		if file.endswith(tuple(extensions_to_rename)):
			
			file_with_extension = directory + '/' + folder_name + os.path.splitext(file)[-1].lower()
			
			try:
				os.rename(folder_absolute_path, file_with_extension)
				print "renaming from (%s) to (%s)" % (folder_absolute_path, folder_name)
			except OSError:
				print "Oops! An error occured when trying to rename the file (%s)" % folder_absolute_path	
			
		
def set_absolute_path():
	
	# open the file and read it
	file = open(config_file, "r").read()
	
	if 'FOLDER_PATH=' not in file:
		print 'File does not contain the right declaration!'
		print 'The first line should be like this:'
		print 'FOLDER_PATH="{absolute_path_to_movies_folder_here}"'
		quit()

	path = absolute_path 	= re.search('"(.+?)"', file).group(1)
	absolute_path 			= absolute_path if os.path.isdir(absolute_path) == True else False
	
	if absolute_path == False:
		print 'path (%s) not valid!' % path
		quit()
		
	# change the value of the global variable
	global main_directory_absolute_path
	main_directory_absolute_path = absolute_path
	
	
def main():
	
	set_absolute_path()
		
	print "------- Welcome to the Movie Cataloger -------"
	print "---------- Created by Diogo Verardi ----------"	
	print "----------- ---------------------- -----------"
	
	for y in os.walk(main_directory_absolute_path):
		rename_main_folders(y[1])
		break
		
	remove_unnecessary_files(main_directory_absolute_path)
	rename_movie_files(main_directory_absolute_path)
	
		
if __name__ == '__main__':
	main()
	
	