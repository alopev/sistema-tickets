from dotenv import load_dotenv
import os
import sys

# Load env vars
load_dotenv()

print("Testing application startup...")

try:
    from app import create_app, socketio
    
    app = create_app()
    
    print("\n✅ Application created successfully")
    print(f"   Debug mode: {app.config.get('DEBUG', False)}")
    print(f"   Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')[:50]}...")
    
    # Check blueprints
    blueprints = list(app.blueprints.keys())
    print(f"\n✅ Registered blueprints ({len(blueprints)}):")
    for bp in blueprints:
        print(f"   - {bp}")
    
    # Check routes
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append(f"{rule.endpoint}: {rule.rule}")
    
    print(f"\n✅ Available routes ({len(routes)}):")
    for route in sorted(routes)[:10]:  # Show first 10
        print(f"   - {route}")
    if len(routes) > 10:
        print(f"   ... and {len(routes) - 10} more")
    
    print("\n✅ Application startup test PASSED!")
    print("\n💡 To run the application:")
    print("   .venv\\Scripts\\python.exe run.py")
    
except Exception as e:
    print(f"\n❌ Application startup test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
