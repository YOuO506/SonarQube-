# SonarQube Test Repository

A small, intentionally imperfect sample repository for testing a SonarQube + Jenkins pipeline.

## Included examples

- `src/app.js`: JavaScript examples that can produce code-smell findings and a security hotspot.
- `web/index.html`: markup/accessibility issues to inspect.
- `web/styles.css`: intentionally repetitive styling.
- `config/app.json` and `config/app.xml`: sample configuration files for language/file indexing.
- `python/demo.py`: an optional Python example. Whether Python is analyzed depends on the language analyzer available on your SonarQube server.

## Setup

1. Create a SonarQube project whose **Project Key** is `Sonar_TestRepo` (or change `sonar.projectKey` above to the key you actually create).
2. Upload the contents of this folder to the root of a new GitHub repository. Keep `sonar-project.properties` at the repository root.
3. In the Jenkins Pipeline, change the Git URL to this new repository and make sure the Jenkins SonarQube connection has a valid token.
4. Run the build and open the matching project in SonarQube.

The examples are intentionally imperfect for practice. Do not copy them into a production application.
