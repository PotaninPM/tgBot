import sqlite3
import time
class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        
    def add_user_mark(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `marks` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
        
    def set_nickname(self,user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname,user_id,))
    
    #действие выдачи промокода
    def set_promo_action(self,user_id, promo_action):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `promo_action` = ? WHERE `user_id` = ?", (promo_action, user_id,))
    
    #выбрать действие подписки
    def get_promo_action(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `promo_action` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                promo_action = str(row[0])
            return promo_action
    
    #выбрать автора промокода
    def get_promo_name(self, author):
        author1 = None
        with self.connection:
            result = self.cursor.execute("SELECT `promo` FROM `promes` WHERE `promo` = ?", (author,)).fetchall()
            for row in result:
                author1 = str(row[0])
        return author1
    
    #есть ли промо у пользователя
    def get_promo_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `promo` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                promo1 = str(row[0])
        return promo1
    #промо для админа
    def get_promo_user_1(self, nickname):
        with self.connection:
            result = self.cursor.execute("SELECT `promo` FROM `users` WHERE `nickname` = ?", (nickname,)).fetchall()
            for row in result:
                promo1 = str(row[0])
        return promo1
    
    #плюс доп промокоды
    def give_queries_promo(self, user_id, promo_queries):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + ? WHERE user_id = ?", (promo_queries, user_id,))

    #выбрать скидку промокода
    def get_promo_disc(self, author):
        disc1 = '0'
        with self.connection:
            result = self.cursor.execute("SELECT `discount` FROM `promes` WHERE `promo` = ?", (author,)).fetchall()
            for row in result:
                disc1 = str(row[0])
        return disc1
    
     #выбрать доп запросы промокода
    def get_promo_queries(self, author):
        queries1 = None
        with self.connection:
            result = self.cursor.execute("SELECT `dop_queries` FROM `promes` WHERE `promo` = ?", (author,)).fetchall()
            for row in result:
                queries1 = str(row[0])
        return queries1
        
    #записать ник кому выдать подписку
    def set_give_nickname(self,user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `sub_give` = ? WHERE `user_id` = ?", (nickname, user_id,))
    
    #выбрать ник кому выыдать подписку
    def get_give_nickname(self,user_id):
        with self.connection:
            result1 =  self.cursor.execute("SELECT `sub_give` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result1:
                get = str(row[0])
            return get
    #время кому выдать подписку
    def set_time_sub1(self, nickname, time_sub):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET time_sub = ? WHERE `nickname` = ?", (time_sub, nickname))
    #общая оценка
    def set_mark(self,user_id, mark):
        with self.connection:
            return self.cursor.execute('INSERT INTO `marks` (user_id, mark) VALUES (?, ?)', (user_id, mark,))
        
    #активация промокода
    def set_promo(self,user_id, promo):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `promo` = ? WHERE `user_id` = ?", (promo, user_id,))
    #удаление промокода
    def delete_promo(self,user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `promo` = 'none' WHERE `user_id` = ?", (user_id,))
    #проверка на повторение ника
    def nickname_exists(self,nickname):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `nickname` = ?", (nickname,)).fetchall()
            return bool(len(result))
        
    def get_signup(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup
        
    def set_signup(self,user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))
    
    def get_nickname(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            nickname1 = None
            for row in result:
                nickname1 = str(row[0])
            return nickname1
        
    def get_sub(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `state_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                sub = str(row[0])
            return sub
    #добавление почты
    def set_email(self,user_id, email):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `email` = ? WHERE `user_id` = ?", (email, user_id,))
    #взять почту
    def get_email(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `email` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                email = str(row[0])
            return email
    #статус подписки у юзера
    def get_sub_1(self,nickname):
        with self.connection:
            state = None
            result2 = self.cursor.execute("SELECT `state_sub` FROM `users` WHERE `nickname` = ?", (nickname,)).fetchall()
            for row in result2:
                state = str(row[0])
            return state

    def give_sub_new(self,user_id):
        new = "Заглянувший"
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'Заглянувший' WHERE user_id = ?", (user_id,))

    def give_sub_inter(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'Интересующийся' WHERE user_id = ?", (user_id,))

    def give_sub_pro(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'Продвинутый' WHERE user_id = ?", (user_id,))

    def give_sub_exp(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'Эксперт' WHERE user_id = ?", (user_id,))
    #выдать подписку по нику
    def give_sub_new1(self,nickname):
        new = "Заглянувший"
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'Заглянувший' WHERE nickname= ?", (nickname,))
            self.cursor.execute("UPDATE `users` SET queries = queries + 60 WHERE nickname= ?", (nickname,))

    def give_sub_inter1(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'Интересующийся' WHERE nickname = ?", (nickname,))
            self.cursor.execute("UPDATE `users` SET queries = queries + 150 WHERE nickname= ?", (nickname,))
    def give_sub_pro1(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'Продвинутый' WHERE nickname = ?", (nickname,))
            self.cursor.execute("UPDATE `users` SET queries = queries + 240 WHERE nickname= ?", (nickname,))
    def give_sub_exp1(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'Эксперт' WHERE nickname = ?", (nickname,))
            self.cursor.execute("UPDATE `users` SET queries = queries + 330 WHERE nickname= ?", (nickname,))
    def give_queries60(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 60 WHERE nickname = ?", (nickname,))
    #
    def get_queries(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `queries` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                queries = str(row[0])
            return queries
    #узнать запросы приветственные
    def get_queries_pr(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `queries_pr` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                queries_pr = str(row[0])
            return queries_pr
    #удалить подписку
    def del_sub(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'неактивна' WHERE user_id = ?", (user_id,))
    
    #удалить подписку для админа
    def del_sub_admin(self, nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET state_sub = 'неактивна' WHERE nickname = ?", (nickname,))
            self.cursor.execute("UPDATE `users` SET time_sub = 0 WHERE nickname = ?", (nickname,))
    #удалить запросы платные
    def del_queries(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries - 1 WHERE user_id = ?", (user_id,))
    #удалить запросы для админа
    def del_queries_admin(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = 0 WHERE nickname = ?", (nickname,))
    #удалить запросы бесплатные
    def del_queries_pr(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries_pr = queries_pr - 1 WHERE user_id = ?", (user_id,))
    #выдать запросы
    def give_queries60(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 60 WHERE user_id = ?", (user_id,))
    
    #выдать запросы для админа
    def give_queries_1(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 1 WHERE nickname = ?", (nickname,))
        
    def give_queries150(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 150 WHERE user_id = ?", (user_id,))
    
    def give_queries240(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 240 WHERE user_id = ?", (user_id,))

    def give_queries330(self,user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 330 WHERE user_id = ?", (user_id,))

#для админа
    def give_queries60_1(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 60 WHERE `nickname` = ?", (nickname,))
            
    def give_queries150_1(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 150 WHERE `nickname` = ?", (nickname,))
        
    def give_queries240_1(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 240 WHERE `nickname` = ?", (nickname,))
    def give_queries330_1(self,nickname):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET queries = queries + 330 WHERE `nickname` = ?", (nickname,))
#установить время подписки(не то время)
    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET time_sub = ? WHERE user_id = ?", (time_sub,user_id,))
#установить то время
    def set_time_sub_end(self, user_id, time_end):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET time_end = ? WHERE user_id = ?", (time_end,user_id,))
    def get_time_sub(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub
    
    def get_sub_status(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            if(time_sub > int(time.time())):
                return True
            else:
                return False
    
    def get_email_per(self, nickname):
        with self.connection:
            result3 = self.cursor.execute("SELECT `email` FROM `users` WHERE `nickname` = ?", (nickname,)).fetchall()
            email1 = None  # initialize to None in case no rows are returned
            for row in result3:
                email1 = str(row[0])
            return email1
    
    #для админа

    def change_action1(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET action = '1' WHERE user_id = ?", (user_id,))
    
    def change_action2(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET action = '2' WHERE user_id = ?", (user_id,))
    
    def change_action3(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET action = '3' WHERE user_id = ?", (user_id,))
    
    def change_action4(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET action = '4' WHERE user_id = ?", (user_id,))
    
    def change_action5(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET action = '5' WHERE user_id = ?", (user_id,))

    def get_action(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `action` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                action = int(row[0])
            return action

    #оценка ответа бота
    def set_answer(self,user_id, mark_answer):
        with self.connection:
            return self.cursor.execute('INSERT INTO `answer` (user_id, mark_answer) VALUES (?, ?)', (user_id, mark_answer,))
        
    
        
