import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import gensim
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity


#NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('gutenberg')


stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# def initialize_models(model_names):
#     model_dict = {}
#     for key, name in model_names.items():
#         try:
#             model_dict[key] = SentenceTransformer(name)
#         except Exception as e:
#             print(f"Error loading model {name}: {e}")
#     return model_dict

# def embed_text(text, model):
#     return model.encode(text)

# def compute_cosine_similarity(embedding1, embedding2):
#     return util.pytorch_cos_sim(embedding1, embedding2).item()

# def clean_text(text, keywords=[]):
#     pattern = r'[^\w\s]'
#     cleaned_text = re.sub(pattern, ' ', text)
#     cleaned_text = re.sub(' +', ' ', cleaned_text)
#     words = cleaned_text.split()
#     filtered_words = [word.lower() for word in words if word.lower() not in keywords and not word.isdigit()]
#     return ' '.join(filtered_words)

# def get_recommendations(df, df_unique_activity_vector, search_vectors, footprint_description, footprint_description_processed, model_dict, top_n_per_model=50, top_shortlist=20):
#     top_n_df = pd.DataFrame()

#     for model_key, search_vector in search_vectors.items():
#         model_column = f'activity_name_vector_{model_key}'

#         df_unique_activity_vector['similarity'] = df_unique_activity_vector[model_column].apply(
#             lambda x: compute_cosine_similarity(search_vector, x))

#         df_unique_activity_vector_top_n = df_unique_activity_vector.sort_values(by='similarity', ascending=False).head(top_n_per_model)

#         temp_df = df[df['processed_activity_name'].isin(df_unique_activity_vector_top_n['processed_activity_name'].unique())]
#         temp_df = pd.merge(temp_df, df_unique_activity_vector_top_n[['processed_activity_name', 'similarity']],
#                            on='processed_activity_name', how='left')

#         temp_df['footprint'] = footprint_description
#         temp_df['search_text'] = footprint_description_processed
#         temp_df['footprint_category'] = 'No Category'
#         temp_df['model'] = model_dict[model_key]

#         cols = temp_df.columns.tolist()
#         cols = cols[-1:] + cols[:-1]
#         temp_df = temp_df[cols].reset_index(drop=True)

#         top_n_df = pd.concat([top_n_df, temp_df], ignore_index=True)

#     top_n_df = top_n_df.fillna('')
#     top_n_df['similarity'] = top_n_df['similarity'].apply(lambda x: float(x))

#     exclude_columns = ['model', 'similarity']
#     group_columns = [col for col in top_n_df.columns if col not in exclude_columns]

#     grouped = top_n_df.groupby(group_columns, as_index=False).agg(
#         recommendation_counter=('model', 'size'),
#         scores=('similarity', 'max'))

#     result_df = pd.DataFrame()
#     grouped = grouped.groupby('search_text')

#     for search_text, group in grouped:
#         distinct_scores = group['scores'].drop_duplicates().sort_values(ascending=False)
#         top_scores = distinct_scores.head(top_shortlist)
#         top_scores_df = group[(group['scores'].isin(top_scores)) | (group['recommendation_counter'] > 1)]
#         result_df = pd.concat([result_df, top_scores_df])

#     return result_df

# def prepare_final_output(df):
#     final_output = df[['footprint', 'recommendation_counter', 'scores', 'activity_id', 'unit_type', 'country', 'year']]
#     final_output = final_output.rename(columns={
#         'activity_id': 'activity_id',
#         'recommendation_counter': 'counter',
#         'scores': 'score',
#         'footprint': 'footprint'
#     })

#     final_output = final_output.drop_duplicates(subset=['footprint', 'counter', 'score', 'activity_id', 'unit_type', 'country', 'year'])

#     final_output = final_output.sort_values(by=['counter', 'score'], ascending=[False, False])

#     return final_output


# def initialize_models(model_names):
#     model_dict = {}
#     for key, name in model_names.items():
#         try:
#             model_dict[key] = SentenceTransformer(name)
#         except Exception as e:
#             print(f"Error loading model {name}: {e}")
#     return model_dict

# def embed_text(text, model):
#     return model.encode(text)

# def compute_cosine_similarity(embedding1, embedding2):
#     return util.pytorch_cos_sim(embedding1, embedding2).item()

# def clean_text(text, keywords=[]):
#     pattern = r'[^\w\s]'
#     cleaned_text = re.sub(pattern, ' ', text)
#     cleaned_text = re.sub(' +', ' ', cleaned_text)
#     words = cleaned_text.split()
#     filtered_words = [word.lower() for word in words if word.lower() not in keywords and not word.isdigit()]
#     return ' '.join(filtered_words)

# def get_recommendations(df, df_unique_activity_vector, search_vectors, footprint_description, footprint_description_processed, model_dict, top_n_per_model=50, top_shortlist=20):
#     top_n_df = pd.DataFrame()

#     for model_key, search_vector in search_vectors.items():
#         model_column = f'activity_name_vector_{model_key}'

#         df_unique_activity_vector['similarity'] = df_unique_activity_vector[model_column].apply(
#             lambda x: compute_cosine_similarity(search_vector, x))

#         df_unique_activity_vector_top_n = df_unique_activity_vector.sort_values(by='similarity', ascending=False).head(top_n_per_model)

#         temp_df = df[df['processed_activity_name'].isin(df_unique_activity_vector_top_n['processed_activity_name'].unique())]
#         temp_df = pd.merge(temp_df, df_unique_activity_vector_top_n[['processed_activity_name', 'similarity']],
#                            on='processed_activity_name', how='left')

#         temp_df['footprint'] = footprint_description
#         temp_df['search_text'] = footprint_description_processed
#         temp_df['footprint_category'] = 'No Category'
#         temp_df['model'] = model_dict[model_key]

#         cols = temp_df.columns.tolist()
#         cols = cols[-1:] + cols[:-1]
#         temp_df = temp_df[cols].reset_index(drop=True)

#         top_n_df = pd.concat([top_n_df, temp_df], ignore_index=True)

#     top_n_df = top_n_df.fillna('')
#     top_n_df['similarity'] = top_n_df['similarity'].apply(lambda x: float(x))

#     exclude_columns = ['model', 'similarity']
#     group_columns = [col for col in top_n_df.columns if col not in exclude_columns]

#     grouped = top_n_df.groupby(group_columns, as_index=False).agg(
#         recommendation_counter=('model', 'size'),
#         scores=('similarity', 'max'))

#     result_df = pd.DataFrame()
#     grouped = grouped.groupby('search_text')

#     for search_text, group in grouped:
#         distinct_scores = group['scores'].drop_duplicates().sort_values(ascending=False)
#         top_scores = distinct_scores.head(top_shortlist)
#         top_scores_df = group[(group['scores'].isin(top_scores)) | (group['recommendation_counter'] > 1)]
#         result_df = pd.concat([result_df, top_scores_df])

#     return result_df

# def prepare_final_output(df):
#     if len(df.columns) == 0:
#         return df
#     final_output = df[['footprint', 'recommendation_counter', 'scores', 'activity_id', 'factor','unit_type', 'country', 'year','id']]
#     final_output = final_output.rename(columns={
#         'activity_id': 'activity_id',
#         'recommendation_counter': 'counter',
#         'scores': 'score',
#         'footprint': 'footprint'
#     })

#     final_output = final_output.drop_duplicates(subset=['footprint', 'counter', 'score', 'factor','activity_id', 'unit_type', 'country', 'year','id'])

#     final_output = final_output.sort_values(by=['counter', 'score'], ascending=[False, False])
#     final_output['rank'] = final_output.groupby(['counter', 'score']).ngroup(ascending=False) + 1
#     # Reset rank within each group of identical 'counter' and 'score'
#     final_output['rank'] = final_output.groupby(['counter', 'score'])['rank'].transform('min')

#     return final_output
## new Version


def preprocess_text(text, remove_words=None):
    if remove_words is None:
      remove_words = []

    # Convert remove_words to lowercase for case-insensitive comparison
    remove_words = set(word.lower() for word in remove_words)

    # Preprocessing steps
    #text = re.sub(r"[,.;@#?!&$]+\ *", " ", text)
    #text = re.sub(r"[,.;@#?!&$]+\ *", " ", text)
    text = text.replace(":", " ")
    text = text.replace("/", " or ")
    text = text.replace("_", " ")
    text = text.replace("-", " ")
    #text = text.replace("type", "")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")

    text = text.lower()  # Convert text to lowercase

    # Remove specified words before tokenization
    words = text.split()
    words = [word for word in words if word not in remove_words]
    tokens =  words
    #text = ' '.join(words)  # Reconstruct the text

    # Tokenization and lemmatization
    tokens = word_tokenize(text)
    #tokens = sorted(set([lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]))  # Lemmatization
    #tokens = (set([lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]))  # Lemmatization
    #tokens = (([lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]))  # Lemmatization

    #tokens = [token for token in tokens if token not in stop_words]  # Remove stopwords

    # Remove specified words after lemmatization
    tokens = [token for token in tokens if token not in remove_words]

    def remove_duplicates(lst):
      seen = set()
      result = []
      for item in lst:
        if item not in seen:
          seen.add(item)
          result.append(item)
      return result

    tokens = remove_duplicates(tokens)


    return ' '.join(tokens)

def update_text(row, df):
    # Get all values in the same group but different subcategory
    other_values = df[(df['category'] == row['category']) & (df['activity_id'] != row['activity_id'])]['processed_activity_id_og']

    unique_words = set()
    relevant_words = row['processed_activity_id_og'].split()
    # Iterate over each entry in other_values and split into words
    for entry in other_values:
      words = entry.split()
      if words not in relevant_words:
        unique_words.update(word.lower() for word in words)

    unique_words_str = ' '.join(set(unique_words))
    tokens = word_tokenize(unique_words_str)
    tokens = sorted(set([lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]))  # Lemmatization
    tokens = [token for token in tokens if token not in stop_words]  # Remove stopwords
    tokens = [token for token in tokens if len(token) > 4]  # Remove short words

    tokens = ['not ' + token + '.' for token in tokens]
    # Join unique words into a single string
    if len(tokens)>0:
        unique_words_str = ' '.join(set(tokens))
        return f"{row['processed_activity_name']}  {unique_words_str}."
    else:
        return row['processed_activity_name']

def remove_source_words(row):
    category_words = set(row['processed_category_og'].split())
    activity_words = row['processed_activity_id_og'].split()
    filtered_words = [word for word in activity_words if word not in category_words]
    return ' '.join(filtered_words)

def preprocess_text(text, remove_words=None):
    if remove_words is None:
      remove_words = []

    # Convert remove_words to lowercase for case-insensitive comparison
    remove_words = set(word.lower() for word in remove_words)

    # Preprocessing steps
    #text = re.sub(r"[,.;@#?!&$]+\ *", " ", text)
    #text = re.sub(r"[,.;@#?!&$]+\ *", " ", text)
    text = text.replace(":", " ")
    text = text.replace("/", " or ")
    text = text.replace("_", " ")
    text = text.replace("-", " ")
    #text = text.replace("type", "")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")

    text = text.lower()  # Convert text to lowercase

    # Remove specified words before tokenization
    words = text.split()
    words = [word for word in words if word not in remove_words]
    tokens =  words
    #text = ' '.join(words)  # Reconstruct the text

    # Tokenization and lemmatization
    tokens = word_tokenize(text)
    #tokens = sorted(set([lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]))  # Lemmatization
    #tokens = (set([lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]))  # Lemmatization
    #tokens = (([lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]))  # Lemmatization

    #tokens = [token for token in tokens if token not in stop_words]  # Remove stopwords

    # Remove specified words after lemmatization
    tokens = [token for token in tokens if token not in remove_words]

    def remove_duplicates(lst):
      seen = set()
      result = []
      for item in lst:
        if item not in seen:
          seen.add(item)
          result.append(item)
      return result

    tokens = remove_duplicates(tokens)


    return ' '.join(tokens)

def initialize_models(model_names):
    model_dict = {}
    for key, name in model_names.items():
        try:
            model_dict[key] = SentenceTransformer(name)
        except Exception as e:
            print(f"Error loading model {name}: {e}")
    return model_dict

def embed_text(text, model):
    return model.encode(text)

def compute_cosine_similarity(embedding1, embedding2):
    return util.pytorch_cos_sim(embedding1, embedding2).item()

def clean_text(text, keywords=[]):
    pattern = r'[^\w\s]'
    cleaned_text = re.sub(pattern, ' ', text)
    cleaned_text = re.sub(' +', ' ', cleaned_text)
    words = cleaned_text.split()
    filtered_words = [word.lower() for word in words if word.lower() not in keywords and not word.isdigit()]
    return ' '.join(filtered_words)

def get_recommendations(df, df_unique_activity_vector, search_vectors, footprint_description, footprint_description_processed, model_dict, top_n_per_model=50, top_shortlist=20):
    top_n_df = pd.DataFrame()

    for model_key, search_vector in search_vectors.items():
        model_column = f'activity_name_vector_{model_key}'

        df_unique_activity_vector['similarity'] = df_unique_activity_vector[model_column].apply(
            lambda x: compute_cosine_similarity(search_vector, x))

        df_unique_activity_vector_top_n = df_unique_activity_vector.sort_values(by='similarity', ascending=False).head(top_n_per_model)

        temp_df = df[df['processed_activity_name'].isin(df_unique_activity_vector_top_n['processed_activity_name'].unique())]
        temp_df = pd.merge(temp_df, df_unique_activity_vector_top_n[['processed_activity_name', 'similarity']],
                           on='processed_activity_name', how='left')

        temp_df['footprint'] = footprint_description
        temp_df['search_text'] = footprint_description_processed
        temp_df['footprint_category'] = 'No Category'
        temp_df['model'] = model_dict[model_key]

        cols = temp_df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        temp_df = temp_df[cols].reset_index(drop=True)

        top_n_df = pd.concat([top_n_df, temp_df], ignore_index=True)

    top_n_df = top_n_df.fillna('')
    top_n_df['similarity'] = top_n_df['similarity'].apply(lambda x: float(x))

    exclude_columns = ['model', 'similarity']
    group_columns = [col for col in top_n_df.columns if col not in exclude_columns]

    grouped = top_n_df.groupby(group_columns, as_index=False).agg(
        recommendation_counter=('model', 'size'),
        scores=('similarity', 'max'))

    result_df = pd.DataFrame()
    grouped = grouped.groupby('search_text')

    for search_text, group in grouped:
        distinct_scores = group['scores'].drop_duplicates().sort_values(ascending=False)
        top_scores = distinct_scores.head(top_shortlist)
        top_scores_df = group[(group['scores'].isin(top_scores)) | (group['recommendation_counter'] > 1)]
        result_df = pd.concat([result_df, top_scores_df])

    return result_df

def prepare_final_output(df):
    if len(df.columns) == 0:
       return df
    final_output = df[['footprint', 'recommendation_counter', 'scores', 'activity_id', 'unit_type', 'country', 'year','id']]
    final_output = final_output.rename(columns={
        'activity_id': 'activity_id',
        'recommendation_counter': 'counter',
        'scores': 'score',
        'footprint': 'footprint'
    })

    final_output = final_output.drop_duplicates(subset=['footprint', 'counter', 'score', 'activity_id', 'unit_type', 'country', 'year','id'])

    order_ranking  = ['score', 'counter']
    final_output = final_output.sort_values(by=order_ranking, ascending=[False, False])
    final_output['rank'] = final_output.groupby(order_ranking).ngroup(ascending=False) + 1
    # Reset rank within each group of identical 'counter' and 'score'
    final_output['rank'] = final_output.groupby(order_ranking)['rank'].transform('min')


    ## identify top 10 reommendations

    return final_output



