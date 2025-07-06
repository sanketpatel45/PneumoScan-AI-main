import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Upload, FileImage } from 'lucide-react';

interface FileUploadProps {
  onUpload: (file: File) => void;
}

export function FileUpload({ onUpload }: FileUploadProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onUpload(acceptedFiles[0]);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif']
    },
    maxFiles: 1
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="w-full max-w-xl mx-auto px-4"
    >
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-4">Upload X-Ray Image</h2>
        <p className="text-gray-400">Upload a chest X-ray image for pneumonia detection</p>
      </div>
      
      <div
        {...getRootProps()}
        className={`p-12 border-2 border-dashed rounded-xl text-center cursor-pointer transition-all duration-200
          ${isDragActive 
            ? 'border-blue-400 bg-blue-400/10' 
            : 'border-white/30 hover:border-white/50 hover:bg-white/5'
          }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center space-y-4">
          {isDragActive ? (
            <>
              <FileImage className="w-16 h-16 text-blue-400" />
              <p className="text-xl text-blue-400">Drop your X-ray image here</p>
            </>
          ) : (
            <>
              <Upload className="w-16 h-16 text-white/70" />
              <div className="space-y-2">
                <p className="text-xl text-white">
                  Drag & drop your X-ray image here
                </p>
                <p className="text-sm text-gray-400">
                  or click to select from your computer
                </p>
              </div>
            </>
          )}
        </div>
      </div>
      
      <p className="text-sm text-center text-gray-500 mt-4">
        Supported formats: PNG, JPG, JPEG, GIF
      </p>
    </motion.div>
  );
}