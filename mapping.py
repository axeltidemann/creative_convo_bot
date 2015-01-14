import random

from hashtags import popular_hashtags

def mapping():
	D = popular_hashtags()
	D.pop('Astrology')
	D.pop('Environment')
	D.pop('General')	
	trending_category = str(random.choice(D.keys()))
	
	hashtag = str(random.choice(D[trending_category]))

	entertainment = ['movies','television','music','theatre','art','singing','cartoons','comedy','comics','magic','pornography','science fiction','stunts','video games','radio']

	social_change = ['politics','law','crime','espionage']
	
	business = ['economics','business','finance']

	tech = ['technology', 'aeronautics']

	education = ['philosophy','literature','education']

	if trending_category == 'TV/Entertainment':
		genre = str(random.choice(entertainment))
		opposite_genre = str(random.choice(education))
	
	elif trending_category == 'Social Change':
		genre = str(random.choice(social_change))
		opposite_genre = str(random.choice(business))
	
	elif trending_category == 'Business':
		genre = str(random.choice(business))
		opposite_genre = str(random.choice(social_change))

	elif trending_category == 'Tech':
		genre = str(random.choice(tech))
		opposite_genre = str(random.choice(social_change))

	elif trending_category == 'Education':
		genre = str(random.choice(education))
		opposite_genre = str(random.choice(entertainment))
	
	return (genre,hashtag,opposite_genre)

if __name__ == "__main__":
    x = mapping()
    print x
