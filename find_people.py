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

genre2category = {
	'aeronautics': 'tech', 'video games': 'entertainment', 'art': 'entertainment', 'radio': 'entertainment', 
	'pornography': 'entertainment', 'politics': 'social_change', 'singing': 'entertainment', 'theatre': 'entertainment', 
	'science fiction': 'entertainment', 'technology': 'tech', 'crime': 'criminal', 'music': 'entertainment', 
	'medicine': 'education', 'comedy': 'entertainment', 'espionage': 'criminal', 'literature': 'education', 
	'finance': 'social_change', 'business': 'social_change', 'philosophy': 'education', 'law': 'social_change', 
	'tragedy': 'criminal', 'stunts': 'entertainment', 'television': 'entertainment', 'magic': 'entertainment', 
	'comics': 'entertainment', 'economics': 'social_change', 'movies': 'entertainment', 'exploration': 'tech', 
	'cartoons': 'entertainment', 'history': 'social_change', 'education' : 'education'
}

genre_category_oppo = {
	'business' : 'entertainment',
	'social_change' : 'business',
}

def guofu_load_data():
	global all_names, all_genre, oppo_map, all_name_set, people_has_oppo
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

def load_from_csv():
	f = open('Veale\'s The NOC List.csv', 'r')
	names = {}

	line = f.readline().strip()
	heads = line.split(';')

	lines = f.readlines();
	csv_reader = csv.reader(lines, delimiter=';')

	for entries in csv_reader:
		name = entries[0]
		if len(name) < 2:
			continue
		print 'is working on:', name, '#entries:', len(entries)
		properties = {}
		for i in range(1,23):
			key = heads[i]
			value = entries[i]
			properties[key] = value
		names[name] = properties


def make_genre_to_names():
	f = open('all_genre.pk', 'w')
	all_genre = {}

	for name in names:
		genre_list = names[name]['Genres'].split(',')
		for genre in genre_list:
			genre = genre.strip()
			if genre in all_genre:
				all_genre[genre].add(name)
			else:
				all_genre[genre] = set([name])

	cp.dump(all_genre, f)
	f.close()

def make_oppo_dict():
	f = open('oppo_map_INKB.pk', 'w')
	oppo_dict = {}

	for name in names:
		oppo_list = names[name]['Opponent'].split(',')
		for oppo in oppo_list:
			oppo = oppo.strip()
			if len(oppo) < 2 or oppo not in names:
				continue
			if name not in oppo_dict:
				oppo_dict[name] = set([oppo])
			else:
				oppo_dict[name].add(oppo)
			if oppo in oppo_dict:
				oppo_dict[oppo].add(name)
			else:
				oppo_dict[oppo] = set([name])

	cp.dump(oppo_dict, f)
	f.close()

	
all_names = None
all_genre = None
oppo_map = None

all_name_set = None
people_has_oppo = None

guofu_load_data()

def people_in_genres(genre_list):
	people_list = []
	for genre in genre_list:
		people_list += all_genre[genre]
	return set(people_list)

def find_people(genre):
	global all_genre, all_names, oppo_map, all_name_set
	global genre2category, category2genre, people_has_oppo
	
	if genre not in all_genre:
		print 'Warning: there is no such genre as', genre
		return None

	genre_category = genre2category[genre];
	people_of_genre = all_genre[genre]
	neighbor_genres = category2genre[genre_category]
	using_big_category = False

	# if there are two few people in the small genre, then use the big category
	if len(people_of_genre) < 2:
		print 'Warning: there is only %d people in genre %s, trying to using the super category' % (len(people_of_genre), genre)
		people_of_genre = people_in_genres(neighbor_genres)
		using_big_category = True

	# if still the case, then nothing we can do...
	if len(people_of_genre) < 2:
		first_people = rand.sample(people_of_genre, 1)[0]
		second_people = rand.sample(all_name_set, 1)[0]
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

