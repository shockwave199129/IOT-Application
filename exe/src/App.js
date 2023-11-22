import './App.css';
import SideMenu from './component/sidebar';
import TopBar from './component/topbar';
import Loader from './component/loading';
import Error from './component/error';

import useSWR from "swr";
import Api from './component/api';
import { useNavigate } from 'react-router-dom';

function App() {

	const navigate = useNavigate();

	function GetUserDevice() {
		const { data, error, isLoading } = useSWR(['device'], Api().Get, {
			refreshInterval: 5000
		});

		if (isLoading) return <Loader />

		if (error) return <Error />

		let returnElemt = []

		Object.values(data.data).forEach(val => {
			let elm = <div key={val._id} className={`btn w-100 btm-sm ${val.status === 'True' ? 'btn-outline-success' : 'btn-outline-danger'}`} onClick={e => { e.preventDefault(); controlDevice(val.device_id) }}>
				<p className="text-end mb-0">
					<span className={`text-sm font-weight-bolder ${val.status === 'True' ? 'text-success' : 'text-danger'}`}>
						{val.status === 'True' ? 'online' : 'offline'}
					</span>
				</p>
				<h4 className='mb-2'>{val.device_name}</h4>
				<h6><small>{val.device_id}</small></h6>
			</div>

			returnElemt.push(elm)
		})
		return returnElemt
	}

	function controlDevice(device_id) {
		navigate("/control/" + device_id)
	}
	return (
		<>
			<main className="main-content position-relative max-height-vh-100 h-100 border-radius-lg ">
				<div className="container-fluid py-4">
					<SideMenu />
					<TopBar pageName='Dashboard' />
					<div className="row justify-content-center mt-3">
						<div className="col-xl-6 col-sm-8 mb-xl-0 mb-4">
							<div className="card">
								<div className="card-header p-3 pt-2">
									<div
										className="icon icon-lg icon-shape bg-gradient-dark shadow-dark text-center border-radius-xl mt-n4 position-absolute">
										<i className="material-icons opacity-10">weekend</i>
									</div>
									<div className="text-end pt-1">

										<h4 className="mb-0">Devices</h4>
									</div>
								</div>
								<hr className="dark horizontal my-0" />
								<div className="card-footer p-3">
									{GetUserDevice()}
									{/* <p className="mb-0"><span className="text-success text-sm font-weight-bolder">+55% </span>than last
										week</p> */}
								</div>
							</div>
						</div>
					</div>
				</div>
			</main>
		</>
	);
}

export default App;
