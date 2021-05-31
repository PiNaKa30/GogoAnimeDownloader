import requests
import wget
import os

print("\n**************************************\n\tGogoAnime Downloader" + 
	"\n  Made by: Shourya Sharma (PiNaKa30)\n**************************************\n")
print("The Homepage of any Anime on GogoAnime is of the following form:")
print(" -> Sample:  https://gogoanime.ai/category/<anime_name> \n -> Example: https://gogoanime.ai/category/naruto-shippuden\n")

print("Visit the homepage of the Anime you want to download and enter the name:")
anime_name = input()

print("Enter starting episode number")
episode_start = int(input())

print("Enter ending episode number")
episode_end = int(input())

count_pass = count_fail = count_skip = 0

if not os.path.exists(anime_name):
    os.makedirs(anime_name)
    print("\nCreating new Directory: ", anime_name)
else:
	print("\nFound existing Directory: ", anime_name)


while(episode_start <= episode_end):

	try:

		episode_url = "https://gogoanime.ai/" + anime_name + "-episode-" + str(episode_start)
		print("\nFetching ", episode_url)

		file_name = "./" + anime_name + "/" + "Episode - " + str(episode_start).zfill(3) + ".mp4";
		if(os.path.isfile(file_name)):
			print("File already exists! Skipping ...")
			count_skip += 1
			episode_start += 1
			continue

		episode_code = requests.get(episode_url)
		index_download = episode_code.text.find('<li class="dowloads">') + 22
		index_start = episode_code.text.find('"', index_download + 1) + 1
		index_end = episode_code.text.find('"', index_start + 1)
		mirror_url = episode_code.text[index_start:index_end]
		mirror_code = requests.get(mirror_url)

		index_download = mirror_code.text.find('<div class="dowload">') + 22
		index_start = mirror_code.text.find('"', index_download + 1) + 1
		index_end = mirror_code.text.find('"', index_start + 1)
		download_url = mirror_code.text[index_start:index_end]

		wget.download(download_url, file_name)
		print("\nSuccessfully fetched Episode ", str(episode_start).zfill(3))

		count_pass += 1

	except:

		print("Error occurred while fetching Episode ", str(episode_start).zfill(3))
		count_fail += 1

	episode_start += 1

print("\n*************************\n\tResults\n*************************\n")
print("Files downloaded: ", count_pass)
print("Files failed: ", count_fail)
print("Files skipped: ", count_skip)