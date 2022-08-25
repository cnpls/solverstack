import React from "react";

// Bootstrap
import Card from "react-bootstrap/Card";

// Components
import CardIcon from "./CardIcon";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

const StackCardWithIcon = (props) => {
    return (
        <Card>
            <CardIcon link={props.link} />
            <Card.Body>
                <Row className="d-flex justify-content-end">
                    <Col lg="10">
                        <Card.Title>{props.title}</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">{props.sub}</Card.Subtitle>
                        <Card.Text>{props.desc}</Card.Text>
                        <Card.Link href={props.link}>Setup</Card.Link>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    );
};

export default StackCardWithIcon;
