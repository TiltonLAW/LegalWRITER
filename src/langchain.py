import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

class LangChain:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token.isalnum() and token not in self.stop_words]
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
        return ' '.join(lemmatized_tokens)

    def filter_queries(self, queries, query):
        preprocessed_query = self.preprocess_text(query)
        filtered_queries = []
        for potential_query in queries:
            preprocessed_potential_query = self.preprocess_text(potential_query)
            if preprocessed_query in preprocessed_potential_query:
                filtered_queries.append(potential_query)
        return filtered_queries

    def filter_results(self, results, query):
        preprocessed_query = self.preprocess_text(query)
        filtered_results = []
        for result in results:
            preprocessed_result = self.preprocess_text(result['title'])
            if preprocessed_query in preprocessed_result:
                filtered_results.append(result)
        return filtered_results

    def rank_queries(self, queries, query):
        filtered_queries = self.filter_queries(queries, query)
        scores = []
        for potential_query in filtered_queries:
            preprocessed_potential_query = self.preprocess_text(potential_query)
            score = 0
            for token in preprocessed_potential_query.split():
                if token in preprocessed_query.split():
                    score += 1
            scores.append(score)
        sorted_queries = [query for _, query in sorted(zip(scores, filtered_queries), reverse=True)]
        return sorted_queries

    def rank_results(self, results, query):
        filtered_results = self.filter_results(results, query)
        scores = []
        for result in filtered_results:
            preprocessed_result = self.preprocess_text(result['title'])
            score = 0
            for token in preprocessed_query.split():
                if token in preprocessed_result.split():
                    score += 1
            scores.append(score)
        sorted_results = [result for _, result in sorted(zip(scores, filtered_results), reverse=True)]
        return sorted_results
