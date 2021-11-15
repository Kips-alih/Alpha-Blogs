import unittest
from app.models import Blog

class BlogTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Blog class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_blog = Blog(1234,'Pickup','Pickup Lines','Superb idea',6/11/2021,3)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog,Blog))
