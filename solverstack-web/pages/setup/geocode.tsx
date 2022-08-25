import React, { useState } from "react";

import Papa from "papaparse";

// Bootstrap
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/Container";

import CustomNav from "../../components/common/CustomNav";
import GeocodeSetup from "../../components/setup/GeocodeSetup";


const Geocode = () => {
    const [fileName, setFileName] = useState("zipcode file");
    const [file, setFile] = useState([]);
    const [result, setResult] = useState([]);

    const onFileUpdate = event => {
        /**
         * Event handler for file input.
         */
        setFileName(event.target.value.split("\\").splice(-1)[0]);

        Papa.parse(event.target.files[0], {
            header: true,
            complete: function(results) {
                setFile(results.data);
            }
        });
    }
    
    const updateResult = (data) => {
        setResult(data);
    }

    return (
        <Container>
            <CustomNav />
            <Row className="d-flex flex-column justify-content-center align-items-center w-75 mx-auto">
                <Col className="pt-3">
                    <GeocodeSetup 
                    inputFile={file} 
                    setOutputFile={updateResult} />
                </Col>
            </Row>
            <Row className="d-flex flex-column justify-content-center align-items-center w-75 mx-auto">
                <Col>
                    <Form.File 
                    id="custom-file" 
                    label={fileName} 
                    custom onChange={onFileUpdate} />
                </Col>
            </Row>
        </Container>
    );
};

export default Geocode;
