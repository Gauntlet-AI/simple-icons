# Simple Icons Codebase Overview

This repository provides over 3,000 SVG icons for popular brands, alongside a build system and associated tooling to ensure consistency and maintainability. Below is a summary of the project’s structure and some guidelines to help you get started.

## Tech Stack

- **Node.js** (version ≥ 18.18.0)  
  Used for running scripts, building the package, and managing dependencies.
- **NPM**  
  Provides package management and script-running capabilities.
- **Docker** (optional)  
  The repo can be containerized to run build and optimization steps safely and consistently.
- **GitHub Actions**  
  CI/CD workflows for linting, testing, and verifying pull requests.

## Repository Structure

- **icons/**  
  Contains all the individual SVG files for each icon.
- **\_data/simple-icons.json**  
  Stores metadata such as titles, colors, and source URLs for each icon.
- **scripts/**  
  Various Node scripts for building, testing, minifying, and updating the package.
- **.github/workflows/**  
  Contains CI/CD pipelines (linting, testing, and publishing).
- **docs/**  
  Intended for documentation like this overview file.
- **README.md**  
  Provides instructions for using the icons, as well as additional usage notes for Node, CDN, and more.

## How to Run Locally

1. Clone the repository (using HTTPS, SSH, or GitHub CLI):

   ```
   git clone https://github.com/simple-icons/simple-icons.git
   ```

   or

   ```
   git clone git@github.com:simple-icons/simple-icons.git
   ```

2. Enter the project directory:

   ```
   cd simple-icons
   ```

3. Install the dependencies:

   ```
   npm install
   ```

4. Run the test suite:

   ```
   npm test
   ```

5. (Optional) Lint the code:

   ```
   npm run lint
   ```

6. If you plan to build or modify the package:
   ```
   npm run build
   ```

After these steps, you will have a local environment set up where you can modify icons, tweak configurations, or contribute new features.

## Using Docker (Optional)

If you prefer working in a containerized environment:

1. Build the Docker image:
   ```
   docker build . -t simple-icons
   ```
2. Run a container with an interactive shell:
   ```
   docker run -it --rm --entrypoint "/bin/ash" simple-icons
   ```
   From inside the container, you can run scripts like you would locally (e.g., npm install, npm test, etc.).

## Code Architecture

1. **Package Creation**  
   The repository wraps the SVG icons in a Node.js package, providing both JavaScript and TypeScript entry points (including a small SDK in “simple-icons/sdk”).
2. **Linting & CI**  
   GitHub Actions workflows ensure new icons and documentation abide by established rules. Pull requests are automatically tested and linted.
3. **Automated Release**  
   The “publish.yml” workflow handles building and publishing the package to npm, as well as preparing generated files (like the minified icons data).

## Contributing

Contributors can add or update icons by:

1. Creating or optimizing an SVG.
2. Adding the icon’s metadata to “\_data/simple-icons.json”.
3. Opening a pull request to the “develop” branch.

For further details, see:

- The main README in the project root for usage instructions.
- CONTRIBUTING.md for guidelines on adding or updating icons.

---

Feel free to extend this documentation with any project-specific needs or processes that emerge as you develop new features or add more icons. If you run into issues, check out the GitHub Discussions or Issues pages for help from the Simple Icons community.
