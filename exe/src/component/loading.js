import React from "react";

export default function Loader() {
    return (
        <div className="h-100 w-100 loader-content" id=" circle-loader" > <div className="circle-container" >

            <svg fill="none" className="circle-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle className="circle" cx="50" cy="50" r="45" />
            </svg>
        </div></div >
    )
}