# Markdown-Web

This setup provides a basic '*framework*' to create a set of searchable static webpages from markdown files. It is designed for customizable, one-time applications. It serves well for rapidly deploying static documentation that can be tailored for internal requirements.

Its primary strength lies in its ease of customization, allowing straightforward adjustment of files to fit specific project requirements. 

This flexibility enables actions such as:

- Have [Paramiko](https://www.paramiko.org/) to connect to management servers, fetch information, and save them to a markdown file that is then converted to HTML and served for internal documentation.
- Pull SFTP CSV data dumps from a remote server, convert the CSV files to markdown, and then served them behind a Cloudflare Zero Trust proxy to provide business reports.
- Pull from an email server for a dedicated Status email, validate email is from an authorized source, and then convert the email to markdown and serve it for display.

