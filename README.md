# Chatbot Project

This project is a chatbot that interacts with users in Telegram, to determine the exact frame that the rocket launched. The chatbot is built using Python and the Telegram Bot API.

## Getting Started

To run the chatbot locally, you'll need to do the following:

1. Clone the project repository.
2. Install the required dependencies using pip install -r requirements.txt.
3. Set up a Telegram bot by following the instructions in the Telegram Bot API documentation.
4. Copy the bot token and paste it into a .env file (see .env.EXAMPLE).
5. Get a HTTPS public URL (eg. ngrok) and paste it into the .env file.
6. Run the chatbot by running main.py.

## Features

The chatbot will interact in the following way:

Use /start to begin the bisection. The chatbot will show you a picture, which you will respond yes or no to whether the rocket has launched. (In the top right of the picture before the time, "-" means not launched, "+" means launched). This will repeat until the exact frame of launch is found.
At any time you can /cancel to stop the bisection.

## Testing

To run the unit tests for the chatbot application, navigate to the project directory and execute the following command:

    python -m unittest discover -v

The `discover` option tells the unittest module to automatically discover and run all tests named "test\_\*" in the project directory and its subdirectories.

The test cases are not contained in a specific folder, but are instead named with the "test\_" prefix. This allows for more flexibility in organizing tests across multiple files and directories.

If you want to run a specific test file, you can specify its path relative to the project directory, like so:

    python -m unittest path/to/test_file.py

You can also run a specific test method by appending the method name to the file path, like so:

    python -m unittest path/to/test_file.py.TestClass.test_method

The `-v` flag enables verbose output, which provides more detailed information about the tests as they run.

Note that you must have all necessary dependencies installed in order for the tests to run properly. See the "Getting Started" section of the README for more information on installing dependencies.```

## Contributing

If you'd like to contribute to the project, feel free to submit a pull request with your changes. Before submitting a pull request, please make sure that your changes pass all the existing unit tests and write new tests if necessary.

## License

This project is licensed under the MIT License
