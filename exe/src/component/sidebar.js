import React from "react";
import { useNavigate } from 'react-router-dom';

export default function SideMenu() {

    const navigate = useNavigate();

    const iconSidenav = document.getElementById('iconSidenav');
    const sidenav = document.getElementById('sidenav-main');
    let body = document.getElementsByTagName('body')[0];
    let className = 'g-sidenav-pinned';

    function toggleSidenav() {
        if (body.classList.contains(className)) {
            body.classList.remove(className);
            setTimeout(function () {
                sidenav.classList.remove('bg-white');
            }, 100);
            sidenav.classList.remove('bg-transparent');

        } else {
            body.classList.add(className);
            sidenav.classList.add('bg-white');
            sidenav.classList.remove('bg-transparent');
            iconSidenav.classList.remove('d-none');
        }
    }

    return (
        <aside
            className="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3   bg-gradient-dark"
            id="sidenav-main">
            <div className="sidenav-header">
                <i className="fas fa-times p-3 cursor-pointer text-white opacity-5 position-absolute end-0 top-0 d-xl-none"
                    aria-hidden="true" id="iconSidenav" onClick={toggleSidenav}></i>
                <a className="navbar-brand m-0" href="#">
                    <img src="../assets/img/logo-ct.png" className="navbar-brand-img h-100" alt="main_logo" />
                    <span className="ms-1 font-weight-bold text-white">IOT Dashboard 2</span>
                </a>
            </div>
            <hr className="horizontal light mt-0 mb-2" />
            <div className="collapse navbar-collapse  w-auto " id="sidenav-collapse-main">
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <a className="nav-link text-white active bg-gradient-primary" href="#" onClick={e => { e.preventDefault(); navigate('/') }}>
                            <div className="text-white text-center me-2 d-flex align-items-center justify-content-center">
                                <i className="material-icons opacity-10">dashboard</i>
                            </div>
                            <span className="nav-link-text ms-1">Dashboard</span>
                        </a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link text-white " href="#" onClick={e => { e.preventDefault(); navigate('/devices') }}>
                            <div className="text-white text-center me-2 d-flex align-items-center justify-content-center">
                                <i className="material-icons opacity-10">table_view</i>
                            </div>
                            <span className="nav-link-text ms-1">Device</span>
                        </a>
                    </li>
                </ul>
            </div>
            <div className="sidenav-footer position-absolute w-100 bottom-0 ">
                <div className="mx-3">
                    <a className="btn bg-gradient-primary w-100" href="#" type="button">Documentation</a>
                </div>
            </div>
        </aside>
    )
}