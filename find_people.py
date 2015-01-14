import pickle as cp
import csv
import random as rand


def guofu_load_data():
	global all_names, all_genre, oppo_map, all_name_set, people_has_oppo
	print 'will load data'
	f = open('names.pk', 'r')
	all_names = cp.load(f)
	f.close()

	f = open('all_genre.pk', 'r')
	all_genre = cp.load(f)
	f.close()

	f = open('oppo_map.pk', 'r')
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
	f = open('all_genre.pk', 'wb')
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
	f = open('oppo_map.pk', 'wb')
	oppo_dict = {}

	for name in names:
		oppo_list = names[name]['Opponent'].split(',')
		for oppo in oppo_list:
			oppo = oppo.strip()
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

def find_people(genre):
	global all_genre, all_names, oppo_map, all_name_set, people_has_oppo
	
	if genre not in all_genre:
		print 'Warning: there is no such genre as', genre
		return None

	people_of_genre = all_genre[genre]
	if len(people_of_genre) == 1:
		print 'Warning: there is only %d people in genre %s' % (len(people_of_genre), genre)
		first_people = rand.sample(people_of_genre, 1)[0]
		second_people = rand.sample(all_name_set, 1)[0]
	elif len(people_of_genre) == 0:
		print 'Warning: there is no people of this genre %s' % genre
		[first_people, second_people] = rand.sample(all_name_set, 2)
	else:
		people_of_genre_has_oppo = people_of_genre & people_has_oppo
		if len(people_of_genre_has_oppo) < 2:
			print 'Warning: no people in genre %s has opponent' % genre
			(first_people, second_people) = rand.sample(people_of_genre, 2)
		else:
			first_people = rand.sample(people_of_genre_has_oppo, 1)[0]
			second_people_cand_list = set(oppo_map[first_people])
			print 'did get 2nd people candidates', str(second_people_cand_list)
			second_people = rand.sample(second_people_cand_list, 1)[0]
	
	print 'did find 1st people', first_people, '2nd people', second_people

	if second_people not in all_name_set:
		print '2nd name %s is not in the KB' % second_people
		second_people_info = {}
	else:
		second_people_info = all_names[second_people]
	first_people_info = all_names[first_people]

	return ({first_people: first_people_info}, {second_people: second_people_info})


