import React from 'react';
import {analyzeIcon} from '../lib/iconAnalysis';
import {Loader2} from 'lucide-react';
import {cn} from '../lib/utils.js';
import ReactMarkdown from 'react-markdown';

export function IconAnalysis({icon, isOpen, onClose}) {
  const [analysis, setAnalysis] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    if (isOpen && !analysis && !loading) {
      setLoading(true);
      setError(null);
      analyzeIcon(icon.title, `/icons/${icon.slug}.svg`)
        .then(result => {
          setAnalysis(result);
          setLoading(false);
        })
        .catch(err => {
          setError(err.message);
          setLoading(false);
        });
    }
  }, [isOpen, icon, analysis]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full mx-4 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          ×
        </button>

        <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">
          AI Analysis: {icon.title}
        </h2>

        {loading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-gray-500" />
          </div>
        )}

        {error && (
          <div className="text-red-500 dark:text-red-400 py-4">
            Error: {error}
          </div>
        )}

        {analysis && (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-gray-200">
                Product Description
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {analysis.productDescription}
              </p>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-gray-200">
                Icon Analysis
              </h3>
              <div className="prose prose-sm dark:prose-invert prose-headings:mb-2 prose-headings:mt-4 prose-p:mt-2 prose-p:mb-2 prose-ul:mt-2 prose-ul:mb-2 prose-li:mt-1 prose-li:mb-1">
                <ReactMarkdown>{analysis.iconAnalysis}</ReactMarkdown>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-gray-200">
                Design Score
              </h3>
              <div className="flex items-center gap-4">
                <div className="h-4 bg-gray-200 dark:bg-gray-600 rounded-full flex-1">
                  <div
                    className={cn(
                      "h-full rounded-full transition-all duration-500",
                      analysis.designScore >= 80 ? "bg-green-500" :
                      analysis.designScore >= 60 ? "bg-yellow-500" :
                      "bg-red-500"
                    )}
                    style={{ width: `${analysis.designScore}%` }}
                  />
                </div>
                <span className="font-mono text-lg font-semibold text-gray-700 dark:text-gray-300">
                  {analysis.designScore}/100
                </span>
              </div>
              {analysis.scoreExplanation && (
                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                  {analysis.scoreExplanation}
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 