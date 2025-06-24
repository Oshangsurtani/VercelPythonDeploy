from app import app

# This is the entry point for Vercel
def handler(request, context):
    return app(request.environ, request.start_response)

# Also export app directly for Vercel
application = app