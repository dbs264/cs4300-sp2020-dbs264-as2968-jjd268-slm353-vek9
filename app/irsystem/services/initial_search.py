import config, random, json
from collections import Counter
from app.irsystem.services import search_helpers as helpers


def random_five(details):
	for detail in details:
		detail["score"] = random.random()
	return helpers.sort_by_score(details)

def basic_search(details):
	for detail in details:
		if "rating" in detail and "user_ratings_total" in detail:
			detail["score"] = detail["rating"] * detail["user_ratings_total"]
		else:
			detail["score"] = 0
	return helpers.sort_by_score(details)

def keyword_search(details, word):
	for place in details:
		score = 0
		if "reviews" in place:
			for review in place["reviews"]:
				text = review["text"]
				if word in text:
					score += 1

		place["score"] = score
	return helpers.sort_by_score(details)

def multiple_key_word_counts(details, words):
	print(words)
	word_list = words.lower().split()
	print(word_list)
	for place in details:
		score = 0
		if "reviews" in place:
			for review in place["reviews"]:
				text_counter = Counter(review["text"].lower().split())
				for word in word_list:
					score += text_counter[word]
		place["score"] = score
	return helpers.sort_by_score(details)



def search_data(query, city):
	details = helpers.load_details(city)
	top_five = multiple_key_word_counts(details, query)
	return [helpers.format_output(x) for x in top_five]


	