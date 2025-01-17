from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.utils import compute_class_weight
import pandas as pd
import jieba

def pre_process(data):
    data['内容']=data['内容'].fillna('')
    data['内容']=data['内容'].astype(str)
    data['内容']=data['内容'].apply(lambda x: ' '.join(jieba.cut(x)))
    stop_words_path = 'stopwords_hit (1).txt'
    with open(stop_words_path, 'r', encoding='utf-8') as f:
        stopwords_list = f.readlines()
        stopwords_list = [stopword.strip() for stopword in stopwords_list]
    def remove_stopwords(text, stopwords):
        words = text.split(' ')
        filtered_words=[word for word in words if word not in stopwords and len(word) > 1]
        return ' '.join(filtered_words)
    data['内容']=data['内容'].apply(lambda x: remove_stopwords(x, stopwords_list))
    return data
def get_feature():
    vect = TfidfVectorizer(max_df=0.8, min_df=2, token_pattern=r"(?u)\b\w+\b")
    return vect
def train(data):
    X=data['内容']
    y=data['评分']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=22)
    model=Pipeline([
        ('vectorizer', get_feature()),
        ('classifier',  MultinomialNB())
    ])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("准确率: ", accuracy_score(y_test, y_pred))
    print("具体的分类文本报告为:\n %s", classification_report(y_test, y_pred,zero_division=1))    #某个类别没有样本时，精确度设为1，防止报警
    return model

def predict(model,text):
    return model.predict([text])[0]


def main():

    data = pd.read_excel('train.xlsx')
    print(data)
    processed_data=pre_process(data)
    print(processed_data)
    model=train(processed_data)
    standard_comment_new=pd.read_csv('standard_comment_unique_deduplicated.csv')
    result=standard_comment_new['内容'].apply(lambda x: predict(model,x))
    result.to_csv('predictions.csv',index=False,encoding='utf-8-sig')

if __name__=="__main__":
    main()