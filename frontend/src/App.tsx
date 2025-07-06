import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Welcome } from './components/Welcome';
import { FileUpload } from './components/FileUpload';
import ChatInterface from './components/ChatInterface';

type Stage = 'welcome' | 'upload' | 'chat';

function App() {
  const [stage, setStage] = useState<Stage>('welcome');
  const [result, setResult] = useState<string>('');

  const handleWelcomeComplete = () => {
    setTimeout(() => setStage('upload'), 1000);
  };

  const handleFileUpload = async (file: File) => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze the image');
      }

      const data = await response.json();
      setResult(`I've analyzed your chest X-ray image "${file.name}". Result: ${data.result}`);
      setStage('chat');
    } catch (error) {
      console.error('Error uploading file:', error);
      setResult('There was an error analyzing your image.');
      setStage('chat');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-black to-gray-900 flex items-center justify-center p-6">
      <div className="w-full">
        <AnimatePresence mode="wait">
          {stage === 'welcome' && (
            <motion.div
              key="welcome"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Welcome onComplete={handleWelcomeComplete} />
            </motion.div>
          )}
          {stage === 'upload' && (
            <motion.div
              key="upload"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <FileUpload onUpload={handleFileUpload} />
            </motion.div>
          )}
          {stage === 'chat' && (
            <motion.div
              key="chat"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="w-full max-w-4xl"
            >
              <ChatInterface initialResult={result} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
