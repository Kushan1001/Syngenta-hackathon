from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer

import pandas as pd

df = pd.read_excel('queries.xlsx')

df.fillna('', inplace=True)

llm = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

X_train, X_test, y_train, y_test = train_test_split(df['query'], df['label'], shuffle=True, test_size=0.2, stratify=df['label'], random_state=42)

X_train_embed = llm.encode(X_train.tolist(), convert_to_numpy=True)
X_test_embed = llm.encode(X_test.tolist(), convert_to_numpy=True)

model = LinearSVC(class_weight='balanced', C = 0.1)
model.fit(X_train_embed, y_train)
