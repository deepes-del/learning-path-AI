# Learning Path AI 

A modern React  for the Learning Path AI application that generates AI-powered learning paths with modules, YouTube recommendations, and quizzes.

## Features

- **Modern UI**: Clean, responsive design built with React and Vite
- **Learning Path Generation**: Generate comprehensive learning paths for any topic
- **Tabbed Interface**: View modules, YouTube recommendations, and quiz questions in separate tabs
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **API Integration**: Communicates with the FastAPI backend

## Tech Stack

- **React** - Frontend library
- **Vite** - Build tool and development server
- **React Router** - Client-side routing
- **Axios** - HTTP client for API requests
- **React Icons** - Icon library
- **CSS Modules** - Styling

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/          # Page components
├── hooks/          # Custom React hooks
├── utils/          # Utility functions and API service
├── styles/         # CSS files
├── App.jsx         # Main App component
├── main.jsx        # Entry point
```

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend/learning-path-ai
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Development

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Open your browser to `http://localhost:3000`

The development server includes a proxy to the backend API running on `http://localhost:8000`.

### Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## API Integration

The frontend communicates with the FastAPI backend through the following endpoints:

- `POST /api/generate` - Generate a learning path for a topic
- `GET /api/learning-path/:id` - Retrieve a specific learning path (not yet implemented in backend)

## Environment Variables

The frontend uses Vite's proxy feature for API requests in development. In production, you may need to configure your web server to proxy API requests to the backend.

## Deployment

The frontend can be deployed to any static hosting service:

1. Build the application:
   ```bash
   npm run build
   ```

2. Deploy the `dist/` folder to your hosting provider

For cloud deployments, you can use services like:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Google Cloud Storage

## Development Workflow

1. Start the backend server (from the root directory):
   ```bash
   python run.py
   ```

2. Start the frontend development server:
   ```bash
   cd frontend/learning-path-ai
   npm run dev
   ```

3. Open your browser to `http://localhost:3000`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit and push
5. Create a pull request

## License

MIT
