import React from "react";
import { useNavigate } from 'react-router-dom';
import cookie from 'js-cookie';
import { useFormik } from "formik";
import * as Yup from "yup";

import Api from "../component/api";

export default function Login() {

    const navigate = useNavigate();

    const schema = Yup.object().shape({
        email: Yup.string().trim().matches(/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$/).required(),
        password: Yup.string().trim().required()
    })

    const formik = useFormik({
        initialValues: {
            email: '',
            password: ''
        },
        // Pass the Yup schema to validate the form
        validationSchema: schema,
        // Handle form submission
        onSubmit: async (values) => {
            HandlePostBtn(values);
        },
    });

    const { errors, touched, values, handleChange, handleSubmit, setFieldValue } = formik;

    function HandlePostBtn(values) {
        Api().Post('login', values).then((res)=>{
            if(res.status == 200) {
                
                Promise.resolve(cookie.set('IOT_APP_AUTH', JSON.stringify(res.data), {expires: 3, path : '/'})).then(
                    navigate('/')
                )
            }
        }).catch((error)=>{
            console.log(error)
        })
    }


    return (
        <div className="vh-100 vw-100 bg-gray-200">
            <main className="main-content  mt-0">
                <div className="page-header align-items-start min-vh-100"
                    style={{ backgroundImage: "url('../assets/img/photo-1497294815431-9365093b7331.jpg')" }}>
                    <span className="mask bg-gradient-dark opacity-6"></span>
                    <div className="container my-auto">
                        <div className="row">
                            <div className="col-lg-4 col-md-8 col-12 mx-auto">
                                <div className="card z-index-0 fadeIn3 fadeInBottom">
                                    <div className="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                                        <div className="bg-gradient-primary shadow-primary border-radius-lg py-3 pe-1">
                                            <h4 className="text-white font-weight-bolder text-center mt-2 mb-0">Sign in</h4>
                                            <div className="row mt-3">

                                            </div>
                                        </div>
                                    </div>
                                    <div className="card-body">
                                        <form role="form" className="text-start" onSubmit={handleSubmit}>
                                            <div className="input-group input-group-outline my-3 mb-2">
                                                <label className="form-label">Email</label>
                                                <input type="email" autoComplete="false" name="email" id="email" onChange={handleChange} className="form-control" />
                                            </div>
                                            {errors.email && touched.email && <p className="error-message mb-2">{errors.email}</p>}
                                            <div className="input-group input-group-outline mb-2">
                                                <label className="form-label">Password</label>
                                                <input type="password" autoComplete="false" id="password" name="password" onChange={handleChange} className="form-control" />
                                            </div>
                                            {errors.password && touched.password && <p className="error-message mb-2">{errors.password}</p>}
                                            <div className="text-center">
                                                <input type="submit" value="Sign In" className="btn bg-gradient-primary w-100 my-4 mb-2" />
                                            </div>
                                            <p className="mt-4 text-sm text-center">
                                                Don't have an account?
                                                <a href="#" onClick={e => { e.preventDefault(); navigate('/regester')}}
                                                    className="text-primary text-gradient font-weight-bold">Sign up</a>
                                            </p>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <footer className="footer position-absolute bottom-2 py-2 w-100">

                    </footer>
                </div>
            </main>
        </div>
    )
}