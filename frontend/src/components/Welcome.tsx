import { motion } from 'framer-motion';
import { Settings as Lungs } from 'lucide-react';

export function Welcome({ onComplete }: { onComplete: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1 }}
      onAnimationComplete={onComplete}
      className="flex flex-col items-center justify-center space-y-6 p-8"
    >
      <div className="flex items-center space-x-3">
        <Lungs className="w-16 h-16 text-blue-400" />
        <h1 className="text-5xl font-bold text-white">PneumoScan AI</h1>
      </div>
      <p className="text-xl text-gray-400 text-center max-w-md">
        Advanced pneumonia detection powered by artificial intelligence
      </p>
    </motion.div>
  );
}