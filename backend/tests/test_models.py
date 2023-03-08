from django.test import TestCase
from api.models import User, Author, Post, Comment, Like, Follow, Inbox
from django.db.utils import IntegrityError

# developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
class TestModels(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("johndoe")
        self.user2 = User.objects.create_user("katedoe")
        self.author1 = Author.objects.create(user=self.user1, displayName='John Doe')
        self.author2 = Author.objects.create(user=self.user2, displayName='Kate Doe')
        self.post = Post.objects.create(title='My first post', author=self.author1)
        self.comment = Comment.objects.create(comment='Cool post!', author=self.author1, _post_id = self.post._id, _post_author_id=self.author1._id)
        self.like = Like.objects.create(summary='John Doe likes your post.', author=self.author1)
        self.follow = Follow.objects.create(actor=self.author1, object=self.author2)
        self.inbox = Inbox.objects.create(author=self.author1)

    # Author Tests

    def test_author_exists(self):
        author = Author.objects.get(pk=self.author1._id)
        self.assertEqual(author.displayName, 'John Doe')

    def test_author_no_user(self):
        """Author without a user should violate integrity"""
        self.assertRaises(IntegrityError, lambda: Author.objects.create())

    def test_author_duplicate_user(self):
        """Multiple authors for the same User should violate integrity"""
        self.assertRaises(IntegrityError, lambda: Author.objects.create(user=self.user2))

    # Post Tests

    def test_post_exists(self):
        post = Post.objects.get(pk=self.post._id)
        self.assertEqual(post.title, 'My first post')

    def test_post_no_author(self):
        """Post with no author should violate integrity"""
        self.assertRaises(Post.author.RelatedObjectDoesNotExist, lambda: Post.objects.create(title='Post with no author'))

    # Comment Tests

    def test_comment_exists(self):
        comment = Comment.objects.get(pk=self.comment._id)
        self.assertEqual(comment.comment, 'Cool post!')

    def test_comment_no_author(self):
        """Comment with no author should violate integrity"""
        self.assertRaises(IntegrityError, lambda: Comment.objects.create(comment='Comment with no author'))

    # Like Tests

    def test_like_exists(self):
        like = Like.objects.get(pk=self.like._id)
        self.assertEqual(like.summary, 'John Doe likes your post.')

    def test_like_no_author(self):
        """Like without an author should violate integrity"""
        self.assertRaises(IntegrityError, lambda: Like.objects.create())

    # Follow Tests

    def test_follow_exists(self):
        follow = Follow.objects.get(pk=self.follow._id)
        self.assertEqual(follow.actor.displayName, 'John Doe')
        self.assertEqual(follow.object.displayName, 'Kate Doe')
    
    def test_follow_no_actor(self):
        """Follow request with no actor (from author) should violate integrity"""
        self.assertRaises(IntegrityError, lambda: Follow.objects.create(object=self.author2))

    def test_follow_no_object(self):
        """Follow request with no object (to author) should violate integrity"""
        self.assertRaises(IntegrityError, lambda: Follow.objects.create(actor=self.author1))

    # Inbox Tests

    def test_inbox_exists(self):
        inbox = Inbox.objects.get(pk=self.inbox._id)
        self.assertEqual(inbox.author.displayName, 'John Doe')

    def test_inbox_add_post(self):
        """Test adding a post to an authors inbox"""
        self.assertEqual(len(self.inbox.items.all()), 0)
        self.inbox.items.add(self.post)
        self.assertEqual(len(self.inbox.items.all()), 1)
        self.assertEqual(self.inbox.items.get(pk=self.post._id), self.post)

    def test_inbox_no_author(self):
        """Inbox belonging to no author should violate integrity"""
        self.assertRaises(IntegrityError, lambda: Inbox.objects.create())