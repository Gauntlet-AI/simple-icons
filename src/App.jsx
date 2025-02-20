import React, {useEffect, useState} from 'react';

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

/** @typedef {import('../types').SimpleIcon} Icon */

/**
 * Convert a hex color to RGB values
 * @param {string} hex
 * @returns {{r: number, g: number, b: number}}
 */
function hexToRgb(hex) {
	const r = parseInt(hex.slice(0, 2), 16);
	const g = parseInt(hex.slice(2, 4), 16);
	const b = parseInt(hex.slice(4, 6), 16);
	return { r, g, b };
}

/**
 * Create a CSS filter to convert black to target hex color
 * @param {string} hex Hex color without # prefix
 * @returns {string} CSS filter string
 */
function createColorFilter(hex) {
	const { r, g, b } = hexToRgb(hex);
	// Convert RGB to HSL-like values for filter
	const brightness = (r + g + b) / (255 * 3);
	const saturation = Math.max(r, g, b) / 255;
	
	return `brightness(0) saturate(100%) invert(${brightness}) sepia(100%) saturate(${saturation * 1000}%) hue-rotate(${Math.atan2(b - r, g - r) * 180 / Math.PI}deg)`;
}

/**
 * @param {{ icon: Icon }} props
 */
function IconPreview({ icon }) {
	const [isColored, setIsColored] = useState(false);
	const [svgContent, setSvgContent] = useState('');
	const [isCopied, setIsCopied] = useState(false);
	const [isHovered, setIsHovered] = useState(false);
	const hoverTimeoutRef = React.useRef(null);
	const iconPath = `/icons/${encodeURIComponent(icon.slug)}.svg`;

	// Cleanup hover timeout on unmount
	useEffect(() => {
		return () => {
			if (hoverTimeoutRef.current) {
				clearTimeout(hoverTimeoutRef.current);
			}
		};
	}, []);

	const handleMouseEnter = () => {
		if (hoverTimeoutRef.current) {
			clearTimeout(hoverTimeoutRef.current);
		}
		setIsHovered(true);
	};

	const handleMouseLeave = () => {
		// Small delay to prevent flickering
		hoverTimeoutRef.current = setTimeout(() => {
			setIsHovered(false);
		}, 50);
	};

	// Update isColored when the parent changes it
	useEffect(() => {
		if (icon.forceColored !== undefined) {
			setIsColored(icon.forceColored);
		}
	}, [icon.forceColored]);

	const copySvgToClipboard = (e) => {
		e.stopPropagation(); // Prevent triggering the color toggle
		navigator.clipboard.writeText(svgContent);
		
		// Show toast
		const toast = document.createElement('div');
		toast.textContent = 'SVG copied to clipboard!';
		toast.style.position = 'fixed';
		toast.style.bottom = '20px';
		toast.style.left = '50%';
		toast.style.transform = 'translateX(-50%)';
		toast.style.backgroundColor = '#333';
		toast.style.color = '#fff';
		toast.style.padding = '8px 16px';
		toast.style.borderRadius = '4px';
		toast.style.fontSize = '14px';
		toast.style.transition = 'all 0.3s ease';
		toast.style.opacity = '0';
		document.body.appendChild(toast);
		
		// Animate in
		setTimeout(() => {
			toast.style.opacity = '1';
		}, 10);

		// Remove toast after delay
		setTimeout(() => {
			toast.style.opacity = '0';
			setTimeout(() => {
				document.body.removeChild(toast);
			}, 300);
		}, 2000);
	};

	const copyHexToClipboard = (e) => {
		e.stopPropagation(); // Prevent triggering the color toggle
		navigator.clipboard.writeText(`#${icon.hex}`);
		setIsCopied(true);
		
		// Show toast
		const toast = document.createElement('div');
		toast.textContent = 'Color copied to clipboard!';
		toast.style.position = 'fixed';
		toast.style.bottom = '20px';
		toast.style.left = '50%';
		toast.style.transform = 'translateX(-50%)';
		toast.style.backgroundColor = '#333';
		toast.style.color = '#fff';
		toast.style.padding = '8px 16px';
		toast.style.borderRadius = '4px';
		toast.style.fontSize = '14px';
		toast.style.transition = 'all 0.3s ease';
		toast.style.opacity = '0';
		document.body.appendChild(toast);
		
		// Animate in
		setTimeout(() => {
			toast.style.opacity = '1';
		}, 10);

		// Reset copy state after animation
		setTimeout(() => {
			setIsCopied(false);
		}, 1000);

		// Remove toast after delay
		setTimeout(() => {
			toast.style.opacity = '0';
			setTimeout(() => {
				document.body.removeChild(toast);
			}, 300);
		}, 2000);
	};

	useEffect(() => {
		fetch(iconPath)
			.then(response => response.text())
			.then(text => {
				setSvgContent(text);
			})
			.catch(error => {
				console.error(`Failed to load icon: ${iconPath}`, error);
			});
	}, [iconPath]);

	return (
		<div className="icon-preview" style={{ 
			display: 'flex',
			flexDirection: 'column',
			height: '100%'
		}}>
			<div style={{ 
				flex: 1, 
				display: 'flex', 
				alignItems: 'center', 
				justifyContent: 'center',
				position: 'relative'
			}}>
				<div 
					onMouseEnter={handleMouseEnter}
					onMouseLeave={handleMouseLeave}
					onClick={copySvgToClipboard}
					style={{ 
						width: '48px',
						height: '48px',
						color: isColored ? `#${icon.hex}` : '#FFFFFF',
						cursor: 'pointer',
						position: 'relative',
						transform: isHovered ? 'scale(1.1)' : 'scale(1)',
						transition: 'all 0.2s ease',
						pointerEvents: 'auto'
					}}
				>
					<div
						dangerouslySetInnerHTML={{ 
							__html: svgContent.replace('<svg', '<svg fill="currentColor"')
						}}
						style={{
							filter: isHovered ? 'brightness(0.8)' : 'none',
							transition: 'all 0.2s ease',
							pointerEvents: 'none'
						}}
					/>
					{isHovered && (
						<div style={{
							position: 'absolute',
							top: '50%',
							left: '50%',
							transform: 'translate(-50%, -50%)',
							backgroundColor: 'rgba(0, 0, 0, 0.5)',
							borderRadius: '50%',
							width: '36px',
							height: '36px',
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							color: '#fff',
							fontSize: '24px',
							pointerEvents: 'none'
						}}>
							⧉
						</div>
					)}
				</div>
			</div>
			<div className="icon-title" style={{ padding: '8px', textAlign: 'center' }}>
				{icon.title}
			</div>
			<div style={{
				borderTop: '1px solid #eee',
				padding: '8px 4px 4px 4px',
				display: 'flex',
				alignItems: 'center',
				gap: '8px'
			}}>
				<div style={{ display: 'flex', alignItems: 'center', gap: '6px', flex: 1 }}>
					<div 
						onClick={() => setIsColored(!isColored)}
						style={{
							backgroundColor: isColored ? '#FFFFFF20' : `#${icon.hex}`,
							padding: '6px 6px',
							borderRadius: '4px',
							fontSize: '14px',
							fontWeight: '500',
							color: isColored ? '#000000' : (getLuminance(icon.hex) > 0.5 ? '#000' : '#fff'),
							cursor: 'pointer',
							transition: 'all 0.2s ease',
							flex: 1,
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'space-between',
							gap: '8px'
						}}
					>
						<span>#{icon.hex}</span>
						<div
							onClick={copyHexToClipboard}
							style={{
								width: '20px',
								height: '20px',
								borderRadius: '50%',
								border: '1px solid currentColor',
								display: 'flex',
								alignItems: 'center',
								justifyContent: 'center',
								cursor: 'pointer',
								fontSize: '12px',
								opacity: 0.8,
								transform: isCopied ? 'scale(1.2)' : 'scale(1)',
								transition: 'all 0.2s ease',
								position: 'relative',
								backgroundColor: 'rgba(128, 128, 128, 0.08)'
							}}
						>
							<div style={{
								position: 'absolute',
								opacity: isCopied ? 0 : 1,
								transition: 'opacity 0.2s ease',
								fontSize: '16px',
								fontWeight: 'bold'
							}}>
								⧉
							</div>
							<div style={{
								position: 'absolute',
								opacity: isCopied ? 1 : 0,
								transition: 'opacity 0.2s ease',
								fontSize: '14px',
								fontWeight: 'bold'
							}}>
								✓
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

function getLuminance(hex) {
	const r = parseInt(hex.slice(0, 2), 16);
	const g = parseInt(hex.slice(2, 4), 16);
	const b = parseInt(hex.slice(4, 6), 16);
	return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
}

/**
 *
 */
function App() {
	const [searchTerm, setSearchTerm] = useState('');
	const [icons, setIcons] = useState(/** @type {Icon[]} */ ([]));
	const [filteredIcons, setFilteredIcons] = useState(/** @type {Icon[]} */ ([]));
	const [error, setError] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [isColoringAll, setIsColoringAll] = useState(false);
	const [coloredIconsCount, setColoredIconsCount] = useState(0);
	const cancelColoringRef = React.useRef(false);

	const startColoringAll = () => {
		if (isColoringAll) {
			cancelColoringRef.current = true;
			return;
		}

		setIsColoringAll(true);
		cancelColoringRef.current = false;
		setColoredIconsCount(0);
		
		const chunkSize = 10;
		const totalIcons = filteredIcons.length;
		
		const processNextChunk = (startIndex) => {
			if (startIndex >= totalIcons || cancelColoringRef.current) {
				setIsColoringAll(false);
				cancelColoringRef.current = false;
				return;
			}
			
			const endIndex = Math.min(startIndex + chunkSize, totalIcons);
			const updatedIcons = [...filteredIcons];
			let coloredInThisChunk = 0;
			
			// Update icons in this chunk
			for (let i = startIndex; i < endIndex; i++) {
				if (!updatedIcons[i].forceColored) {
					updatedIcons[i] = { ...updatedIcons[i], forceColored: true };
					coloredInThisChunk++;
				}
			}
			
			setFilteredIcons(updatedIcons);
			setColoredIconsCount(prev => prev + coloredInThisChunk);
			
			// Process next chunk after a small delay
			setTimeout(() => processNextChunk(endIndex), 100);
		};
		
		processNextChunk(0);
	};

	// Debug function to test various path combinations
	/** @param {string} slug */
	const testIconPath = (slug) => {
		const encodedSlug = encodeURIComponent(slug);
		const paths = [
			`/icons/${encodedSlug}.svg`,
			`../icons/${encodedSlug}.svg`,
			`/src/icons/${encodedSlug}.svg`,
			`${globalThis.location.origin}/icons/${encodedSlug}.svg`,
		];

		console.group('Testing icon paths for:', slug);
		for (const path of paths) {
			fetch(path)
				.then((response) => {
					console.log(`Path ${path}:`, {
						status: response.status,
						ok: response.ok,
						contentType: response.headers.get('content-type'),
					});
					response.text().then((text) => {
						console.log(
							`Path ${path} content starts with:`,
							text.slice(0, 100),
						);
					});
				})
				.catch((error) => {
					console.log(`Path ${path}:`, {error: error.message});
				});
		}

		console.groupEnd();
	};

	/** @param {string} title */
	const generateIconSlug = (title) => {
		// First apply special character mappings
		const mapped = title
			.toLowerCase()
			.replaceAll(
				new RegExp(
					`[${Object.keys(TITLE_TO_SLUG_REPLACEMENTS).join('')}]`,
					'g',
				),
				(char) => TITLE_TO_SLUG_REPLACEMENTS[char.toLowerCase()] || char,
			);

		// Then remove remaining special characters and spaces
		return mapped
			.replaceAll(/[^a-z\d]/g, '') // Remove special characters
			.replaceAll(/\s+/g, ''); // Remove spaces
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

				// Test paths for the first icon
				if (iconsList.length > 0) {
					testIconPath(iconsList[0].slug);
				}
			})
			.catch((error) => {
				console.error('Error loading icons:', error);
				setError(error.message);
				setIsLoading(false);
			});
	}, []);

	useEffect(() => {
		if (searchTerm.trim() === '') {
			setFilteredIcons(icons);
		} else {
			const filtered = icons.filter((icon) =>
				icon.title.toLowerCase().includes(searchTerm.toLowerCase()),
			);
			setFilteredIcons(filtered);
		}
	}, [searchTerm, icons]);

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
		<div className="container">
			<h1>Simple Icons Development Environment</h1>
			<div className="status-info">Loaded {icons.length} icons</div>
			<div style={{
				display: 'flex',
				alignItems: 'center',
				gap: '1rem',
				margin: '2rem 1rem'
			}}>
				<input
					type="text"
					placeholder="Search icons..."
					value={searchTerm}
					onChange={(e) => setSearchTerm(e.target.value)}
					className="search-input"
					style={{ margin: 0 }}
				/>
				<div className="button-bar">
					<button
						onClick={startColoringAll}
						disabled={false}
						className={`action-button primary ${isColoringAll ? 'disabled' : ''}`}
					>
						{isColoringAll 
							? `Coloring... ${Math.round((coloredIconsCount / filteredIcons.length) * 100)}% (Click to Cancel)`
							: 'Color All Symbols'
						}
					</button>
				</div>
			</div>
			<div className="icons-grid">
				{filteredIcons.map((icon) => (
					<div key={icon.slug} className="icon-card">
						<IconPreview icon={{...icon, forceColored: icon.forceColored}} />
					</div>
				))}
			</div>
		</div>
	);
}

export default App;
