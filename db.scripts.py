import sqlite3
db_name = 'scholl.db'
conn = None
curor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' видаляє всі таблиці '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()    
    quizes = [
        ('Своя гра', ),
        ('Хто хоче стати мільйонером?', ),
        ('Найрозумніший', )]

    questions = [
        ('Скільки місяців на рік мають 28 днів?', 'Всі', 'Один', 'Жодного', 'Два'),
        ('Яким стане зелена скеля, якщо впаде в Червоне море?', 'Мокрим', 'Червоним', 'Не зміниться', 'Фіолетовим'),
        ('Якою рукою краще розмішувати чай?', 'Ложкою', 'Правий', 'Лівий', 'Будь-який'),
        ("Що не має довжини, глибини, ширини, висоти, а можна виміряти?", "Час", "Дурність", "Море", "Повітря"),
        ('Коли сіткою можна витягнути воду?', 'Коли вода замерзла', 'Коли немає риби', 'Коли спливла золота рибка', 'Коли сітка порвалася'),
        ('Що більше слона і нічого не важить?', 'Тінь слона', 'Повітряна куля', 'Парашут', 'Хмара')]
    
    quiz_content_data = [
        (3, 4),
        (2, 2),
        (1, 3),
        (1, 1),
        (3, 1),
        (2, 4)
    ]

    query = '''CREATE TABLE IF NOT EXISTS quiz (
                id INTEGER PRIMARY KEY,
                Name Text
                
                )'''
     
    do(query)
    query = '''CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY,
                answer TEXT,
                question TEXT,
                wrong_1 TEXT,
                wrong_2 TEXT,
                wrong_3 TEXT
                
                )'''
     
    do(query)
    query = '''CREATE TABLE IF NOT EXISTS quiz_content (
                    id INTEGER PRIMARY KEY,
                    quiz_id INTEGER,
                    question_id INTEGER,
                    FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                    FOREIGN KEY (question_id) REFERENCES question (id))'''
                
    do(query)
    query = '''INSERT INTO question(
        question, answer, wrong_1, wrong_2, wrong_3)
        VALUES (?, ?, ?, ?, ?)
    '''
    cursor.executemany(query, questions)
    query = '''INSERT INTO quiz(
        Name)
        VALUES(?)
    '''
    cursor.executemany(query, quizes)

    query = '''INSERT INTO quiz_content(
        quiz_id, question_id)
        VALUES(?, ?)
    '''
    cursor.executemany(query, quiz_content_data)
    conn.commit()
def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    show_tables()

def get_question_after(question_id, quiz_id):
    open()
    query='''
    SLECT quiz_content.id, question.quietion, question.qnswer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id
    '''
    cursor.execute(query, [question_id, quiz_id])
    res = cursor.fetchone()
    close()
    return res
if __name__ == "__main__":
    main()
