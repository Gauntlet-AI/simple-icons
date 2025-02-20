import {Moon, Sun} from 'lucide-react';
import React from 'react';
import {Button} from './button';

/**
 *
 */
export function ThemeToggle() {
	const [theme, setTheme] = React.useState(() => {
		if (typeof globalThis !== 'undefined') {
			return document.documentElement.classList.contains('dark')
				? 'dark'
				: 'light';
		}

		return 'light';
	});

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
			onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
			title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
		>
			<Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
			<Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
			<span className="sr-only">Toggle theme</span>
		</Button>
	);
}
