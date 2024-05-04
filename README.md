# Handblog

Handblog is a dynamic blogging platform designed to streamline content creation and management. This guide will help you set up and run the project on your local machine.

## Prerequisites

Before you start, ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org).

## Getting Started

### Setting Up the Virtual Environment

Create a virtual environment to manage the project's dependencies separately from your global Python environment:

```bash
python -m venv virt
```

### Activating the Virtual Environment

On macOS and Linux:

```bash
source virt/bin/activate
```

On Windows:

```bash
virt\Scripts\activate
```

### Installing Dependencies

Install all required packages from the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

### Running the Project

Execute the following command to start the project:

```bash
python3 app.py
```

## Usage

Once the application is running, you can access it by navigating to http://localhost:5000 in your web browser (assuming the app runs on port 5000).

## Contributing

We welcome contributions to Handblog. If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.

## Contact

If you have any questions or feedback, please contact chunchiehdev@gmail.com.
