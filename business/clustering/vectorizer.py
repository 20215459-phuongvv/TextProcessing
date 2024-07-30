from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

def vectorize_documents(documents, min_df=2, n_components=83, n_iter=20):
    vectorizer = TfidfVectorizer(token_pattern="\S+", min_df=min_df)
    vectors = vectorizer.fit_transform(documents)
    print("Tf-idf shape:", vectors.shape)
    
    svd = TruncatedSVD(n_components=n_components, n_iter=n_iter, random_state=42)
    svd_vectors = svd.fit_transform(vectors)
    
    # print("Document 1's Vector:")
    # print(svd_vectors[0])
    
    return svd_vectors