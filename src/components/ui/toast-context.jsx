import React, {createContext, useContext, useState} from 'react';
import {
	Toast,
	ToastDescription,
	ToastProvider,
	ToastTitle,
	ToastViewport,
} from './toast';

const ToastContext = createContext({
	showToast(/** @type {string} */ message) {},
});

/**
 * @param {{ children: React.ReactNode }} props
 */
export function ToastContextProvider({children}) {
	const [toasts, setToasts] = useState(
		/** @type {{ id: number, message: string }[]} */ ([]),
	);

	const showToast = (message) => {
		const id = Date.now();
		setToasts((previous) => [...previous, {id, message}]);
		setTimeout(() => {
			setToasts((previous) => previous.filter((toast) => toast.id !== id));
		}, 3000);
	};

	return (
		<ToastContext.Provider value={{showToast}}>
			<ToastProvider>
				{children}
				{toasts.map((toast) => (
					<Toast key={toast.id}>
						<ToastDescription>{toast.message}</ToastDescription>
					</Toast>
				))}
				<ToastViewport />
			</ToastProvider>
		</ToastContext.Provider>
	);
}

export const useToast = () => {
	const context = useContext(ToastContext);
	if (!context) {
		throw new Error('useToast must be used within a ToastContextProvider');
	}

	return context;
};
