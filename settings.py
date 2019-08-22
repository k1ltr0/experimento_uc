from os import environ

SESSION_CONFIG_DEFAULTS = {"real_world_currency_per_point": 1, "participation_fee": 0}
SESSION_CONFIGS = [
    {
        "name": "my_session",
        "display_name": "my_session",
        "num_demo_participants": 2,
        "app_sequence": ["public_goods"],
    }
]
LANGUAGE_CODE = "en"
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = "vesion 0.0.9"
ROOMS = [{"name": "my_room", "display_name": "my_room"}]

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

SECRET_KEY = environ.get("OTREE_SECRET_KEY")

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ["otree"]
