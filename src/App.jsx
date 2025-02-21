// @ts-check
import {ChevronDown, ChevronRight, Grid, LayoutGrid, Maximize2, Paintbrush, X, Sparkles} from 'lucide-react';
import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import {IconBox} from './components/IconBox';
import {Button} from './components/ui/button.jsx';
import {ThemeToggle} from './components/ui/theme-toggle';
import {ToastContextProvider} from './components/ui/toast-context';
import './styles/globals.css';
import {cn} from './lib/utils.js';

// Constants for localStorage keys
const STORAGE_KEYS = {
	SEARCH_TERM: 'icon-study-search',
	SELECTED_TAGS: 'icon-study-tags',
	IS_COMPACT_VIEW: 'icon-study-compact-view',
	SHOW_AI_BUTTONS: 'icon-study-show-ai',
	COLORED_ICONS: 'icon-study-colored-icons',
};

/**
 * Helper function to safely parse JSON from localStorage
 * @template T
 * @param {string} key
 * @param {T} defaultValue
 * @returns {T}
 */
const getStoredValue = (key, defaultValue) => {
	try {
		const item = localStorage.getItem(key);
		return item ? JSON.parse(item) : defaultValue;
	} catch (error) {
		console.error('Error reading from localStorage:', error);
		return defaultValue;
	}
};

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

/** @typedef {import('../types').SimpleIcon & { forceColored?: boolean, industry?: string[] }} Icon */

/**
 * Process a chunk of icons for coloring.
 * @param {number} startIndex The starting index of the chunk.
 * @param {Icon[]} icons The array of icons to process.
 * @param {number} chunkSize The size of each chunk.
 * @param {(icons: Icon[]) => void} onUpdate Callback to update the icons.
 * @param {(count: number) => void} onProgress Callback to update the progress.
 * @param {() => boolean} shouldCancel Function to check if processing should be cancelled.
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
		onUpdate(icons); // Ensure final state is updated
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

	// Use requestAnimationFrame instead of setTimeout for smoother updates
	requestAnimationFrame(() => {
		processIconChunk(
			endIndex,
			updatedIcons,
			chunkSize,
			onUpdate,
			onProgress,
			shouldCancel,
		);
	});
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

/** @type {Record<string, string[]>} */
const INDUSTRY_CATEGORIES = {
	"Manufacturing": [
		"Computer and Electronic Product Manufacturing",
		"Electrical Equipment, Appliance, and Component Manufacturing",
		"Food Manufacturing",
		"Machinery Manufacturing",
		"Transportation Equipment Manufacturing",
		"Chemical Manufacturing",
		"Fabricated Metal Product Manufacturing",
		"Primary Metal Manufacturing",
	],
	"Technology & Services": [
		"Data Processing, Hosting, and Related Services",
		"Software Publishers",
		"Professional, Scientific, and Technical Services",
		"Information Security",
		"Computer Systems Design",
		"Internet Publishing and Broadcasting",
	],
	"Telecommunications & Media": [
		"Telecommunications",
		"Broadcasting (except Internet)",
		"Motion Picture and Sound Recording Industries",
		"Publishing Industries (except Internet)",
	],
	"Commerce & Retail": [
		"Electronic Shopping and Mail-Order Houses",
		"Electronics and Appliance Stores",
		"Merchant Wholesalers, Durable Goods",
		"Merchant Wholesalers, Nondurable Goods",
		"Nonstore Retailers",
	],
	"Financial Services": [
		"Credit Intermediation and Related Activities",
		"Securities, Commodity Contracts, and Other Financial Investments",
		"Insurance Carriers and Related Activities",
		"Funds, Trusts, and Other Financial Vehicles",
		"Monetary Authorities-Central Bank",
	],
	"Transportation & Logistics": [
		"Air Transportation",
		"Rail Transportation",
		"Water Transportation",
		"Truck Transportation",
		"Transit and Ground Passenger Transportation",
		"Pipeline Transportation",
		"Warehousing and Storage",
	],
	"Other Industries": [] // This will catch any uncategorized industries
};

/**
 *
 */
function App() {
	const [searchTerm, setSearchTerm] = useState(() => getStoredValue(STORAGE_KEYS.SEARCH_TERM, ''));
	const [icons, setIcons] = useState(/** @type {Icon[]} */ ([]));
	const [filteredIcons, setFilteredIcons] = useState(/** @type {Icon[]} */ ([]));
	const [visibleIcons, setVisibleIcons] = useState(/** @type {Icon[]} */ ([]));
	const [error, setError] = useState(/** @type {string | null} */ (null));
	const [isLoading, setIsLoading] = useState(true);
	const [isColoringAll, setIsColoringAll] = useState(false);
	const [coloredIconsCount, setColoredIconsCount] = useState(0);
	const [isCompactView, setIsCompactView] = useState(() => getStoredValue(STORAGE_KEYS.IS_COMPACT_VIEW, false));
	const [lastColoredIndex, setLastColoredIndex] = useState(0);
	const [isViewTransitioning, setIsViewTransitioning] = useState(false);
	const [isThemeTransitioning, setIsThemeTransitioning] = useState(false);
	const [selectedTags, setSelectedTags] = useState(() => getStoredValue(STORAGE_KEYS.SELECTED_TAGS, []));
	const [expandedCategories, setExpandedCategories] = useState(/** @type {string[]} */ ([]));
	const [showAiButtons, setShowAiButtons] = useState(() => getStoredValue(STORAGE_KEYS.SHOW_AI_BUTTONS, true));
	const cancelColoringReference = useRef(false);

	// Lazy loading related states
	const [currentPage, setCurrentPage] = useState(1);
	const [hasMore, setHasMore] = useState(true);
	const ICONS_PER_PAGE = 700; // Only used in regular view
	const COMPACT_CHUNK_SIZE = 500; // Size of chunks to load in compact view
	const observerTarget = useRef(null);
	const loadingChunkReference = useRef(false);

	// Get unique industry tags and their counts, organized by category
	const categorizedTags = useMemo(() => {
		const tagCounts = new Map();
		icons.forEach(icon => {
			if (icon.industry) {
				icon.industry.forEach(tag => {
					tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1);
				});
			}
		});

		// Create a map of categories to their tags and counts
		const categorized = new Map();
		
		// First, categorize all known tags
		for (const [category, industries] of Object.entries(INDUSTRY_CATEGORIES)) {
			const categoryTags = new Map();
			industries.forEach(industry => {
				if (tagCounts.has(industry)) {
					categoryTags.set(industry, tagCounts.get(industry));
					tagCounts.delete(industry); // Remove from original map
				}
			});
			if (categoryTags.size > 0) {
				categorized.set(category, new Map([...categoryTags.entries()].sort((a, b) => a[0].localeCompare(b[0]))));
			}
		}

		// Add remaining uncategorized tags to "Other Industries"
		if (tagCounts.size > 0) {
			categorized.set("Other Industries", new Map([...tagCounts.entries()].sort((a, b) => a[0].localeCompare(b[0]))));
		}

		return categorized;
	}, [icons]);

	// Calculate category counts
	const categoryIconCounts = useMemo(() => {
		const counts = new Map();
		for (const [category, tags] of categorizedTags.entries()) {
			counts.set(category, Array.from(tags.values()).reduce((sum, count) => sum + count, 0));
		}
		return counts;
	}, [categorizedTags]);

	/**
	 * Toggle the expanded state of a category
	 * @param {string} category The category to toggle
	 */
	const toggleCategory = useCallback((category) => {
		setExpandedCategories(prev => 
			prev.includes(category)
				? prev.filter(c => c !== category)
				: [...prev, category]
		);
	}, []);

	// Effect to handle chunked loading in compact view
	useEffect(() => {
		if (!isCompactView) return;

		const loadNextChunk = () => {
			if (loadingChunkReference.current) return;
			loadingChunkReference.current = true;

			setVisibleIcons((previous) => {
				const nextChunkEnd = previous.length + COMPACT_CHUNK_SIZE;
				const newIcons = filteredIcons.slice(0, nextChunkEnd);

				// If we've loaded all icons, set hasMore to false
				if (newIcons.length >= filteredIcons.length) {
					setHasMore(false);
				}

				loadingChunkReference.current = false;
				return newIcons;
			});
		};

		// Start loading chunks
		if (visibleIcons.length < filteredIcons.length) {
			requestAnimationFrame(loadNextChunk);
		}
	}, [isCompactView, filteredIcons, visibleIcons.length]);

	const loadMoreIcons = useCallback(() => {
		if (isCompactView) {
			// In compact view, start with first chunk
			setVisibleIcons(filteredIcons.slice(0, COMPACT_CHUNK_SIZE));
			setHasMore(filteredIcons.length > COMPACT_CHUNK_SIZE);
			return;
		}

		// Regular view - paginate as before
		const startIndex = (currentPage - 1) * ICONS_PER_PAGE;
		const endIndex = startIndex + ICONS_PER_PAGE;
		const newIcons = filteredIcons.slice(0, endIndex);

		setVisibleIcons((previous) => {
			if (currentPage === 1 || previous.length > newIcons.length) {
				return newIcons;
			}

			return previous.length >= newIcons.length ? previous : newIcons;
		});
		setHasMore(endIndex < filteredIcons.length);
	}, [currentPage, filteredIcons, isCompactView, ICONS_PER_PAGE]);

	// Memoize the IconBox components to prevent unnecessary re-renders
	const memoizedIcons = useMemo(
		() =>
			visibleIcons.map((icon) => (
				<IconBox key={icon.slug} icon={icon} isCompact={isCompactView} showAiButton={showAiButtons} />
			)),
		[visibleIcons, isCompactView, showAiButtons],
	);

	// Intersection Observer setup
	useEffect(() => {
		// Don't set up observer in compact view since we load all icons at once
		if (isCompactView) {
			return;
		}

		const observer = new IntersectionObserver(
			(entries) => {
				if (entries[0].isIntersecting && hasMore) {
					setCurrentPage((previous) => previous + 1);
				}
			},
			{
				rootMargin: '300% 0px',
				threshold: 0.1,
			},
		);

		if (observerTarget.current) {
			observer.observe(observerTarget.current);
		}

		return () => observer.disconnect();
	}, [hasMore, isCompactView]);

	// Load more icons when page changes
	useEffect(() => {
		loadMoreIcons();
	}, [currentPage, loadMoreIcons, filteredIcons]);

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

				// First set the base icons
				setIcons(iconsList);
				
				// Then apply any stored colored state
				const coloredIconSlugs = new Set(getStoredValue(STORAGE_KEYS.COLORED_ICONS, []));
				const iconsWithColorState = iconsList.map(icon => ({
					...icon,
					forceColored: coloredIconSlugs.has(icon.slug)
				}));
				
				// Apply initial filters based on stored search and tags
				let filtered = iconsWithColorState;
				const storedSearch = getStoredValue(STORAGE_KEYS.SEARCH_TERM, '');
				const storedTags = getStoredValue(STORAGE_KEYS.SELECTED_TAGS, []);
				
				if (storedSearch.trim() !== '' || storedTags.length > 0) {
					filtered = iconsWithColorState.filter((icon) => {
						const matchesSearch = icon.title.toLowerCase().includes(storedSearch.toLowerCase());
						const matchesTags = storedTags.length === 0 || 
							(icon.industry && icon.industry.some(tag => storedTags.includes(tag)));
						return matchesSearch && matchesTags;
					});
				}

				setFilteredIcons(filtered);
				setColoredIconsCount(coloredIconSlugs.size);
				
				// Set initial visible icons based on view mode
				if (getStoredValue(STORAGE_KEYS.IS_COMPACT_VIEW, false)) {
					setVisibleIcons(filtered.slice(0, COMPACT_CHUNK_SIZE));
				} else {
					setVisibleIcons(filtered.slice(0, ICONS_PER_PAGE));
				}
				
				setIsLoading(false);
			})
			.catch((error) => {
				console.error('Error loading icons:', error);
				setError(error.message);
				setIsLoading(false);
			});
	}, []);

	// Save state to localStorage when it changes
	useEffect(() => {
		localStorage.setItem(STORAGE_KEYS.SEARCH_TERM, JSON.stringify(searchTerm));
	}, [searchTerm]);

	useEffect(() => {
		localStorage.setItem(STORAGE_KEYS.SELECTED_TAGS, JSON.stringify(selectedTags));
	}, [selectedTags]);

	useEffect(() => {
		localStorage.setItem(STORAGE_KEYS.IS_COMPACT_VIEW, JSON.stringify(isCompactView));
	}, [isCompactView]);

	useEffect(() => {
		localStorage.setItem(STORAGE_KEYS.SHOW_AI_BUTTONS, JSON.stringify(showAiButtons));
	}, [showAiButtons]);

	// Save colored icons state
	useEffect(() => {
		if (!isColoringAll) {  // Only save when not actively coloring
			const coloredIcons = filteredIcons
				.filter(icon => icon.forceColored)
				.map(icon => icon.slug);
			localStorage.setItem(STORAGE_KEYS.COLORED_ICONS, JSON.stringify(coloredIcons));
		}
	}, [filteredIcons, isColoringAll]);

	// Restore colored icons state after initial load
	useEffect(() => {
		if (icons.length > 0 && !isLoading) {
			const coloredIconSlugs = new Set(getStoredValue(STORAGE_KEYS.COLORED_ICONS, []));
			if (coloredIconSlugs.size > 0) {
				setFilteredIcons(icons => 
					icons.map(icon => ({
						...icon,
						forceColored: coloredIconSlugs.has(icon.slug)
					}))
				);
				setColoredIconsCount(coloredIconSlugs.size);
			}
		}
	}, [icons.length, isLoading]);

	// Effect to filter icons when search term or tags change
	useEffect(() => {
		// Apply filters based on search and tags
		let filtered = icons;
		
		if (searchTerm.trim() !== '' || selectedTags.length > 0) {
			filtered = icons.filter((icon) => {
				const matchesSearch = icon.title.toLowerCase().includes(searchTerm.toLowerCase());
				const matchesTags = selectedTags.length === 0 || 
					(icon.industry && icon.industry.some(tag => selectedTags.includes(tag)));
				return matchesSearch && matchesTags;
			});
		}

		// Preserve colored state from the current filtered icons
		const coloredSlugs = new Set(
			filteredIcons
				.filter(icon => icon.forceColored)
				.map(icon => icon.slug)
		);

		filtered = filtered.map(icon => ({
			...icon,
			forceColored: coloredSlugs.has(icon.slug)
		}));

		setFilteredIcons(filtered);

		// Reset visible icons based on view mode
		if (isCompactView) {
			setVisibleIcons(filtered.slice(0, COMPACT_CHUNK_SIZE));
			setHasMore(filtered.length > COMPACT_CHUNK_SIZE);
		} else {
			setVisibleIcons(filtered.slice(0, ICONS_PER_PAGE));
			setCurrentPage(1);
			setHasMore(filtered.length > ICONS_PER_PAGE);
		}
	}, [searchTerm, selectedTags, icons, isCompactView]);

	// Reset progress when search term or filters change
	useEffect(() => {
		setLastColoredIndex(0);
		setColoredIconsCount(filteredIcons.filter(icon => icon.forceColored).length);
		setIsColoringAll(false);
		cancelColoringReference.current = true;
	}, [searchTerm, selectedTags]);

	const startColoringAll = () => {
		if (isColoringAll) {
			cancelColoringReference.current = true;
			setIsColoringAll(false);
			return;
		}

		setIsColoringAll(true);
		cancelColoringReference.current = false;

		// Count already colored icons up to lastColoredIndex
		const alreadyColoredCount = filteredIcons
			.slice(0, lastColoredIndex)
			.filter(icon => icon.forceColored)
			.length;
		setColoredIconsCount(alreadyColoredCount);

		processIconChunk(
			lastColoredIndex,
			filteredIcons,
			10,
			(updatedIcons) => {
				setFilteredIcons(updatedIcons);
				if (cancelColoringReference.current) {
					setIsColoringAll(false);
				}
				// Check if we're done
				if (lastColoredIndex >= filteredIcons.length) {
					setIsColoringAll(false);
					cancelColoringReference.current = true;
				}
			},
			(count) => {
				setColoredIconsCount((previous) => previous + count);
				setLastColoredIndex((prev) => {
					const newIndex = Math.min(prev + 10, filteredIcons.length);
					// If we've reached the end, stop the process
					if (newIndex >= filteredIcons.length) {
						setIsColoringAll(false);
						cancelColoringReference.current = true;
					}
					return newIndex;
				});
			},
			() => cancelColoringReference.current,
		);
	};

	const uncolorAll = () => {
		// First stop any active coloring
		if (isColoringAll) {
			cancelColoringReference.current = true;
			setIsColoringAll(false);
		}

		// Wait a tiny bit to ensure the coloring process has stopped
		setTimeout(() => {
			// Reset all icons to uncolored state
			setFilteredIcons((icons) =>
				icons.map((icon) => ({...icon, forceColored: false}))
			);
			setColoredIconsCount(0);
			setLastColoredIndex(0);
			cancelColoringReference.current = true;
		}, 50);
	};

	const handleViewChange = () => {
		setIsViewTransitioning(true);
		loadingChunkReference.current = false;

		// Immediately set the new view state
		setIsCompactView((previous) => {
			const newIsCompact = !previous;

			// Get the current filtered icons with their colored state
			const currentFiltered = filteredIcons;

			if (newIsCompact) {
				// If switching to compact view, start with first chunk
				setVisibleIcons(currentFiltered.slice(0, COMPACT_CHUNK_SIZE));
				setHasMore(currentFiltered.length > COMPACT_CHUNK_SIZE);
			} else {
				// If switching to regular view, reset to initial state
				setVisibleIcons(currentFiltered.slice(0, ICONS_PER_PAGE));
				setCurrentPage(1);
				setHasMore(true);
			}

			return newIsCompact;
		});

		// Give a small delay for the layout to be ready
		setTimeout(() => {
			setIsViewTransitioning(false);
		}, 150);
	};

	if (error) {
		return (
			<div className="container">
				<h1>Icon Study</h1>
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
				<h1>Icon Study</h1>
				<div className="loading-message">Loading icons...</div>
			</div>
		);
	}

	return (
		<ToastContextProvider>
			<div
				className={cn(
					'min-h-screen bg-background text-foreground',
					'transition-opacity duration-200',
					isThemeTransitioning && 'opacity-0',
				)}
			>
				<div className="container py-10 space-y-8">
					<div className="space-y-2">
						<h1 className="text-3xl font-bold tracking-tight">
							Icon Study
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
						<ThemeToggle
							onTransitionStart={() => setIsThemeTransitioning(true)}
							onTransitionEnd={() => setIsThemeTransitioning(false)}
						/>
						<Button
							variant={isCompactView ? 'secondary' : 'outline'}
							size="icon"
							onClick={handleViewChange}
							disabled={isViewTransitioning}
							className="relative"
						>
							{isViewTransitioning ? (
								<div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary" />
							) : isCompactView ? (
								<LayoutGrid className="h-4 w-4" />
							) : (
								<Grid className="h-4 w-4" />
							)}
						</Button>
						{isCompactView && (
							<Button
								variant={showAiButtons ? 'secondary' : 'outline'}
								size="icon"
								onClick={() => setShowAiButtons(!showAiButtons)}
								className="relative"
								title={showAiButtons ? "Hide AI buttons" : "Show AI buttons"}
							>
								<Sparkles className="h-4 w-4" />
							</Button>
						)}
						<Button
							variant="outline"
							size="icon"
							onClick={startColoringAll}
							disabled={isColoringAll && cancelColoringReference.current}
							className="relative transition-all duration-200"
						>
							<div 
								className="transition-transform duration-1000 ease-in-out"
								style={{
									animation: isColoringAll ? 'breathe 2s ease-in-out infinite' : undefined,
								}}
							>
								<Paintbrush className="h-4 w-4" />
							</div>
							<style>{`
								@keyframes breathe {
									0%, 100% { transform: scale(0.9); }
									50% { transform: scale(1.1); }
								}
							`}</style>
							{(isColoringAll || coloredIconsCount > 0) && (
								<svg
									className="absolute inset-0 -rotate-90"
									viewBox="0 0 32 32"
								>
									<circle
										className={cn(
											"transition-all duration-200",
											isColoringAll ? "text-primary" : "text-primary/50"
										)}
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
						{coloredIconsCount > 0 && (
							<Button
								variant="outline"
								size="icon"
								onClick={uncolorAll}
								className="relative transition-all duration-200"
								title="Remove all colors"
							>
								<div className="relative">
									<Paintbrush className="h-4 w-4 text-muted-foreground" />
									<X className="h-3 w-3 absolute -top-1 -right-1 text-destructive" />
								</div>
							</Button>
						)}
					</div>

					{/* Industry Tags */}
					<div className="space-y-4">
						<div className="flex items-center justify-between">
							<div className="flex items-center gap-2">
								<h2 className="text-sm font-medium">Filter by Industry</h2>
								{(selectedTags.length > 0 || searchTerm.trim() !== '') && (
									<Button
										variant="outline"
										size="sm"
										onClick={() => {
											setSearchTerm('');
											setSelectedTags([]);
										}}
										className="h-8 px-3 text-xs flex items-center gap-1.5"
									>
										<X className="h-3 w-3" />
										Clear All Filters
									</Button>
								)}
							</div>
							{selectedTags.length > 0 && (
								<Button
									variant="ghost"
									size="sm"
									onClick={() => setSelectedTags([])}
									className="h-8 px-2 text-xs"
								>
									Clear Tags
								</Button>
							)}
						</div>
						<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
							{Array.from(categorizedTags.entries()).map(([category, tags]) => (
								<div key={category} className="space-y-2">
									<button
										onClick={() => toggleCategory(category)}
										className="flex items-center gap-2 w-full text-left text-sm font-medium hover:text-primary transition-colors"
									>
										{expandedCategories.includes(category) ? (
											<ChevronDown className="h-4 w-4" />
										) : (
											<ChevronRight className="h-4 w-4" />
										)}
										{category}
									</button>
									{expandedCategories.includes(category) && (
										<div className="flex flex-wrap gap-2 pl-6">
											{Array.from(tags.entries()).map(([tag, count]) => (
												<button
													key={tag}
													onClick={() => {
														setSelectedTags(prev =>
															prev.includes(tag)
																? prev.filter(t => t !== tag)
																: [...prev, tag]
														);
													}}
													className={cn(
														'inline-flex items-center text-xs px-3 h-7 rounded-full transition-colors',
														'border border-input hover:bg-accent hover:text-accent-foreground',
														selectedTags.includes(tag)
															? 'bg-primary text-primary-foreground hover:bg-primary/90'
															: 'bg-background'
													)}
												>
													{tag}
												</button>
											))}
										</div>
									)}
								</div>
							))}
						</div>
					</div>

					<div
						className={cn(
							'grid transition-opacity duration-200',
							isViewTransitioning ? 'opacity-0' : 'opacity-100',
							isCompactView
								? 'grid-cols-[repeat(auto-fill,minmax(56px,1fr))] gap-0.5'
								: 'grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 2xl:grid-cols-10 gap-4',
						)}
					>
						{memoizedIcons}
						{!isCompactView && hasMore && (
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
