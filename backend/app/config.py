# app/config.py
import os

DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", "http://dynamodb:8000")
AWS_REGION = os.getenv("AWS_REGION", "us-west-2") 