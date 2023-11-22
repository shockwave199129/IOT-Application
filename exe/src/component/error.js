import React from "react";
import "./error.css"

export default function Error(msg = '') {
    return (
        <div className="body loading">
            <h1 className="h1">500</h1>
            <h2 className="h2">Unexpected Error <b>:(</b></h2>
            {msg.length > 0 &&
                <h2 className="h2">
                    {msg}
                </h2>
            }
            <div className="gears">
                <div className="gear one">
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                </div>
                <div className="gear two">
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                </div>
                <div className="gear three">
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                </div>
            </div>
        </div>
    )
}