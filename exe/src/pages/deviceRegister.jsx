import React, { useEffect, useState } from "react";

import SideMenu from '../component/sidebar';
import TopBar from '../component/topbar';
import Loader from '../component/loading';
import useSWR from "swr";
import Api from "../component/api";

export default function DeviceRegister() {

    const [scriptOutput, setScriptOutput] = useState('');

    const handleButtonClick = () => {

    };

    useEffect(() => {

    }, [])

    return (
        <main className="main-content position-relative max-height-vh-100 h-100 border-radius-lg ">
            <div className="container-fluid py-4">
                <SideMenu />
                <TopBar pageName='Register Devices' />
                <div className="row justify-content-center mt-3">
                    <div className="col-xl-6 col-sm-8 mb-xl-0 mb-4">
                        <div className="card">
                            <div className="card-header p-3 pt-2">
                                <div className="text-center pt-1">
                                    <h4 className="mb-0">Register Devices</h4>
                                </div>
                            </div>
                            <hr className="dark horizontal my-0" />
                            <div className="card-body p-3">
                                {'hello'}
                            </div>
                            <div className="card-footer d-flex justify-content-center">
                                {/* <div id="joyDiv" className="mb-3" style={{ width: "300px", height: "300px", backgroundColor: "azure", border: "10px azure solid", borderRadius: "10px" }}>

                                </div> */}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    )
}