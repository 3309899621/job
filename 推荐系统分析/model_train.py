import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import logging
import joblib
import os
import jieba
import re
from sklearn.pipeline import Pipeline
import numpy as np
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if not os.path.exists('models'):
    os.makedirs('models')

logger.info("正在从JSONL文件读取数据...")
df = pd.read_json('data.jsonl', lines=True)

df = df[['positionName', 'keywords', 'content']]

def standardize_position_name(name):
    name = name.lower().strip()
    mapping = {
        r'.*数据分析.*': '数据分析师',
        r'.*算法.*': '算法工程师',
        r'.*python.*': 'Python开发工程师',
        r'.*java.*': 'Java开发工程师',
        r'.*前端.*': '前端开发工程师',
        r'.*后端.*': '后端开发工程师',
        r'.*全栈.*': '全栈开发工程师',
        r'.*运维.*': 'IT运维工程师',
        r'.*测试.*': '软件测试工程师',
        r'.*产品.*': '产品经理',
        r'.*ui.*|.*设计师.*': 'UI设计师',
        r'.*运营.*': '运营专员',
        r'.*新媒体.*': '新媒体运营',
        r'.*主播.*': '主播',
        r'.*销售.*': '销售专员'
    }
    
    for pattern, std_name in mapping.items():
        if re.match(pattern, name):
            return std_name
    return name

df['positionName'] = df['positionName'].apply(standardize_position_name)
position_counts = df['positionName'].value_counts()
logger.info("\n原始职位分布情况：")
logger.info(f"总样本数：{len(df)}")
logger.info(f"总类别数：{len(position_counts)}")
logger.info(f"每个类别的平均样本数：{len(df)/len(position_counts):.2f}")
logger.info(f"样本数最多的前10个类别：\n{position_counts.head(10)}")

min_samples_per_class = 15
valid_positions = position_counts[position_counts >= min_samples_per_class].index
df_filtered = df[df['positionName'].isin(valid_positions)]

logger.info(f"\n过滤前的样本数：{len(df)}")
logger.info(f"过滤后的样本数：{len(df_filtered)}")
logger.info(f"过滤后的职位类别数：{len(valid_positions)}")

skill_keywords = {
    'python': ['python', 'django', 'flask', 'pandas', '爬虫'],
    'java': ['java', 'spring', 'springboot', 'mybatis'],
    'web': ['html', 'css', 'javascript', 'js', 'vue', 'react', 'angular'],
    'database': ['sql', 'mysql', 'oracle', 'mongodb', 'redis'],
    'bigdata': ['hadoop', 'spark', 'hive', '大数据', '数据仓库'],
    'ai': ['机器学习', '深度学习', 'tensorflow', 'pytorch', '人工智能'],
    'operation': ['运营', '用户增长', '数据分析', '用户运营', '内容运营'],
    'product': ['产品', '原型', '需求分析', '用户体验', 'PRD'],
    'design': ['设计', 'ui', 'ue', 'sketch', 'photoshop'],
    'test': ['测试', '自动化测试', '性能测试', '接口测试'],
}

def enhance_features(text):
    enhanced_text = text
    for category, keywords in skill_keywords.items():
        for keyword in keywords:
            if keyword in text.lower():
                enhanced_text += f" {category}"
    return enhanced_text

def clean_text(text):
    if isinstance(text, list):
        text = ' '.join(text)
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', str(text))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

stopwords = set(['的', '了', '和', '与', '或', '等', '及', '都', '要', '把', '这', '那', '你', '我', '他',
                '有', '是', '在', '能', '好', '会', '上', '着', '给', '到', '中', '来', '为', '很',
                '对', '就', '而', '使', '向', '并', '但', '却', '让', '去', '该', '些', '被', '比'])

def chinese_tokenizer(text):
    words = jieba.cut(text)
    words = [word for word in words if word not in stopwords and len(word) > 1]
    return ' '.join(words)

logger.info("正在进行文本预处理...")
df_filtered['keywords'] = df_filtered['keywords'].apply(clean_text)
df_filtered['content'] = df_filtered['content'].apply(clean_text)

logger.info("正在进行分词...")
df_filtered['keywords'] = df_filtered['keywords'].apply(chinese_tokenizer)
df_filtered['content'] = df_filtered['content'].apply(chinese_tokenizer)

df_filtered['features'] = df_filtered.apply(
    lambda x: enhance_features(f"{x['keywords']} {x['content']}"), 
    axis=1
)

X = df_filtered['features']
y = df_filtered['positionName']

position_counts_final = y.value_counts()
logger.info("\n最终职位分布情况：")
logger.info(f"保留的职位类别数：{len(position_counts_final)}")
logger.info(f"每个类别的平均样本数：{len(df_filtered)/len(position_counts_final):.2f}")
logger.info(f"样本数最多的前10个类别：\n{position_counts_final.head(10)}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
logger.info(f"训练集大小：{len(X_train)}")
logger.info(f"测试集大小：{len(X_test)}")

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=15000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )),
    ('clf', RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    ))
])

param_grid = {
    'tfidf__max_features': [12000, 15000],
    'clf__n_estimators': [250, 300],
    'clf__min_samples_split': [2, 3],
    'clf__max_depth': [None, 50, 100]
}

logger.info("开始进行参数调优...")
grid_search = GridSearchCV(pipeline, param_grid, cv=3, n_jobs=-1, verbose=2, scoring='f1_weighted')
grid_search.fit(X_train, y_train)

logger.info(f"最佳参数: {grid_search.best_params_}")

y_pred = grid_search.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
logger.info(f"测试集准确率: {accuracy:.4f}")

logger.info("\n分类报告:\n{}".format(classification_report(y_test, y_pred)))

logger.info("正在保存模型...")
joblib.dump(grid_search.best_estimator_, 'models/position_classifier.joblib')
logger.info("模型保存完成！")

logger.info("测试模型预测...")
loaded_model = joblib.load('models/position_classifier.joblib')

user_interest = "数据分析 Python SQL 数据挖掘 机器学习"
user_interest_cleaned = clean_text(user_interest)
user_interest_tokenized = chinese_tokenizer(user_interest_cleaned)
user_interest_enhanced = enhance_features(user_interest_tokenized)
predicted_position = loaded_model.predict([user_interest_enhanced])
logger.info(f"用户兴趣: '{user_interest}', 推荐岗位: {predicted_position[0]}")

proba = loaded_model.predict_proba([user_interest_enhanced])
top_n = 3
top_classes_idx = np.argsort(proba[0])[-top_n:][::-1]
for idx in top_classes_idx:
    position = loaded_model.classes_[idx]
    probability = proba[0][idx]
    logger.info(f"推荐职位: {position}, 匹配度: {probability:.2%}")