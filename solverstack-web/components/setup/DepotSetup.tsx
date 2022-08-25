import React, { useState, useRef, useEffect } from "react";

import Papa from "papaparse";

import BubbleMap from "../maps/BubbleMap";
import WorldAtlasJson from "../maps/MapJson";
import * as mapTypes from "../maps/MapTypes";

// Bootstrap
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

const axios = require('axios');


const svgHeight: number = 350;

const DepotSetup = (props) => {
    /**
     * Setup page for geocode module. 
     * 
     * Requires users to input csv file containing
     * zipcodes and country abbreviations.
     */
    const atlasJson = WorldAtlasJson();
    const svgContainerRef = useRef<HTMLDivElement>(null);
    const [svgWidth, setSvgWidth] = useState<any>(null);
    const [csvUrl, setCsvUrl] = useState<string>("");
    const [origins, setOrigins] = useState<Array<mapTypes.CoordinateMarker>>(Array<mapTypes.CoordinateMarker>(0));
    const [destinations, setDestinations] = useState<Array<mapTypes.CoordinateMarker>>(Array<mapTypes.CoordinateMarker>(0));

    const handleSvgWidth = () => {
        /**
         * Get current width of div containing rendered SVG and 
         * set svg width state.
         */
        if (!svgContainerRef) {
            return;
        }
        
        if (svgContainerRef.current) {
            setSvgWidth(svgContainerRef.current.offsetWidth);
        }
    }

    if (props.inputFile.length > 0 && destinations.length == 0) {
        let parsedDestinations = Array<mapTypes.CoordinateMarker>(props.inputFile.length);

        for (var i = 0; i < props.inputFile.length; i++) {

            parsedDestinations[i] = {
                latitude: parseFloat(props.inputFile[i].latitude),
                longitude: parseFloat(props.inputFile[i].longitude)
            };
        }

        setDestinations(parsedDestinations);

        axios.post(
            process?.env?.DEPOT_SERVICE_URL,
            {stack_id: 2, nodes: props.inputFile} // NOTE: for MVP stack_id is hardcoded
            ).then(function (response) {
                
                setOrigins(response.data.depots);
                props.setOutputFile(response.data.depots);

                const csv = Papa.unparse(response.data.depots);
                const csvData = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
                const csvUrl = window.URL.createObjectURL(csvData);
    
                setCsvUrl(csvUrl);
            }).catch(function (error) {
                console.log(error);
                return error;
            });
    }

    useEffect(() => {
        window.addEventListener("load", handleSvgWidth);
        window.addEventListener("resize", handleSvgWidth);
    }, []);


    return (
        <Accordion defaultActiveKey="0">
            <Card>
                <Accordion.Toggle as={Card.Header} eventKey="0">
                    <Row className="d-flex justify-content-end">
                        <Col>
                            <h4>Depot</h4>
                        </Col>
                        <Accordion.Toggle as={Button} eventKey="0">
                            Toggle Collapse
                        </Accordion.Toggle>
                    </Row>
                </Accordion.Toggle>
                <Accordion.Collapse eventKey="0">
                    <Card.Body>
                        <Form>
                            <Row className="mb-4">
                                <Col className="p-0">
                                    <div 
                                    className="svg-container"
                                    ref={svgContainerRef}>
                                        <BubbleMap 
                                        height={svgHeight}
                                        width={svgWidth}
                                        atlasJson={atlasJson}
                                        origins={origins}
                                        destinations={destinations} />
                                    </div>
                                </Col>
                            </Row>
                            <Row className="d-flex justify-content-end">
                                {destinations.length > 0 &&
                                    <a href={csvUrl}><Button className="download-btn">Download</Button></a>
                                }
                            </Row>
                        </Form>
                    </Card.Body>
                </Accordion.Collapse>
            </Card>
        </Accordion>
    );
};

export default DepotSetup;
