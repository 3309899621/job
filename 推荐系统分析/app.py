from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils import PositionRecommender, GLM_analysis
import pymysql
import markdown
import threading
import time
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key'
recommender = PositionRecommender()

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

tasks = {}

mysql_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'password',
    'database': 'lagou_db',
    'charset': 'utf8mb4'
}

def run_analysis(user_interest, input_text, task_id):
    try:
        logger.debug(f"Starting analysis for task_id: {task_id}")
        position_results = recommender.predict(user_interest)
        glm_results = GLM_analysis(input_text)
        tasks[task_id] = {
            'status': 'completed',
            'position_results': position_results,
            'glm_results': glm_results
        }
        logger.debug(f"Task {task_id} completed successfully")
    except Exception as e:
        logger.error(f"Error in run_analysis for task_id {task_id}: {str(e)}")
        tasks[task_id] = {'status': 'error', 'error': str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            gender = request.form.get('gender')
            age = request.form.get('age')
            direction = request.form.get('interest_direction')
            keywords = request.form.get('interest_keywords')
            level = request.form.get('current_level')
            hours = request.form.get('study_hours')
            
            if not all([gender, age, direction, keywords]):
                return render_template('index.html', error="所有字段均为必填项！")

            keywords_list = keywords.split()
            user_interest = ' '.join(keywords_list)

            task_id = str(time.time())
            tasks[task_id] = {'status': 'running'}
            logger.debug(f"Task {task_id} created with status 'running'")

            session['user_data'] = {
                'gender': gender,
                'age': age,
                'direction': direction,
                'keywords': keywords_list
            }
            session['task_id'] = task_id
            logger.debug(f"Session data set: {session.get('user_data')}, task_id: {task_id}")

            thread = threading.Thread(target=run_analysis, args=(user_interest, f"关键词: {keywords}, 年龄: {age}, 当前技术：{level}, 每天空闲时间: {hours}", task_id))
            thread.start()

            return render_template('loading.html', task_id=task_id)
        
        except Exception as e:
            logger.error(f"Error in POST /index: {str(e)}")
            return render_template('index.html', error=f"提交失败：{str(e)}")
    
    return render_template('index.html')

@app.route('/check_status/<task_id>')
def check_status(task_id):
    task = tasks.get(task_id, {'status': 'not_found'})
    logger.debug(f"Checking status for task_id {task_id}: {task['status']}")
    return jsonify({'status': task['status']})

@app.route('/analysis')
def analysis():
    if 'user_data' not in session or 'task_id' not in session:
        logger.warning("Session data missing, redirecting to index")
        return redirect(url_for('index'))

    task_id = session['task_id']
    task = tasks.get(task_id)
    if not task or task['status'] != 'completed':
        logger.warning(f"Task {task_id} not completed or not found: {task}")
        return redirect(url_for('index'))

    user_data = session['user_data']
    position_results = task['position_results']
    logger.debug(f"Rendering analysis for task_id {task_id}")

    return render_template('analysis.html', 
                         gender=user_data['gender'], 
                         age=user_data['age'], 
                         direction=user_data['direction'], 
                         keywords=user_data['keywords'], 
                         results=position_results)

@app.route('/knowledge')
def knowledge():
    if 'user_data' not in session or 'task_id' not in session:
        logger.warning("Session data missing, redirecting to index")
        return redirect(url_for('index'))

    task_id = session['task_id']
    task = tasks.get(task_id)
    if not task or task['status'] != 'completed':
        logger.warning(f"Task {task_id} not completed or not found: {task}")
        return redirect(url_for('index'))

    user_data = session['user_data']
    glm_results = task['glm_results']
    logger.debug(f"Rendering knowledge for task_id {task_id}")

    return render_template('knowledge.html', 
                         gender=user_data['gender'], 
                         age=user_data['age'], 
                         direction=user_data['direction'], 
                         keywords=user_data['keywords'], 
                         nodes=glm_results['nodes'], 
                         links=glm_results['links'])

@app.route('/learning')
def learning():
    if 'user_data' not in session or 'task_id' not in session:
        logger.warning("Session data missing, redirecting to index")
        return redirect(url_for('index'))

    task_id = session['task_id']
    task = tasks.get(task_id)
    if not task or task['status'] != 'completed':
        logger.warning(f"Task {task_id} not completed or not found: {task}")
        return redirect(url_for('index'))

    user_data = session['user_data']
    glm_results = task['glm_results']
    recommend_path_html = markdown.markdown(glm_results['recommend_path'])
    logger.debug(f"Rendering learning for task_id {task_id}")

    return render_template('learning.html', 
                         gender=user_data['gender'], 
                         age=user_data['age'], 
                         direction=user_data['direction'], 
                         keywords=user_data['keywords'], 
                         recommend_path=recommend_path_html)

@app.route('/lagou')
def lagou():
    if 'user_data' not in session or 'task_id' not in session:
        logger.warning("Session data missing, redirecting to index")
        return redirect(url_for('index'))

    task_id = session['task_id']
    task = tasks.get(task_id)
    if not task or task['status'] != 'completed':
        logger.warning(f"Task {task_id} not completed or not found: {task}")
        return redirect(url_for('index'))

    user_data = session['user_data']
    position_results = task['position_results']

    position_names = [rec['position'] for rec in position_results]
    try:
        mysql_conn = pymysql.connect(**mysql_config)
        cursor = mysql_conn.cursor()
        query = "SELECT position_name, data_url, company_full_name, company_size, education, salary, last_login FROM jobs WHERE position_name IN (%s)" % ','.join(['%s'] * len(position_names))
        cursor.execute(query, position_names)
        jobs = cursor.fetchall()
        cursor.close()
        mysql_conn.close()
        logger.debug(f"Queried jobs for positions {position_names}: {len(jobs)} results")
    except Exception as e:
        logger.error(f"Database query failed: {str(e)}")
        return render_template('lagou.html', error=f"数据库查询失败：{str(e)}")

    logger.debug(f"Rendering lagou for task_id {task_id}")
    return render_template('lagou.html', 
                         gender=user_data['gender'], 
                         age=user_data['age'], 
                         direction=user_data['direction'], 
                         keywords=user_data['keywords'], 
                         jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True, port=8888)