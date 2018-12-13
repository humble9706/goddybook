from django.apps import AppConfig


class SimplePostsPostsConfig(AppConfig):
    name = 'simple_posts_posts'

    def ready(self):
    	#import signal handlers
    	import simple_posts_posts.signals
