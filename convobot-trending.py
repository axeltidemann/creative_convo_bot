#convobot module - hashtags.org parsing...
#output: 1 popular hashtag per category

from pattern.web import Twitter

hashTagCats = ["Entertainment", "General", "Business", "Tech", "Education", "Environment", "Social", "Astrology"]


print Twitter().trends(cached=False)

### saving category name and one (first) hashtag 

###returns a list of tuples (categoryname, hashtag)




