from src.front.app import app

if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port='8082', debug=True, dev_tools_ui=False)
