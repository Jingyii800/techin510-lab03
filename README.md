# 📖 CharGPT Prompts Library
Welcome to the Prompt Library, the ideal place for storing and querying custom ChatGPT prompts. Enhance the productivity with easy access to a variety of prompts tailored for different contexts.

## Features

- **Prompt Management**: Create, read, update, and delete prompts with ease.
- **Prompt Search**: Quickly find prompts with a keyword search function.
- **Favorite**: Mark prompts as favorites for swift access.
- **Sort and Filter**: Organize your prompts by date or favorites.
- **Prompt Templates**: Copy templates for generating ChatGPT prompts.

## Getting Started

- Clone this repository and set up your virtual environment:
```bash
pip install -r requirements.txt
```
- Optional: Create a database and replace the database URL in '.env":
```bash
DATABASE_URL=[YOUR DATABASE URL]
```
- Run the app:
```bash
streamlit run app.py
```

## Preview
![image](https://github.com/Jingyii800/techin510-lab03/assets/112589476/a62939bb-98b6-4e1e-adbc-7a21fe463b58)

## Lessons Learned
- Streamlit Interactivity: Leveraging Streamlit's interactive widgets improves user engagement.
- Database Operations: Employing psycopg2 for PostgreSQL management enhances data handling efficiency.
- User-Driven Design: Implementing user-centric features such as search and favorites demonstrates the importance of UX design.

## Future Improvements
- Advanced Search: Implement full-text search for more nuanced prompt retrieval.
- Rich Text Editing: Introduce rich text editors for better prompt formatting.
- Template Variables: Allow users to define variables within templates for more dynamic prompt generation.
