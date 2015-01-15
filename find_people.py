import pickle as cp
import csv
import random as rand

category2genre = {
	'entertainment' : ['movies','television','music','theatre','art','singing','cartoons','comedy','comics','magic','pornography','science fiction','stunts','video games','radio'], 
	'social_change' : ['politics','law','crime','espionage'],
	'business' : ['economics','business','finance'],
	'tech' : ['technology', 'aeronautics'],
	'education' : ['philosophy','literature', 'education'],
}

genre2category = {}

genre_category_oppo = {
	'entertainment' : 'education',
	'business' : 'social_change',
	'social_change' : 'business',
	'tech' : 'social_change',
	'education' : 'entertainment'
}

def guofu_load_data():
	global all_names, all_genre, oppo_map, all_name_set, people_has_oppo
	global category2genre, genre2category
	f = open('names.pk', 'r')
	all_names = cp.load(f)
	f.close()

	f = open('all_genre.pk', 'r')
	all_genre = cp.load(f)
	f.close()

	f = open('oppo_map_INKB.pk', 'r')
	oppo_map = cp.load(f)
	f.close()

	all_name_set = set(all_names.keys())
	people_has_oppo = set(oppo_map.keys())

	for category in category2genre:
		genre_list = category2genre[category]
		for genre in genre_list:
			genre2category[genre] = category

	
all_names = None
all_genre = None
oppo_map = None

all_name_set = None
people_has_oppo = None

guofu_load_data()

def people_in_genres(genre_list):
	global all_genre
	people_list = []
	for genre in genre_list:
		people_list += all_genre[genre]
	return set(people_list)

def try_genre(genre, contrast='opponent'):
	global all_genre, people_has_oppo

	people_of_genre = all_genre[genre]
	if len(people_of_genre) < 1:
		return None

	if contrast == 'None':
		if len(people_of_genre) < 2:
			return None
		else:
			res_list = rand.sample(people_of_genre, 2)
			return (res_list[0], res_list[1])

	if contrast == 'opponent':
		people_of_genre_has_oppo = people_of_genre & people_has_oppo

	elif contrast == 'genre':
		genre_category = genre2category[genre]
		oppo_category = genre_category_oppo[genre_category]
		oppo_genres = category2genre[genre_category]
		return try_genres(oppo_genres)

	if len(people_of_genre_has_oppo) < 1:
		return None

	first_people = rand.sample(people_of_genre_has_oppo, 1)[0]
	second_people_cand_list = oppo_map[first_people]
	second_people = rand.sample(second_people_cand_list, 1)[0]

def try_genres(genre_list, contrast='opponent'):
	global people_has_oppo

	people_of_genre = people_in_genres(genre_list)
	if len(people_of_genre) < 1:
		return None

	if contrast == 'None':
		if len(people_of_genre) < 2:
			return None
		else:
			res_list = rand.sample(people_of_genre, 2)
			return (res_list[0], res_list[1])

	if contrast == 'opponent':
		people_of_genre_has_oppo = people_of_genre & people_has_oppo

	if len(people_of_genre_has_oppo) < 1:
		return None

	first_people = rand.sample(people_of_genre_has_oppo, 1)[0]
	second_people_cand_list = oppo_map[first_people]
	second_people = rand.sample(second_people_cand_list, 1)[0]

def find_people(genre):
	global all_genre, all_names, oppo_map, all_name_set
	global genre2category, category2genre, people_has_oppo
	
	if genre not in all_genre:
		print 'Warning: there is no such genre as', genre
		return None

	# best case: direct hit
	res = try_genre(genre)
	if res is not None:
		return res

	# if not, try big category
	genre_category = genre2category[genre]
	neighbor_genres = category2genre[genre_category]
	res = try_genres(neighbor_genres)
	if res is not None:
		return res

	# still not? try contrast by genre
	res = try_genre(genre, 'genre')
	if res is not None:
		return res

	# still not? no contrast then
	res = try_genre(genre, 'None')
	if res is not None:
		return res

	# still not? no contrast in big category
	res = try_genres(neighbor_genres)
	if res is not None:
		return res

	# finally, pure random
	res_list = rand.sample(all_name_set, 2)
	return (res_list[0], res_list[1])


def find_people_v1(genre):
	global all_genre, all_names, oppo_map, all_name_set
	global genre2category, category2genre, people_has_oppo
	
	if genre not in all_genre:
		print 'Warning: there is no such genre as', genre
		return None

	people_of_genre = all_genre[genre]
	#print 'did get people of genre', str(people_of_genre)
	genre_category = genre2category[genre]
	#print 'did get genre category', genre_category
	neighbor_genres = category2genre[genre_category]
	using_big_category = False

	# if there are two few people in the small genre, then use the big category
	if len(people_of_genre) < 2:
		print 'Warning: there is only %d people in genre %s, trying to using the super category %s' % (len(people_of_genre), genre, genre_category)
		people_of_genre = people_in_genres(neighbor_genres)
		using_big_category = True

	# if still the case, then nothing we can do...
	if len(people_of_genre) < 2:
		first_people = rand.sample(people_of_genre, 1)[0]
		second_people = rand.sample(all_name_set, 1)[0]
		return first_people, second_people
	else:
		# people in genre with opponents
		people_of_genre_has_oppo = people_of_genre & people_has_oppo
		# if there is no people with opponents...
		if len(people_of_genre_has_oppo) < 1:
			# if we already used the big category
			if using_big_category == True:
				print 'Warning: no people in genre %s has opponent, trying to find a people from opposite genre category of %s' % (genre, genre_category)
				(first_people, second_people) = rand.sample(people_of_genre, 2)
				return (first_people, second_people)
			else:
				# otherwise, try to use the big category
				people_of_genre = people_in_genres(neighbor_genres)
				people_of_genre_has_oppo = people_of_genre & people_has_oppo
				if len(people_of_genre_has_oppo) < 1:
					# if still has this trouble...
					print 'Warning: no people in genre %s has opponent, trying to find a people from opposite genre category of %s' % (genre, genre_category)
					(first_people, second_people) = rand.sample(people_of_genre, 2)
					return (first_people, second_people)
				else:
					first_people = rand.sample(people_of_genre_has_oppo, 1)[0]
					second_people_cand_list = set(oppo_map[first_people])
					# print 'did get 2nd people candidates', str(second_people_cand_list)
					second_people = rand.sample(second_people_cand_list, 1)[0]
					return first_people, second_people
		else:
			first_people = rand.sample(people_of_genre_has_oppo, 1)[0]
			second_people_cand_list = set(oppo_map[first_people])
			# print 'did get 2nd people candidates', str(second_people_cand_list)
			second_people = rand.sample(second_people_cand_list, 1)[0]
			return first_people, second_people
	return first_people, second_people

def test():
	for category in category2genre:
		for genre in category2genre[category]:
			print 'will test %s in %s' % (genre, category) 
			for i in range(5):
				print find_people(genre)


