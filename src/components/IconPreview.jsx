import {Check, Copy, Maximize2, Sparkles} from 'lucide-react';
import React, {useEffect, useState} from 'react';
import {cn} from '../lib/utils.js';
import {IconAnalysis} from './IconAnalysis';
import {useToast} from './ui/toast-context';

/**
 * Calculate the relative luminance of a hex color.
 * @param {string} hex The hex color without # prefix.
 * @returns {number} - The relative luminance value between 0 and 1.
 */
function getLuminance(hex) {
	const r = Number.parseInt(hex.slice(0, 2), 16);
	const g = Number.parseInt(hex.slice(2, 4), 16);
	const b = Number.parseInt(hex.slice(4, 6), 16);
	return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
}

/**
 * @param {{ icon: import('../../types').SimpleIcon & { forceColored?: boolean }, isCompact?: boolean }} props
 */
export function IconPreview({icon, isCompact}) {
	const [isColored, setIsColored] = useState(false);
	const [svgContent, setSvgContent] = useState('');
	const [isCopied, setIsCopied] = useState(false);
	const [isHovered, setIsHovered] = useState(false);
	const [isAnalysisOpen, setIsAnalysisOpen] = useState(false);
	const {showToast} = useToast();
	/** @type {React.MutableRefObject<NodeJS.Timeout | null>} */
	const hoverTimeoutReference = React.useRef(null);
	const iconPath = `/icons/${encodeURIComponent(icon.slug)}.svg`;

	// Cleanup hover timeout on unmount
	useEffect(() => {
		return () => {
			if (hoverTimeoutReference.current) {
				clearTimeout(hoverTimeoutReference.current);
			}
		};
	}, []);

	const handleMouseEnter = () => {
		if (hoverTimeoutReference.current) {
			clearTimeout(hoverTimeoutReference.current);
		}

		setIsHovered(true);
	};

	const handleMouseLeave = () => {
		hoverTimeoutReference.current = setTimeout(() => {
			setIsHovered(false);
		}, 50);
	};

	// Update isColored when the parent changes it
	useEffect(() => {
		if (icon.forceColored !== undefined) {
			setIsColored(icon.forceColored);
		}
	}, [icon.forceColored]);

	/**
	 * @param {React.MouseEvent<HTMLDivElement>} e
	 */
	const copySvgToClipboard = (e) => {
		e.stopPropagation();
		navigator.clipboard.writeText(svgContent);
		showToast('SVG copied to clipboard!');
	};

	/**
	 * @param {React.MouseEvent<HTMLDivElement>} e
	 */
	const copyHexToClipboard = (e) => {
		e.stopPropagation();
		navigator.clipboard.writeText(`#${icon.hex}`);
		setIsCopied(true);
		setTimeout(() => setIsCopied(false), 1000);
		showToast('Hex Code Copied!');
	};

	useEffect(() => {
		console.log('Fetching icon:', iconPath);
		fetch(iconPath)
			.then((response) => {
				if (!response.ok) {
					throw new Error(
						`Failed to load icon: ${response.status} ${response.statusText}`,
					);
				}

				return response.text();
			})
			.then((text) => {
				console.log('Loaded icon:', icon.slug);
				setSvgContent(text);
			})
			.catch((error) => {
				console.error(`Failed to load icon: ${iconPath}`, error);
			});
	}, [iconPath, icon.slug]);

	return (
		<>
			<div
				className={cn(
					'flex flex-col h-full relative overflow-hidden w-full',
					!isCompact && 'rounded-lg border bg-white dark:bg-gray-700',
				)}
			>
				{!isCompact && (
					<div className="bg-gray-50 dark:bg-gray-800 border-b flex items-center justify-between">
						<div className="px-3 py-1.5 text-xs font-medium line-clamp-2 text-center border-b border-gray-200 dark:border-gray-600 flex-1">
							{icon.title}
						</div>
						<button
							onClick={() => setIsAnalysisOpen(true)}
							className="px-2 py-1.5 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors duration-200"
							title="AI Analysis"
						>
							<Sparkles size={16} />
						</button>
					</div>
				)}

				<div className={cn('flex-1', isCompact ? 'p-0' : 'p-0.5 py-3')}>
					<div className="flex items-center justify-center h-full">
						<div
							className={cn(
								'relative cursor-pointer',
								'transition-all duration-200 ease-out',
								'hover:scale-110',
								isCompact ? 'w-full h-full' : 'w-16 h-16',
							)}
							onMouseEnter={handleMouseEnter}
							onMouseLeave={handleMouseLeave}
							onClick={copySvgToClipboard}
							style={{
								color: isColored ? `#${icon.hex}` : 'currentColor',
							}}
						>
							<div
								dangerouslySetInnerHTML={{
									__html: svgContent.replace(
										'<svg',
										'<svg fill="currentColor"',
									),
								}}
								className={cn(
									'transition-all duration-200 w-full h-full',
									isHovered && 'opacity-75',
								)}
								style={{pointerEvents: 'none'}}
							/>
							{isHovered && (
								<div
									className={cn(
										'absolute inset-0 flex items-center justify-center',
										'bg-black/60 backdrop-blur-[1px]',
										'rounded-sm',
										'text-white pointer-events-none',
										'animate-in fade-in-0 duration-200',
									)}
								>
									<Copy
										size={isCompact ? 24 : 40}
										className="animate-in zoom-in-50 duration-200"
									/>
								</div>
							)}
						</div>
					</div>
				</div>

				{!isCompact && (
					<div
						className={cn(
							'flex items-center',
							'transition-colors duration-200',
							getLuminance(icon.hex) > 0.5 ? 'text-gray-900' : 'text-white',
						)}
						style={{
							backgroundColor: `#${icon.hex}`,
						}}
					>
						<button
							onClick={() => setIsColored(!isColored)}
							className={cn(
								'flex-1 flex items-center justify-between',
								'px-3 py-1.5 text-xs font-medium',
								'transition-colors duration-200 hover:bg-black/5',
							)}
						>
							<span className="flex items-center gap-1.5">
								<div
									className={cn(
										'w-2 h-2 rounded-full border',
										getLuminance(icon.hex) > 0.5
											? 'border-black/10'
											: 'border-white/10',
									)}
									style={{backgroundColor: `#${icon.hex}`}}
								/>
								#{icon.hex}
							</span>
							<div
								onClick={copyHexToClipboard}
								className={cn(
									'w-5 h-5 rounded-full',
									'flex items-center justify-center',
									'bg-white/10 backdrop-blur-[1px]',
									'hover:bg-white/20',
									'transition-all duration-200',
									isCopied && 'scale-110 bg-white/30',
								)}
							>
								{isCopied ? <Check size={12} /> : <Copy size={12} />}
							</div>
						</button>
					</div>
				)}
			</div>
			<IconAnalysis
				icon={icon}
				isOpen={isAnalysisOpen}
				onClose={() => setIsAnalysisOpen(false)}
			/>
		</>
	);
}
