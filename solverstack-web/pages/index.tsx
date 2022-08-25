import React from "react";
import Head from "next/head";
import Row from "react-bootstrap/Row";

import CustomNav from "../components/common/CustomNav";


const Home: React.FunctionComponent = (props: any) => {
    return (
        <div className="container">
            <Head>
                <title>solverstack</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <CustomNav />

            <main>
                <Row className="d-flex flex-column justify-content-center align-items-center w-75 mx-auto">
                    <h1>Welcome</h1>
                </Row>
            </main>
        </div>
    );
};

export default Home;
