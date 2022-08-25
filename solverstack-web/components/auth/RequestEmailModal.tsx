import React, { useRef, useState, useEffect } from "react";
import axios from "axios";

// Bootstrap
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import { Row } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";

function RequestEmailModal(props) {
    const [email, setEmail] = useState("");

    const emailInputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        if (email) {
            axios.post(props.envobj.USER_AUTH_URL + "auth/github/register", { email }).then(res => {
                props.onHide();
            });
        }
    }, [email]);

    const handleFormSubmit = e => {
        e.preventDefault();
        const email = emailInputRef.current?.value || "";
        setEmail(email);
    };

    return (
        <Modal show={props.show} onHide={() => {}} size="lg" aria-labelledby="contained-modal-title-vcenter" centered>
            <Modal.Header className={"p-4"}>
                <Modal.Title id="contained-modal-title-vcenter">Please enter your email.</Modal.Title>
            </Modal.Header>
            <Modal.Body className={"p-4"}>
                <Row className="d-flex justify-content-center">
                    <Col lg={8} md={8} sm={8}>
                        <Form onSubmit={handleFormSubmit}>
                            <Form.Group>
                                <Form.Label className="m-0" column="lg" htmlFor="user-input">
                                    Email
                                </Form.Label>
                                <Form.Control type="email" id="request-email" size="lg" placeholder="Email" ref={emailInputRef} />
                            </Form.Group>
                            <Form.Group className={"d-flex w-100 justify-content-end"}>
                                <Button type={"submit"}>Submit</Button>
                            </Form.Group>
                        </Form>
                    </Col>
                </Row>
            </Modal.Body>
        </Modal>
    );
}

export default RequestEmailModal;
