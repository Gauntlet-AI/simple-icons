import React from 'react';
import {analyzeIcon, getDesignScore} from '../lib/iconAnalysis';
import {Loader2} from 'lucide-react';
import {cn} from '../lib/utils.js';
import ReactMarkdown from 'react-markdown';

export function IconAnalysis({icon, isOpen, onClose}) {
  const [analysis, setAnalysis] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [score, setScore] = React.useState(null);
  const [scoreLoading, setScoreLoading] = React.useState(false);
  const [scoreError, setScoreError] = React.useState(null);
  const [showTopFade, setShowTopFade] = React.useState(false);
  const [showBottomFade, setShowBottomFade] = React.useState(false);
  const scrollContainerRef = React.useRef(null);

  const handleScroll = React.useCallback((e) => {
    const element = e.target;
    const showTop = element.scrollTop > 10;
    const showBottom = element.scrollHeight - element.scrollTop - element.clientHeight > 10;
    
    setShowTopFade(showTop);
    setShowBottomFade(showBottom);
  }, []);

  // Initial check for fade visibility
  React.useEffect(() => {
    if (scrollContainerRef.current) {
      const element = scrollContainerRef.current;
      setShowBottomFade(element.scrollHeight > element.clientHeight);
    }
  }, [analysis]);

  React.useEffect(() => {
    if (isOpen && !analysis && !loading) {
      setLoading(true);
      setError(null);
      analyzeIcon(icon.title, `/icons/${icon.slug}.svg`)
        .then(result => {
          console.log('Initial Analysis Response:', result);
          setAnalysis(result);
          setLoading(false);
          
          // After getting the analysis, fetch the score
          setScoreLoading(true);
          setScoreError(null);
          return getDesignScore(result.productDescription, result.iconAnalysis);
        })
        .then(scoreResult => {
          console.log('Score Response:', scoreResult);
          setScore(scoreResult);
          setScoreLoading(false);
        })
        .catch(err => {
          console.error('API Error:', err);
          if (!analysis) {
            setError(err.message);
            setLoading(false);
          } else {
            setScoreError(err.message);
            setScoreLoading(false);
          }
        });
    }
  }, [isOpen, icon, analysis]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 overflow-y-auto p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full my-4 relative max-h-[90vh] flex flex-col">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          ×
        </button>

        <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white flex items-center gap-4">
          <div className="w-8 h-8 flex items-center justify-center">
            <img src={`/icons/${icon.slug}.svg`} alt={icon.title} className="w-6 h-6" />
          </div>
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
          <div className="space-y-6 flex-1 flex flex-col min-h-0">
            <div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-gray-200">
                Product Description
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {analysis.productDescription}
              </p>
            </div>

            <div className="flex-1 min-h-0">
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
                  ref={scrollContainerRef}
                  onScroll={handleScroll}
                  className="prose prose-sm dark:prose-invert prose-headings:mb-2 prose-headings:mt-4 prose-p:mt-2 prose-p:mb-2 prose-ul:mt-2 prose-ul:mb-2 prose-li:mt-1 prose-li:mb-1 overflow-y-auto max-h-[30vh] px-4 py-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg shadow-inner scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent hover:scrollbar-thumb-gray-400 dark:hover:scrollbar-thumb-gray-500"
                >
                  <ReactMarkdown>{analysis.iconAnalysis}</ReactMarkdown>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-3 text-gray-800 dark:text-gray-200">
                Design Score
              </h3>
              {scoreLoading ? (
                <div className="flex items-center justify-center py-6">
                  <Loader2 className="h-6 w-6 animate-spin text-gray-500" />
                </div>
              ) : scoreError ? (
                <div className="text-red-500 dark:text-red-400 py-2">
                  Error loading score: {scoreError}
                </div>
              ) : score && (
                <>
                  <div className="flex items-center gap-4">
                    <div className="h-4 bg-gray-200 dark:bg-gray-600 rounded-full flex-1">
                      <div
                        className={cn(
                          "h-full rounded-full transition-all duration-500",
                          score.designScore >= 80 ? "bg-green-500" :
                          score.designScore >= 60 ? "bg-yellow-500" :
                          "bg-red-500"
                        )}
                        style={{ width: `${score.designScore}%` }}
                      />
                    </div>
                    <span className="font-mono text-lg font-semibold text-gray-700 dark:text-gray-300">
                      {score.designScore}/100
                    </span>
                  </div>
                  {score.scoreExplanation && (
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                      {score.scoreExplanation}
                    </p>
                  )}
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 