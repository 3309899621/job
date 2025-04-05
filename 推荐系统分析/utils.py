from zhipuai import ZhipuAI
import json
import joblib
import jieba
import re
import numpy as np
import os

class PositionRecommender:
    def __init__(self, model_path='models/position_classifier.joblib'):
        self.model_path = model_path
        self.model = None
        self.stopwords = set(['的', '了', '和', '与', '或', '等', '及', '都', '要', '把', '这', '那', '你', '我', '他',
                            '有', '是', '在', '能', '好', '会', '上', '着', '给', '到', '中', '来', '为', '很',
                            '对', '就', '而', '使', '向', '并', '但', '却', '让', '去', '该', '些', '被', '比'])
        
        self.skill_keywords = {
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

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"模型文件 {self.model_path} 不存在")
        self.model = joblib.load(self.model_path)

    def clean_text(self, text):
        if isinstance(text, list):
            text = ' '.join(text)
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', str(text))
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def chinese_tokenizer(self, text):
        words = jieba.cut(text)
        words = [word for word in words if word not in self.stopwords and len(word) > 1]
        return ' '.join(words)

    def enhance_features(self, text):
        enhanced_text = text
        for category, keywords in self.skill_keywords.items():
            for keyword in keywords:
                if keyword in text.lower():
                    enhanced_text += f" {category}"
        return enhanced_text

    def preprocess_text(self, text):
        cleaned_text = self.clean_text(text)
        tokenized_text = self.chinese_tokenizer(cleaned_text)
        enhanced_text = self.enhance_features(tokenized_text)
        return enhanced_text

    def predict(self, text, top_n=5):
        if self.model is None:
            self.load_model()

        processed_text = self.preprocess_text(text)
        proba = self.model.predict_proba([processed_text])
        top_classes_idx = np.argsort(proba[0])[-top_n:][::-1]
        
        results = []
        for idx in top_classes_idx:
            position = self.model.classes_[idx]
            probability = proba[0][idx]
            results.append({
                'position': position,
                'probability': probability
            })
        
        return results
    
def GLM_analysis(input_text):
    client = ZhipuAI(api_key="60a107de2b381145b3ab9955187f2e50.Z4hUWiul0ggb2pFg")
    system_prompt = '''Roleplay: 你现在是一个兴趣爱好分析官，你可以根据用户提供的关键词以及年龄给用户推荐合适的信息。
    Task: 根据用户提供的关键词以及年龄完成下面的任务:
    1. 生成一个可以用于pyecharts的数据字典，要保证数据字典是正确的，关系之间有着正确的关系，以及一个推荐学习路径，必须为markdown格式。样例：
    ```json
    {
    "nodes": [
        {"name": "CEO", "symbolSize": 60},
        {"name": "经理A", "symbolSize": 40},
        {"name": "经理B", "symbolSize": 40},
        {"name": "员工1", "symbolSize": 20},
        {"name": "员工2", "symbolSize": 20},
    ], 
    "links": [
        {"source": "CEO", "target": "经理A", "value": "直属"},
        {"source": "CEO", "target": "经理B", "value": "直属"},
        {"source": "经理A", "target": "员工1", "value": "管理"},
        {"source": "经理B", "target": "员工2", "value": "管理"},
    ],
    "recommend_path": "markdown内容"}
    ```
    2. pyecharts的数据字典必须的符合样例，学习路径必须为优美的html格式。
    3. 输出的内容必须符合正常的json格式，且可以被json.loads正常格式化，不要回答不属于规范的其它内容。
    4. 不要输出多余的内容。
    '''
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": input_text},
    ]

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=messages
    )
    markdown_content = response.choices[0].message.content
    index_dict = json.loads(markdown_content.split('```json')[-1].split('```')[0].strip())
    return index_dict