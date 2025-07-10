# Databricks RAG Chat App

A modern Streamlit-based chat application that provides an intuitive interface for querying SharePoint data using Databricks' Retrieval-Augmented Generation (RAG) capabilities.

## 🚀 Features

- **Modern UI**: Beautiful, responsive chat interface with custom styling
- **RAG Integration**: Powered by Databricks model serving endpoints
- **SharePoint Data**: Query and retrieve information from SharePoint documents
- **User Authentication**: Built-in user identification and session management
- **Real-time Chat**: Interactive conversation flow with message history
- **Deployment Ready**: Configured for cloud deployment with environment variables

## 📋 Prerequisites

- Python 3.8+
- Databricks workspace with model serving capabilities
- Access to SharePoint data
- MLflow deployment client configured

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chat-app-kp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export SERVING_ENDPOINT="your-databricks-serving-endpoint-name"
   ```

## 🚀 Usage

### Local Development

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8501`

### Cloud Deployment

The app is configured for deployment with the following files:

- `app.yaml`: Deployment configuration for cloud platforms
- `requirements.txt`: Python dependencies
- Environment variables configured for serving endpoint integration

## 🏗️ Architecture

### Core Components

- **`app.py`**: Main Streamlit application with UI and chat logic
- **`model_serving_utils.py`**: Databricks model serving integration utilities
- **`requirements.txt`**: Python dependencies
- **`app.yaml`**: Deployment configuration

### Key Features

- **Session Management**: Persistent chat history and user state
- **User Authentication**: Automatic user identification from request headers
- **Responsive Design**: Mobile-friendly interface with custom CSS styling
- **Error Handling**: Graceful error handling and user feedback

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SERVING_ENDPOINT` | Databricks model serving endpoint name | Yes |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | Disable Streamlit usage statistics | No |

### Model Serving Endpoint

The app requires a Databricks model serving endpoint that supports:
- Chat completion task type
- Conversational agent schema
- Message-based input/output format

## 🎨 UI Features

- **Dark Theme**: Modern dark color scheme with neon accents
- **Chat Interface**: Clean, intuitive chat layout
- **Responsive Design**: Works on desktop and mobile devices
- **Custom Styling**: Tailored CSS for professional appearance
- **Message History**: Persistent conversation threads

## 🔒 Security

- User authentication via request headers
- Environment variable configuration
- Secure model serving endpoint integration
- Input validation and sanitization

## 📝 API Integration

The app integrates with Databricks model serving endpoints using MLflow's deployment client:

```python
from mlflow.deployments import get_deploy_client

# Query endpoint with messages
response = get_deploy_client('databricks').predict(
    endpoint=endpoint_name,
    inputs={'messages': messages, "max_tokens": max_tokens}
)
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment
1. Configure your cloud platform (Google Cloud, AWS, Azure)
2. Set environment variables
3. Deploy using the provided `app.yaml` configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Kaustav Paul**

## 🆘 Support

For support and questions:
- Check the Databricks documentation for model serving
- Review the Streamlit documentation for UI components
- Open an issue in the repository

---

**Note**: This application requires proper configuration of Databricks model serving endpoints and SharePoint data access. Ensure all prerequisites are met before deployment. 