import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from 'react-router-dom';

import SideMenu from '../component/sidebar';
import TopBar from '../component/topbar';
import Loader from '../component/loading';
import useSWR from "swr";
import Api from "../component/api";

import JoyStick from "../vendor/myJoystck";

export default function Control() {
    let { device_id } = useParams();

    var currentData = "C";

    function GetUserDevice() {
        const { data, error, isLoading } = useSWR(['device/' + device_id], Api().Get, {
            refreshInterval: 2000
        });

        if (isLoading) return <Loader />

        if (error) return <>
            <div className={`border rounded p-3 w-100 btm-sm border-danger`} >
                <p className="text-end mb-0">
                    <span className={`text-sm font-weight-bolder text-danger`}>
                        {'offline'}
                    </span>
                </p>
                <h4 className='mb-2'>Device Not Found</h4>
                <h6><small>{device_id}</small></h6>
            </div>
        </>

        let elm = <div key={data.data._id} className={`border rounded p-3 w-100 btm-sm ${data.data.status === 'True' ? 'border-success' : 'border-danger'}`} >
            <p className="text-end mb-0">
                <span className={`text-sm font-weight-bolder ${data.data.status === 'True' ? 'text-success' : 'text-danger'}`}>
                    {data.data.status === 'True' ? 'online' : 'offline'}
                </span>
            </p>
            <h4 className='mb-2'>{data.data.device_name}</h4>
            <h6><small>{data.data.device_id}</small></h6>
        </div>

        return elm
    }

    function updateControlData(stickData) {
        if (currentData !== stickData.cardinalDirection) {
            Api().Post('device/' + device_id + '/store', { control_value: stickData.cardinalDirection, device: device_id }).then((res) => {
                if (res.status === 201) {
                    currentData = stickData.cardinalDirection
                }
            }).catch(err => {
                console.log(err)
            })
        }
    }

    useEffect(() => {
        if (document.getElementById('joyDiv').children.length === 0)
            JoyStick('joyDiv', {}, updateControlData)
    }, [])

    return (
        <main className="main-content position-relative max-height-vh-100 h-100 border-radius-lg ">
            <div className="container-fluid py-4">
                <SideMenu />
                <TopBar pageName='Device Control' />
                <div className="row justify-content-center mt-3">
                    <div className="col-xl-6 col-sm-8 mb-xl-0 mb-4">
                        <div className="card">
                            <div className="card-header p-3 pt-2">
                                <div className="text-center pt-1">
                                    <h4 className="mb-0">Devices</h4>
                                </div>
                            </div>
                            <hr className="dark horizontal my-0" />
                            <div className="card-body p-3">
                                {GetUserDevice()}
                            </div>
                            <div className="card-footer d-flex justify-content-center">
                                <div id="joyDiv" className="mb-3" style={{ width: "300px", height: "300px", backgroundColor: "azure", border: "10px azure solid", borderRadius: "10px" }}>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    )
}
