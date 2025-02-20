// @ts-check
import {Grid, LayoutGrid, Maximize2, Paintbrush} from 'lucide-react';
import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import {IconBox} from './components/IconBox';
import {Button} from './components/ui/button.jsx';
import {ThemeToggle} from './components/ui/theme-toggle';
import {ToastContextProvider} from './components/ui/toast-context';
import './styles/globals.css';
import {cn} from './lib/utils.js';

/** @type {{ [key: string]: string }} */
const TITLE_TO_SLUG_REPLACEMENTS = {
	'+': 'plus',
	'.': 'dot',
	'&': 'and',
	đ: 'd',
	ħ: 'h',
	ı: 'i',
	ĸ: 'k',
	ŀ: 'l',
	ł: 'l',
	ß: 'ss',
	ŧ: 't',
	'#': 'sharp',
	'-': '',
	é: 'e',
	è: 'e',
	ê: 'e',
	ë: 'e',
	ü: 'u',
	ř: 'r',
	î: 'i',
	í: 'i',
	ì: 'i',
	ï: 'i',
	ö: 'o',
	ò: 'o',
	ó: 'o',
	ô: 'o',
	õ: 'o',
	ã: 'a',
	à: 'a',
	á: 'a',
	â: 'a',
	ä: 'a',
	å: 'a',
	ż: 'z',
	ź: 'z',
	ž: 'z',
	É: 'e',
	È: 'e',
	Ê: 'e',
	Ë: 'e',
	Î: 'i',
	Í: 'i',
	Ì: 'i',
	Ï: 'i',
	Ö: 'o',
	Ò: 'o',
	Ó: 'o',
	Ô: 'o',
	Õ: 'o',
	Ã: 'a',
	À: 'a',
	Á: 'a',
	Â: 'a',
	Ä: 'a',
	Å: 'a',
	Ż: 'z',
	Ź: 'z',
	Ž: 'z',
};

/** @typedef {import('../types').SimpleIcon & { forceColored?: boolean }} Icon */

/**
 * Process a chunk of icons for coloring.
 * @param {number} startIndex The starting index of the chunk.
 * @param {Icon[]} icons The array of icons to process.
 * @param {number} chunkSize The size of each chunk.
 * @param {(icons: Icon[]) => void} onUpdate Callback to update the icons.
 * @param {(count: number) => void} onProgress - Callback to update the progress.
 * @param {() => boolean} shouldCancel - Function to check if processing should be cancelled
 */
function processIconChunk(
	startIndex,
	icons,
	chunkSize,
	onUpdate,
	onProgress,
	shouldCancel,
) {
	if (startIndex >= icons.length || shouldCancel()) {
		return;
	}

	const endIndex = Math.min(startIndex + chunkSize, icons.length);
	const updatedIcons = [...icons];
	let coloredInThisChunk = 0;

	for (let i = startIndex; i < endIndex; i++) {
		if (!updatedIcons[i].forceColored) {
			updatedIcons[i] = {...updatedIcons[i], forceColored: true};
			coloredInThisChunk++;
		}
	}

	onUpdate(updatedIcons);
	onProgress(coloredInThisChunk);

	setTimeout(() => {
		processIconChunk(
			endIndex,
			updatedIcons,
			chunkSize,
			onUpdate,
			onProgress,
			shouldCancel,
		);
	}, 100);
}

/**
 * @param {string} title
 */
const generateIconSlug = (title) => {
	// First apply special character mappings
	const mapped = title
		.toLowerCase()
		.replaceAll(
			new RegExp(`[${Object.keys(TITLE_TO_SLUG_REPLACEMENTS).join('')}]`, 'g'),
			(char) => TITLE_TO_SLUG_REPLACEMENTS[char.toLowerCase()] || char,
		);

	// Then remove remaining special characters and spaces
	return mapped
		.replaceAll(/[^a-z\d]/g, '') // Remove special characters
		.replaceAll(/\s+/g, ''); // Remove spaces
};

/**
 *
 */
function App() {
	const [searchTerm, setSearchTerm] = useState('');
	const [icons, setIcons] = useState(/** @type {Icon[]} */ ([]));
	const [filteredIcons, setFilteredIcons] = useState(
		/** @type {Icon[]} */ ([]),
	);
	const [visibleIcons, setVisibleIcons] = useState(/** @type {Icon[]} */ ([]));
	const [error, setError] = useState(/** @type {string | null} */ (null));
	const [isLoading, setIsLoading] = useState(true);
	const [isColoringAll, setIsColoringAll] = useState(false);
	const [coloredIconsCount, setColoredIconsCount] = useState(0);
	const [isCompactView, setIsCompactView] = useState(false);
	const cancelColoringReference = React.useRef(false);

	// Lazy loading related states
	const [currentPage, setCurrentPage] = useState(1);
	const [hasMore, setHasMore] = useState(true);
	const ICONS_PER_PAGE = 700; // Load many more icons at once
	const observerTarget = useRef(null);

	const loadMoreIcons = useCallback(() => {
		const startIndex = (currentPage - 1) * ICONS_PER_PAGE;
		const endIndex = startIndex + ICONS_PER_PAGE;
		const newIcons = filteredIcons.slice(0, endIndex);

		// Instead of replacing all icons, append new ones
		setVisibleIcons((previous) => {
			// If we're on page 1, or if the filtered results have changed, start fresh
			if (currentPage === 1 || previous.length > newIcons.length) {
				return newIcons;
			}

			// Otherwise, keep existing icons and append new ones
			return previous.length >= newIcons.length ? previous : newIcons;
		});
		setHasMore(endIndex < filteredIcons.length);
	}, [currentPage, filteredIcons]);

	// Memoize the IconBox components to prevent unnecessary re-renders
	const memoizedIcons = useMemo(
		() =>
			visibleIcons.map((icon) => (
				<IconBox key={icon.slug} icon={icon} isCompact={isCompactView} />
			)),
		[visibleIcons, isCompactView],
	);

	// Intersection Observer setup
	useEffect(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				if (entries[0].isIntersecting && hasMore) {
					setCurrentPage((previous) => previous + 1);
				}
			},
			{
				// Trigger loading when sentinel is 3 viewport heights away
				rootMargin: '300% 0px',
				threshold: 0.1,
			},
		);

		if (observerTarget.current) {
			observer.observe(observerTarget.current);
		}

		return () => observer.disconnect();
	}, [hasMore]);

	// Load more icons when page changes
	useEffect(() => {
		loadMoreIcons();
	}, [currentPage, loadMoreIcons]);

	useEffect(() => {
		if (searchTerm.trim() === '') {
			setFilteredIcons(icons);
		} else {
			const filtered = icons.filter((icon) =>
				icon.title.toLowerCase().includes(searchTerm.toLowerCase()),
			);
			setFilteredIcons(filtered);
		}

		// Reset pagination when search changes
		setCurrentPage(1);
		setHasMore(true);
	}, [searchTerm, icons]);

	const startColoringAll = () => {
		if (isColoringAll) {
			cancelColoringReference.current = true;
			return;
		}

		setIsColoringAll(true);
		cancelColoringReference.current = false;
		setColoredIconsCount(0);

		processIconChunk(
			0,
			filteredIcons,
			10,
			setFilteredIcons,
			(count) => setColoredIconsCount((previous) => previous + count),
			() => cancelColoringReference.current,
		);
	};

	useEffect(() => {
		console.log('App mounted, fetching data...');
		setIsLoading(true);

		// Fetch the icons data
		fetch('/_data/simple-icons.json')
			.then(async (response) => {
				console.log('Received response:', {
					status: response.status,
					ok: response.ok,
					contentType: response.headers.get('content-type'),
					url: response.url,
				});

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				try {
					const data = await response.json();
					console.log('Received data:', {
						type: typeof data,
						isArray: Array.isArray(data),
						length: data?.length,
						sample: data?.[0],
					});
					return data;
				} catch (error_) {
					console.error('JSON parse error:', error_);
					throw new Error('Failed to parse JSON response');
				}
			})
			.then((data) => {
				if (!Array.isArray(data)) {
					console.error('Data is not an array:', data);
					throw new Error('Invalid data format: expected an array');
				}

				// Keep track of used slugs and their counts
				const slugCounts = new Map();

				// Handle the array structure using the enhanced generateIconSlug
				const iconsList = data.map((icon) => {
					// Use the predefined slug if it exists, otherwise generate one
					const baseSlug = icon.slug || generateIconSlug(icon.title);

					// Get the count for this slug
					const count = slugCounts.get(baseSlug) || 0;
					// Increment the count for next time
					slugCounts.set(baseSlug, count + 1);

					// If this is a duplicate (count > 0), append the count to make it unique
					const uniqueSlug = count > 0 ? `${baseSlug}${count}` : baseSlug;

					return {
						...icon,
						slug: uniqueSlug,
					};
				});

				console.log('Processed icons:', {
					length: iconsList.length,
					sample: iconsList[0],
				});

				setIcons(iconsList);
				setFilteredIcons(iconsList);
				setIsLoading(false);
			})
			.catch((error) => {
				console.error('Error loading icons:', error);
				setError(error.message);
				setIsLoading(false);
			});
	}, []);

	if (error) {
		return (
			<div className="container">
				<h1>Simple Icons Development Environment</h1>
				<div className="error-message">
					Error loading icons: {error}
					<br />
					<small>Check the console for more details</small>
				</div>
			</div>
		);
	}

	if (isLoading) {
		return (
			<div className="container">
				<h1>Simple Icons Development Environment</h1>
				<div className="loading-message">Loading icons...</div>
			</div>
		);
	}

	return (
		<ToastContextProvider>
			<div className="min-h-screen bg-background text-foreground">
				<div className="container py-10 space-y-8">
					<div className="space-y-2">
						<h1 className="text-3xl font-bold tracking-tight">
							Simple Icons Development Environment
						</h1>
						<p className="text-muted-foreground">Loaded {icons.length} icons</p>
					</div>

					<div className="flex items-center gap-4">
						<input
							type="text"
							placeholder="Search icons..."
							value={searchTerm}
							onChange={(e) => setSearchTerm(e.target.value)}
							className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
						/>
						<ThemeToggle />
						<Button
							variant={isCompactView ? 'secondary' : 'outline'}
							size="icon"
							onClick={() => setIsCompactView(!isCompactView)}
						>
							{isCompactView ? (
								<LayoutGrid className="h-4 w-4" />
							) : (
								<Grid className="h-4 w-4" />
							)}
						</Button>
						<Button
							variant="outline"
							size="icon"
							onClick={startColoringAll}
							disabled={isColoringAll}
							className="relative"
						>
							<Paintbrush className="h-4 w-4" />
							{isColoringAll && (
								<svg
									className="absolute inset-0 -rotate-90"
									viewBox="0 0 32 32"
								>
									<circle
										className="text-primary"
										strokeWidth="3"
										stroke="currentColor"
										fill="none"
										r="14"
										cx="16"
										cy="16"
										style={{
											strokeDasharray: `${2 * Math.PI * 14}`,
											strokeDashoffset: `${2 * Math.PI * 14 * (1 - coloredIconsCount / filteredIcons.length)}`,
											transition: 'stroke-dashoffset 0.2s ease',
										}}
									/>
								</svg>
							)}
						</Button>
					</div>

					<div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 2xl:grid-cols-10 gap-4">
						{memoizedIcons}
						{hasMore && (
							<div
								ref={observerTarget}
								className="col-span-full h-10 flex items-center justify-center"
								style={{
									position: 'relative',
									top: '-200vh',
								}}
							>
								<div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
							</div>
						)}
					</div>
				</div>
			</div>
		</ToastContextProvider>
	);
}

export default App;
