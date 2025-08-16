from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from django.conf import settings

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index('email', unique=True)

        # Sample users (super heroes)
        users = [
            {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Steve Rogers", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "dc"},
            {"name": "Clark Kent", "email": "superman@dc.com", "team": "dc"},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {"name": "marvel", "members": ["ironman@marvel.com", "cap@marvel.com"]},
            {"name": "dc", "members": ["batman@dc.com", "superman@dc.com"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user": "ironman@marvel.com", "activity": "run", "distance": 5},
            {"user": "cap@marvel.com", "activity": "cycle", "distance": 10},
            {"user": "batman@dc.com", "activity": "swim", "distance": 2},
            {"user": "superman@dc.com", "activity": "fly", "distance": 100},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"user": "superman@dc.com", "points": 100},
            {"user": "cap@marvel.com", "points": 80},
            {"user": "ironman@marvel.com", "points": 70},
            {"user": "batman@dc.com", "points": 60},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"user": "ironman@marvel.com", "workout": "bench press", "weight": 200},
            {"user": "cap@marvel.com", "workout": "push ups", "reps": 100},
            {"user": "batman@dc.com", "workout": "pull ups", "reps": 50},
            {"user": "superman@dc.com", "workout": "squat", "weight": 500},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
