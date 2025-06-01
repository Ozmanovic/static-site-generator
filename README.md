# Static Site Generator

**A guided project from [Boot.dev](https://www.boot.dev/courses/build-static-site-generator-python)**

This is a custom-built static site generator written in Python that converts Markdown files into a complete HTML website. The project demonstrates core programming concepts including file I/O, recursive algorithms, HTML/CSS generation, and command-line interfaces.

## Project Description

This static site generator takes Markdown content files and converts them into a fully functional static website. It features:

- **Markdown to HTML conversion**: Supports headings, paragraphs, lists, links, images, code blocks, and blockquotes
- **Template system**: Uses a customizable HTML template for consistent page layout
- **Recursive directory processing**: Automatically processes nested content directories
- **Static asset copying**: Copies CSS, images, and other static files to the output directory
- **Local development server**: Built-in HTTP server for testing the generated site
- **Configurable base paths**: Support for deployment to subdirectories

The generator processes content from the `content/` directory, applies the `template.html` template, copies static assets from `static/`, and outputs everything to the `docs/` directory.

## Installation Instructions

### Prerequisites

- **Python 3.6 or higher** - Check your version with `python3 --version`
- **Git** (optional) - For cloning the repository

### Setup Steps

1. **Clone or download the repository**:

   ```bash
   git clone <repository-url>
   cd static-site-generator
   ```

2. **Verify Python installation**:

   ```bash
   python3 --version
   ```

3. **No additional dependencies required** - This project uses only Python standard library modules.

## Usage Instructions

### Basic Usage

The static site generator can be run in several ways:

#### Method 1: Direct Python execution

```bash
python3 src/main.py
```

#### Method 2: Using the build script

```bash
./build.sh
```

#### Method 3: Build and serve locally

```bash
./main.sh
```

### Command-Line Arguments

The generator accepts an optional base path argument for deployment to subdirectories:

```bash
python3 src/main.py "/your-subdirectory/"
```

For example, to deploy to GitHub Pages under a project subdirectory:

```bash
python3 src/main.py "/static-site-generator/"
```

### What Each Command Does

- **`python3 src/main.py`**: Generates the static site with default settings (base path "/")
- **`./build.sh`**: Runs the generator with the "/static-site-generator/" base path
- **`./main.sh`**: Builds the site AND starts a local development server on port 8888

### Expected Output

When you run the generator, you should see output similar to:

```
Copying file: /path/to/static/index.css to /path/to/docs/index.css
Copying file: /path/to/static/images/tolkien.png to /path/to/docs/images/tolkien.png
Generating page from content/index.md to docs/index.html using template.html
Generating page from content/contact/index.md to docs/contact/index.html using template.html
Generating page from content/blog/glorfindel/index.md to docs/blog/glorfindel/index.html using template.html
```

### Viewing Your Site

After generation, your site will be available in the `docs/` directory:

1. **View files directly**: Open `docs/index.html` in your browser
2. **Use the development server**: Run `./main.sh` and visit `http://localhost:8888`

## Project Structure

```
static-site-generator/
├── src/                    # Source code
│   ├── main.py            # Main entry point and site generation logic
│   ├── textnode.py        # Markdown parsing and text node handling
│   ├── htmlnode.py        # HTML node classes and rendering
│   └── test_*.py          # Unit tests
├── content/               # Markdown content files
│   ├── index.md          # Homepage content
│   ├── contact/          # Contact page
│   └── blog/             # Blog posts
├── static/               # Static assets (CSS, images)
│   ├── index.css         # Site stylesheet
│   └── images/           # Image files
├── template.html         # HTML template for all pages
├── docs/                 # Generated output (created by generator)
├── build.sh             # Build script
├── main.sh              # Build and serve script
└── test.sh              # Test runner script
```

## Customization

### Adding Content

1. **Create new Markdown files** in the `content/` directory
2. **Ensure each file starts with an H1 header** (required for page titles)
3. **Use standard Markdown syntax** for formatting
4. **Reference images and links** with paths starting from the root (e.g., `/images/photo.jpg`)

### Modifying the Template

Edit `template.html` to change the site layout. The template uses these placeholders:

- `{{ Title }}` - Replaced with the H1 header from each Markdown file
- `{{ Content }}` - Replaced with the converted HTML content

### Adding Static Assets

Place CSS, images, and other static files in the `static/` directory. They will be copied to `docs/` during generation.

## Testing

Run the test suite to verify everything is working:

```bash
./test.sh
```

Or run tests directly:

```bash
python3 -m unittest discover -s src
```

## Troubleshooting

### Common Issues

1. **"No H1 header found" error**:

   - Ensure each Markdown file starts with a line like `# Page Title`

2. **Permission denied on scripts**:

   ```bash
   chmod +x build.sh main.sh test.sh
   ```

3. **Port 8888 already in use**:

   - Kill the existing process or change the port in `main.sh`

4. **Images not displaying**:
   - Check that image paths in Markdown start with `/` (e.g., `/images/photo.jpg`)
   - Verify images exist in the `static/images/` directory

### Development Tips

- The `docs/` directory is completely regenerated each time you run the generator
- Test your changes locally using `./main.sh` before deploying
- Check the console output for file processing information and errors

## License

This project is part of the Boot.dev curriculum and is intended for educational purposes.
