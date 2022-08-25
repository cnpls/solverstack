import React, { useState } from "react";

import Papa from "papaparse";

// Bootstrap
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/Container";

import CustomNav from "../../components/common/CustomNav";
import GeocodeSetup from "../../components/setup/GeocodeSetup";
import DepotSetup from "../../components/setup/DepotSetup";
import RouteSetup from "../../components/setup/RouteSetup";

const Chained = () => {
    const [geocodeInputFileName, setGeocodeFileName] = useState("zipcode file");
    const [geocodeInput, setGeocodeInput] = useState([]);
    const [geocodeResult, setGeocodeResult] = useState([]);
    const [routeInput, setRouteInput] = useState({});
    const [routeResult, setRouteResult] = useState([]);

    const onGeocodeFile = event => {
        /**
         * Event handler for file input.
         */
        setGeocodeFileName(event.target.value.split("\\").splice(-1)[0]);

        Papa.parse(event.target.files[0], {
            header: true,
            complete: function(results) {
                setGeocodeInput(results.data);
            }
        });
    }

    const updateGeocodeResult = (data) => {
        setGeocodeResult(data);
    }

    const updateDepotResult = (data) => {
        setRouteInput({
            demand: geocodeResult,
            olat: data[0].latitude,
            olon: data[0].longitude
        });
    }

    const updateRouteResult = (data) => {
        setRouteResult(data);
    }

    return (
        <Container>
            <CustomNav />
            <Row className="d-flex flex-column justify-content-center align-items-center pb-1 pt-3 w-75 mx-auto">
                <Col>
                    <Form.File 
                    id="custom-file" 
                    label={geocodeInputFileName} 
                    custom onChange={onGeocodeFile} />
                </Col>
            </Row>
            <Row className={"d-flex flex-column justify-content-center align-items-center pb-2 w-75 mx-auto"}>
                <Col className="pt-3">
                    <GeocodeSetup 
                    inputFile={geocodeInput} 
                    setOutputFile={updateGeocodeResult} />
                </Col>
            </Row>
            <Row className={"d-flex flex-column justify-content-center align-items-center pb-2 w-75 mx-auto"}>
                <Col className="pt-3">
                    <DepotSetup 
                    inputFile={geocodeResult} 
                    setOutputFile={updateDepotResult} />
                </Col>
            </Row>
            <Row className={"d-flex flex-column justify-content-center align-items-center pb-2 w-75 mx-auto"}>
                <Col className="pt-3">
                    <RouteSetup
                    inputFile={routeInput} 
                    setOutputFile={updateRouteResult} />
                </Col>
            </Row>
        </Container>
    );
};

export default Chained;
