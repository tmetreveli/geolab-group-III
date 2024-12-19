from models import Comment, User, Product, Dog

comments = Comment.query.get().all()
print(comments)