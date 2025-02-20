import {Moon, Sun} from 'lucide-react';
import React from 'react';
import {Button} from './button';

/**
 * @typedef {object} ThemeToggleProps
 * @property {() => void} [onTransitionStart]
 * @property {() => void} [onTransitionEnd]
 */

/**
 * @param {ThemeToggleProps} props
 */
export function ThemeToggle({ onTransitionStart, onTransitionEnd }) {
	const [theme, setTheme] = React.useState(() => {
		if (typeof globalThis !== 'undefined') {
			return document.documentElement.classList.contains('dark')
				? 'dark'
				: 'light';
		}

		return 'light';
	});
	const [isTransitioning, setIsTransitioning] = React.useState(false);

	const handleThemeChange = () => {
		setIsTransitioning(true);
		onTransitionStart?.();
		
		// Wait for fade out
		setTimeout(() => {
			// Change theme
			setTheme(theme === 'dark' ? 'light' : 'dark');
			
			// Wait a bit to ensure theme is applied
			setTimeout(() => {
				setIsTransitioning(false);
				onTransitionEnd?.();
			}, 100);
		}, 200);
	};

	React.useEffect(() => {
		const root = document.documentElement;
		if (theme === 'dark') {
			root.classList.add('dark');
		} else {
			root.classList.remove('dark');
		}
	}, [theme]);

	return (
		<Button
			variant="outline"
			size="icon"
			onClick={handleThemeChange}
			disabled={isTransitioning}
			className="relative"
			title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
		>
			{isTransitioning ? (
				<div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary" />
			) : (
				<>
					<Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
					<Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
				</>
			)}
			<span className="sr-only">Toggle theme</span>
		</Button>
	);
}
