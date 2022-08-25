import React from "react";

// Bootstrap
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";

import CustomNav from "../components/common/CustomNav";
import StackCardWithIcon from "../components/users/StackCardWithIcon"; // NOTE: for MVP use the already-completed user components


const Discover = () => {
    return (
        <Container>
            <CustomNav />
            <Row className="d-flex flex-column justify-content-center align-items-center w-75 mx-auto">
                <h1>Discover</h1>
            </Row>
            <hr/>
            <Row className={"d-flex flex-column justify-content-center align-items-center pb-4 mb-2 w-50 mx-auto"}>
                <Col>
                    <StackCardWithIcon 
                    title={"Chained Stack Demo"}
                    sub={"Geocode, Depot, Route (created by @fingafrog)"}
                    desc={"this is an example of a stack a user creates to chain multiple stacks together"}
                    link={"/setup/chained"} />
                </Col>
            </Row>
            <Row className={"d-flex flex-column justify-content-center align-items-center pb-4 mb-2 w-50 mx-auto"}>
                <Col>
                    <StackCardWithIcon 
                    title={"Geocode"}
                    sub={"Base Module (created by @fingafrog)"}
                    desc={"geocode zipodes for .csv files"}
                    link={"/setup/geocode"} />
                </Col>
            </Row>
            <Row className={"d-flex flex-column justify-content-center align-items-center pb-4 mb-2 w-50 mx-auto"}>
                <Col>
                    <StackCardWithIcon 
                    title={"Depot"}
                    sub={"Base Module (created by @fingafrog)"}
                    desc={"origin location positioning within geocoded demand .csv data"}
                    link={"/setup/depot"} />
                </Col>
            </Row>
            <Row className={"d-flex flex-column justify-content-center align-items-center pb-4 mb-2 w-50 mx-auto"}>
                <Col>
                    <StackCardWithIcon 
                    title={"Route"}
                    sub={"Super Module (created by @fingafrog)"}
                    desc={"shipment routing for origin-positioned & geocoded demand .csv data"}
                    link={"/setup/route"} />
                </Col>
            </Row>
        </Container>
    );
};

export default Discover;
