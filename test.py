from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_game_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_game = {
    'title': 'Cat Images',
    'price': 'Cats acting weird',
    'images': 'https://upload.wikimedia.org/wikipedia/commons/e/ee/Grumpy_Cat_by_Gage_Skidmore.jpg'
    
}
sample_form_data = {
    'title': sample_game['title'],
    'price': sample_game['price'],
    'images': '\n'.join(sample_game['images'])
}


class gamesTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the games homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'game', result.data)

    def test_new(self):
        """Test the new game creation page."""
        result = self.client.get('/games/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New game', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_game(self, mock_find):
        """Test showing a single game."""
        mock_find.return_value = sample_game

        result = self.client.get(f'/games/{sample_game_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat images', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_game(self, mock_find):
        """Test editing a single game."""
        mock_find.return_value = sample_game

        result = self.client.get(f'/games/{sample_game_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat images', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_game(self, mock_insert):
        """Test submitting a new game."""
        result = self.client.post('/games', data=sample_form_data)

        # After submitting, should redirect to that game's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_game)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_game(self, mock_update):
        result = self.client.post(
            f'/games/{sample_game_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_game_id}, {
                                       '$set': sample_game})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_game(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(
            f'/games/{sample_game_id}/delete', data=form_data)
        self.assertEqual(result.status, '308 PERMANENT REDIRECT')
        mock_delete.assert_called_with({'_id': sample_game_id})


if __name__ == '__main__':
    unittest_main()
