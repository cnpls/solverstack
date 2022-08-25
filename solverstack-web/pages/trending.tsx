import React from "react";

// Bootstrap
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";

import CustomNav from "../components/common/CustomNav";


const Trending = () => {
    return (
        <Container>
            <CustomNav />
            <Row className="d-flex flex-column justify-content-center align-items-center w-75 mx-auto">
                <h1>Trending</h1>
            </Row>
            <hr/>
            <Row className="d-flex flex-column justify-content-center align-items-center w-75 mx-auto">
                <h2>Coming soon...</h2>
            </Row>
        </Container>
    );
};

export default Trending;
