import React from 'react';
import {cn} from '../lib/utils.js';
import {IconPreview} from './IconPreview';
import {BookOpen} from 'lucide-react';

/**
 * @param {{
 *   icon: import('../../types').SimpleIcon & { forceColored?: boolean },
 *   isCompact?: boolean
 * }} props
 */
export function IconBox({icon, isCompact}) {
	const [showLicenseTooltip, setShowLicenseTooltip] = React.useState(false);

	return (
		<div
			className={cn(
				'flex items-stretch w-full relative',
				'border border-black dark:border-white',
				'rounded-lg bg-white dark:bg-gray-400',
				'transition-all duration-200 ease-out hover:shadow-lg',
			)}
		>
			<IconPreview
				icon={{...icon, forceColored: icon.forceColored}}
				isCompact={isCompact}
			/>
			<div className="absolute bottom-[calc(2.5rem+1px)] right-1.5 flex flex-col gap-1">
				{icon.guidelines && (
					<a
						href={icon.guidelines}
						target="_blank"
						rel="noopener noreferrer"
						className="p-0.5 rounded-full bg-white/90 dark:bg-gray-700/90 hover:bg-white dark:hover:bg-gray-700 transition-colors shadow-sm border border-black/50 dark:border-white/50"
						title="View brand guidelines"
					>
						<BookOpen size={8} className="text-gray-700 dark:text-gray-200" />
					</a>
				)}
				{icon.license && (
					<button
						className="w-[14px] h-[14px] rounded-full bg-white/90 dark:bg-gray-700/90 hover:bg-white dark:hover:bg-gray-700 transition-colors shadow-sm relative border border-black/50 dark:border-white/50 flex items-center justify-center"
						title="View license information"
						onMouseEnter={() => setShowLicenseTooltip(true)}
						onMouseLeave={() => setShowLicenseTooltip(false)}
					>
						<span className="text-[9px] font-medium leading-none text-gray-700 dark:text-gray-200 -translate-y-[0.5px]">i</span>
						{showLicenseTooltip && (
							<div className="absolute bottom-full right-0 mb-1 px-1.5 py-0.5 text-[10px] bg-black text-white dark:bg-white dark:text-black rounded shadow-lg whitespace-nowrap">
								{icon.license.type}
							</div>
						)}
					</button>
				)}
			</div>
		</div>
	);
}
