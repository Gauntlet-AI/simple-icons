import { Plus, Upload } from 'lucide-react';
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import ReactMarkdown from 'react-markdown';
import { Button } from './ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { cn } from '../lib/utils';

export function UploadLogoModal() {
  const [isOpen, setIsOpen] = useState(false);
  const [businessName, setBusinessName] = useState('');
  const [description, setDescription] = useState('');
  const [brandColor, setBrandColor] = useState('#000000');
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [showTopFade, setShowTopFade] = useState(false);
  const [showBottomFade, setShowBottomFade] = useState(false);
  const scrollContainerReference = React.useRef(null);

  const handleScroll = useCallback((e) => {
    const element = e.target;
    const showTop = element.scrollTop > 10;
    const showBottom =
      element.scrollHeight - element.scrollTop - element.clientHeight > 10;

    setShowTopFade(showTop);
    setShowBottomFade(showBottom);
  }, []);

  // Initial check for fade visibility
  React.useEffect(() => {
    if (scrollContainerReference.current) {
      const element = scrollContainerReference.current;
      setShowBottomFade(element.scrollHeight > element.clientHeight);
    }
  }, [analysisData]);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/svg+xml': ['.svg'],
      'image/png': ['.png'],
    },
    maxFiles: 1,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !businessName || !description) return;

    setIsAnalyzing(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('businessName', businessName);
      formData.append('description', description);
      formData.append('brandColor', brandColor);

      const response = await fetch('/api/analyze-uploaded-logo', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze logo');
      }

      const data = await response.json();
      setAnalysisData(data);
    } catch (error) {
      console.error('Error analyzing logo:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClose = () => {
    setIsOpen(false);
    setFile(null);
    setPreviewUrl('');
    setBusinessName('');
    setDescription('');
    setBrandColor('#000000');
    setAnalysisData(null);
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="icon" className="relative">
          <Plus className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Upload Your Logo</DialogTitle>
          <DialogDescription>
            Upload your logo to get an AI-powered analysis and design score.
          </DialogDescription>
        </DialogHeader>
        {!analysisData ? (
          <form onSubmit={handleSubmit} className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="businessName">Business Name</Label>
              <Input
                id="businessName"
                value={businessName}
                onChange={(e) => setBusinessName(e.target.value)}
                placeholder="Enter your business name"
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="description">Product Description</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Concisely and accurately describe your product/business"
                maxLength={512}
                required
              />
              <p className="text-xs text-muted-foreground">
                {description.length}/512 characters
              </p>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="brandColor">Brand Color (optional)</Label>
              <div className="flex gap-2">
                <Input
                  id="brandColor"
                  type="color"
                  value={brandColor}
                  onChange={(e) => setBrandColor(e.target.value)}
                  className="w-12 p-1 h-10"
                />
                <Input
                  type="text"
                  value={brandColor}
                  onChange={(e) => setBrandColor(e.target.value)}
                  placeholder="#000000"
                  className="font-mono"
                  pattern="^#[0-9A-Fa-f]{6}$"
                />
              </div>
            </div>
            <div className="grid gap-2">
              <Label>Logo</Label>
              <div
                {...getRootProps()}
                className={cn(
                  'border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-colors',
                  isDragActive
                    ? 'border-primary bg-primary/5'
                    : 'border-muted-foreground/25 hover:border-muted-foreground/50'
                )}
              >
                <input {...getInputProps()} />
                {previewUrl ? (
                  <div className="flex flex-col items-center gap-2">
                    <img
                      src={previewUrl}
                      alt="Preview"
                      className="w-16 h-16 object-contain"
                    />
                    <p className="text-sm text-muted-foreground">
                      Click or drag to replace
                    </p>
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-2">
                    <Upload className="w-8 h-8 text-muted-foreground/50" />
                    <p className="text-sm text-muted-foreground">
                      Drop your logo here or click to upload
                    </p>
                    <p className="text-xs text-muted-foreground">
                      SVG or PNG files only
                    </p>
                  </div>
                )}
              </div>
            </div>
            <Button
              type="submit"
              disabled={!file || !businessName || !description || isAnalyzing}
              className="w-full mt-2"
            >
              {isAnalyzing ? 'Analyzing...' : 'Review My Logo'}
            </Button>
          </form>
        ) : (
          <div className="space-y-6 py-4">
            <div className="flex items-center gap-6">
              <img
                src={previewUrl}
                alt="Analyzed Logo"
                className="w-24 h-24 object-contain bg-white rounded-lg shadow-sm"
              />
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-200">
                  {businessName}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mt-1">
                  {analysisData.productDescription}
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-gray-200">
                Icon Analysis
              </h3>
              <div className="relative">
                {showTopFade && (
                  <div className="absolute inset-x-0 top-0 h-4 bg-gradient-to-b from-white dark:from-gray-800 to-transparent pointer-events-none z-10 transition-opacity duration-200" />
                )}
                {showBottomFade && (
                  <div className="absolute inset-x-0 bottom-0 h-4 bg-gradient-to-t from-white dark:from-gray-800 to-transparent pointer-events-none z-10 transition-opacity duration-200" />
                )}
                <div
                  ref={scrollContainerReference}
                  onScroll={handleScroll}
                  className="prose prose-sm dark:prose-invert prose-headings:mb-2 prose-headings:mt-4 prose-p:mt-2 prose-p:mb-2 prose-ul:mt-2 prose-ul:mb-2 prose-li:mt-1 prose-li:mb-1 overflow-y-auto max-h-[40vh] px-6 py-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg shadow-inner scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent hover:scrollbar-thumb-gray-400 dark:hover:scrollbar-thumb-gray-500"
                >
                  <ReactMarkdown>{analysisData.iconAnalysis}</ReactMarkdown>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-gray-200">
                Design Score
              </h3>
              <div className="flex items-center gap-4 bg-gray-50 dark:bg-gray-700/50 p-6 rounded-lg">
                <div className="text-4xl font-bold text-gray-800 dark:text-gray-200">
                  {analysisData.designScore}/100
                </div>
                <div className="flex-1 text-gray-600 dark:text-gray-300">
                  {analysisData.scoreExplanation}
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-3 mt-6 pt-4 border-t">
              <Button variant="outline" onClick={handleClose}>
                Close
              </Button>
              <Button onClick={() => setAnalysisData(null)}>
                Analyze Another Logo
              </Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
} 