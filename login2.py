import sqlite3
from config import DATABASE

# Varsayılan beceriler ve durumlar (bot ilk kez çalıştırıldığında eklenecek)
skills = [(_,) for _ in (['Python', 'SQL', 'API', 'Discord'])]
statuses = [(_,) for _ in ([
    'Prototip Oluşturma',
    'Geliştirme Aşamasında',
    'Tamamlandı, kullanıma hazır',
    'Güncellendi',
    'Tamamlandı, ancak bakımı yapılmadı'
])]


class DB_Manager:
    """Veritabanı yönetimi sınıfı.
    Proje, beceri, durum gibi tüm CRUD işlemleri (oluşturma, okuma, güncelleme, silme)
    bu sınıf üzerinden yürütülür.
    """

    def __init__(self, database):
        self.database = database

    # ------------------- 📦 TABLO OLUŞTURMA ------------------- #
    def create_tables(self):
        """Veritabanında gerekli tüm tabloları oluşturur."""
        conn = sqlite3.connect(self.database)
        with conn:
            # Projeler tablosu
            conn.execute('''CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                project_name TEXT NOT NULL,
                description TEXT,
                url TEXT,
                image_name TEXT, -- 📸 proje resmi dosya adı
                status_id INTEGER,
                FOREIGN KEY(status_id) REFERENCES status(status_id)
            )''')

            # Beceriler tablosu
            conn.execute('''CREATE TABLE IF NOT EXISTS skills (
                skill_id INTEGER PRIMARY KEY,
                skill_name TEXT UNIQUE
            )''')

            # Proje-beceri bağlantısı
            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills (
                project_id INTEGER,
                skill_id INTEGER,
                FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
                FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
            )''')

            # Durum tablosu
            conn.execute('''CREATE TABLE IF NOT EXISTS status (
                status_id INTEGER PRIMARY KEY,
                status_name TEXT UNIQUE
            )''')
            conn.commit()

    # ------------------- 💾 TEMEL SQL METODLARI ------------------- #
    def __executemany(self, sql, data):
        """Birden fazla veri ekleme/güncelleme işlemini yürütür."""
        conn = sqlite3.connect(self.database)
        with conn:
            try:
                conn.executemany(sql, data)
                conn.commit()
            except sqlite3.Error as e:
                print("Veritabanı hatası:", e)

    def __select_data(self, sql, data=tuple()):
        """SELECT sorguları için yardımcı metod."""
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    # ------------------- 🔰 BAŞLANGIÇ VERİLERİ ------------------- #
    def default_insert(self):
        """Varsayılan beceri ve durumları veritabanına ekler."""
        sql = 'INSERT OR IGNORE INTO skills (skill_name) VALUES (?)'
        self.__executemany(sql, skills)
        sql = 'INSERT OR IGNORE INTO status (status_name) VALUES (?)'
        self.__executemany(sql, statuses)

    # ------------------- 🧱 PROJE İŞLEMLERİ ------------------- #
    def insert_project(self, data):
        """Yeni proje ekler."""
        sql = '''INSERT INTO projects 
        (user_id, project_name, description, url, image_name, status_id)
        VALUES (?, ?, ?, ?, ?, ?)'''
        self.__executemany(sql, data)

    def get_projects(self, user_id):
        """Belirli bir kullanıcının tüm projelerini getirir."""
        sql = '''
        SELECT projects.project_id, projects.project_name, projects.description, 
               projects.url, projects.image_name, status.status_name 
        FROM projects 
        JOIN status ON projects.status_id = status.status_id
        WHERE user_id = ?'''
        return self.__select_data(sql, (user_id,))

    def get_project_id(self, project_name, user_id):
        """Belirli bir proje adının ID’sini döndürür."""
        result = self.__select_data(
            'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?',
            (project_name, user_id,)
        )
        return result[0][0] if result else None

    def get_project_info(self, user_id, project_name):
        """Bir projenin tüm bilgilerini döndürür."""
        sql = """
        SELECT project_name, description, url, image_name, status_name 
        FROM projects 
        JOIN status ON status.status_id = projects.status_id
        WHERE project_name=? AND user_id=?
        """
        return self.__select_data(sql, (project_name, user_id))

    def update_projects(self, param, data):
        """Bir projenin belirli bir alanını günceller.
        data = (yeni_değer, project_name, user_id)
        """
        sql = f'UPDATE projects SET {param} = ? WHERE project_name = ? AND user_id = ?'
        self.__executemany(sql, [data])

    def delete_project(self, user_id, project_id):
        """Bir projeyi tamamen siler."""
        sql = 'DELETE FROM projects WHERE user_id = ? AND project_id = ?'
        self.__executemany(sql, [(user_id, project_id)])

    # ------------------- 🎯 BECERİ İŞLEMLERİ ------------------- #
    def get_skills(self):
        """Tüm becerileri döndürür."""
        return self.__select_data('SELECT * FROM skills')

    def get_project_skills(self, project_name):
        """Bir projenin sahip olduğu becerileri döndürür."""
        sql = '''
        SELECT skill_name FROM projects 
        JOIN project_skills ON projects.project_id = project_skills.project_id 
        JOIN skills ON skills.skill_id = project_skills.skill_id 
        WHERE project_name = ?
        '''
        res = self.__select_data(sql, (project_name,))
        return ', '.join([x[0] for x in res])

    def insert_skill(self, user_id, project_name, skill_name):
        """Bir projeye beceri ekler."""
        project_id = self.get_project_id(project_name, user_id)
        skill_id = self.__select_data(
            'SELECT skill_id FROM skills WHERE skill_name = ?', (skill_name,)
        )[0][0]
        sql = 'INSERT INTO project_skills (project_id, skill_id) VALUES (?, ?)'
        self.__executemany(sql, [(project_id, skill_id)])

    def delete_skill(self, project_id, skill_id):
        """Bir projeden belirli bir beceriyi kaldırır."""
        sql = 'DELETE FROM project_skills WHERE project_id = ? AND skill_id = ?'
        self.__executemany(sql, [(project_id, skill_id)])

    def insert_skill_name(self, skill_name):
        """Yeni bir beceri ismini veritabanına ekler."""
        sql = 'INSERT OR IGNORE INTO skills (skill_name) VALUES (?)'
        self.__executemany(sql, [(skill_name,)])

    # ------------------- 📊 DURUM İŞLEMLERİ ------------------- #
    def get_statuses(self):
        """Tüm proje durumlarını döndürür."""
        sql = 'SELECT * FROM status'
        return self.__select_data(sql)

    def get_status_id(self, status_name):
        """Bir durum adının ID’sini döndürür."""
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        return res[0][0] if res else None

    def insert_status_name(self, status_name):
        """Yeni bir durum adı ekler."""
        sql = 'INSERT OR IGNORE INTO status (status_name) VALUES (?)'
        self.__executemany(sql, [(status_name,)])


# ------------------- 🚀 TEST VE BAŞLANGIÇ ------------------- #
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()
    manager.insert_project([
        (
            1,
            'Yapay Zeka Projesi',
            'AI tabanlı chatbot',
            'http://example.com',
            'ai_project.png',
            manager.get_status_id('Prototip Oluşturma')
        )
    ])
    print("Veritabanı hazırlandı ve örnek proje eklendi.")
