import random

def mapping(trending_category):

	entertainment = ['movies','television','music','theatre','art','singing','cartoons','comedy','comics','magic','pornography','science fiction','stunts','video games','radio']

	social_change = ['politics','economics','business','finance','law','history']

	tech = ['technology', 'aeronautics','exploration']

	criminal = ['crime','espionage','tragedy']

	education = ['philosophy','medicine','literature']


	if trending_category == 'entertainment':
		genre = str(random.choice(entertainment))
	
	elif trending_category == 'social change':
		genre = str(random.choice(social_change))

	elif trending_category == 'tech':
		genre = str(random.choice(tech))

	elif trending_category == 'criminal':
		genre = str(random.choice(criminal))

	elif tending_category == 'education':
		genre = str(random.choice(education))
	
	return genre