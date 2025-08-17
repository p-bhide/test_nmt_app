PROJECT_DIR="nmt_app"
VENV_NAME="nmt_venv"

if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_NAME"
fi

echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

pip install -r requirements_new.txt

cd "$PROJECT_DIR"
export FLASK_APP=app.py
export FLASK_ENV=development 
export FLASK_DEBUG=1

echo "Starting Flask application..."
flask run