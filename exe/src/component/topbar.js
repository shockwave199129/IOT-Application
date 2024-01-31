import React from "react";
import { useEffect, useState } from "react";
import cookie from 'js-cookie';
import { useNavigate } from 'react-router-dom';

import Api from "./api";

export default function TopBar({ pageName }) {

    const navigate = useNavigate();

    const iconSidenav = document.getElementById('iconSidenav');
    const sidenav = document.getElementById('sidenav-main');
    let body = document.getElementsByTagName('body')[0];
    let className = 'g-sidenav-pinned';

    var [logedUser, setLogedUser] = useState('User')

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

    function userLogout() {
        cookie.remove('IOT_APP_AUTH')
        cookie.remove('IOT_APP_USER')
        navigate('/login')
    }

    useEffect(() => {

        let user_info = cookie.get('IOT_APP_USER');

        if (user_info === '' || typeof user_info === 'undefined') {

        } else {
            let __v = JSON.parse(user_info)
            setLogedUser(__v.username)
        }
        /* if (iconNavbarSidenav) {
            iconNavbarSidenav.addEventListener("click", (event)=>{
                event.preventDefault();
                toggleSidenav();
            });
        }

        if (iconSidenav) {
            iconSidenav.addEventListener("click", (event)=>{
                event.preventDefault();
                console.log('hi2')
                toggleSidenav()
            });
        }

        return (() => {
            if (iconNavbarSidenav) {
                iconNavbarSidenav.removeEventListener("click", toggleSidenav);
            }

            if (iconSidenav) {
                iconSidenav.removeEventListener("click", toggleSidenav);
            }
        }) */
    }, [])

    return (
        <nav className="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl" id="navbarBlur"
            data-scroll="true">
            <div className="container-fluid py-1 px-3">
                <nav aria-label="breadcrumb" className="d-flex">
                    <ol className="breadcrumb bg-transparent mb-0 pb-0 pt-1 px-0 me-sm-3 me-3">
                        <li className="nav-item d-xl-none ps-3 d-flex align-items-center">
                            <a href="#" className="nav-link text-body p-0" onClick={e => { e.preventDefault(); toggleSidenav() }} id="iconNavbarSidenav">
                                <div className="sidenav-toggler-inner">
                                    <i className="sidenav-toggler-line"></i>
                                    <i className="sidenav-toggler-line"></i>
                                    <i className="sidenav-toggler-line"></i>
                                </div>
                            </a>
                        </li>
                    </ol>
                    <h4 className="font-weight-bolder mb-0">{pageName}</h4>
                </nav>
                <nav className="float-end d-flex justify-content-end">
                    <h6 className="me-3 ms-2 m-0">{logedUser}</h6>
                    <h6 className="m-0"><a href="#" onClick={e => { e.preventDefault(); userLogout() }}>Logout</a></h6>
                </nav>
            </div>
        </nav>
    )
}