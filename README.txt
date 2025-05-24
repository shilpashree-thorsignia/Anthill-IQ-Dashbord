# Using Existing Railway Tables with Django

If you already have tables in your Railway PostgreSQL database, you should still define Django models that match the structure of those tables. This allows you to use Django's ORM to fetch and display data easily in your application.

## How to Use an Existing Table

1. **Define a Django model** that matches your table's columns.
2. **Tell Django not to manage the table** by adding the following to your model's Meta class:

    class Meta:
        managed = False
        db_table = 'contact'

This ensures Django will use the existing table and will not try to create, modify, or delete it during migrations.

## Example: Contact Model

    class Contact(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()
        phone = models.CharField(max_length=20)
        company = models.CharField(max_length=100)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name

        class Meta:
            managed = False
            db_table = 'contact'

## Why Not Use Raw SQL?

Using Django models gives you all the benefits of the Django ORM, including security, easy querying, and integration with the rest of your Django app. Raw SQL is possible, but not recommended unless you have a specific reason.

# Vercel Deployment Instructions

## 1. Environment Variables
In your Vercel dashboard, add the following environment variables for your project:
- `SECRET_KEY` (use the generated Django secret key)
- `DATABASE_URL` (your Railway PostgreSQL URL)
- `DEBUG` (set to `False` for production)
- `ALLOWED_HOSTS` (set to `.vercel.app,your-custom-domain.com`)

## 2. Static Files
Django is configured to use WhiteNoise for static file serving. No extra setup is needed for static files on Vercel.

## 3. vercel.json
The `vercel.json` file is already set up to use the Django WSGI application:
```
{
    "version": 2,
    "builds": [
        {
            "src": "anthill_iq/wsgi.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "anthill_iq/wsgi.py"
        }
    ]
}
```

## 4. Requirements
All required packages for Django and deployment are listed in `requirements.txt`.

## 5. Deploy
- Push your code to GitHub.
- Connect your repository to Vercel.
- Set the environment variables as above.
- Deploy! 