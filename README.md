# Retrieval Augmented Generation with Local LLMs and Qdrant

This project showcases an end-to-end implementation for integrating local language models (LLMs) with Qdrant Vector Database and a choice of relational database management systems (RDBMS). The default RDBMS is SQLite, but the implementation is flexible and can be adapted to other RDBMS based on specific use cases.

## Features

- **Local LLM Integration**: Leverage the power of local LLMs for efficient processing.
- **Vector Database**: Qdrant is used as the Vector Database to manage and retrieve vectorized data efficiently.
- **Relational Database Support**: Default implementation with SQLite; adaptable to other RDBMS systems.
- **Embedding Model**: Utilizes OpenAI's `text-embedding-ada-002` model for generating text embeddings.
- **UI Framework**: User-friendly interface built with Gradio.
- **Ollama Framework**: Supports advanced LLM operations for enhanced functionality.

## Technology Stack

- **Embedding Model**: OpenAI `text-embedding-ada-002`
- **UI Framework**: Gradio
- **Framework for Local LLMs**: Ollama
- **Relational Database**: SQLite (default, customizable)
- **Vector Database**: Qdrant

## Key Workflow

1. **Data Ingestion**: Input data is processed and vectorized using OpenAI's embedding model.
2. **Vector Storage**: Vectorized data is stored in Qdrant for efficient similarity-based searches.
3. **Relational Storage**: Metadata and additional structured data are stored in the relational database.
4. **Retrieval Augmented Generation**:
   - User queries are embedded.
   - Relevant vectors are retrieved from Qdrant.
   - Retrieved data augments the generation process by the LLM.
5. **Interactive UI**: Gradio provides an intuitive interface for users to interact with the system.

## Data Scraping

The data must be ingested into the vector database based on your requirements. This project is based on medical plans, and a separate script was used to crawl and collect medical plans. However, this script is not included in the project. This project can create other applications by modifying the prompt and embedding flow.

## How to Use

### Prerequisites

- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Configuration

1. Set up your preferred RDBMS if not using SQLite.
2. Configure Qdrant and ensure it is running.
3. Update the `config.properties` file with your OpenAI API key and database configurations.

### Run the Application

1. Start the application 
   ``` docker compose up ```
2. Install your choice of LLM model through Ollama
   ```    

### Customization

- Update the database configuration and connection logic in `backend/database` to replace SQLite with your preferred RDBMS.
- Modify the embedding model by updating `backend/services/embedding_service.py`.

## Folder Structure

```
.
├── backend
│   ├── database
│   │   ├── factory.py
│   │   ├── feedback_repository.py
│   │   ├── feedback_service.py
│   │   └── sqlite_feedback_repository.py
│   ├── services
│   │   ├── controller.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   └── qdrant_service.py
│   ├── utils
│   │   ├── config.py
│   │   └── formatters.py
│   ├── Dockerfile
│   ├── app.py
│   └── config.properties
├── ui
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── README.md
├── docker-compose.yml
├── requirements.txt
```

## Screenshots
#### Image 1 User Interface for question input and choice of LLM selection and 
<img width="1586" alt="image" src="https://github.com/user-attachments/assets/ee81026b-d956-4a56-b561-f2e5e2b85391" />

#### Image 2 Retrieving saved history
<img width="1586" alt="image" src="https://github.com/user-attachments/assets/2e2f27b4-ca4f-4e7c-be49-c043c867b024" />


## Future Enhancements

- Support for additional embedding models including local embedding models and frameworks should be added.
- Incorporate advanced vector retrieval techniques.
- Add Reranking logic, RAG fusion and Multi Query Functionalities

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to star, fork and contribute to this project and share your feedback!
