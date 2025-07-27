#!/bin/bash

# TaskFlow API Run Script
# DDSE-compliant task management API startup script
# Following MDD-001 product strategy for simple deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="TaskFlow API"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
APP_MODULE="app.main:app"
DEFAULT_HOST="0.0.0.0"
DEFAULT_PORT="8000"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi

    # Check Python version using Python itself (no bc dependency)
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
    PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

    # Check if Python version is 3.8 or higher
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi

    print_success "Python $PYTHON_VERSION found"
}

# Function to setup virtual environment
setup_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
}

# Function to activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    print_success "Virtual environment activated"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."

    # Upgrade pip first
    pip install --upgrade pip

    # Install requirements
    if [ -f "$REQUIREMENTS_FILE" ]; then
        pip install -r "$REQUIREMENTS_FILE"
        print_success "Dependencies installed successfully"
    else
        print_error "Requirements file not found: $REQUIREMENTS_FILE"
        exit 1
    fi
}

# Function to run database initialization
init_database() {
    print_status "Initializing database..."
    # Database will be auto-created by SQLAlchemy on first run
    # This is per ADR-002 data storage strategy
    print_success "Database initialization ready"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    if [ -d "$PROJECT_DIR/tests" ]; then
        python -m pytest tests/ -v
        print_success "Tests completed"
    else
        print_warning "No tests directory found"
    fi
}

# Function to start the application
start_app() {
    local host=${1:-$DEFAULT_HOST}
    local port=${2:-$DEFAULT_PORT}
    local reload=${3:-"--reload"}

    print_status "Starting $PROJECT_NAME..."
    print_status "Host: $host"
    print_status "Port: $port"
    print_status "API Documentation: http://$host:$port/docs"
    print_status "Alternative Documentation: http://$host:$port/redoc"
    print_status "Health Check: http://$host:$port/health"

    echo
    print_success "$PROJECT_NAME is starting..."
    echo

    # Start the FastAPI application with uvicorn
    uvicorn "$APP_MODULE" --host "$host" --port "$port" $reload
}

# Function to show help
show_help() {
    echo "TaskFlow API Run Script"
    echo "DDSE-compliant task management API"
    echo
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  setup           Setup virtual environment and install dependencies"
    echo "  dev             Run in development mode (with auto-reload)"
    echo "  prod            Run in production mode (no auto-reload)"
    echo "  test            Run tests"
    echo "  clean           Clean virtual environment and cache files"
    echo "  help            Show this help message"
    echo
    echo "Options:"
    echo "  --host HOST     Host to bind to (default: $DEFAULT_HOST)"
    echo "  --port PORT     Port to bind to (default: $DEFAULT_PORT)"
    echo
    echo "Examples:"
    echo "  $0 setup                    # Setup environment"
    echo "  $0 dev                      # Run in development mode"
    echo "  $0 dev --host 127.0.0.1     # Run on localhost only"
    echo "  $0 prod --port 3000         # Run in production on port 3000"
    echo "  $0 test                     # Run tests"
    echo
    echo "First time setup:"
    echo "  $0 setup && $0 dev"
    echo
}

# Function to clean up
clean_project() {
    print_status "Cleaning project..."

    # Remove virtual environment
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
        print_success "Virtual environment removed"
    fi

    # Remove Python cache files
    find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true

    # Remove database file if exists
    if [ -f "$PROJECT_DIR/taskflow.db" ]; then
        rm "$PROJECT_DIR/taskflow.db"
        print_success "Database file removed"
    fi

    print_success "Project cleaned"
}

# Function to setup project
setup_project() {
    print_status "Setting up $PROJECT_NAME..."

    check_python
    setup_venv
    activate_venv
    install_dependencies
    init_database

    print_success "Setup completed successfully!"
    echo
    print_status "To start the application, run:"
    print_status "  $0 dev"
    echo
}

# Parse command line arguments
COMMAND=""
HOST="$DEFAULT_HOST"
PORT="$DEFAULT_PORT"

while [[ $# -gt 0 ]]; do
    case $1 in
        setup|dev|prod|test|clean|help)
            COMMAND="$1"
            shift
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Default to help if no command provided
if [ -z "$COMMAND" ]; then
    COMMAND="help"
fi

# Change to project directory
cd "$PROJECT_DIR"

# Execute commands
case $COMMAND in
    setup)
        setup_project
        ;;
    dev)
        if [ ! -d "$VENV_DIR" ]; then
            print_warning "Virtual environment not found. Running setup first..."
            setup_project
        fi
        activate_venv
        start_app "$HOST" "$PORT" "--reload"
        ;;
    prod)
        if [ ! -d "$VENV_DIR" ]; then
            print_error "Virtual environment not found. Please run 'setup' first."
            exit 1
        fi
        activate_venv
        start_app "$HOST" "$PORT" ""
        ;;
    test)
        if [ ! -d "$VENV_DIR" ]; then
            print_error "Virtual environment not found. Please run 'setup' first."
            exit 1
        fi
        activate_venv
        run_tests
        ;;
    clean)
        clean_project
        ;;
    help)
        show_help
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac
