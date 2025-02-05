import random
import secrets
import string
import openai
from django.utils import timezone
from .models import Artwork, Comment
from django.contrib.auth import get_user_model
from decouple import config

openai_client = openai.OpenAI(
    api_key=config('OPENAI_API_KEY'),
    base_url="https://models.inference.ai.azure.com"
)
User = get_user_model()


def generate_comment(artwork):
    prompt = (
        f"Comment on this artwork made by {artwork.artist.title} titled '{artwork.title}': "
        f"{artwork.description}. Make sure the comment is respectful and relevant to the artwork. "
        "Make it seem like a real user commenting on an art forum. Answer with just the generated comment."
    )
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip() if response.choices else None

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None


def generate_username():
    prompt = "Generate a realistic and concise username for an art forum user, it doesn't have to be art related, be creative. Reply with only the username, nothing else. You can use spaces, numbers, and special characters."
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip() if response.choices else None

def generate_password(length=12):
                characters = string.ascii_letters + string.digits + string.punctuation
                return ''.join(secrets.choice(characters) for _ in range(length))

def post_random_comment():
    artworks = list(Artwork.objects.all())
    if not artworks:
        print("No artworks available for commenting.")
        return None

    artwork = random.choice(artworks)
    comment_text = generate_comment(artwork)

    if not comment_text:
        print("Failed to generate comment text.")
        return None

    if random.choice([True, False]):
        username = generate_username()
        new_user = User.objects.create_user(username=username, password=generate_password())
        new_user.is_staff = True
        new_user.save()
        user = new_user
        print(f"Created new staff user: {user.username}")
    else:
        staff_users = list(User.objects.filter(is_staff=True))
        if not staff_users:
            username = generate_username()
            new_user = User.objects.create_user(username=username, password=generate_password())
            new_user.is_staff = True
            new_user.save()
            user = new_user
            print(f"No existing staff users. Created new staff user: {user.username}")
        else:
            user = random.choice(staff_users)
            print(f"Using existing staff user: {user.username}")

    Comment.objects.create(
        artwork=artwork,
        user=user,
        text=comment_text,
        created_at=timezone.now()
    )
    print(f"Posted comment by {user.username}: {comment_text}")

    return comment_text
