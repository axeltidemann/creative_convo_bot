import random

from hashtags import popular_hashtags

def mapping():
	D = popular_hashtags()
	D.pop('Astrology')
	D.pop('Environment')	
	trending_category = str(random.choice(D.keys()))
	
	hashtag = str(random.choice(D[trending_category]))

	entertainment = ['movies','television','music','theatre','art','singing','cartoons','comedy','comics','magic','pornography','science fiction','stunts','video games','radio']

	social_change = ['politics','law','crime','espionage']
	
	general = ['history','exploration','tragedy','medicine']
	
	business = ['economics','business','finance']

	tech = ['technology', 'aeronautics']

	education = ['philosophy','literature']

	if trending_category == 'TV/Entertainment':
		genre = str(random.choice(entertainment))
	
	elif trending_category == 'Social Change':
		genre = str(random.choice(social_change))
		
	elif trending_category == 'General':
		genre = str(random.choice(general))
	
	elif trending_category == 'Business':
		genre = str(random.choice(business))

	elif trending_category == 'Tech':
		genre = str(random.choice(tech))

	elif trending_category == 'Education':
		genre = str(random.choice(education))	
	
	print trending_category
	
	return (genre,hashtag)


if __name__ == "__main__":
    x = mapping()
    print x
