import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

import {
	createBrowserRouter,
	RouterProvider,
} from "react-router-dom";

import App from './App';
import Login from './pages/login';
import Regester from './pages/regester';
import Control from './pages/control';
import DeviceRegister from './pages/deviceRegister';

import reportWebVitals from './reportWebVitals';

const router = createBrowserRouter([
	{
		path: "/",
		element: <App />
	},
	{
		path: '/login',
		element: <Login />
	},
	{
		path: '/regester',
		element: <Regester />
	},
	{
		path: '/control/:device_id',
		element: <Control />
	},
	{
		path: '/devices',
		element: <DeviceRegister />
	}
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
