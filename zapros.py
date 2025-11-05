PRAGMA = "PRAGMA foreign_keys=on"

CREATE_VICTOR ='''
CREATE TABLE IF NOT EXISTS victorina(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)'''

CREATE_Q = '''CREATE TABLE IF NOT EXISTS questions(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    txt TEXT,right_ans TEXT, wrong TEXT,
  	score INTEGER
)'''

CREATE_CON = '''CREATE TABLE IF NOT EXISTS content(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
  	v_id INTEGER,
    q_id INTEGER,
    FOREIGN key(v_id) REFERENCES victorina(id),
    FOREIGN key(q_id) REFERENCES questions(id)
)'''

ADD_VICTOR = 'INSERT INTO victorina (name) VALUES '
ADD_QUESTS = 'INSERT INTO questions (txt,right_ans,wrong,score) VALUES '
ADD_CONTENT = 'INSERT INTO content (v_id,q_id) VALUES '

SELECT = 'SELECT * FROM '
DROP = 'DROP TABLE IF EXISTS '
COUNT = 'SELECT COUNT(*) FROM '
NEXT = '''
SELECT content.id, 
       questions.txt, questions.right_ans, questions.wrong, questions.score
    FROM questions, content
    WHERE content.q_id == questions.id
    AND content.id > ? AND content.v_id == ?
    ORDER BY content.id
    LIMIT 1'''

CHECK = '''SELECT content.id, questions.txt, questions.right_ans
    FROM questions, content
    WHERE content.id = ? AND (questions.right_ans LIKE ?)'''

GET_FIRST = '''SELECT q_id
    FROM content
    WHERE v_id = ?
    ORDER BY q_id
    LIMIT 1'''

COUNT_QS = '''SELECT COUNT(*)
FROM content
WHERE v_id = ?'''


QS = [(
    'Какой ты король сегодня?', 'Печенек',
    'Молочка$БАнанов$Всего сущего',1
)
,(
    'Кто ты по жизни?', 'Тупица мохнатулька',
    'Король печенек с молочком$Тупица$Биздарь',1
),(
    'Оформишь ДЦП?', 'ДА',
    'нет$нет$НЕТ',1
),(
    'Откроешь базу и вернёшь моего бр бр патапима?','ДА',
    'НЕТ$НЕЗНАЮ$нет',1
),(
    'Что споёшь соседу по парте','Я ФУФЕЛШМЕРТС',
    'Собака съела стол$aria math$8 800',1
)]


VS = [
    ('Король печенек'),
    ('Король бананов'),
    ('какой ты король сегодня'), 
    ('кто ты по жизни')
]
CONTENT = [
    (3,1),
    (4,2),
    (4,3),
    (4,4),
    (4,5)
]