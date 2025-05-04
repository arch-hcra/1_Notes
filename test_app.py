import unittest
import os
from app import app, save_record, read_records, delete_record  # Замените на путь к вашему приложению

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Настройка тестового клиента перед каждым тестом."""
        self.app = app.test_client()
        self.app.testing = True
        # Удаляем файл records.txt перед каждым тестом
        if os.path.exists('records.txt'):
            os.remove('records.txt')

    def test_save_record(self):
        save_record('Test notes')
        records = read_records()
        self.assertEqual(records, ['Test notes'])

    def test_read_records(self):
        save_record('First notes')
        save_record('Second notes')
        records = read_records()
        self.assertEqual(records, ['First notes', 'Second notes'])

    def test_delete_record(self):
        save_record('Note for del')
        delete_record('Note for del')
        records = read_records()
        self.assertEqual(records, [])

    def test_add_record_route(self):
        
        response = self.app.post('/add', data={'text': 'Test notes'})
        self.assertEqual(response.status_code, 302)
        records = read_records()
        self.assertIn('Test notes', records)

    
    def test_delete_record_route(self):
        save_record('Note for del')
        response = self.app.post('/delete', data={'text': 'Note for del'})
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
        records = read_records()
        self.assertNotIn('Note for del', records)

if __name__ == '__main__':
    unittest.main()
