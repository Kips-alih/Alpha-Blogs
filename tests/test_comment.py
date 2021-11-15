import unittest
from app.models import Comment,User
from flask_login import current_user
from app import db

class TestComment(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_comment = Comment(id=1,comment='Comment for pitches',date_posted='2021-11-14',user = self.user_id ,pitch_id=12345,)


    def tearDown(self):
        Comment.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))


    def test_check_instance_variables(self):

        self.assertEquals(self.new_comment.comment,'Comment for blogs')
        self.assertEquals(self.new_comment.id,1)
        self.assertEquals(self.new_comment.user,self.user_id)
        self.assertEquals(self.new_comment.pitch_id,12345)



    def test_save_review(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)


    def test_get_review_by_id(self):

        self.new_comment.save_comment()
        got_comments = Comment.get_comments(12345)
        self.assertTrue(len(got_comments) == 1)