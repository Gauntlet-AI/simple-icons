import React from 'react';
import {cn} from '../lib/utils.js';
import {IconPreview} from './IconPreview';

/**
 * @param {{
 *   icon: import('../../types').SimpleIcon & { forceColored?: boolean },
 *   isCompact?: boolean
 * }} props
 */
export function IconBox({icon, isCompact}) {
	return (
		<div
			className={cn(
				'flex items-stretch w-full',
				'border border-black dark:border-white',
				'rounded-lg bg-white dark:bg-gray-400',
				'transition-all duration-200 ease-out hover:shadow-lg',
			)}
		>
			<IconPreview
				icon={{...icon, forceColored: icon.forceColored}}
				isCompact={isCompact}
			/>
		</div>
	);
}
